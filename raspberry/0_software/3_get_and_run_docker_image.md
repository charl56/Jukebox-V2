Démarrage de base : en mode AP, et donc on peut utiliser directement la version de la jukebox, installé sur la raspberry
Donc etape 4




Pour mettre à jour l'app ; 

edit file : /etc/wpa_supplicant/wpa_supplicant.conf, for ssid & psk

Mode client, pour pull la dernière image
sudo ./wifi-ap-switch.sh client
./pull-jukebox.sh


Pour repasser en mode AP, et lancer la nouvelle image

sudo ./wifi-ap-switch.sh ap
./start-jukebox.sh



Infos : 

Le scipt fonctionne, mais parfois le mode client ne s'active pas. Alords redemarrer la carte, et init le mode client 
En vrai vait mieux redemarrer avant de changer de mode

Parfoids si le mode client est activé trop longtemps, il faut redemarrer
    J'ai eu 1 fois le cas, donc dans le doute
Mode client pour mettre à jour l'image docker, ou la raspberry elle meme. Sinon mode AP pour utilisation


