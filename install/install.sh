#!/usr/bin/bash

source ./utils.sh


# Select the type of installation
read -r -d '' prompt << EOM
How do you want to install Linux?
Linux alongside Windows: w
Linux: l
VirtualBox: v
EOM

system=$(select_option "$prompt" is_valid_option wlv)

# Ask if user wants to create a new partition
prompt="Use fdisk to create a new partition? y/n"
new_part=$(select_option "$prompt" is_valid_option yn)

# Create a new partition if the answer was y
if [[ $new_part = "y" ]]
then
    # Select an fdisk script to create the new partition scheme
    prompt="Enter a script for partitioning the disk (e.g. VirtualBox.fdisk):"
    script=$(select_option "$prompt" file_exists)

    prompt="Enter the disk you wish to partition (e.g. /dev/sda):"
    disk=$(select_option "$prompt" disk_exists)

    # Make a partition table using an fdisk script
    sed "s|<DISK>|$DISK|g" $script | sfdisk --force $disk
    sfdisk $disk < $script

    if [[ $system != "w" ]]
    then
        # Create a FAT32 filesystem for the EFI partition
        efi_partition="${disk}1"
        mkfs.fat -F32 $efi_partition
    else
        prompt="Enter the name of the EFI partition:"
        efi_partition=$(select_option "$prompt" disk_exists)
    fi

    # Create a LVM scheme for the other partition
    pvcreate --dataalignment 1m "${disk}2"
    vgcreate volgroup0 "${disk}2"
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
    mkdir /mnt && mount /dev/volgroup0/lv_root /mnt
    mkdir /mnt/home && mount /dev/volgroup0/lv_home /mnt/home
    mkdir /mnt/efi && mount $efi_partition /mnt/efi

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
