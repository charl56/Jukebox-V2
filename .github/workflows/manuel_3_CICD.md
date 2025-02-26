### Étape 1 : Configurer les variables secretes
Liste des variables à initialiser, dans le dépôt GitHub sous Settings > Secrets and variables > Actions > New repository secret : 
- PAT : Private Access Token, généré sur Github
- SSH_HOST : Adresse IP du serveur
- SSH_PORT : Port utilisé pour se connecter en SSH au serveur
- SSH_PRIVATE_KEY : Clé privé de connection SSH
- SSH_USER : Utilisateur qui se connecte en SSH
- WORK_DIR : Chemion du dossier, où se trouve le docker-compose.yml du projet

#### Sur ton serveur, génère une clé avec un nom définit
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
Ajouter la clé au fichier `/home/{SSH_USER}/.ssh/autorizedkey`, ou un truc comme ça

### Étape 2 : Créer un Workflow GitHub Actions
Crée un fichier .github/workflows/docker-publish.yml dans ton dépôt GitHub.


### Étape 3 : Configurer Docker Compose
Exemple du fichier docker-compose.yml

### Étape 4 : Tester le Workflow
Push le code sur la branche main de ton dépôt GitHub.
GitHub Actions exécutera le workflow de déploiement.
