# Jukebox

This project combines **hardware** and **software** to create a connected jukebox.
It runs on a **Raspberry Pi 3B**, which hosts a web server you can access to control music playback.
The hardware part manages various components directly connected to the Pi for full jukebox functionality.

---

## Web technologies Used

* **Python**: 3.11.1
* **Node.js**: 16.17.0

---

## Run Locally

### 1. Frontend Setup

1. Navigate to the `frontend` folder:

   ```bash
   cd frontend
   ```
2. Install dependencies (only needed the first time or after adding new ones):

   ```bash
   npm install
   ```
3. Start the development server:

   ```bash
   npm run dev
   ```

---

### 2. Backend Setup

1. Navigate to the `backend` folder:

   ```bash
   cd backend
   ```
2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   python app.py
   ```

* **Access the app at**: [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## Raspberry Pi Setup

Full instructions are available here:
📄 [Step-by-step guide](./raspberry/README.MD)

