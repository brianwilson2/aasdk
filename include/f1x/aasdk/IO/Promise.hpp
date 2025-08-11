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

#include <functional>
#include <type_traits>
#include <boost/asio/strand.hpp>
#include <f1x/aasdk/Common/Data.hpp>

namespace f1x
{
namespace aasdk
{
namespace io
{

template <
    typename ResolveArgumentType = void,
    typename ErrorArgumentType = void>
class Promise
{
public:
    using ResolveHandler = typename std::conditional<
        std::is_void<ResolveArgumentType>::value,
        std::function<void()>,
        std::function<void(ResolveArgumentType)>
    >::type;

    using RejectHandler = typename std::conditional<
        std::is_void<ErrorArgumentType>::value,
        std::function<void()>,
        std::function<void(ErrorArgumentType)>
    >::type;

    explicit Promise(boost::asio::strand<boost::asio::io_context::executor_type>& strand)
        : ioContextWrapper_(strand.get_io_context())
    {}

    void then(ResolveHandler resolveHandler, RejectHandler rejectHandler)
    {
        resolveHandler_ = std::move(resolveHandler);
        rejectHandler_ = std::move(rejectHandler);
    }

    void resolve(ResolveArgumentType arg)
    {
        if (resolveHandler_)
        {
            ioContextWrapper_.post([self = this->shared_from_this(), arg = std::move(arg)]() {
                self->resolveHandler_(arg);
            });
        }
    }

    void resolve()
    {
        if (resolveHandler_)
        {
            ioContextWrapper_.post([self = this->shared_from_this()]() {
                self->resolveHandler_();
            });
        }
    }

    void reject(ErrorArgumentType arg)
    {
        if (rejectHandler_)
        {
            ioContextWrapper_.post([self = this->shared_from_this(), arg = std::move(arg)]() {
                self->rejectHandler_(arg);
            });
        }
    }

    void reject()
    {
        if (rejectHandler_)
        {
            ioContextWrapper_.post([self = this->shared_from_this()]() {
                self->rejectHandler_();
            });
        }
    }

    bool isPending() const
    {
        return ioContextWrapper_.isRunning();
    }

private:
    boost::asio::io_context& ioContextWrapper_;
    ResolveHandler resolveHandler_;
    RejectHandler rejectHandler_;
};

} // namespace io
} // namespace aasdk
} // namespace f1x

