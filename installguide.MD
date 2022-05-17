# Arch Linux Installation (as of 2022)

If your system BIOS is UEFI (which most probably is) you must enable it before installing Arch Linux.

## Establishing an Internet Connection

To install Arch Linux an Internet connection is required since many parts of the software must be downloaded. First of all, it is necessary to check if 
the install medium correctly detects the system's network hardware.

### List Networking Devices
To print a list of all of your networking devides run the command `ip link`. If, among the listed devices, you see an item similiar to the following, 
`enp020f0u2u3: <BROADCAST, MULTICAST, UP, LOWER_UP> ...`, it means you have a functioning wired connection and you don't need to take any further action. 
If you see something like `wlan0: <NO-CARRIER. BROADCAST, MULTICAST, UP> ... state DOWN mode DORMANT ...` it means that you have a 
wireless device but it is not enabled. In order to see if your devices are connected to your local network run the command `ip a` to show a very similar 
list of your devices and their associated IP addresses. If you don't see an IP address then you must troubleshoot that before continuing.

#### Enabling Wireless Connection

To enable your wireless device run the command `iwctl` to access a shell for configuring the device. Inside the configuration shell run the command 
`device list` to see a list of the detected wireless devices. If you don't see a any device listed or if your listed devices are not working properly 
you should solve that problem first before continuing with the installation.

Run the command `station wlan0 scan` (substitute `wlan0` for the name of your devide) to scan for available networks, in order to actually print the 
networks run the command `station <yourDeviceName> get-networks`. Finally, run the command `station <yourDeviceName> connect "<yourNetwork>"` to connect 
to your wireless network. You will be prompted for the network's password, after you enter it your device should be connected (you may want to wait for 
a couple of seconds to make sure your device had enough time to establish the connection). Hit Ctrl + D to exit the shell.

### Testing your Internet Connection

To verify that your Internet connection is functioning properly run the command `ping -c 5 8.8.8.8` to send 5 packets of data to Google's DNS server 
(8.8.8.8). You should see a text confirming that the server actually received the packets, which means that your connection is working. If you cannot 
send data to the server you must troubleshoot your Internet connection with your service provider.

## Formating the Disk

