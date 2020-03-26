#Extract available web conferences from canvas
from os import system
try:
    import selenium
except:
    system('py -m pip install selenium')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


#Get username and input
usernameString = input("Enter Canvas Username: ")
passwordString = input("Enter Canvas Pumpkin: ")
classlist = input("Enter your classes here eg Chem Robotics Christian PE: ").split(" ")#["Robotics","Biotech","Christian"]
classtimes = ["0835","0925","1110","1200","1340","1430"]

#Startup browser
browser = webdriver.Chrome()
browser.get(('https:scotch.instructure.com/login/ldap'))

#Fill in username
username = browser.find_element_by_id('pseudonym_session_unique_id')
username.send_keys(usernameString)
#Fill in password
password = browser.find_element_by_id('pseudonym_session_password')
password.send_keys(passwordString)

#Sign in
signInButton = browser.find_element_by_class_name('Button.Button--login')
signInButton.click()

#Join function
def joinConference():
    allTabs = browser.window_handles
    if len(allTabs) < 2: #If no tab opened
        print("tabs")
        join = browser.find_element_by_class_name("btn.btn-small.join-button.btn-primary")
        join.click()
    time.sleep(5)
    if len(allTabs) >= 2: #If tab opened
        #Joined conference tab
        print("Successfully connected")
        browser.switch_to_window(allTabs[1])
        time.sleep(5)
        try:
            #If there is both mic and listen option, choose listen
            listenButton = browser.find_element_by_class_name("button--Z2dosza jumbo--Z12Rgj4 default--Z19H5du circle--Z2c8umk")
            listenButton.click()
        except:
            #If there is only one option, have to click allow access
            

        return True

    else:
        print("Failed... Retrying")
        return False


#Current time to match formation hrsmins
currenttime = None
def updateTime():
    global currenttime
    currenttime = time.ctime().split(" ")
    currenttime = currenttime[3]
    currenttime = currenttime.replace(":","")
    currenttime = currenttime[:-2]

#Main Loop
while True:
    for period in range(0,6):
        joinSuccess = False
        updateTime()
        if classtimes[period] == currenttime:
            currentclass = classlist[period]
            print(f"Attempting to connect to class: {currentclass}")

            #Default go to homepage
            homePage = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ic-app-header__logomark")))
            homePage.click()
            #Close all other tabs
            tabs = browser.window_handles
            for tab in tabs:
                browser.switch_to_window(tab)
                if browser.current_url != "https://scotch.instructure.com/":
                    elem = browser.find_element_by_tag_name("body")
                    elem.send_keys(Keys.CONTROL+'t')

            #Wait for login and then choose class
            classButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, f'{currentclass}')))
            classButton.click()

            conference = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "conferences")))
            conference.click()


            #Keep attempting to join class
            while joinConference() == False:
                pass
            time.sleep(70) #Avoid joining same class twice
