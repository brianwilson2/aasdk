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

#pragma once
#pragma once

#include <boost/asio.hpp>
#include <functional>
#include <memory>

namespace aasdk {
namespace messenger {

template<typename T = void>
class Promise : public std::enable_shared_from_this<Promise<T>> {
public:
    using ResolveHandler = std::function<void(T)>;
    using RejectHandler = std::function<void(std::exception_ptr)>;

    Promise(boost::asio::io_context& ioContext)
        : strand_(boost::asio::make_strand(ioContext)) {}

    void resolve(T value) {
        auto self = this->shared_from_this();
        boost::asio::post(strand_, [this, self, value = std::move(value)] {
            if (resolveHandler_) {
                resolveHandler_(std::move(value));
            }
        });
    }

    void reject(std::exception_ptr error) {
        auto self = this->shared_from_this();
        boost::asio::post(strand_, [this, self, error] {
            if (rejectHandler_) {
                rejectHandler_(error);
            }
        });
    }

    void then(ResolveHandler onResolve, RejectHandler onReject = nullptr) {
        resolveHandler_ = std::move(onResolve);
        rejectHandler_  = std::move(onReject);
    }

private:
    boost::asio::strand<boost::asio::io_context::executor_type> strand_;
    ResolveHandler resolveHandler_;
    RejectHandler rejectHandler_;
};

} // namespace messenger
} // namespace aasdk