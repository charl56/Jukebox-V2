# Utiliser une image Python officielle
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY backend/requirements.txt .
COPY backend/app.py .
COPY backend/routes ./routes
COPY backend/templates ./templates
COPY backend/static ./static
COPY backend/utils.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir la variable d'environnement pour Docker
ENV IS_DOCKER=True

# Exposer le port 5025
EXPOSE 5025

# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]


# docker build -t jukebox-app .
# docker run -p 5025:5025 -d jukebox-app
