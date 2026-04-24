import sys,os,keyboard,time,json,wget,ctypes,time,requests,scanner_,traceback,urllib3
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSignal,QThread,QTimer

from datetime import timedelta

from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QSystemTrayIcon, QMenu,QLabel,
    QLineEdit,QPushButton,QStackedWidget,QProgressBar
)
from PyQt5.QtCore import Qt
from dotenv import dotenv_values
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

version=1.4
BASE_URL=""
session = requests.Session()
session.verify = False

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive",
}
def detect_wifi(target_ssid="SRMIST"):
    window.status.setText("Detecting Network......")
    scan_results = scanner_.get_scanner()
    print(scan_results)
    for network in scan_results:
        print(network.strip())
        if network.strip() == target_ssid:
            print("College Wi-Fi detected!")
            window.status.setText("Network Detected......")
            
            
            return True
    return False
def detect_wifi1():
        global BASE_URL
        val=False
        try:
            requests.get("https://iach.srmist.edu.in/")
            val=True
            BASE_URL="https://iach.srmist.edu.in/"
        except:
           
            
            try:
                requests.get("https://iac.srmist.edu.in/")
                val=True
                BASE_URL="https://iac.srmist.edu.in/"
            except Exception as e:
                print(e)
                pass
        return val

    
    


def is_connected():
    
    try:
        response = requests.get("http://clients3.google.com/generate_204", timeout=5)
        
        return response.status_code == 204
    
    except:
        return False


200      


def encrypt_password(password, token, m, e):
    n = int(m, 16)
    exp = int(e, 16)
    key = RSA.construct((n, exp))
    cipher = PKCS1_v1_5.new(key)
    plain = (token + password).encode("utf-8")
    encrypted = cipher.encrypt(plain)
    hex_enc = encrypted.hex()
    return "".join(reversed([hex_enc[i:i+2] for i in range(0, len(hex_enc), 2)]))




def post_login_handshake():
    endpoints = [
        "/Connect/GetStateAndView",
        "/Connect/GetAttributes",
        "/Connect/viewManager/GetViewCustomContent"
    ]

    for ep in endpoints:
        try:
            resp = session.post(
                BASE_URL + ep,
                headers={
                    **headers,
                    "Content-type": "application/x-www-form-urlencoded",
                    "Referer": f"{BASE_URL}/Connect/PortalMain",
                    "Origin": BASE_URL,
                    "X-Requested-With": "XMLHttpRequest",
                },
                data=""
            )
            print(f"{ep} → {resp.status_code}")
        except Exception as e:
            print(f"{ep} failed: {e}")

def login(progress):
    try:

        session.get(f"{BASE_URL}/Connect/PortalMain", headers=headers)
        progress.emit("message","Getting Instance......!")
        progress.emit("sty","color:blue;")
        if not window.isVisible():
            window.tray.showMessage("AWA","Getting Instance!")
        config=dotenv_values(os.path.join(os.getenv("APPDATA"),"AWA")+"\\.env")
        try:
            rsa_data = session.get(f"{BASE_URL}/Connect/RSASettings", headers=headers).json()
            m = rsa_data["m"]
            e = rsa_data["e"]
            token = rsa_data.get("loginToken", "")

        
            encrypted_pass = encrypt_password(config["PASSWORD"], token, m, e)
        except:
            progress.emit("message","Server not responding...!")
            progress.emit("sty","color:red;")
            return 
        login_data = {
            "realm": "passwordRealm",
            "username": config["USER_NAME"],
            "password": encrypted_pass,
        }
   
        progress.emit("message","Entering Credential....!")
    
       
        if not window.isVisible():
                window.tray.showMessage("AWA","Entering Credential...!")
        login_headers = {
            **headers,
            "Content-type": "application/x-www-form-urlencoded",
            "Referer": f"{BASE_URL}/Connect/PortalMain",
            "Origin": BASE_URL,
            "X-Requested-With": "XMLHttpRequest",
        }
        window.status.setText("Logging In........")
        resp = session.post(
            f"{BASE_URL}/Connect/Login",
            data=login_data,
            headers=login_headers
        )

        result = resp.json()
        print("Login response:", result)

        if result.get("type") == "SUCCESS":
        
           
            progress.emit("message","Just some last steps....!")
            
            post_login_handshake()
            progress.emit("message","Logged In!")
            progress.emit("sty","color:green;")
        
            if not window.isVisible():
                window.tray.showMessage("AWA","Logged In.....!")
            
            with open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log","a") as r:
                yo=time.time()
                r.writelines("\n"+str(yo))
                print("this is a proble")
                window.assertedtime=yo

            if is_connected():
                progress.emit("message","Connected to the Internet!")
                progress.emit("sty","color:green;")
                with open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log","a") as r:
                    yo=time.time()
                    r.writelines("\n"+str(yo))
                    print("this is a proble")
                    window.assertedtime=yo
            else:
                progress.emit("message","Internet Still blocked")
                progress.emit("sty","color:red;")
        else:
            print("Login failed:", result.get("message"))
            return False
    except Exception as e:
        print(e,'ye')