In order to install the operating system you need to allocate enough space in your hardrive to write all the needed programs and the data you will store 
once you start using it. If you are installing Arch Linux alongside Windows in the same hard drive go to the section 
[Formating a Disk with Windows](https://github.com/Fugante/Arch-Linux-Installation/new/main#formating-a-disk-with-windows), otherwise continue to next 
section in order to use the whole drive for Linux.

### Partitioning a Dedicated Disk

Run the command `fdisk /dev/<yourDisk>` to modify the disk's partition table in interactive mode. **Do not** enter the name of a 
logical partition, only use the name of the physical volume (eg.: use /dev/sda, not /dev/sda1). The instructions to format your disk are different 
depending on wheter you have Windows in the same hardrive or not.

If you do not have Windows you have to create a partition scheme and create 2 partitions, one for the OS and the other for the boot process.
To create a partition scheme hit the the letter **g** to create a [GPT Scheme](). Next, for the boot partition, hit the letter **n** to create a new 
partition. Just after that you will be asked to select the new partition's starting sector, just hit **Enter** to accept the default value. Then, type 
`+500M` to allocate 500 MiB of memory (no more is needed). After that, type **t** to select the type partition type; select the [EFI Partition](). Now 
you must create a partition for storing the operating system. Hit **n** again to create a new partition. Again, select the default value for the 
starting sector. When asked to select the ending sector just hit **Enter** to use all the avaiable space (if that is what you want). Type **t** again 
to select the partition type and type **2** to select the 2nd partition. This time select Linux LVM. Finally, type **w** to apply the changes and exit 
the program.

### Partitioning a Disk with Windows

If you want to install Arch Linux in a system that already has Windows installed, and you don't want to remove it, then you need to take enough space 
for Linux. The ideal situation would be to install new separate hardrive altogether, but since that is not always possible then you need to take it 
from the existing Windows filesystem. To allocate some space, enter to the Windows OS and open the disk management utility 
(it usually is [diskmgmt.msc]()). It may be usefull to format the new partition (NTFS, FAT32, etc.) because some Linux programs such as `fdisk` or 
`cfdisk` may not be able to recognize the free space.

Now, you just have to reformat the partition that you allocated for Linux. Run the command `fdisk /dev/<yourDisk>` to format your 
physical disk. Type **t** to change the type of one of the existing logical partitions. Select the number of the partition you want to modify. **Be extra 
careful here, you may lose all your data and your Windows installation if you format the wrong partition**.

### Formating the Partitions

If you have Windows installed, then you already have a UEFI partition and you just have to format the partition where Linux will live. Run the command 
`pvcreate --dataalignment 1m /dev/<yourDiskAndPartitionNumber>` to create a new LVM physical volume. Next, create a new volume group and assign it to 
the LVM partition with the command `vgcreate volgroup0 /dev/<yourDiskAndPartitionNumber>`. In this case volgroup0 is the name of the volume. Then, 
you must create a logical volume, which acts similar to a disk partition, using the command `lvcreate -L 30GB <volumeName> -n lv_root`. The previous 
command creates a new logical volume in the specified volumen (eg.: volumeName = volgroup0), allocates 30GB of space for it and names it lv_root. Repeat 
the previous step to create a new volume that will hold all of the data not critical for the OS. Run `lvcreate -l 100%FREE <volumeName> -n lv_home`. In 
this case the option `-l 100%FREE` tells the program to use all remaining available space.

Once the logical volumes have been created you have to run a series of commands to verify that they were created properly. Run `modprobe dm_mod` to 
activate the volumes. Then, run `vgscan` to scan for volume groups, you should see the the of the volume group that you created in the previous steps. 
Finally, activate the volume groups by running the command `vgchange -ay`.

Now that the LVM volumes are configured and running, you must create a filesytem format in order to be able to use them. To create a Linux filesystem 
format run `mkfs.ext4 /dev/<volumeGroup>/<logicalVolume>` (/dev/volgroup0/lv_root if you used the names in the guide). Do the same for the other logical 
volume. The final step is to mount the partitions and create a file to tell the OS the structure of the disk. Mount the lv_root volume in the /mnt 
directory by running `mount /dev/<volumeGroup>/<rootLogicalVolume> /mnt`. Create a new directory in the mounted volume with the command 
`mkdir /mnt/home`. Use that new directory to mount the other volume, `mount /dev/<volumeGroup>/<homeLogicalVolume> /mnt/home`. If you have Windows 
installed, you also need to mount the EFI partition, run `mkdir /mnt/efi` followed by `mount /dev/<windowsEFIPartition> /mnt/efi`. Finally create a 
[genfstab]() file by running the commands `mkdir /mnt/etc` and `genfstab -U -p >> /mnt/etc/fstab`. You can verify that all of the partitions are listed 
in the file by running `cat /mnt/etc/fstab`.

## Installing the Kernel

Finally now you are able to actually install the operating system. The actual installation is quite simple and you only need to run a couple of 
commands. First run `pacstrap -i /mnt base` to install the base programs. Now you have to change your working directory in order to continue. Run 
`arch-root /mnt` to enter as the root user in the /mnt directory where the OS will be installed. Then, run 
`pacman -S linux linux-headers linux-lts linux-lts-headers` to install the most up-to-date Linux kernel as well as the long-term-support one.
And, that's it! You have Installed Arch Linux.

### Installing Additional Packages

Although you already have installed the operating system, you may want (you obviously want) to install additional tools to make the OS more friendly. 
Use [pamcan]() to install anything else you may need. Here is a list of packages I recomend installing:
- [vim](). VIM text editor
- [base-devel](). Developer utilities such as grep, sed, etc.
- [openssh](). A ssh protocol comunications manager (run `systemctl enable sshd` to enable it)
- [networkmanager]() (run `systemctl enable NetworkManager` to enable it)
- [wpa_supplicant]()
- [wireless_tools]()
- [netctl]()
- [dialog](). Connect to WiFi bia command line
- [lvm2](). LVM support

### Configuring the OS

With that your are almost done installing Arch Linux. But, there are still some configuration files to change and commands to run before rebooting the
system.

First, go to the file located at /etc/mkinitcpio.conf and change the line that has written "HOOKS=(base udev ... block filesystems ...)" so that it now 
says "HOOKS=(base udev ... block lvm2 filesystems ...)". Make the change take effect by running the commands `mkinitcpio -p linux` and 
`mkinitcpio -p linux-lts`. 

Now, go to the file at /etc/locale.gen and remove the hash symbol (uncomment) in the line that corresponds to your locale. For instance, if your locale
is Mexican Spanish, uncomment the line that says "#es_MX.UTF-8 UTF-8". Then run `locale-gen` to make the change take effect.

### Making a User

You also want (need) to create a user to login next time you boot the system since doing everything as the root user is a terrible idea. First, make 
sure no one can operate as the root user without a password. Run `passwd` and enter the password when the prompt ask you to do it. Next, crate a the 
user you will be using. Run `useradd -m -g users -G wheel <username>` to create a new user and add it to the users and wheel groups. Then run 
`passwd <username>` to set a new password for your newly created user and you are done.

You may want to install **sudo** to gain root privileges temporarily. Install the package with pacman, `pacman -S sudo`. Next you just need to change a 
configuration file to make sudo work properly. Run the command `EDITOR=vim visudo` to edit the sudo config file using vim. Uncomment the line that says 
"%wheel ALL=(ALL) ALL". With that you should be able to sudo in and out of the root user.

## GRUB Installation (for UEFI Systems)

By this point you have allocated as much memory in the hard drive as you want for the OS, created the filesystem, installed Linux and done the basic 
configurations. However, if you reboot your computer you won't be able to enter into your fresh new Arch Linux system. For that to happen you still need 
install [GRUB](), a boot utility that detects the bootable sections of your hardrive and the installed operating systems.

To install grub first download it with pacman along with other utilities, `pacman -S grub efibootmgr dosfstools os-prober mtools`. The 
[efibootmgr]() allows GRUB to run in UEFI systems; [os-prober]() is a utility that allows Arch Linux detect Windows operating systems. Now create a 
directory called "efi" in the boot dir (if you haven't already), `mkdir /boot/EFI`. Mount the EFI partition into the new directory by running 
`mount /dev/<EFIPartition>`. Next, install GRUB using the command `grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck`. You can 
specify the efi directory by passing the argument `--efi-directory=/<pathToDir>`. Then, create the directory `mkdir /boo/grub/locale` if it doesn't exist 
already. Copy the file GRUB messages file to the GRUB directory, `cp /usr/share/locale/en\@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo`. Finally, 
generate the configuration file by running the command `grub-mkconfig -o /boot/grub/grub.cfg`.

Congratulations! Now you should be able to reboot your system and enter into your brand-new Arch Linux system. To reboot the system run `exit` to get out 
of the arch-linux root. Now run `umount -a` to unmount all the devices. Now you can run `reboot` to restart your system.
