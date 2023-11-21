VOLUME_GROUP_NAME="vg0"
ROOT_VOLUME_NAME="root"
HOME_VOLUME_NAME="home"
EFI_PARTITION_SIZE="500"
MAIN_PARTITION_SIZE="0"
EFI_PARTITION_SIZE_TEXT="Enter EFI partition size (in MiB) or press Enter for default (500MiB): \n"
MAIN_PARTITION_SIZE_TEXT="Enter main partition size (in MiB) or press Enter for default (rest of disk): \n"

function printToTty
{
    printf $1 > /dev/tty
}

function askDiskName
{
    printToTty "Available disks:\n"
    lsblk -dplnx size -o name,size > /dev/tty
    read -p "Enter disk: " disk
    if [ -e "/dev/${disk}" ]; then
        echo $disk
    fi
    printToTty "\nInvalid disk\n\n"
    askDiskName
}

function askPartitionSize
{
    text=$1
    minSize=$2
    read size -p $text
    if [ -z $size ]; then
        echo $minSize
    fi
    if [ $size -gt $minSize ]; then
        echo $size
    fi
    printToTty "\nSize must be greater than ${minSize}MiB\n\n"
    askPartitionSize $text $minSize
}

function partitionDisk
{
    disk=$1
    efiPartitionSize=$2
    mainPartitionSize=$3
    (
        printf "g\n" # create GPT partition table
        printf "n\n" # new partition
        printf "\n"  # default partition number
        printf "\n"  # default first sector
        printf "+${efiPartitionSize}MiB\n" # partition size
        printf "t\n" # change partition type
        printf "1\n" # select partition 1 (EFI)
        printf "n\n" # new partition
        printf "\n"  # default partition number
        printf "\n"  # default first sector
        if [ $mainPartitionSize -eq 0 ]; then
            printf "\n"  # default last sector
        else
            printf "+${mainPartitionSize}MiB\n" # partition size
        fi
        printf "t\n" # change partition type
        printf "2\n" # select partition 2 (main)
        printf "lvm\n" # change partition type to LVM
        printf "w\n" # write changes
    ) | fdisk /dev/$disk
}

function createEfiAndLvmPartitions
{
    efiPartition=$1
    partition=$2
    pvcreate --dataalignment 1m "/dev/${partition}"
    vgcreate $VOLUME_GROUP_NAME "/dev/${partition}"
    lvcreate -L 50GB $VOLUME_GROUP_NAME -n $ROOT_VOLUME_NAME
    lvcreate -l 100%FREE $VOLUME_GROUP_NAME -n $HOME_VOLUME_NAME
    modprobe dm_mod
    vgscan
    vgchange -ay
    mkfs.fat -F32 "/dev/${efiPartition}"
    mkfs.ext4 "/dev/${VOLUME_GROUP_NAME}/${ROOT_VOLUME_NAME}"
    mkfs.ext4 "/dev/${VOLUME_GROUP_NAME}/${HOME_VOLUME_NAME}"
}

function installKernel
{
    efiPartition=$1
    mount /dev/${VOLUME_GROUP_NAME}/${ROOT_VOLUME_NAME} /mnt
    mkdir /mnt/home
    mount /dev/${VOLUME_GROUP_NAME}/${HOME_VOLUME_NAME} /mnt/home
    mkdir /mnt/boot
    mkdir /mnt/boot/efi
    mount "/dev/${efiPartition}" /mnt/boot/efi
    mkdir /mnt/etc
    genfstab -U -p /mnt > /mnt/etc/fstab
    pacstrap /mnt base
    arch-chroot /mnt
    pacman -S --noconfirm linux linux-lts linux-headers linux-lts-headers linux-firmware
}

function configureSystem
{
    # System configuration
    pacman -S --noconfirm lvm2
    sed -E 's/#.*(HOOKS=.*lvm2.*)/\1/' -i /etc/mkinitcpio.conf
    sed -E 's/(HOOKS=.*kms.*)/#    \1/' -i /etc/mkinitcpio.conf
    mkinitcpio -p linux
    mkinitcpio -p linux-lts
    sed -E 's/#(es_MX.UTF-8 UTF-8)/\1/' -i /etc/locale.gen
    locale-gen
    # User configuration
    printToTty "Setting root password\n"
    passwd
    printToTty "Creating user\n"
    read name -p "Enter username: "
    useradd -m -g users -G wheel $name
    passwd $name
    printToTty "Configuring sudo\n"
    pacman -S --noconfirm sudo
    sed -E 's/#.*(wheel.*)/\1/' -i /etc/sudoers
}

function installBootloader
{
    pacman -S --noconfirm grub efibootmgr dosfstools os-prober mtools
    grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck
    mkdir /boot/grub/locale
    cp /usr/share/locale/en\@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo
    grub-mkconfig -o /boot/grub/grub.cfg
}


cat ./title.txt

printf "---- CREATING PARTITIONS ----\n"
disk=$(askDiskName)
efiPartitionSize=$(askPartitionSize $EFI_PARTITION_SIZE_TEXT $EFI_PARTITION_SIZE)
mainPartitionSize=$(askPartitionSize $MAIN_PARTITION_SIZE_TEXT $MAIN_PARTITION_SIZE)
printf "Creating partitions on /dev/${disk}\n"
partitionDisk $disk $efiPartitionSize $mainPartitionSize
efiPartition="${disk}1"
partition="${disk}2"
printf "Creating EFI and LVM partitions\n"
createEfiAndLvmPartitions $efiPartition $partition

printf "---- INSTALLING SYSTEM ----\n"
installKernel $efiPartition
configureSystem

printf "---- INSTALLING BOOTLOADER ----\n"
installBootloader

printf "Rebooting"
exit
umount -R /mnt
reboot


# printf "Installing network tools\n"
# pacman -S --noconfirm iwd

# printf "Installing utilities\n"
# pacman -S --noconfirm vim base-devel openssh