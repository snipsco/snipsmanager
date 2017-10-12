#!/bin/bash

echo "dtoverlay=lirc-rpi
dtparam=gpio_in_pin=16
dtparam=gpio_in_pull=down
dtparam=gpio_out_pin=13
dtparam=spi=on
enable_uart=1
start_x=1" >> /boot/config.txt