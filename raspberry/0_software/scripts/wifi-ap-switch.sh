#!/bin/bash

# Config
SSID="Jukebox"
PASSWORD="12345678"
INTERFACE="wlan0"
SUBNET="192.168.50.1/24"

AP_MODE() {
    # Stop services for Client mode
    systemctl stop wpa_supplicant dhcpcd

    # Config to be AP mode
    ip addr flush dev $INTERFACE
    ip addr add $SUBNET dev $INTERFACE

    # Restart interface
    ifconfig $INTERFACE down
    ifconfig $INTERFACE up

    # Start services for AP mode
    systemctl start hostapd dnsmasq

    echo "AP Mode enable"
}

CLIENT_MODE() {
    
    # Stop services for AP mode
    systemctl stop hostapd dnsmasq

    # Config for Client mode
    ip addr flush dev $INTERFACE

    # Restart interface
    ifconfig $INTERFACE down
    ifconfig $INTERFACE up

    # Restart services for Client mode
    systemctl restart wpa_supplicant dhcpcd

    # To be sure config of wpa will be good and enable
    wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -B

    echo "Client Mode enable"
}

case "$1" in
    ap)
        AP_MODE
        ;;
    client)
        CLIENT_MODE
        ;;
    *)
        echo "Usage: $0 {ap|client}"
        exit 1
        ;;
esac
