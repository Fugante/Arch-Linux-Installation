#! /usr/bin/bash

fdisk /dev/sda < sed -e "s/#.*//g" sda.fdisk
