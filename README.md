# XBeeNet

## INSTALL
1. Preinstalls: make sure the following is installed/up to date on any nodes using this:
```
sudo apt update
sudo apt upgrade
sudp apt install openssh-client openssh-server
```

2.
```
sudo dpkg -i meshnet_*_all.deb
```

## OPERATION
VERY IMPORTANT: The XBee module must be plugged into a USB port and the proper configuration set for the program to run successfully. If it doesnt work, try plugging in the XBee, checking the configs, and rebooting/restarting the service
1. Plug in the XBee to a USB port
2. Check the port in use, examples:
```
ls /dev | grep USB
#or 
sudo dmesg # check the last handful of lines after plugging in XBee for what port was brought up
```
3. Modify the configs
```
sudo nano /etc/meshnet/config.toml
# make sure to set a unique IP, such as 10.0.0.2
# make the sure the port is correct
# change the net ID as desired
```
4. Start the service
```
sudo systemctl start meshnet.service
#or
sudo reboot now
```
5. Monitor running status
```
tail -n 50 -f /var/log/meshnet.log
```
6. Connect with ssh to other nodes:
```
ssh <user>@10.0.0.2
```
CAUTION: if you have previously connected via SSH to a different node with the same IP, you may need to reset some ssh settings:
```
ssh-keygen -f "/home/<user>/.ssh/known_hosts" -R "10.0.0.2"
```

## UNINSTALL
See the included uninstall script
```
sudo dpkg -P meshnet
sudo ./uninstall.sh
```



