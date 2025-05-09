#!/bin/bash
set -e

# Créer un répertoire de sauvegarde pour les fichiers statiques originaux
if [ ! -d "/app/static_original" ]; then
    # Si le dossier static existe encore (avant le montage du volume)
    if [ -d "/app/static" ]; then
        echo "Sauvegarde des fichiers statiques originaux..."
        mkdir -p /app/static_original
        cp -r /app/static/* /app/static_original/
    fi
fi

# Vérifier si le volume monté est vide
if [ -z "$(ls -A /app/static 2>/dev/null)" ]; then
    echo "Le volume monté est vide. Initialisation avec les fichiers originaux..."
    # Copier les fichiers de référence vers le volume monté
    cp -r /app/static_original/* /app/static/
    echo "Initialisation terminée."
else
    echo "Le volume contient déjà des données. Aucune initialisation nécessaire."
fi

# Exécuter la commande originale
exec "$@"