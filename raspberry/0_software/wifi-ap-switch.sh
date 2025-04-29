#!/bin/bash
# Script inspiré des solutions GitHub [1][2] et StackExchange [3]

# Configuration
SSID="Jukebox"
PASSWORD="12345678"
INTERFACE="wlan0"
SUBNET="192.168.50.1/24"

AP_MODE() {
    # Arrêt des services réseau
    systemctl stop dhcpcd
    systemctl disable dhcpcd

    ifconfig $INTERFACE down

    # Configuration IP statique
    ip addr add $SUBNET dev $INTERFACE
    ifconfig $INTERFACE up

    systemctl enable hostapd
    systemctl enable dnsmasq

    # Démarrer hostapd et dnsmasq
    systemctl start hostapd
    systemctl start dnsmasq
}

CLIENT_MODE() {
    # Arrêt des services AP
    systemctl stop hostapd
    systemctl stop dnsmasq

    systemctl disable hostapd
    systemctl disable dnsmasq

    # Réinitialisation interface
    ip addr flush dev $INTERFACE
    ifconfig $INTERFACE down

    systemctl enable dhcpcd

    systemctl restart dhcpcd
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
