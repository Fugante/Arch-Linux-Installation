#! /usr/bin/bash

fdisk /dev/sda < sda.fdisk
mkfs.fat -F32 /dev/sda1
pvcreate --dataalignment 1m /dev/sda2
vgcreate volgroup0 /dev/sda2
lvcreate -L 30GB volgroup0 -n lv_root
lvcreate -l 100%FREE volgroup0 -n lv_home
modprobe dm_mod
vgscan
vgchange -ay
mkfs.ext4 /dev/volgroup0/lv_root
mount /dev/volgroup0/lv_root /mnt
mkfs.ext4 /dev/volgroup0/lv_home
mkdir /mnt/home
mount /dev/volgroup0/lv_home /mnt/home
mkdir /mnt/etc
genfstab -U -p /mnt >> /mnt/etc/fstab
