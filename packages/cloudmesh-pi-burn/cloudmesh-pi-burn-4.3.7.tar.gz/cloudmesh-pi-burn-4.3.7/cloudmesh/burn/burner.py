import crypt
import os
import pathlib
import random
import re
import string
import subprocess
import sys
import textwrap
import time

from cloudmesh.burn.image import Image
from cloudmesh.burn.sdcard import SDCard
from cloudmesh.burn.usb import USB
from cloudmesh.burn.util import os_is_linux
from cloudmesh.burn.util import os_is_mac
from cloudmesh.burn.util import os_is_pi
from cloudmesh.burn.util import os_is_windows
from cloudmesh.common.JobScript import JobScript
from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.Tabulate import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.util import banner
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile
from cloudmesh.common.util import yn_choice


# TODO: make sure everything is compatible with --dryrun

def sudo_writefile(filename, content, append=False):
    """
    Write a file into the file with the given filename using sudo
    The file is first created in ~/.cloudmesh/tmp/tmp.txt

    TODO: append is not implemented

    :param filename: The filename
    :type filename: str
    :param content: The content of the file
    :type content: str
    :param append: if True the content will be appended to the existing file
    :type append: bool
    :return: The new content of the file
    :rtype: str
    """
    os.system('mkdir -p ~/.cloudmesh/tmp')
    tmp = "~/.cloudmesh/tmp/tmp.txt"

    if append:
        content = sudo_readfile(filename, split=False) + content

    writefile(tmp, content)

    result = subprocess.getstatusoutput(f"sudo cp {tmp} {filename}")

    # If exit code is not 0
    if result[0] != 0:
        Console.warning(f"{filename} was not created correctly -> {result[1]}")

    return result[1]


def sudo_readfile(filename, split=True):
    """
    Reads the file specified via sudo by filename and returns its content

    :param filename: The filename
    :type filename: str
    :param split: if True splits the lines and returns a list
    :type split: bool
    :return: either str or list of the file content
    :rtype: str or list
    """
    result = subprocess.getoutput(f"sudo cat {filename}")

    if split:
        result = result.split('\n')

    return result


# def dmesg():
#    return subprocess.getoutput(f"dmesg")

def gen_strong_pass():
    """
    Generates a password from letters, digits and punctuation

    :return: password
    :rtype: str
    """
    length = random.randint(10, 15)
    password_characters = \
        string.ascii_letters + \
        string.digits + \
        string.punctuation
    return ''.join(random.choice(password_characters) for i in range(length))


