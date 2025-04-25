## Steps to install Docker on Raspberry Pi (3B):

1. **Make sure your system is up to date:**

```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install required dependencies:**

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

3. **Add Docker’s official GPG key:**

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. **Add the Docker repository for ARM:**

```bash
echo \
  "deb [arch=armhf signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. **Update packages with the new repository:**

```bash
sudo apt update
```

6. **Install Docker Engine:**

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

7. **Test Docker:**

```bash
sudo docker run hello-world
```

You should see a message confirming that Docker is working properly 🎉

---

### 🔧 (Optional) Use Docker without `sudo`:

Add your user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

Then **restart your session or reboot the Pi**:

```bash
sudo reboot
```

After that, you can run:

```bash
docker ps
```

without needing `sudo`.
