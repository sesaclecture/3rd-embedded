#!/bin/bash

# nmcli connection show

HOTSPOT="RPi-Hotspot"

sudo rfkill unblock wifi

sudo raspi-config nonint do_wifi_country KR

sudo nmcli connection modify "$HOTSPOT" \
  connection.autoconnect yes \
  connection.autoconnect-priority 100 \
  802-11-wireless.mode ap \
  802-11-wireless.band bg \
  802-11-wireless.channel 6 \
  802-11-wireless.powersave 2 \
  ipv4.method shared \
  ipv6.method ignore

sudo iw dev wlan0 set power_save off

sudo tee /etc/NetworkManager/conf.d/wifi-powersave-off.conf > /dev/null <<EOF
[connection]
wifi.powersave = 2
EOF

sudo systemctl restart NetworkManager

echo "DONE"
echo "If hotspot is not visible, reboot Raspberry Pi."
