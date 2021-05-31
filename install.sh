#! /usr/bin/bash

sed -e "s/#.*//g" sda.fdisk > sda.fdisk.tmp
fdisk /dev/sda < sda.fdisk.tmp
rm sda.fdisk.tmp