class Worker(QThread):
    progress = pyqtSignal(str,str)
 
    def run(self):
        if window.startup:
            window.startup=False
            time.sleep(4)
        else:
            pass
        self.progress.emit("message","Checking Connectivity.....!")
        self.progress.emit("sty","color:red;")
        if  not is_connected():
            try:
                if detect_wifi():
                    login(self.progress)
                else:
                    self.progress.emit("message","WiFi not detected!")
                    self.progress.emit("sty","color:red;")
            except:
                try:
                    if detect_wifi1():
                        login(self.progress)
                    
                    else:
                        self.progress.emit("message","WiFi not detected!")
                        self.progress.emit("sty","color:red;")  
                except Exception as e:
                    print(e)
                 
        else:
            self.progress.emit("message","Already Connected to Internet!")
            self.progress.emit("sty","color:green;")
            window.assertedtime=None 
            # window.close()

 
 
def exception_hook(exctype, value, tb):
    print(''.join(traceback.format_exception(exctype, value, tb)))
    sys.exit(1)

     
class Keyboard_Monitor(QThread):
    progress=pyqtSignal()
    def run(self):
        while True:
            if keyboard.is_pressed("Alt") and keyboard.is_pressed("S"):
                if not window.thread_.isRunning():
                    window.start_thread()

            
            if keyboard.is_pressed("Alt") and keyboard.is_pressed("Q"):break



class UAMS_DOWNLOAD(QThread):
    progress = pyqtSignal(int)
    def __init__(self, url):
        super().__init__()
        self.url=url
    def run(self):
        wget.download(self.url,bar=self.downloaprogress,out=os.getcwd()+"\\"+"_internal.zip")
    def downloaprogress(self,csize,tsize,width):
        print(csize/tsize*100)
        self.progress.emit(int(csize/tsize*100))

