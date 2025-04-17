### ✅ Étapes pour installer Docker sur Raspberry Pi (3B) :

1. **Assure-toi que ton système est à jour :**

```bash
sudo apt update && sudo apt upgrade -y
```

2. **Installe les dépendances :**

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

3. **Ajoute la clé GPG officielle de Docker :**

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. **Ajoute le dépôt Docker compatible ARM :**

```bash
echo \
  "deb [arch=armhf signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. **Met à jour les paquets avec le nouveau dépôt :**

```bash
sudo apt update
```

6. **Installe Docker Engine :**

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

7. **Teste Docker :**

```bash
sudo docker run hello-world
```

Tu devrais voir un message indiquant que Docker fonctionne bien 🎉

---

### 🔧 (Optionnel) Utiliser Docker sans `sudo` :

Ajoute ton utilisateur au groupe `docker` :

```bash
sudo usermod -aG docker $USER
```

Puis **redémarre ta session ou redémarre la Pi** :

```bash
sudo reboot
```

Après ça, tu pourras faire :

```bash
docker ps
```

sans avoir besoin de `sudo`.

---

Tu veux aussi Docker Compose (en ligne de commande) ou tu comptes utiliser `docker compose` directement ?