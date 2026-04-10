import sys,os,keyboard,time
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSignal,QThread,QTimer

from datetime import timedelta

from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QSystemTrayIcon, QMenu,QLabel,
    QLineEdit,QPushButton,QStackedWidget
)
from PyQt5.QtCore import Qt

from selenium import webdriver
import time,requests,scanner_
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import dotenv_values






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
        val=False
        try:
            requests.get("https://iach.srmist.edu.in/Connect/PortalMain")
            val=True
            
        except:
           
            
            try:
                requests.get("https://iac.srmist.edu.in/Connect/PortalMain")
                val=True
            except:
                pass
        return val

    
    


def is_connected():
    window.status.setText("Checking Network Connectivity.......")
    try:
        response = requests.get("http://clients3.google.com/generate_204", timeout=5)
        
        return response.status_code == 204
    
    except:
        return False


def main():
        opns = Options()
        opns.add_argument('--headless') 
        opns.add_argument('--disable-gpu')
        opns.add_argument('--no-sandbox')  
        browser=webdriver.Chrome(options=opns)
        z=True
        count=0
        url=''
        window.status.setStyleSheet("color:red;")
        window.status.setText("Detecting Captive Portal......")
    
        


        try:
            requests.get("https://iach.srmist.edu.in/Connect/PortalMain")
            url="https://iach.srmist.edu.in/Connect/PortalMain"
            window.status.setText("Hostel Network detected.....")

        except:
           
            url="https://iac.srmist.edu.in/Connect/PortalMain"
            window.status.setText("UB Network detected.....")

    


        browser.get(url)
        window.status.setText("Getting Instance.....")
        if not window.isVisible():
                window.tray.showMessage("AWA","Getting Instance!")
        time.sleep(2)
        config=dotenv_values(os.path.join(os.getenv("APPDATA"),"AWA")+"\\.env")
        while z and count<2000:
            count+=1

            username=browser.find_element(By.XPATH,'/html/body/div/table/tbody/tr[1]/td/div[2]/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/div/div[1]/div/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[3]/input')
            password=browser.find_element(By.ID,'LoginUserPassword_auth_password')
            button=browser.find_element(By.XPATH,'/html/body/div/table/tbody/tr[1]/td/div[2]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/a[1]/span')
            time.sleep(2)
            window.status.setStyleSheet("color:blue;")
            username.send_keys(config["USER_NAME"])
            window.status.setText("User Name Entered.....")
            time.sleep(2)
            password.send_keys(config["PASSWORD"])
            window.status.setText("Password Entered.....")
            time.sleep(2)
            button.click()

            time.sleep(2)
            window.status.setText("Assuring Login.....")
            z=False
   
        x=True
        while x:
            try:
                logout_btn=browser.find_element(By.XPATH,'/html/body/div/table/tbody/tr[1]/td/div[2]/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td/a[1]/span')
                window.status.setText('logged in successfully!!!!')
                window.status.setStyleSheet("color:green;")
                if not window.isVisible():
                    window.tray.showMessage("AWA","Logged IN!")

                    
                browser.quit()
                x=False
                with open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\times.log","a") as r:
                        yo=time.time()
                        r.writelines("\n"+str(yo))
                        window.assertedtime=yo
            
                    
                        
            
            except Exception as e:
                print(e)

class Worker(QThread):
    progress = pyqtSignal(int)
 
    def run(self):
        if  not is_connected():
            try:
                if detect_wifi():
                    main()
            except:
                try:
                    if detect_wifi1():
                        main()
                except Exception as e:
                    window.status.setText(str(e))
        else:
            window.status.setText("Already Connected to Internet!")
            window.status.setStyleSheet("color:green;")
            window.assertedtime=None 
            # window.close()
class IntialSetup(QThread):
    def run(self):
 
        opns = Options()
        opns.add_argument('--headless') 
        opns.add_argument('--disable-gpu')
        opns.add_argument('--no-sandbox')  
        browser=webdriver.Chrome(options=opns)
        browser.get("https://google.com")
        browser.quit()
     
class Keyboard_Monitor(QThread):
    def run(self):
        while True:
            if keyboard.is_pressed("Alt") and keyboard.is_pressed("S"):
                if not window.thread_.isRunning():
                    window.start_thread()
            if keyboard.is_pressed("Alt") and keyboard.is_pressed("Q"):break



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
        self.nstatus=self.findChild(QLabel,"nstatus")
        self.restart=self.findChild(QPushButton,"restart")
        self.restart.clicked.connect(lambda:os.execl(sys.executable,sys.executable,*sys.argv))
       
       
        
     
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
            self.thread_.finished.connect(lambda:self.connectbtn.setEnabled(True))
            self.thread_.finished.connect(self.thread_finished)
            self.connectbtn.setEnabled(False)
            self.thread_.start()
    def intialsetup(self):
            self.thread = IntialSetup()
            self.thread.finished.connect(lambda:self.page.setCurrentIndex(2))
            self.thread.start()
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
                     
            except Exception as e:
                print("error1",e)
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
            if is_connected():
                QTimer.singleShot(0,self.intialsetup)
                x=open(os.path.join(os.getenv("APPDATA"),"AWA")+"\\.env","x")
                x.write("USER_NAME="+self.uname.text())
                x.write("\n")
                x.write("PASSWORD="+self.passw.text())
                x.close()
                
                self.nstatus.setText("Wait a while!")
            else:
                self.nstatus.setText("Not connected to the Internet!")
                self.nstatus.setStyleSheet("color:'red';") 
   

          

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
    









app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = MainWindow()
window.show()
if scanner_.get_processes():
    print('yeah')
    sys.exit(0)
else:
    pass
sys.exit(app.exec_())