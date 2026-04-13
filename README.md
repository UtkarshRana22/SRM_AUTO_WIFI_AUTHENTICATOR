# SRM_AUTO_WIFI_AUTHENTICATOR

A Windows-based automation tool that detects network conditions and automatically authenticates the user on the **SRMIST captive portal** using Selenium.

The project is packaged as a **standalone executable with an installer**, enabling seamless background execution.

---

## ✨ Features

* 🌐 Detects internet connectivity intelligently
* 🧠 Detects **captive portal presence**
* 🤖 Automates SRMIST captive portal authentication
* 🖥 Headless browser execution
* ⚙️ Distributed as a **standalone `.exe`**
* 📦 Installer support via **Inno Setup**
* 🚫 No dependency on `netsh` or Location Services
* ⚡ Smart execution logic to avoid unnecessary runs
* ⌨️ **Global keyboard shortcuts support**

  * `Alt + S` → Trigger authentication manually
  * `Alt + Q` → Close the application instantly

---

## 🧰 Tech Stack

* Python 3.8+
* Selenium (with automatic driver management)
* Requests
* PyQt5
* python-dotenv
* auto-py-to-exe (executable packaging)
* Inno Setup (installer creation)

---

## 📦 Installation

### 🔹 For End Users (Recommended)

1. Run the installer (`.exe`)
2. Complete setup
3. Launch the application

> No Python installation required

---

### 🔹 For Developers

```bash
pip install selenium requests pyqt5
```

---

## ⚙️ How It Works

1. **Connectivity Check**

   * Sends a request to Google's `generate_204` endpoint

2. **Captive Portal Detection**

   * If the request is **redirected** or does not return the expected `204` status, a captive portal is detected

3. **Authentication Flow**

   * Launches a headless browser
   * Opens captive portal
   * Submits login form
   * Verifies successful authentication

---

## ▶️ Usage

### Run Executable

```
SRM_AUTO_WIFI_AUTHENTICATOR.exe
```

### Run via Python (Developer Mode)

```bash
python main.py
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action                          |
| -------- | ------------------------------- |
| Alt + S  | Manually trigger authentication |
| Alt + Q  | Exit the application            |

> Shortcuts work globally when the application is running in the background.

---

## ⚠️ Important Notes

### 🔐 Admin Privileges

* If installed in `Program Files`, the app may require **administrator privileges**
* Some operations may fail without elevation

---

### 📡 Wi-Fi Requirement

> You must already be connected to a network that uses the SRM captive portal

This tool does **not** connect to Wi-Fi — it only handles authentication.

---

## 🚧 Challenges & Limitations

* **Portal Dependency**

  * Breaks if captive portal UI changes

* **Captive Portal Detection Variability**

  * Detection relies on HTTP response behavior (redirect/status mismatch)
  * May vary depending on network configuration

* **Headless Browser Variability**

  * May behave differently across systems

---

## 🐛 Troubleshooting

### Authentication does not trigger

* Ensure you are connected to a network requiring login
* Try opening a browser manually to confirm captive portal

---

### Authentication fails

* Portal UI may have changed
* Update selectors/XPaths

---

## 📜 Legal & Usage Notice

This project is intended **for educational and personal convenience purposes only**.

Automating captive portal authentication may violate institutional IT policies.
Users are responsible for ensuring compliance with their organization's guidelines.

The author assumes **no responsibility** for misuse or policy violations.

---

## 🧾 License

MIT License
Use, modify, and distribute responsibly.

