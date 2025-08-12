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

#include <boost/asio.hpp>
#include <functional>
#include <memory>
#include <utility>

namespace aasdk
{

template<typename T = void>
class Promise : public std::enable_shared_from_this<Promise<T>>
{
public:
    using ResolveHandler = std::function<void(T)>;
    using RejectHandler  = std::function<void(const std::exception_ptr&)>;

    explicit Promise(boost::asio::io_context& ioContext)
        : strand_(boost::asio::make_strand(ioContext)),
          isActive_(true)
    {
    }

    void then(ResolveHandler onResolve, RejectHandler onReject = nullptr)
    {
        onResolve_ = std::move(onResolve);
        onReject_  = std::move(onReject);
    }

    void resolve(T value)
    {
        if (!isActive_) return;
        auto self = this->shared_from_this();
        boost::asio::post(strand_,
            [this, self, value = std::move(value)]()
            {
                if (onResolve_) onResolve_(std::move(value));
                reset();
            });
    }

    void reject(const std::exception_ptr& e)
    {
        if (!isActive_) return;
        auto self = this->shared_from_this();
        boost::asio::post(strand_,
            [this, self, e]()
            {
                if (onReject_) onReject_(e);
                reset();
            });
    }

    void cancel()
    {
        isActive_ = false;
        reset();
    }

private:
    void reset()
    {
        onResolve_ = nullptr;
        onReject_  = nullptr;
    }

    boost::asio::strand<boost::asio::io_context::executor_type> strand_;
    ResolveHandler onResolve_;
    RejectHandler onReject_;
    bool isActive_;
};

template<>
class Promise<void> : public std::enable_shared_from_this<Promise<void>>
{
public:
    using ResolveHandler = std::function<void()>;
    using RejectHandler  = std::function<void(const std::exception_ptr&)>;

    explicit Promise(boost::asio::io_context& ioContext)
        : strand_(boost::asio::make_strand(ioContext)),
          isActive_(true)
    {
    }

    void then(ResolveHandler onResolve, RejectHandler onReject = nullptr)
    {
        onResolve_ = std::move(onResolve);
        onReject_  = std::move(onReject);
    }

    void resolve()
    {
        if (!isActive_) return;
        auto self = this->shared_from_this();
        boost::asio::post(strand_,
            [this, self]()
            {
                if (onResolve_) onResolve_();
                reset();
            });
    }

    void reject(const std::exception_ptr& e)
    {
        if (!isActive_) return;
        auto self = this->shared_from_this();
        boost::asio::post(strand_,
            [this, self, e]()
            {
                if (onReject_) onReject_(e);
                reset();
            });
    }

    void cancel()
    {
        isActive_ = false;
        reset();
    }

private:
    void reset()
    {
        onResolve_ = nullptr;
        onReject_  = nullptr;
    }

    boost::asio::strand<boost::asio::io_context::executor_type> strand_;
    ResolveHandler onResolve_;
    RejectHandler onReject_;
    bool isActive_;
};

} // namespace aasdk