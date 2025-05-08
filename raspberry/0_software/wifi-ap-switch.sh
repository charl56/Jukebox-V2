#!/bin/bash
# Script inspiré des solutions GitHub [1][2] et StackExchange [3]

# Configuration
SSID="Jukebox"
PASSWORD="12345678"
INTERFACE="wlan0"
SUBNET="192.168.50.1/24"

AP_MODE() {
    # Arrêt des services réseau
    systemctl stop dhcpcd wpa_supplicant

    ifconfig $INTERFACE down

    # Configuration IP statique
    ip addr add $SUBNET dev $INTERFACE
    ifconfig $INTERFACE up

    # Démarrer hostapd et dnsmasq
    systemctl start hostapd dnsmasq

    echo "Mode AP activé"
}

CLIENT_MODE() {
    # Arrêt des services AP
    systemctl stop hostapd dnsmasq

    ip addr flush dev $INTERFACE

    ifconfig $INTERFACE down
    ifconfig $INTERFACE up
    systemctl restart wpa_supplicant dhcpcd

    wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -B

    echo "Mode client activé"
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
