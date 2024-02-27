#!/bin/bash

systemctl stop meshnet.service
systemctl disable meshnet.service

dpkg -P meshnet

rm /etc/systemd/system/meshnet.service
systemctl reset-failed
systemctl daemon-reload

rm -r /opt/meshnet
rm -r /etc/meshnet
rm -r /var/log/meshnet.log

