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
#include <f1x/aasdk/USB/AccessoryModeStartQuery.hpp>
#include <f1x/aasdk/USB/IUSBEndpoint.hpp>
#include <f1x/aasdk/IO/Promise.hpp>

using namespace f1x::aasdk;
using namespace f1x::aasdk::usb;
using namespace f1x::aasdk::io;

void AccessoryModeStartQuery::start(Promise::Pointer promise)
{
    boost::asio::dispatch(
        boost::asio::bind_executor(
            strand_,
            [this, self = this->shared_from_this(), promise = std::move(promise)]() mutable
            {
                if (promise_)
                {
                    promise->reject(error::Error(error::ErrorCode::OPERATION_IN_PROGRESS));
                    return;
                }

                promise_ = std::move(promise);

                auto usbEndpointPromise = IUSBEndpoint::Promise::defer(strand_);
                usbEndpointPromise->then(
                    [this, self](unsigned int) mutable {
                        promise_->resolve(usbEndpoint_);
                        promise_.reset();
                    },
                    [this, self](const error::Error& e) mutable {
                        promise_->reject(e);
                        promise_.reset();
                    }
                );

                usbEndpoint_->controlTransfer(common::DataBuffer(data_), cTransferTimeoutMs, std::move(usbEndpointPromise));
            }
        )
    );
}