# noinspection PyPep8
class Burner(object):

    def __init__(self, dryrun=False):
        """
        Initializes the burner

        TODO: dryrun may not be specified for all functions. Not yet enabled.
              Hence do not use dryrun

        :param dryrun: if True onle the commands will be listed that would
                       be executed
        """
        self.dryrun = dryrun
        self.hostname = None
        self.keypath = None

    def shrink(self, image=None):
        if image is None:
            Console.error("Image must have a value")
        image = path_expand(image)
        command = f"sudo /usr/local/bin/pishrink.sh {image}"
        print(command)
        os.system(command)

    def shrink_install(self):
        """
        Installs /usr/local/bin/pishrink.sh
        @return:
        @rtype:
        """

        if os_is_linux():
            banner("Installing pishrink.sh into /usr/local/bin")
            script = \
                """
                wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
                chmod +x pishrink.sh
                sudo mv pishrink.sh /usr/local/bin
                """

            result = JobScript.execute(script)
            print(Printer.write(result,
                                order=["name", "command", "status", "stdout", "returncode"]))
        else:
            raise NotImplementedError

    def backup(self, device=None, to_file=None, blocksize="4M"):
        if device is None:
            Console.error("Device must have a value")
        if to_file is None:
            Console.error("To file must have a value")
        else:
            to_file = path_expand(to_file)
            command = f"sudo dd if={device} bs={blocksize} |" \
                      f" pv -w 80 |" \
                      f"dd of={to_file} bs={blocksize} conv=fsync status=progress"
            print(command)
            os.system(command)

    def copy(self, device=None, from_file=None):
        if device is None:
            Console.error("Device must have a value")
        if from_file is None:
            Console.error("From file must have a value")
        burner.burn_sdcard(from_file, device)

    def detect(self):
        """
        Detects if a USB card writer can be found. and just prints the result
        """
        # Clear dmesg table so that info doesn't get confused with previous detects
        self.system('sudo dmesg -c')
        banner("Detecting USB Card Writers(s)")

        print("Make sure the USB Writers(s) is removed ...")
        if not yn_choice("Is the writer(s) removed?"):
            sys.exit()
        usb_out = set(Shell.execute("lsusb").splitlines())
        print("Now plug in the Writer(s) ...")
        if not yn_choice("Is the writer(s) plugged in?"):
            sys.exit()
        usb_in = set(Shell.execute("lsusb").splitlines())

        writer = usb_in - usb_out
        if len(writer) == 0:
            print(
                "ERROR: we did not detect the device, make sure it is plugged.")
            sys.exit()
        else:
            banner("Detected Card Writers")

            print("\n".join(writer))
            print()

    def info(self, print_stdout=True):
        """
        Finds out information about USB devices

        TODO: should we rename print_stdout to debug? seems more in
              line with cloudmesh

        :param print_stdout: if set to True prints debug information
        :type print_stdout: bool
        :return: dict with details about the devices
        :rtype: dict
        """

        print("dryrun:    ", self.dryrun)

        if os_is_pi():
            banner("This is  Raspberry PI")
        elif os_is_mac():
            banner("This is Mac")
        elif os_is_windows():
            banner("This is a Windows COmputer")
        elif os_is_linux():
            banner("This is a Linux Computer")
        else:
            Console.error("unkown OS")
            sys.exit(1)

        if os_is_pi():
            result = USB.fdisk("/dev/mmcblk0")
            if print_stdout:
                banner("Operating System SD Card")
                print(result)

        details = USB.get_from_usb()

        if print_stdout:
            banner("USB Device Probe")
            print(Printer.write(
                details,
                order=["address",
                       "bus",
                       "idVendor",
                       "idProduct",
                       "hVendor",
                       "hProduct",
                       "iManufacturer",
                       "iSerialNumber",
                       "usbVersion",
                       "comment"],
                header=["Adr.",
                        "bus",
                        "Vendor",
                        "Prod.",
                        "H Vendor",
                        "H Prod.",
                        "Man.",
                        "Ser.Num.",
                        "USB Ver.",
                        "Comment"]
            )
            )

        # devices = USB.get_devices()

        # banner("Devices found")

        # print ('\n'.join(sorted(devices)))

        details = USB.get_from_dmesg()

        if print_stdout:
            banner("SD Cards Found")
            print(Printer.write(details,
                                order=[  # "name",
                                    "dev",
                                    # "device",
                                    # "bus",
                                    # "sg",
                                    "active",
                                    "info",
                                    "readable",
                                    "formatted",
                                    "empty",
                                    "size",
                                    "direct-access",
                                    "removable",
                                    "writeable"],
                                header=[  # "Name",
                                    "Path",
                                    # "Device",
                                    # "Bus",
                                    # "Sg",
                                    "Plugged-in",
                                    "Info",
                                    "Readable",
                                    "Formatted",
                                    "Empty",
                                    "Size",
                                    "Access",
                                    "Removable",
                                    "Writeable"]))

            # lsusb = USB.get_from_lsusb()
            # from pprint import pprint
            # pprint (lsusb)

            # endors = USB.get_vendor()
            # print(vendors)

            # udev = subprocess.getoutput("udevadm info -a -p  $(udevadm info -q path -n /dev/sda)")
            #
            # attributes = ["vendor","model", "model", "version", "manufacturer",
            #     "idProduct", "idVendor"]
            # for line in udev.splitlines():
            #    if any(word in line for word in attributes):
            #        print(line)

        if print_stdout:

            if os_is_linux():
                card = SDCard(os="raspberry", host="ubuntu")
                m = card.ls()

                banner("Mount points")
                if len(m) != 0:
                    print(Printer.write(m,
                                        order=["name", "path", "type", "device", "parameters"],
                                        header=["Name", "Path", "Type", "Device", "Parameters"]))
                else:
                    Console.warning("No mount points found. Use cms burn mount")
                    print()

        # Convert details into a dict where the key for each entry is the device
        details = {detail['dev']: detail for detail in details}

        return details

        #
        # use also lsub -v
        #

        # see also
        # https://raspberry-pi-guide.readthedocs.io/en/latest/system.html
        # this is for fedora, but should also work for raspbian

    def system(self, command):
        """
        System command that uses subprocess to execute terminal commands
        Returns the stdout of the command

        TODO: check typr of return

        :param command: the command
        :type command: str
        :return: the stdout of the command
        :rtype: str
        """
        # if self.dryrun:
        #     print(command)
        # else:
        #     os.system(command)
        res = subprocess.getstatusoutput(command)
        # If exit code is not 0, warn user
        if res[0] != 0 and res[0] != 32:
            Console.warning(
                f'Warning: "{command}" did not execute properly -> {res[1]} :: exit code {res[0]}')

        return res[1]

    def burn_sdcard(self, image, device, blocksize="4M"):
        """
        Burns the SD Card with an image

        :param image: Image object to use for burning
        :type image: str
        :param device: Device to burn to, e.g. /dev/sda
        :type device: str
        :param blocksize: the blocksize used when writing, default 4M
        :type blocksize: str
        """
        if os_is_pi():

            image_path = Image(image).fullpath

            command = f"sudo dd bs={blocksize} if={image_path} of={device}"

            result = subprocess.getoutput(command)

            if "failed to open" in result:
                Console.error("The image could not be found")
                sys.exit(1)
        elif os_is_linux():
            image_path = Image(image).fullpath

            print(image_path)
            print(device)
            print(blocksize)
            if device is None:
                # or device == "none":
                Console.error("Please specify a device")

            # find device

            command = f"dd if={image_path} |" \
                      " pv -w 80 |" \
                      " sudo dd of={device} bs={blocksize} conv=fsync status=progress"
            print(command)
            os.system(command)

        else:
            raise NotImplementedError("Only implemented to be run on a PI")

    def set_hostname(self, hostname, mountpoint):
        """
        Sets the hostname on the sd card

        :param hostname: the hostname
        :type hostname: str
        :param mountpoint: the mountpunt of the device on which the hostanme
                           is found
        :type mountpoint: str
        """
        self.hostname = hostname
        # write the new hostname to /etc/hostname
        if not self.dryrun:
            self.system(
                f'echo {hostname} | sudo cp /dev/stdin {mountpoint}/etc/hostname')
        else:
            print()
            print("Write to /etc/hostname")
            print(hostname)

        # change last line of /etc/hosts to have the new hostname
        # 127.0.1.1 raspberrypi   # default
        # 127.0.1.1 red47         # new
        if not self.dryrun:
            # with open(f'{mountpoint}/etc/hosts', 'r') as f:  # read /etc/hosts
            f = sudo_readfile(f'{mountpoint}/etc/hosts')
            # lines = [l for l in f.readlines()][:-1]  # ignore the last line
            lines = f[:-1]
            newlastline = '127.0.1.1 ' + hostname + '\n'

        if not self.dryrun:
            new_hostsfile_contents = ''.join(lines) + newlastline
            sudo_writefile(f'{mountpoint}/etc/hosts', new_hostsfile_contents)
        else:
            print()
            print("Write to /etc/hosts")
            print('127.0.1.1 ' + hostname + '\n')

    def set_static_ip(self, ip, mountpoint, iface="eth0", mask="16"):
        """
        Sets the static ip on the sd card for the specified interface
        Also writes to master hosts file for easy access

        :param ip: ips address
        :type ip: str
        :param mountpoint: the mountpunt of the device on which the ip
                           is found
        :type mountpoint: str
        :param iface: the network Interface
        :type iface: str
        :param mask: the subnet Mask
        :type mask: str
        :return:
        :rtype:
        """

        # Adds the ip and hostname to /etc/hosts if it isn't already there.
        def add_to_hosts(ip):
            # with open('/etc/hosts', 'r') as host_file:
            #     hosts = host_file.readlines()
            hosts = sudo_readfile('/etc/hosts')

            replaced = False
            for i in range(len(hosts)):
                ip_host = hosts[i].split()

                if len(ip_host) > 1:
                    if ip_host[0] == ip:
                        ip_host[1] = self.hostname
                        hosts[i] = f"{ip_host[0]}\t{ip_host[1]}\n"
                        replaced = True

                    elif ip_host[1] == self.hostname:
                        ip_host[0] = ip
                        hosts[i] = f"{ip_host[0]}\t{ip_host[1]}\n"
                        replaced = True
            if not replaced:
                hosts.append(f"{ip}\t{self.hostname}\n")

            # with open('/etc/hosts', 'w') as host_file:
            #     host_file.writelines(hosts)
            config = ""
            for line in hosts:
                config = config + line + '\n'

            sudo_writefile('/etc/hosts', config)

        # Add static IP and hostname to master's hosts file and configure worker with static IP
        if not self.dryrun:
            add_to_hosts(ip)

            # Configure static LAN IP
            if iface == "eth0":
                interfaces_conf = textwrap.dedent(f"""
                auto {iface}
                iface {iface} inet static
                    address {ip}/{mask}
                """)
                # with open(f'{mountpoint}/etc/network/interfaces',
                #           'a') as config:
                #     config.write(interfaces_conf)
                sudo_writefile(f'{mountpoint}/etc/network/interfaces',
                               interfaces_conf, append=True)

            # Configure static wifi IP
            elif iface == "wlan0":
                dnss = \
                    self.system("cat /etc/resolv.conf | grep nameserver").split()[
                        1]  # index 0 is "nameserver" so ignore
                routerss = self.system(
                    "ip route | grep default | awk '{print $3}'")  # omit the \n at the end
                dhcp_conf = textwrap.dedent(f"""
                        interface wlan0
                        static ip_address={ip}
                        static routers={routerss}
                        static domain_name_servers={dnss}
                        """)
                # with open(f'{mountpoint}/etc/dhcpcd.conf', 'a') as config:
                #     config.write(dhcp_conf)
                sudo_writefile(f'{mountpoint}/etc/dhcpcd.conf', dhcp_conf,
                               append=True)
        else:
            print('interface eth0\n')
            print(f'static ip_address={ip}/{mask}')

    def set_key(self, name, mountpoint):
        """
        Copies the public key into the .ssh/authorized_keys file on the sd card

        :param name: name of public key, e.g. 'id_rsa' for ~/.ssh/id_rsa.pub
        :type name: str
        :param mountpoint: the mountpunt of the device on which the key
                           is found
        :type mountpoint: str
        """
        # copy file on burner computer ~/.ssh/id_rsa.pub into
        #   mountpoint/home/pi/.ssh/authorized_keys
        self.system(f'mkdir -p {mountpoint}/home/pi/.ssh/')
        self.system(
            f'cp {name} {mountpoint}/home/pi/.ssh/authorized_keys')

    def mount(self, device, mountpoint="/mount/pi"):
        """
        Mounts the current SD card

        :param device: device to mount, e.g. /dev/sda
        :type device: str
        :param mountpoint: the mountpunt of the device on which the pi user
                           is found
        :type mountpoint: str
        """
        if os_is_linux():
            card = SDCard(os="raspberry", host="ubuntu")
            dmesg = USB.get_from_dmesg()

            for usbcard in dmesg:

                dev = usbcard['dev']
                sd1 = f"{dev}1"
                sd2 = f"{dev}2"
                try:
                    if os.path.exists(sd1):
                        Console.ok(f"mounting {sd1} {card.boot_volume}")
                        self.system(f"sudo mkdir -p {card.boot_volume}")
                        self.system(f"sudo mount -t vfat {sd1} {card.boot_volume}")
                except Exception as e:
                    print(e)
                try:
                    if os.path.exists(sd2):
                        Console.ok(f"mounting {sd2} {card.root_volume}")
                        self.system(f"sudo mkdir -p {card.root_volume}")
                        self.system(f"sudo mount -t ext4 {sd2} {card.root_volume}")
                except Exception as e:
                    print(e)

        if os_is_pi():

            # mount p2 (/) and then p1 (/boot)

            if not self.dryrun:
                # wait for the OS to detect the filesystems
                # in burner.info(), formatted will be true if the card has FAT32
                #   filesystems on it
                counter = 0
                max_tries = 5
                b = Burner()
                while counter < max_tries:
                    time.sleep(1)
                    formatted = b.info(print_stdout=False)[device]['formatted']
                    if formatted:
                        break
                    counter += 1
                    if counter == max_tries:
                        print("Timed out waiting for OS to detect filesystem"
                              " on the burned card")
                        sys.exit(1)

            self.system(f'sudo mkdir -p {mountpoint}')
            self.system(f'sudo mount {device}2 {mountpoint}')
            self.system(f'sudo mount {device}1 {mountpoint}/boot')

    def unmount(self, device=None):
        """
        Unmounts the current SD card

        :param device: device to unmount, e.g. /dev/sda
        :type device: str
        """
        if not self.dryrun:
            self.system('sudo sync')  # flush any pending/in-process writes

        if device is None:

            if os_is_linux():
                user = os.environ["USER"]
                os.system(f"sudo umount /media/{user}/boot")
                os.system(f"sudo rmdir /media/{user}/boot")

                os.system(f"sudo umount /media/{user}/rootfs")
                os.system(f"sudo rmdir /media/{user}/rootfs")

            else:
                Console.error("Please specify the mount path")
        else:

            # unmount p1 (/boot) and then p2 (/)
            self.system(f'sudo umount {device}1')
            # noinspection PyBroadException
            # try:
            #     print(f"trying to unmount {device}1")
            #     self.system(f'sudo umount {device}1')
            # except:
            #     pass

            # Occasionally there are issues with unmounting. Pause for good effect.
            self.system('sleep 1')
            self.system(f'sudo umount {device}2')

    def enable_ssh(self, mountpoint):
        """
        Enables ssh on next boot of sd card

        :param mountpoint: mount point of the /boot file system wher the
                           ssh is enabled. by adding a file ssh
        :type mountpoint: str
        """
        if os_is_pi():
            # touch mountpoint/boot/ssh
            command = f'sudo touch {mountpoint}/boot/ssh'
            self.system(command)
        elif os_is_linux():
            card = SDCard(os="raspberry", host="ubuntu")

            print("OOOO")
            command = f"sudo touch {card.boot_volume}/ssh"
            self.system(command)

        else:
            raise NotImplementedError

    # IMPROVE

    # TODO: docstring
    def disable_password_ssh(self, mountpoint):
        # sshd_config = self.filename("/etc/ssh/sshd_config")
        sshd_config = f'{mountpoint}/etc/ssh/sshd_config'
        new_sshd_config = ""
        updated_params = False

        def sets_param(param, line):
            """See if a config line sets this parameter to something."""
            # front is only whitespace maybe a comment
            front = r'^\s*#?\s*'
            # only whitespace between param and value
            middle = r'\s+'
            # end can include a comment
            end = r'\s*(?:#.*)?$'
            re_sets_param = front + param + middle + r'.*' + end
            return re.search(re_sets_param, line) is not None

        force_params = [
            ("ChallengeResponseAuthentication", "no"),
            ("PasswordAuthentication", "no"),
            ("UsePAM", "no"),
            ("PermitRootLogin", "no"),
        ]

        found_params = set()
        # with open(sshd_config, 'r') as f:
        f = sudo_readfile(sshd_config)

        for line in f:
            found_a_param = False
            for param, value in force_params:
                if sets_param(param, line):
                    # Only set the parameter once
                    if param not in found_params:
                        new_sshd_config += param + " " + value + "\n"
                        updated_params = True
                    found_a_param = True
                    found_params.add(param)
            if not found_a_param:
                new_sshd_config += line
        # Check if any params not found
        for param, value in force_params:
            if param not in found_params:
                new_sshd_config += param + " " + value + "\n"
                updated_params = True
        if updated_params:
            # NOTE: This is actually necessary, see comment in method
            #
            # as we no longer do it on osx, we need to identify if this is still needed
            #
            # self.truncate_file(sshd_config)
            # with open(sshd_config, "w") as f:
            #     f.write(new_sshd_config)
            sudo_writefile(sshd_config, new_sshd_config)

    # IMPROVE
    # ok osx
    def activate_ssh(self, public_key, debug=False, interactive=False):
        """
        Sets the public key path and copies it to the SD card

        TODO: this has bugs as we have not yet thought about debug,
              interactive, yesno yesno we can take form cloudmesh.common

        BUG: this just raise a non implementation error

        :param public_key: the public key location
        :type public_key: str
        :param debug: if set to tru debug messages will be printed
        :type debug: bool
        :param interactive: set to tru if you like interactive mode
        :type interactive: bool
        :return: True if successful
        :rtype: bool
        """

        raise NotImplementedError

        # set the keypath
        self.keypath = public_key
        if debug:
            print(self.keypath)
        if not os.path.isfile(self.keypath):
            Console.error("key does not exist", self.keypath)
            sys.exit()

        if self.dryrun:
            print("DRY RUN - skipping:")
            print("Activate ssh authorized_keys pkey:{}".format(public_key))
            return
        elif interactive:
            if not yn_choice("About to write ssh config. Please confirm:"):
                return

        # activate ssh by creating an empty ssh file in the boot drive
        pathlib.Path(self.filename("/ssh")).touch()
        # Write the content of the ssh rsa to the authorized_keys file
        key = pathlib.Path(public_key).read_text()
        ssh_dir = self.filename("/home/pi/.ssh")
        print(ssh_dir)
        if not os.path.isdir(ssh_dir):
            os.makedirs(ssh_dir)
        auth_keys = ssh_dir / "authorized_keys"
        auth_keys.write_text(key)

        # We need to fix the permissions on the .ssh folder but it is hard to
        # get this working from a host OS because the host OS must have a user
        # and group with the same pid and gid as the raspberry pi OS. On the PI
        # the pi uid and gid are both 1000.

        # All of the following do not work on OS X:
        # execute("chown 1000:1000 {ssh_dir}".format(ssh_dir=ssh_dir))
        # shutil.chown(ssh_dir, user=1000, group=1000)
        # shutil.chown(ssh_dir, user=1000, group=1000)
        # execute("sudo chown 1000:1000 {ssh_dir}".format(ssh_dir=ssh_dir))

        # Changing the modification attributes does work, but we can just handle
        # this the same way as the previous chown issue for consistency.
        # os.chmod(ssh_dir, 0o700)
        # os.chmod(auth_keys, 0o600)

        # /etc/rc.local runs at boot with root permissions - since the file
        # already exists modifying it shouldn't change ownership or permissions
        # so it should run correctly. One lingering question is: should we clean
        # this up later?

        new_lines = textwrap.dedent('''
                    # FIX298-START: Fix permissions for .ssh directory 
                    if [ -d "/home/pi/.ssh" ]; then
                        chown pi:pi /home/pi/.ssh
                        chmod 700 /home/pi/.ssh
                        if [ -f "/home/pi/.ssh/authorized_keys" ]; then
                            chown pi:pi /home/pi/.ssh/authorized_keys
                            chmod 600 /home/pi/.ssh/authorized_keys
                        fi
                    fi
                    # FIX298-END
                    ''')
        rc_local = self.filename("/etc/rc.local")
        new_rc_local = ""
        already_updated = False
        with rc_local.open() as f:
            for line in f:
                if "FIX298" in line:
                    already_updated = True
                    break
                if line == "exit 0\n":
                    new_rc_local += new_lines
                    new_rc_local += line
                else:
                    new_rc_local += line
        if not already_updated:
            with rc_local.open("w") as f:
                f.write(new_rc_local)
        self.disable_password_ssh()

    def configure_wifi(self,
                       ssid,
                       psk=None,
                       mountpoint='/mount/pi',
                       interactive=False):
        """
        Sets the wifi. Only works for psk based wifi

        :param ssid: the ssid
        :type ssid: str
        :param psk: the psk
        :type psk: str
        :param mountpoint: the mont pount
        :type mountpoint: str
        :param interactive: true if you like to run it interactively
        :type interactive: bool
        """
        if psk is not None:
            wifi = textwrap.dedent("""\
                    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
                    update_config=1 
                    country=US

                    network={{
                            ssid=\"{network}\"
                            psk=\"{pwd}\"
                            key_mgmt=WPA-PSK
                    }}""".format(network=ssid, pwd=psk))
        else:
            wifi = textwrap.dedent("""\
                    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
                    update_config=1 
                    country=US

                    network={{
                            ssid=\"{network}\"
                            key_mgmt=NONE
                    }}""".format(network=ssid))

        # Per fix provided by Gregor, we use this path to get around rfkill block on boot
        path = f"{mountpoint}/boot/wpa_supplicant.conf"
        # path = f"{mp}/etc/wpa_supplicant/wpa_supplicant.conf"
        if self.dryrun:
            print("DRY RUN - skipping:")
            print("Writing wifi ssid:{} psk:{} to {}".format(ssid,
                                                             psk, path))
            return

        # with open(path, 'w') as f:
        #     f.write(wifi)
        sudo_writefile(path, wifi)

    # TODO
    def format_device(self, device='dev/sda', hostname=None):
        """
        Formats device with one FAT32 partition

        WARNING: This is a potential risky way of automating
                 the process using fdisk. ONly use on SDCards that you can lose.

        WARNING: make sure you have the right device, this comamnd could
                 potentially erase your OS

        :param device: The defice on which we format
        :type device: str
        :param hostname: the hostname
        :type hostname: str
        """
        if not os_is_pi():
            raise NotImplementedError("Only implemented to be run on a PI")

        Console.info("Formatting device...")
        self.unmount(device)
        StopWatch.start(f"format {device} {hostname}")

        pipeline = textwrap.dedent("""d

                                    d
                                    
                                    d

                                    d

                                    n
                                    p
                                    1


                                    t
                                    b""")

        command = f'(echo "{pipeline}"; sleep 1; echo "w") | sudo fdisk {device}'
        result = subprocess.getoutput(command)

        StopWatch.stop(f"format {device} {hostname}")
        StopWatch.status(f"format {device} {hostname}", True)

        #
        # TODO: we should have a test here
        #
        StopWatch.benchmark(sysinfo=True, csv=False)

        Console.ok("Formating completed ...")

        Console.info("Wait while the card is written ...")

    # This is to prevent desktop access of th pie (directly plugging monitor, keyboard, mouse into pi, etc.)
    #
    # Currently, ssh login is only possible with an authorized key. (No passwords)
    # Plugging pi directly into desktop, however, will still prompt for a user and password.
    # I can't figure out how to disable it

    def disable_terminal_login(self, mountpoint, password):
        """
        disables and replaces the password with a random string so that by
        accident the pi can not be logged into. The only way to login is via the
        ssh key

        :param mountpoint: the mountpount for the system
        :type mountpoint: str
        :param password: the password for login
        :type password: str
        :return: file in /etc/shadow
        :rtype: a written file
        """

        # Generates random salt for password generation
        def random_salt(length=10):
            letters_and_digits = string.ascii_letters + string.digits
            return ''.join(
                random.choice(letters_and_digits) for i in range(length))

        salt = random_salt()
        if password is not None:
            pswd = crypt.crypt(password, f'$6${salt}')
        else:
            raise NotImplementedError()

        # Make sure there's an 'x' in /etc/passwd
        #        with open(f'{mountpoint}/etc/passwd', 'r') as f:
        #            info = [l for l in f.readlines()]

        info = sudo_readfile(f'{mountpoint}/etc/passwd')

        for i in range(len(info)):
            inf = info[i].split(":")
            if inf[0] == 'pi':
                inf[1] = 'x'
                info[i] = ':'.join(inf)

        content = '\n'.join(info)

        # with open(f'{mountpoint}/etc/passwd', 'w') as f:
        #     f.writelines(info)

        sudo_writefile(f'{mountpoint}/etc/passwd', content)

        # Add it to shadow file
        # with open(f'{mountpoint}/etc/shadow', 'r') as f:
        #     data = [l for l in f.readlines()]

        data = sudo_readfile(f'{mountpoint}/etc/shadow')

        content = ""
        for i in range(len(data)):
            dat = data[i].split(":")
            if dat[0] == 'pi':
                dat[1] = pswd
                data[i] = ':'.join(dat)

        content = '\n'.join(data)

        # with open(f'{mountpoint}/etc/shadow', 'w') as f:
        #     f.writelines(data)
        sudo_writefile(f'{mountpoint}/etc/shadow', content)


