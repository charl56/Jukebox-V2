# Connexion à la Raspberry Pi et lancement de l'appli

## Première connexion

1. Brancher la carte SD à l'ordinateur.
2. Modifier le fichier `root/cmdline.txt`.
3. Ajouter à la fin du fichier : `ip=169.254.25.25`


## Connexion SSH

1. Brancher la Raspberry Pi au PC via un câble Ethernet.
2. Exécuter la commande SSH suivante :
```bash
ssh -L 5025:127.0.0.1:5025 charl@169.254.25.25
```
3. Mot de passe : `network!`


## Création d'un tunnel avec MobaXterm

1. Ouvrir MobaXterm.
2. Accéder au menu : `Tunneling`.
3. Configurer les options suivantes :

   - **Forwarded port** : `5025`

   * SSH Server :
     - **Adresse** : `169.254.25.25`
     - **User** : `charl`
     - **Port** : `22`

   * Remote Server :
     - **Adresse** : `127.0.0.1`
     - **Port** : `5025`

---
Avec ce setup, vous recevrez le port 5025 de la Raspberry Pi sur votre PC.
