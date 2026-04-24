

# SRM AWA 

A Windows-based automation tool that detects network conditions and automatically authenticates the user on the **SRMIST captive portal** using **direct HTTP requests (no browser automation).**

The project is packaged as a **standalone executable with an installer**, enabling seamless background execution.

Supports Windows and requires an active Wi-Fi connection.

---

## ✨ Features

* 🌐 Detects internet connectivity intelligently
* 🧠 Detects **captive portal presence**
* ⚡ Fast authentication using **direct HTTP requests (no Selenium/browser)**
* 🖥 Fully background execution (no visible browser)
* 🔄 **Built-in auto-update system**

  * Automatically checks for new versions
  * Downloads updates in the background
  * Seamlessly installs updates
* ⚙️ Distributed as a **standalone `.exe`**
* 📦 Installer support via **Inno Setup**
* ⚡ Smart execution logic to avoid unnecessary runs
* ⌨️ **Global keyboard shortcuts support**

  * `Alt + S` → Trigger authentication manually
  * `Alt + Q` → Close the application instantly

---

## 🧰 Tech Stack

* Python 3.8+
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
pip install requests pyqt5 python-dotenv
```

---

## ⚙️ How It Works

### 1. Connectivity Check

* Sends a request to Google's `generate_204` endpoint
* If response is `204`, internet is already available

---

### 2. Captive Portal Detection

* If the request is **redirected** or returns a non-204 response
* The system assumes a captive portal is active

---

### 3. Authentication Flow (No Browser)

* Captures session cookies from the captive portal
* Sends a **POST request** with login credentials
* Handles required headers and tokens
* Verifies successful authentication via response validation

---

## 🔄 Auto Update System

The application includes a built-in update delivery mechanism to ensure users always have the latest version.

### How it works

1. Checks for updates from a remote source
2. Downloads the latest version if available
3. Closes the running application
4. Triggers an updater process (script/executable)
5. Replaces old files and relaunches the application

### Benefits

* Ensures compatibility with captive portal changes
* Delivers bug fixes instantly
* No manual reinstall required

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

### 🔄 Updates

* Internet connection is required for update checks
* Antivirus may flag updater behavior (due to file replacement mechanisms)

---

## 🚧 Challenges & Limitations

* **Portal Dependency**

  * Breaks if captive portal API or request structure changes

* **Session Handling**

  * Requires correct handling of cookies/tokens

* **Network Variability**

  * Captive portal detection may vary depending on network behavior

---

## 🐛 Troubleshooting

### Authentication does not trigger

* Ensure you are connected to a network requiring login
* Try opening a browser manually to confirm captive portal

---

### Authentication fails

* Captive portal request structure may have changed
* Re-check headers, cookies, and payload format

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

---
