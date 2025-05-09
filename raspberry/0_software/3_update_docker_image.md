Démarrage de base : en mode AP, et donc on peut utiliser directement la version de la jukebox, installé sur la raspberry
Donc etape 4




Pour mettre à jour l'app ; 

edit file : /etc/wpa_supplicant/wpa_supplicant.conf, for ssid & psk

Mode client, pour pull la dernière image
sudo ./wifi-ap-switch.sh client
Patienter le temps que la carte se connect
Verif : ping google.com
./pull-jukebox.sh
Si bug pendant, refaire la commande

reboot



Infos : 
Le script permet de passer en mode ap : sudo ./wifi-ap-switch.sh ap
Mais parfois cela bug, il faut mieux redémarer la carte, avec : reboot
Elle sera en mode AP au démarrage