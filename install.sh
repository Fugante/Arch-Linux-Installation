#!/usr/bin/bash


# Ask if user wants to create a new partition
NEW_PART=""
while [[ ! *"$NEW_PART"* =~ [yn] ]]
do
    echo "Use fdisk to create a new partition? y/n"
    read NEW_PART
done


if [[ $NEW_PART == "y" ]]
then
    # Make a partition table using an fdisk script
    sfdisk /dev/nvme0n1 < nvme0n1.fdisk

    # Create a FAT32 filesystem for the EFI partition
    mkfs.fat -F32 /dev/nvme0n1p1

    # Create a LVM scheme for the other partition
    pvcreate --dataalignment 1m /dev/nvme0n1p2
    vgcreate volgroup0 /dev/nvme0n1p2
    # Allocate 30 GiB for the root directory
    lvcreate -L 30GB volgroup0 -n lv_root
    # Allocate the rest for the home directory
    lvcreate -l 100%FREE volgroup0 -n lv_home
    modprobe dm_mod
    vgscan
    vgchange -ay
    # Create a Linux ext4 for the new logical partitions
    mkfs.ext4 /dev/volgroup0/lv_root
    mount /dev/volgroup0/lv_root /mnt
    mkfs.ext4 /dev/volgroup0/lv_home

    # Create directories to mount the new partitions
    mkdir /mnt/home
    mount /dev/volgroup0/lv_home /mnt/home

    # Create a file with the partitions info
    mkdir /mnt/etc
    genfstab -U -p /mnt >> /mnt/etc/fstab
fi

# Install pacman in the new system
pacstrap /mnt base
 
# Change working directory
arch-root /mnt

# Install the Linux kernel
pacman -S linux linux-headers linux-lts linux-lts-headers linux-firmware
pacman -S vim base-devel openssh
systemctl enable sshd
pacman -S networkmanager wireless_tools netctl
systemctl enable networkmanager
pacman -S lvm2