# How to Update the Application

1. **Edit Wi-Fi Settings**
   Open the file `/etc/wpa_supplicant/wpa_supplicant.conf` and update the `ssid` and `psk` with your Wi-Fi credentials.

2. **Switch to Client Mode**
   Run the following command to switch to Wi-Fi client mode:

   ```bash
   sudo ./wifi-ap-switch.sh client
   ```

   Wait a few moments for the Raspberry Pi to connect to the network.

3. **Check Connection**
   Verify the connection with:

   ```bash
   ping google.com
   ```

4. **Pull the Latest Jukebox Version**
   Run the update script:

   ```bash
   ./pull-jukebox.sh
   ```

   > If an error occurs, simply run the command again.

5. **Reboot the Raspberry Pi**

   ```bash
   sudo reboot
   ```

---

## Additional Info

* ⚠️ Sometimes this command may not work properly. In that case, it's better to reboot:

  ```bash
  sudo reboot
  ```

  > The Raspberry Pi will start in AP mode by default.
