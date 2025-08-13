/*
*  This file is part of aasdk library project.
*  Copyright (C) 2018 f1x.studio (Michal Szwaj)
*
*  aasdk is free software: you can redistribute it and/or modify
*  it under the terms of the GNU General Public License as published by
*  the Free Software Foundation; either version 3 of the License, or
*  (at your option) any later version.

*  aasdk is distributed in the hope that it will be useful,
*  but WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*  GNU General Public License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with aasdk. If not, see <http://www.gnu.org/licenses/>.
*/
#include <f1x/aasdk/USB/USBEndpoint.hpp>
#include <f1x/aasdk/USB/IUSBWrapper.hpp>
#include <f1x/aasdk/Error/Error.hpp>
#include <utility>

namespace f1x {
namespace aasdk {
namespace usb {

// Constructor
USBEndpoint::USBEndpoint(IUSBWrapper& usbWrapper,
                         boost::asio::io_context& ioService,
                         DeviceHandle handle,
                         uint8_t endpointAddress)
    : usbWrapper_(usbWrapper)
    , strand_(ioService.get_executor())
    , handle_(std::move(handle))
    , endpointAddress_(endpointAddress)
{
}

// Accessor for the underlying libusb handle
std::shared_ptr<libusb_device_handle> USBEndpoint::getHandle() const {
    if (!handle_) {
        throw std::runtime_error("USBEndpoint::getHandle() called but handle_ is null");
    }
    return handle_;
}

void USBEndpoint::controlTransfer(common::DataBuffer buffer, uint32_t timeout, Promise::Pointer promise)
{
    if(endpointAddress_ == 0)
    {
        promise->reject(error::Error(error::ErrorCode::USB_INVALID_TRANSFER_METHOD));
        return;
    }

    auto* transfer = usbWrapper_.allocTransfer(0);
    if(transfer == nullptr)
    {
        promise->reject(error::Error(error::ErrorCode::USB_TRANSFER_ALLOCATION));
        return;
    }

    usbWrapper_.fillControlTransfer(
        transfer,
        handle_,                                     // DeviceHandle
        buffer.data,                                 // unsigned char* data
        reinterpret_cast<libusb_transfer_cb_fn>(&USBEndpoint::transferHandler), // callback
        this,                                        // user_data
        timeout                                      // timeout in ms
    );

    this->transfer(transfer, std::move(promise));
}

void USBEndpoint::interruptTransfer(common::DataBuffer buffer, uint32_t timeout, Promise::Pointer promise)
{
    if(endpointAddress_ == 0)
    {
        promise->reject(error::Error(error::ErrorCode::USB_INVALID_TRANSFER_METHOD));
        return;
    }

    auto* transfer = usbWrapper_.allocTransfer(0);
    if(transfer == nullptr)
    {
        promise->reject(error::Error(error::ErrorCode::USB_TRANSFER_ALLOCATION));
        return;
    }

    usbWrapper_.fillInterruptTransfer(
        transfer,
        handle_,
        endpointAddress_,
        buffer.data,
        buffer.size,
        reinterpret_cast<libusb_transfer_cb_fn>(&USBEndpoint::transferHandler),
        this,      // user_data
        timeout
    );

    this->transfer(transfer, std::move(promise));
}

void USBEndpoint::bulkTransfer(common::DataBuffer buffer, uint32_t timeout, Promise::Pointer promise)
{
    if(endpointAddress_ == 0)
    {
        promise->reject(error::Error(error::ErrorCode::USB_INVALID_TRANSFER_METHOD));
        return;
    }

    auto* transfer = usbWrapper_.allocTransfer(0);
    if (transfer == nullptr)
    {
         promise->reject(error::Error(error::ErrorCode::USB_TRANSFER_ALLOCATION));
         return;
    }

    usbWrapper_.fillBulkTransfer(
        transfer,
        handle_,                         // DeviceHandle
        endpointAddress_,                 // uint8_t endpoint
        buffer.data,                      // unsigned char* data
        buffer.size,                      // int length
        reinterpret_cast<libusb_transfer_cb_fn>(&USBEndpoint::transferHandler), // callback
        this,                             // user_data
        timeout                            // timeout in milliseconds
    );

    this->transfer(transfer, std::move(promise));
}

void USBEndpoint::transfer(libusb_transfer *transfer, Promise::Pointer promise)
{
    boost::asio::dispatch(
        boost::asio::bind_executor(
            strand_,
            [this, self = this->shared_from_this(), transfer, promise = std::move(promise)]() mutable {
                auto submitResult = usbWrapper_.submitTransfer(transfer);

                if(submitResult == 0)
                {
                    if(self_ == nullptr)
                    {
                        self_ = std::move(self);
                    }
                    transfers_.insert(std::make_pair(transfer, std::move(promise)));
                }
                else
                {
                    promise->reject(error::Error(error::ErrorCode::USB_TRANSFER, submitResult));
                    usbWrapper_.freeTransfer(transfer);
                }
            }
        )
    );
}

uint8_t USBEndpoint::getAddress()
{
    return endpointAddress_;
}

void USBEndpoint::cancelTransfers()
{
    boost::asio::dispatch(
        boost::asio::bind_executor(
            strand_,
            [this, self = this->shared_from_this()]() mutable {
                for (const auto& transfer : transfers_)
                {
                    usbWrapper_.cancelTransfer(transfer.first);
                }
            }
        )
    );
}

DeviceHandle USBEndpoint::getDeviceHandle() const
{
    return handle_;
}

void USBEndpoint::transferHandler(libusb_transfer *transfer)
{
    auto self = reinterpret_cast<USBEndpoint*>(transfer->user_data)->shared_from_this();
    boost::asio::dispatch(
        boost::asio::bind_executor(
            self->strand_,
            [self, transfer]() mutable {
                if(self->transfers_.count(transfer) == 0)
                {
                    return;
                }

                auto promise(std::move(self->transfers_.at(transfer)));

                if(transfer->status == LIBUSB_TRANSFER_COMPLETED)
                {
                    promise->resolve(transfer->actual_length);
                }
                else
                {
                    auto error = transfer->status == LIBUSB_TRANSFER_CANCELLED
                        ? error::Error(error::ErrorCode::OPERATION_ABORTED)
                        : error::Error(error::ErrorCode::USB_TRANSFER);
                    promise->reject(error);
                }

                self->usbWrapper_.freeTransfer(transfer);
                self->transfers_.erase(transfer);

                if(self->transfers_.empty())
                {
                    self->self_.reset();
                }
            }
        )
    );
}

}  // namespace usb
}  // namespace aasdk
}  // namespace f1x
