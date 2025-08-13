#!/bin/bash

# Change to your aasdk root folder before running this script

# Backup the original file first
cp include/f1x/aasdk/IO/IOContextWrapper.hpp include/f1x/aasdk/IO/IOContextWrapper.hpp.bak

# Use sed to replace all instances of strand_->post(...) with strand_->post(..., boost::asio::strand_executor::allocator<void>())
# Note: adjust allocator if needed; here I used a common fix seen for Boost.Asio issues

sed -i 's/strand_->post(\([^)]*\))/strand_->post(\1, boost::asio::strand_executor::allocator<void>())/g' include/f1x/aasdk/IO/IOContextWrapper.hpp

echo "All strand_->post calls updated with allocator argument in IOContextWrapper.hpp"
