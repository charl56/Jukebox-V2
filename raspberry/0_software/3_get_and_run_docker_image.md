## Pull and Run the Docker Image

Download the latest public Jukebox image:

```bash
docker pull ghcr.io/charl56/jukebox-public:latest
```






Dans l'exemple j'ai le dossier /home/user/jukebox/data, sur ma Raspberry


Run the container in detached mode with port forwarding:

```bash
docker run -p 5025:5025 -v /home/user/jukebox/data:/app/static -d ghcr.io/charl56/jukebox-public:latest
```

The Jukebox service will now be accessible on port **5025** 🎶