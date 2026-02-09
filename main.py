from selenium import webdriver
import time,requests,scanner_
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import dotenv_values

def detect_wifi(target_ssid="SRMIST"):

    scan_results = scanner_.get_scanner()
    print(scan_results)
    for network in scan_results:
        print(network)
        if network == target_ssid:
            print("College Wi-Fi detected!")
            return True
    return False


def is_connected():
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
        try:
            requests.get("https://iach.srmist.edu.in/Connect/PortalMain")
            url="https://iach.srmist.edu.in/Connect/PortalMain"
        except:
             url="https://iac.srmist.edu.in/Connect/PortalMain"
        
           
        browser.get(url)
        time.sleep(2)
        config=dotenv_values(".env")
        while z and count<2000:
            count+=1

            username=browser.find_element(By.XPATH,'/html/body/div/table/tbody/tr[1]/td/div[2]/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/div/div[1]/div/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[3]/input')
            password=browser.find_element(By.ID,'LoginUserPassword_auth_password')
            button=browser.find_element(By.XPATH,'/html/body/div/table/tbody/tr[1]/td/div[2]/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td/a[1]/span')
            time.sleep(2)
            username.send_keys(config["USER_NAME"])
            time.sleep(2)
            password.send_keys(config["PASSWORD"])
            time.sleep(2)
            button.click()

            time.sleep(5)
            z=False

        x=True
        while x:
            try:
                logout_btn=browser.find_element(By.XPATH,'/html/body/div/table/tbody/tr[1]/td/div[2]/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td/a[1]/span')
                print('logged in successfully!!!!')
                browser.quit()
                x=False
                y=input('Press enter to exit')
            except Exception as e:
                print(e)
if  not is_connected():
    if not detect_wifi():
        main()
