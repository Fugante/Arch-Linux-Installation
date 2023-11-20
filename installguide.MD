# Arch Linux Installation (as of 2022)
If your system BIOS is UEFI (which most probably is) you must enable it before installing
Arch Linux.

## Establishing an Internet Connection
To install Arch Linux an Internet connection is required since many parts of the software
must be downloaded. First of all, it is necessary to check if the install medium
correctly detects the system's network hardware.

### List Networking Devices
To print a list of all of your networking devides run the command

```shell
ip link
```

If, among the listed devices, you see an item similiar to this:

```shell
enp020f0u2u3: <BROADCAST, MULTICAST, UP, LOWER_UP> ...
```

it means you have a functioning
wired connection and you don't need to take any further action. If you see something like

```shell
wlan0: <NO-CARRIER. BROADCAST, MULTICAST, UP> ... state DOWN mode DORMANT ...
```

it means that you have a wireless device but it is not enabled. In order to see if your
devices are connected to your local network run the command

```shell
ip a
```

to show a very similar list of your devices and their associated IP addresses. If you
don't see an IP address then you must troubleshoot that before continuing.

#### Enabling Wireless Connection
To enable your wireless device enter the [iwctl](https://wiki.archlinux.org/title/Iwd)
shell:

```shell
iwctl
```

To access a shell for configuring the device. Inside the configuration shell run the
following command to see a list of the detected wireless devices.

```shell
device list
```

If you don't see a any device listed or if your listed devices are not working properly
you should solve that problem first before continuing with the installation.

Run the next command to scan for available networks.

```shell
station <deviceName> scan
```

In order to actually print the networks run the command

```shell
station <yourDeviceName> get-networks
```

Finally, to  connect to your wireless network run the command:

```shell
station <yourDeviceName> connect "<yourNetwork>"
```

You will be prompted for the network's password, after you enter it your device should be
connected (you may want to wait for a couple of seconds to make sure your device had
enough time to establish the connection). Hit `Ctrl + D` to exit the shell.

### Testing your Internet Connection
To verify that your Internet connection is functioning properly run the command

```shell
ping -c 5 8.8.8.8
```

 to send 5 packets of data to Google's DNS server (8.8.8.8). You should see a text
confirming that the server actually received the packets, which means that your
connection is working. If you cannot send data to the server you must troubleshoot your
Internet connection with your service provider.

## Formating the Disk
In order to install the operating system you need to allocate enough space in your
hardrive to write all the needed programs and the data you will store once you start
using it. If you are installing Arch Linux alongside Windows in the same hard drive go to
the section
[Formating a Disk with Windows](https://github.com/Fugante/Arch-Linux-Installation/new/main#formating-a-disk-with-windows),
otherwise continue to next section in order to use the whole drive for Linux.

### Partitioning a Dedicated Disk
Run the command

```
fdisk /dev/<yourDisk>
```

to modify the disk's partition table in interactive mode. **Do not** enter the name of a
logical partition, only use the name of the physical volume (e.g.: use /dev/sda, **not**
/dev/sda1). The instructions to format your disk are different depending on wheter you
have Windows in the same hardrive or not.

If you do not have Windows you have to create a partition scheme and create 2 partitions,
one for the OS and the other for the boot process. To create a partition scheme hit the
the letter `g` to create a [GPT Scheme](). Next, for the boot partition, hit the letter
`n` to create a new partition. Just after that you will be asked to select the new
partition's starting sector, just hit `Enter` to accept the default value. Then,
type `+500M` to allocate 500 MiB of memory (no more is needed). After that, type `t` to
select the type partition type; select the [EFI Partition](). Now you must create a
partition for storing the operating system. Hit `n` again to create a new partition.
Again, select the default value for the starting sector. When asked to select the ending
sector just hit `Enter` to use all the avaiable space (if that is what you want). Type
`t` again to select the partition type and type `2` to select the 2nd partition. This
time select Linux LVM. Finally, type `w` to apply the changes and exit the program.

### Partitioning a Disk with Windows
If you want to install Arch Linux in a system that already has Windows installed, and you
don't want to remove it, then you need to take enough space for Linux. The ideal
situation would be to install new separate hardrive altogether, but since that is not
always possible then you need to take it from the existing Windows filesystem. To
allocate some space, enter to the Windows OS and open the disk management utility (it
usually is [diskmgmt.msc]()). It may be usefull to format the new partition (NTFS, FAT32,
etc.) because some Linux programs such as `fdisk` or `cfdisk` may not be able to
recognize the free space.

Now, you have to reformat the partition that you allocated for Linux. Run the
command

```shell
fdisk /dev/<yourDisk>
```

to format your physical disk. Type `t` to change the type of one of the existing logical
partitions. Select the number of the partition you want to modify. **Be extra careful
here, you may lose all your data and your Windows installation if you format the wrong
partition**.

### Formating the Partitions
If you have Windows installed, then you already have a UEFI partition and you just have
to format the partition where Linux will live. First, to create a new LVM physical
volume run the command

```shell
pvcreate --dataalignment 1m /dev/<yourDiskAndPartitionNumber>
```

Next, create a new volume group and assign it to the LVM partition with
the command

```shell
vgcreate volgroup0 /dev/<yourDiskAndPartitionNumber>
```

In this case volgroup0 is the name of the volume. Then, you must create a logical volume,
which acts similar to a disk partition, using the command

```shell
lvcreate -L 30GB <volumeName> -n lv_root
```

The previous command creates a new logical volume in the specified volumen
(e.g.: volumeName = volgroup0), allocates 30GB of space for it and names it lv_root.
Repeat the previous step to create a new volume that will hold all of the data not
critical for the OS. Run

```shell
lvcreate -l 100%FREE <volumeName> -n lv_home
```

In this case the option `-l 100%FREE` tells the program to use all remaining available
space.

Once the logical volumes have been created you have to run a series of commands to verify
that they were created properly. to activate the volumes run:

```shell
modprobe dm_mod
```

Then, to scan for volume groups run:

```shell
vgscan
```

You should see listed the name of the volume group that you created in the previous
steps. Finally, activate the volume groups by running the command

```shell
vgchange -ay
```

Now that the LVM volumes are configured and running, you must create a filesytem format
in order to be able to use them. To create a Linux filesystem format run
(`/dev/volgroup0/lv_root` if you used the names in this guide):

```shell
mkfs.ext4 /dev/<volumeGroup>/<rootLogicalVolume>
```

Do the same for the other logical volume.

```shell
mkfs.ext4 /dev/<volumeGroup>/<homeLogicalVolume>
```

Also, you need to format the EFI partition in order install grub later on.

```shell
mkfs.fat -F32 /dev/<efiPartition>
```

The final step is to mount the partitions and
create a file to tell the OS the structure of the disk. Mount the lv_root volume in the
/mnt directory by running

```shell
mount /dev/<volumeGroup>/<rootLogicalVolume> /mnt
```

Create a new directory in the mounted volume with the command

```shell
mkdir /mnt/home
```

Use that new directory to mount the other volume:

```shell
mount /dev/<volumeGroup>/<homeLogicalVolume> /mnt/home
```

If you have Windows installed, you also need to mount the EFI partition, run:

```shell
mkdir /mnt/efi
mount /dev/<windowsEFIPartition> /mnt/efi
```

Finally create a [genfstab](https://wiki.archlinux.org/title/Fstab) file by running the
commands:

```shell
mkdir /mnt/etc
genfstab -U -p /mnt > /mnt/etc/fstab
```

You can verify that all of the partitions are listed in the file by running

```shell
cat /mnt/etc/fstab
```

## Installing the Kernel
Finally now you are able to actually install the operating system. The actual
installation is quite simple and you only need to run a couple of commands. To install
the base programs first run:

```shell
pacstrap -i /mnt base
```

Now you have to change your working directory in order to continue. Run

```shell
arch-chroot /mnt
```

to enter as the root user in the /mnt directory where the OS will be installed. Then, run

```shell
pacman -S linux linux-headers linux-lts linux-lts-headers linux-firmware
```

to install the most up-to-date Linux kernel as well as the long-term-support one. And,
that's it! You have installed Arch Linux.

### Installing Additional Packages
Although you already have installed the operating system, you may want (you obviously
want) to install additional tools to make the OS more friendly. Use
[pamcan](https://wiki.archlinux.org/title/pacman) to install anything else you may need.
Here is a list of packages may be usefull to have:
- [vim](https://wiki.archlinux.org/title/vim). VIM text editor
- [base-devel](https://archlinux.org/groups/x86_64/base-devel/).
Developer utilities such as grep, sed, etc.
- [openssh](https://www.openssh.com/).
A ssh protocol comunications manager (`systemctl enable sshd` to enable it)
- [networkmanager](https://networkmanager.dev/)
(`systemctl enable NetworkManager` to enable it)
- [wireless_tools](https://hewlettpackard.github.io/wireless-tools/Tools.html)
- [netctl](https://wiki.archlinux.org/title/netctl)
- [lvm2](https://sourceware.org/lvm2/). LVM support

### Critical Configurations
With that your are almost done installing Arch Linux. But, there are still some
configuration files to change and commands to run before rebooting the system.

First, go to the file located at /etc/mkinitcpio.conf and change the line that has
written "HOOKS=(base udev ... block filesystems ...)" so that it now says "HOOKS=(base
udev ... block lvm2 filesystems ...)". Make the change take effect by running the
commands

```shell
mkinitcpio -p linux
mkinitcpio -p linux-lts
```

Now, go to the file at /etc/locale.gen and remove the hash symbol (uncomment) in the line
that corresponds to your locale. For instance, if your locale is Spanish - Mexico,
uncomment the line that says "#es_MX.UTF-8 UTF-8". Then run

```shell
locale-gen
```

to make the change take effect.

### Making a User
You also need to create a user to login next time you boot the system since doing
everything as the root user is a terrible idea. First, make sure no one can operate as
the root user without a password. Run

```shell
passwd
```

and enter the password when the prompt ask you to do it. Next, crate a the user you will
be using. Run

```shell
useradd -m -g users -G wheel <username>
```

to create a new user and add it to the users and wheel groups. Then run

```shell
passwd <username>
```

to set a new password for your newly created user and you are done.

You may want to install sudo to gain root privileges temporarily. Install the package
with pacman

```shell
pacman -S sudo
```

Next you just need to change a configuration file to make sudo work properly. Run the
command

```shell
sed -E 's/#.*(wheel.*)/\1/' -i /etc/sudoers
```

uncomment the line that says "%wheel ALL=(ALL)ALL". Now you should be able to sudo in and
out of the root user.

## GRUB Installation (for UEFI Systems)
By this point you have allocated as much memory in the hard drive as you want for the OS,
created the filesystem, installed Linux and done the basic configurations. However, if
you reboot your computer you won't be able to enter into your fresh new Arch Linux
system. For that to happen you still need install
[GRUB](https://www.gnu.org/software/grub/), a boot utility that detects the bootable
sections of your hardrive and the installed operating systems.

To install grub first download it with pacman along with other utilities,

```shell
pacman -S grub efibootmgr dosfstools os-prober mtools
```

The [efibootmgr](https://github.com/rhboot/efibootmgr) allows GRUB to run in UEFI
systems; [os-prober](https://joeyh.name/code/os-prober/) is a utility that allows Arch
Linux detect Windows operating systems. Now create a directory called "efi" or "EFI" in the boot
dir (if you haven't already)

```shell
mkdir /boot/efi
```

Mount the EFI partition into the new directory by running

```shell
mount /dev/<EFIPartition>
```

Next, install GRUB using the command

```shell
grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck
```

You can specify the efi directory by passing the argument `--efi-directory=/<pathToDir>`.
Then, create the directory boot/grub/locale if it doesn't exist already

```shell
mkdir /boot/grub/locale
```

Copy the file GRUB messages file to the GRUB directory,

```shell
cp /usr/share/locale/en\@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo
```

Finally, generate the configuration file by running the command

```shell
grub-mkconfig -o /boot/grub/grub.cfg
```

Congratulations! Now you should be able to reboot your system and enter into your
brand-new Arch Linux system. To reboot the system run

```shell
exit
```

to get out of the arch-linux root. Now run

```shell
umount -a
```

to unmount all the devices. Now you can run

```shell
reboot
```

to restart your system.

## Configuring Arch Linux
Once you have Arch Linux installed you may start using for whatever you want, but,
most certainly, 5 minutes won't pass before you need to tweak some part of your system.

### Timezone
To see a list of available timezones use the command

```shell
timedatectl list-timezones
```

To set your timezone run the command

```shell
timedatectl set-timezone <timezone>
```

### System Clock
The system's clock is set and synchronized according to your hardware clock. However, it
may be off by some small amount of time. To have synchronized with the web's clock use
[systemd-timesyncd](https://wiki.archlinux.org/title/systemd-timesyncd)

```shell
systemctl enable systemd-timesyncd
```

### Network Configurations
In order to able to use to connect to either local and external networks, and access the
internet, you need to configure your networking programs.

First, set your system's [hostname](https://en.wikipedia.org/wiki/Hostname). Run

```shell
hostnamectl set-hostname <hostname>
```

to set it. Next add the the localhost address and hostname's address to the host file,
you can do it with simply by running

```shell
echo "127.0.0.1" localhost >> /etc/hosts
echo "127.0.1.1" <hostname> >> /etc/hosts
```

If you are using a wired connection, you should have already an internet connection. If
you are going to use a wifi connection you need to do some further configurations.
By this point you should already have enabled the NetworkManager daemon. Run

```shell
systemctl enable NetworkManager
```

if it's not enabled. Then use the [nmcli](https://man.archlinux.org/man/nmcli.1) to
connect to your wireless network. To display a list available networks:

```shell
nmcli device wifi list
```

To connect to a network run

```shell
nmcli device wifi connect <SSID_or_BSSID> password <password>
```

With that, your connection should be stablished. You can always use `ip a` to show a
list of your networking hardware and their associated IP address. Also, use
`ping <address>` to test your internet connection.

## Troubleshooting Arch Linux
Even if you did followed the steps correctly and your installation process went smooth,
you may find any kind of problem when you first start Arch Linux. There is no simple way
to know the way to solve the problem since it may be caused by anything. Notheless, there
are some problems that are more common than others and therefore easier to troubleshoot.

### Graphics Card Related Errors
One of the most common source of errors is the graphics card compatibility. If you
initialize the OS and the screen freezes or the text is badly rendered you may have
compability issue with your graphics card.

You can change the graphics settings at boot time by using GRUB's tools. In the GRUB
OS menu, press `e` to edit the boot script. You will se a list of commands for booting
the system. Go to line that says "linux ..." and add the word "nomodeset" at the end. It
should be something like this
"linux /boot/vmlinuz-linux-lts root=/dev/sda1 rw loglevev=3 nomodeset". Then hit
`Ctrl + X` to boot using the modified script. Your system should boot without freezing
now. Bear in mind that this is no solution! You should find the root of the problem
(perhaps wrong video drivers) and fix it so you don't have to boot the OS using this
method.