class UAMS_DOWNLOAD_FILE_CHECKER(QThread):
    def run(self):
        while not os.path.exists("_internal.zip"):
            pass





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
       
        if not getattr(sys,"frozen",False):

            uic.loadUi("design.ui", self)  
        else:
            uic.loadUi(os.getcwd()+"\\_internal\\design.ui", self)  
        self.autotrigger=None
        self.assertedtime=0 

        self.keyboard_monitor=Keyboard_Monitor()
        self.keyboard_monitor.progress.connect(lambda:print(time.time()))
        self.keyboard_monitor.finished.connect(lambda:sys.exit(0))
        self.keyboard_monitor.start()
        
  

        if not os.path.exists(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log"):
            os.makedirs(os.path.join(os.getenv("APPDATA"),"AWA"),exist_ok=True)
            x=open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log","+x")
            x.write("TIME LOGS AWA")
            x.close()
        
        
        if not getattr(sys,"frozen",False):

            self.setWindowIcon(QIcon("favicon.ico")) 
        else:
            self.setWindowIcon(QIcon(os.getcwd()+"\\_internal\\ic_launcher.png"))   
               

        
        self.setWindowTitle("AWA")
        self.setWindowFlags(
        Qt.Window |
        Qt.WindowCloseButtonHint |
        Qt.WindowMinimizeButtonHint
    )
        self.uname=self.findChild(QLineEdit,"uname")
        self.passw=self.findChild(QLineEdit,"passw")
        self.btn=self.findChild(QPushButton,'Save')
        self.connectbtn=self.findChild(QPushButton,"connect")
        self.page=self.findChild(QStackedWidget,"pageview")

        self.status=self.findChild(QLabel,"status")
        self.btn.clicked.connect(self.save_creds)
        self.connectbtn.clicked.connect(self.start_thread)
        self.timeleft=self.findChild(QLabel,"timeleft")
        self.timeleftlabel=self.findChild(QLabel,"timeleftlabel")
        
  
       
       #update and message system
        self.message=self.findChild(QLabel,"message")
        self.updatenow=self.findChild(QPushButton,"updatenow")
        self.updatelater=self.findChild(QPushButton,"updatelater")
        self.okay=self.findChild(QPushButton,"okay")
        self.pbar=self.findChild(QProgressBar,"progressBar")
        self.okay.clicked.connect(lambda:self.page.setCurrentIndex(1))
        self.UAMS=False
        self.startup=False
     
        if not getattr(sys,"frozen",False):

            self.tray = QSystemTrayIcon(QIcon("ic_launcher.png"), self)  
        else:
            self.tray = QSystemTrayIcon(QIcon(os.getcwd()+"\\_internal\\ic_launcher.png"), self)
        
        self.tray.setToolTip("AWA is Running")
        tray_menu = QMenu()
        self.tray.setContextMenu(tray_menu)

       
        self.tray.activated.connect(self.on_tray_clicked)

        self.tray.show()
        
        
        
        if not os.path.exists(os.path.join(os.getenv("APPDATA"),"AWA")+"\\.env"):
            self.page.setCurrentIndex(0)
        else:
            self.page.setCurrentIndex(1)
            QTimer.singleShot(0,self.start_thread)

        if not os.path.exists(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log"):
            x=open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log","+x")
            x.write("TIME LOGS AWA")
            x.close()
        
        
    def start_thread(self):
            self.thread_ = Worker()
            self.thread_.finished.connect(self.thread_finished)
            self.thread_.progress.connect(self.thread_progress)
            self.connectbtn.setEnabled(False)
            self.thread_.start()

    def thread_finished(self):
            
            try:
              
                z=self.assertedtime
                if z!=None:
                    print("this")
                    print(z)
                    t=int(float(z))
                    timeto=86400-(int(float(time.time()))-t)
                    timeto*=1000
                    print(timeto)
                    if timeto>=0:
                        self.autotrigger=QTimer(self)
                        self.autotrigger.setSingleShot(True)
                        self.autotrigger.timeout.connect(self.start_thread)
                        self.autotrigger.start(timeto)
                        print(self.autotrigger.remainingTime())
                        autotrigger_monitor=QTimer(self)
                        autotrigger_monitor.timeout.connect(self.timer_function_)
                        autotrigger_monitor.start(1000)
                  
                else:
                    print("that")              
                    with open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log","r") as r:
                        yo=[y.strip() for y in r.readlines() if y!='TIME LOGS AWA']
                        if len(yo)!=0:
                            print(yo)
                            t=int(float(yo[len(yo)-1]))
                            timeto=86400-(int(float(time.time()))-t)
                            timeto*=1000

                            print(timeto)
                            if timeto>=0:
                                self.autotrigger=QTimer(self)
                                self.autotrigger.setSingleShot(True)
                                self.autotrigger.timeout.connect(self.start_thread)
                                self.autotrigger.start(timeto)
                                print(self.autotrigger.remainingTime(),'ye')
                                timer=QTimer(self)
                                timer.timeout.connect(self.timer_function_)
                                timer.start(1000)
                                self.autotrigger_monitor=QTimer(self)
                                self.autotrigger_monitor.timeout.connect(self.check_timeout_)
                                self.autotrigger_monitor.start(1000)
                self.connectbtn.setEnabled(True)
                if not len(sys.argv)>1:
                    if not self.UAMS: 
                        self.UAMS_check()
                else:
                    if "https://" in sys.argv[1]:
                        self.UAMS_START_DOWNLOAD(sys.argv[1])
            except Exception as e:
                print("error1",e)
  
  
    def thread_progress(self,event,message):
        if event=="message": self.status.setText(message)
        else: self.status.setStyleSheet(message)
    def timer_function_(self):
        self.timeleft.setText(str(timedelta(milliseconds=self.autotrigger.remainingTime())))
    def check_timeout_(self):
        if self.autotrigger.remainingTime()<=0:
            if not self.thread_.isRunning():
                self.start_thread()
               

    def on_tray_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger: 
            self.show_window()
    def save_creds(self):
        if not os.path.exists(os.path.join(os.getenv("APPDATA"),"AWA")+"\\.env"):
      

            x=open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\.env","x")
            x.write("USER_NAME="+self.uname.text())
            x.write("\n")
            x.write("PASSWORD="+self.passw.text())
            x.close()
            os.execl(sys.executable,sys.executable,*sys.argv)
    
        

    def keyPressEvent(self, event):


        if event.key() == Qt.Key_Escape:
            self.close()
    

    def show_window(self):
        self.showNormal()        
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        event.ignore()
        self.tray.showMessage("AWA","Active!")
        self.hide()

    def UAMS_check(self):
        self.pbar.setVisible(False)
        self.okay.setVisible(False)
        self.updatenow.setVisible(False)
        self.updatelater.setVisible(False)
        self.UAMS=True
       
        if is_connected():
            try:
                branch= "main" if getattr(sys,"frozen",False) else "Test"
        
                resp=requests.get("https://raw.githubusercontent.com/UtkarshRana22/SRM_AUTO_WIFI_AUTHENTICATOR/"+branch+"/setup/UAMS.json")
                dict_=json.loads(resp.text)
                print(dict_)
                if dict_["update"] and dict_["version"]!=version:
                        if not dict_["force_update"]:
                            self.page.setCurrentIndex(2)
                            self.message.setText(dict_["message"])
                            self.updatelater.setVisible(True)
                            self.updatenow.setVisible(True)
                            
                            self.updatenow.clicked.connect(lambda:self.UAMS_START_SETUP(dict_["url"]))
                            self.updatelater.clicked.connect(lambda:self.page.setCurrentIndex(1))
                        else:
                            self.UAMS_START_SETUP(dict_["url"])
                else:
                    if dict_["showmessage"]:
                        self.page.setCurrentIndex(2)
                        self.message.setText(dict_["message"])
                        self.okay.setVisible(True)

            except Exception as e:
                print(e)
                pass
        

    def UAMS_START_SETUP(self,url):
         
        print("ran UAMS_START_SETUP")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "AWA.exe",url, None, 1)
        sys.exit(0)
    
    def UAMS_START_DOWNLOAD(self,url):
        self.autotrigger.stop()
        self.autotrigger_monitor.stop()
        if os.path.exists(os.getcwd()+"\\_internal.zip"): os.remove(os.getcwd()+"\\_internal.zip")
        self.download_thread=UAMS_DOWNLOAD(url)
        self.download_thread.progress.connect(self.UAMS_DOWNLOAD_PROGRESS)
        self.download_thread.finished.connect(self.UAMS_DOWNLOAD_FINISHED)
        self.page.setCurrentIndex(2)
        self.pbar.setValue(0)
        self.pbar.setVisible(True)
        self.updatelater.setVisible(False)
        self.updatenow.setVisible(False)
        self.okay.setVisible(False)
        self.message.setText("Do not close the application\nUpdating......")
        self.download_thread.start()
    def UAMS_DOWNLOAD_PROGRESS(self,value):
        self.pbar.setValue(int(value))
    def UAMS_DOWNLOAD_FINISHED(self):
        self.pbar.setVisible(False)
        self.message.setText("Unpacking everything!")
        self.UAMS_FILE=UAMS_DOWNLOAD_FILE_CHECKER()
        self.UAMS_FILE.finished.connect(self.unpack)
        self.UAMS_FILE.start()
        
        


    def unpack(self):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "AWA_updater.exe","", None, 1)
        sys.exit(0)




app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = MainWindow()
window.show()
if scanner_.get_processes():
    print('yeah')
    sys.exit(0)
else:
    pass
sys.excepthook = exception_hook

sys.exit(app.exec_())