class MultiBurner(object):
    """
    This class uses a single or multicard burner to burn SD Cards. It detects
    how many SD Cards are there and uses them. We assume no other USB devices
    are plugged in other than a keyboard or a mouse.

    """

    # System command that uses subprocess to execute terminal commands
    # Returns the stdout of the command
    def system(self, command):
        """

        :param command:
        :return:
        """
        res = subprocess.getstatusoutput(command)
        # If exit code is not 0, warn user
        if res[0] != 0:
            Console.warning(
                f'Warning: "{command}" did not execute properly -> {res[1]} :: exit code {res[0]}')

        return res[1]

    # noinspection PyUnboundLocalVariable
    def burn_all(self,
                 image="latest",
                 device=None,
                 blocksize="4M",
                 progress=True,
                 hostnames=None,
                 ips=None,
                 key=None,
                 password=None,
                 ssid=None,
                 psk=None,
                 fromatting=True):
        """
        TODO: provide documentation

        :param image:
        :type image:
        :param device:
        :type device:
        :param blocksize:
        :type blocksize:
        :param progress:
        :type progress:
        :param hostnames:
        :type hostnames:
        :param ips:
        :type ips:
        :param key:
        :type key:
        :param password:
        :type password:
        :param ssid:
        :type ssid:
        :param psk:
        :type psk:
        :param fromatting:
        :type fromatting:
        :return:
        :rtype:
        """

        # :param devices: string with device letters

        # print (device)

        #
        # define the dev
        #
        devices = {}  # dict of {device_name: empty_status}
        #
        # probe the dev
        #
        # pprint(Burner().info())
        info_statuses = Burner().info()

        # If the user specifies a particular device, we only care about that
        # device

        if device is not None:
            for dev in device:
                devices[dev] = info_statuses[dev]['empty']
            # Change to empty to skip next loop
            info_statuses = {}

        for device in info_statuses.keys():
            # print("call the info command on the device and "
            #      "figure out if an empty card is in it")
            # change the status based on what you found
            devices[device] = info_statuses[device]['empty']

        # if we detect a non empty card we interrupt and tell
        # which is not empty.
        # (print out status of the devices in a table)
        device_statuses = devices.values()
        if False in device_statuses:
            print("\nEmpty status of devices:")
            for dev, empty_status in devices.items():
                x = "" if empty_status else "not "
                Console.info(f"Device {dev} is {x}empty")
        print()

        # detect if there is an issue with the cards, readers
        # TODO what exactly should be done here?

        # ask if this is ok to burn otherwise
        burn_all = yn_choice("Burn non-empty devices too?")

        # if no burn all of them for which we have status "empty card"
        if not burn_all:
            # delete from devices dict any non-empty devices
            devices_to_delete = []
            for device in devices.keys():
                if devices[device]:
                    # can't delete while iterating
                    devices_to_delete.append(device)
            for device in devices_to_delete:
                del devices[device]

        print("Burning these devices:")
        print(' '.join(devices.keys()))

        keys = list(devices.keys())
        count = 0
        for i in range(len(hostnames)):
            # for device, status in devices.items():
            # We might be using one device slot to burn multiple cards
            device = keys[i % len(keys)]
            # status = devices[device]
            hostname = hostnames[i]
            ip = None if not ips else ips[i]

            self.burn(image, device, blocksize, progress, hostname,
                      ip, key, password, ssid, psk, fromatting)

            count += 1
            Console.info(f'Burned card {count}')
            self.system('tput bel')  # ring the terminal bell to notify user
            if i < len(hostnames) - 1:
                if (i + 1) != ((i + 1) % len(keys)):
                    choice = input(
                        f"Slot {keys[(i + 1) % len(keys)]} "
                        "needs to be reused. Do you wish to continue? [y/n] ")
                    while (choice != 'y') and (choice != 'n'):
                        choice = input("Please use [y/n] ")
                    if choice == 'n':
                        break
                input('Insert next card and press enter...')
                print('Burning next card...')
                print()

        Console.info(f"You burned {count} SD Cards")
        Console.ok("Done :)")

    def burn(self,
             image="latest",
             device=None,
             blocksize="4M",
             progress=True,
             hostname=None,
             ip=None,
             key=None,
             password=None,
             ssid=None,
             psk=None,
             fromatting=True):
        """
        Burns the image on the specific device

        TODO: provide documentation

        :param image:
        :type image:
        :param device:
        :type device:
        :param blocksize:
        :type blocksize:
        :param progress:
        :type progress:
        :param hostname:
        :type hostname:
        :param ip:
        :type ip:
        :param key:
        :type key:
        :param password:
        :type password:
        :param ssid:
        :type ssid:
        :param psk:
        :type psk:
        :param fromatting:
        :type fromatting:
        :return:
        :rtype:
        """

        mp = '/mount/pi'
        if key is None:
            key = '~/.ssh/id_rsa.pub'

        elif key == 'root':
            key = f'/{key}/.ssh/id_rsa.pub'

        else:
            key = f'/home/{key}/.ssh/id_rsa.pub'

        # don't do the input() after burning the last card
        # use a counter to check this

        counter = 0
        burner = Burner()

        print("counter", counter)
        StopWatch.start(f"create {device} {hostname}")

        if fromatting:
            burner.format_device(device=device, hostname=hostname)

        burner.burn(image, device, blocksize=blocksize)
        burner.mount(device, mp)
        burner.set_hostname(hostname, mp)
        burner.disable_terminal_login(mp, password)
        if ssid:
            Console.warning(
                "Warning: In the future, try to interface with the workers via ethernet/switch rather than WiFi")
            burner.configure_wifi(ssid, psk, mp)
        burner.enable_ssh(mp)
        burner.disable_password_ssh(mp)
        burner.set_key(key, mp)
        if ip:
            interface = "wlan0" if ssid is not None else "eth0"
            burner.set_static_ip(ip, mp, iface=interface)

        burner.unmount(device)
        # for some reason, need to do unmount twice for it to work properly
        burner.unmount(device)
        time.sleep(2)
        StopWatch.stop(f"create {device} {hostname}")
        StopWatch.status(f"create {device} {hostname}", True)
