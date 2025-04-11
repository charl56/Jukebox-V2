# docker build -t jukebox-app .
# docker run -p 5025:5025 -d jukebox-app


# Utiliser une image Python officielle
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY requirements.txt .
COPY app.py .
COPY routes ./routes
COPY templates ./templates
COPY static ./static
COPY utils.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir la variable d'environnement pour Docker
ENV IS_ON_SERVER=True
ENV IS_ON_RASPBERRY=False

# Exposer le port 5025
EXPOSE 5025

# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]



