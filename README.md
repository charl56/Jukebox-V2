# Projet Jukebox



Lancer le projet en local
explication de la pipeline pour déployer
preparer la raspberry
lancer depuis la raspberry















## Technologies

- **Python**: 3.11.1
- **Node.js**: 16.17.0

## Démarrage en local

### 1. Configuration du Frontend

1. Accédez au dossier `frontend` :
   ```bash
   cd frontend
   ```
2. Installez les dépendances (nécessaire uniquement la première fois ou si des bibliothèques ont été ajoutées) :
   ```bash
   npm install
   ```
3. Lancez le serveur de développement :
   ```bash
   npm run dev
   ```

### 2. Configuration du Backend

1. Accédez au dossier `backend` :
   ```bash
   cd backend
   ```
2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez l'application :
   ```bash
   python app.py
   ```

- **Accès à l’application** : [http://127.0.0.1:8080](http://127.0.0.1:8080)

---





## Démarrage manuel sur la Raspberry Pi

Pour la préparation de la raspberry, référez-vous au fichier **Jukebox.xlsx**, onglet "Setup Raspberry".

### Étapes de déploiement

1. **Connexion à la Raspberry Pi en SSH**  
   Suivez les instructions dans le fichier `ssh_raspberry.md` pour établir la connexion SSH.


Créer un dossier srv/jukebox/static, puis lancer le docker compose 

-- 
2. **Déploiement du Frontend**
   - En local, exécutez :
     ```bash
     npm run build:raspberry
     ```
   - **Copie initiale** : copiez le dossier `backend` en entier sur la Raspberry Pi.
   - **Mises à jour** : après chaque mise à jour, seul le dossier `templates` (situé dans `backend/templates`) doit être transféré.

3. **Déploiement du Backend sur la Raspberry Pi**
   - Accédez au dossier `backend` :
     ```bash
     cd backend
     ```
   - Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```
   - Lancez l'application :
     ```bash
     python ./app.py
     ```

- **Accès à l’application sur Raspberry Pi** : [http://127.0.0.1:5025](http://127.0.0.1:5025)