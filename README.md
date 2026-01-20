````md
# SRM_AUTO_WIFI_AUTHENTICATOR

A Python-based automation script that detects the **SRMIST Wi-Fi network** and automatically authenticates the user on the SRM captive portal using **modern Selenium** (browser drivers are managed automatically).

Designed for seamless, hands-free Wi-Fi authentication on campus — including support for **Windows autorun**.

---

## ✨ Features

- 📡 Detects nearby Wi-Fi networks (Windows)
- 🌐 Checks existing internet connectivity
- 🤖 Automates SRMIST captive portal authentication
- 🔐 Secure credential handling via `.env`
- 🖥 Headless browser execution
- 🔁 Can be configured to **run automatically on Windows startup**

---

## 🧰 Tech Stack

- Python 3.8+
- Selenium (automatic driver management)
- Requests
- python-dotenv
- Windows `netsh` Wi-Fi utilities

---

## 📦 Installation

```bash
pip install selenium requests python-dotenv
````

> Selenium automatically downloads and manages the correct browser driver.

---

## 📁 Project Structure

```
.
├── main.py        # Authentication logic
├── scanner_.py    # Wi-Fi scanning module
├── .env           # Credentials
└── README.md
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
USER_NAME=your_registration_number
PASSWORD=your_wifi_password
```


---

## ⚙️ How It Works

1. **Internet Connectivity Check**

   * Sends a request to Google’s `generate_204` endpoint

2. **Wi-Fi Detection**

   * Scans available networks using `netsh wlan show networks`
   * Looks for the `SRMIST` SSID

3. **Portal Authentication**

   * Opens the SRMIST captive portal
   * Injects credentials from `.env`
   * Submits the login form
   * Confirms successful authentication

---

## ▶️ Usage

```bash
python main.py
```

The script will:

* Exit if internet access already exists
* Exit if SRMIST Wi-Fi is not detected
* Authenticate automatically when required

---

## 🔁 Windows Autorun (Optional)

You can fully automate authentication by running this script at **Windows startup**.

### Method 1: Startup Folder (Simple)

1. Press `Win + R`
2. Enter:

   ```
   shell:startup
   ```
3. Create a shortcut to:

   ```bash
   python path\to\main.py
   ```
4. Ensure Python is added to PATH

---

### Method 2: Task Scheduler (Recommended)

1. Open **Task Scheduler**
2. Create a **Basic Task**
3. Trigger: **At log on**
4. Action: **Start a program**
5. Program/script:

   ```text
   python
   ```
6. Arguments:

   ```text
   path\to\main.py
   ```
7. Start in:

   ```text
   path\to\project\folder
   ```
8. Enable:

   * “Run whether user is logged on or not”
   * “Run with highest privileges” (optional)

---

## ⚠️ Important Disclaimers

### 1. Wi-Fi Must Be Connected

> **You must already be connected to the SRMIST Wi-Fi network before this script runs.**

This tool does **not** connect to Wi-Fi — it only handles captive portal authentication.

---

### 2. Location Services Required (Windows)

> **Windows Location Services must be enabled for `netsh wlan show networks` to detect SSIDs.**

Enable via:

```
Settings → Privacy & Security → Location → Location services → ON
```

---

## ⚠️ Notes & Limitations

* Windows only
* Absolute XPaths may break if portal UI changes
* Headless Chrome is enabled by default
* Retry limits prevent infinite execution

---

## 🐛 Troubleshooting

**Script runs but does nothing**

* Confirm autorun path is correct
* Ensure Python is in PATH
* Try running manually once to verify setup

**SSID not detected**

* Check Location Services
* Ensure Wi-Fi is enabled

---

## 📜 Legal & Usage Notice

This project is intended **for educational and personal convenience only**.
Automating captive portals may violate institutional IT policies.

The author assumes **no responsibility** for misuse or policy violations.

---

## 🧾 License

MIT License
Use, modify, and distribute responsibly.


