edit file : /etc/wpa_supplicant/wpa_supplicant.conf, for ssid & psk





Scénario de lancement a ce moment : 

conenction
sudo ./wifi-ap-switch.sh client
./pull-jukebox.sh

sudo ./wifi-ap-switch.sh ap
./start-jukebox.sh





Infos : 

Le scipt fonctionne, mais parfois le mode client ne s'active pas. Alords redemarrer la carte, et init le mode client 
En vrai vait mieux redemarrer avant de changer de mode

Parfoids si le mode client est activé trop longtemps, il faut redemarrer
    J'ai eu 1 fois le cas, donc dans le doute
Mode client pour mettre à jour l'image docker, ou la raspberry elle meme. Sinon mode AP pour utilisation




On se connecte au reseau de la raspb erry : 

ssid : Jukebox
psk : 12345678






Se connecter au wifi avec son tel par exemple
    Aller sur l'addresse http://localhost:5025

Si possible, ajouter un DNS sur la raspberry, pour avoir une meilleur addresse