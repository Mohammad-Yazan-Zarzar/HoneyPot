import base64
import json
from datetime import datetime
import subprocess
import mysql.connector
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# from appium.webdriver.common.touch_action import TouchAction
# from selenium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import imaplib
import email
from email.header import decode_header
import time
import os.path
# from appium.webdriver.common.touch_action import TouchAction
import string
from selenium.webdriver.support.ui import WebDriverWait

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random

# from appium.webdriver.common.mobileby import MobileBy
# from appium.webdriver.support.ui import Select
# import Json
x = True
def generate_random_string(length):
    # Get all the ASCII letters in lowercase and uppercase
    letters = string.ascii_letters
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string




def getNumber():
    print('getNumber')

def readGmailApi():
    with open('client_secret_3.json', 'r') as f:
        creds_data = json.load(f)
        creds = Credentials.from_info(creds_data)

    # Create a Gmail API client
    service = build('gmail', 'v1', credentials=creds)

    # Retrieve the list of email messages
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print(f'Number of messages: {len(messages)}')

        # Iterate through the messages and print the subject and body
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']

            # Find the subject and body of the email
            subject = next((header for header in headers if header['name'] == 'Subject'), None)
            if subject:
                subject = subject['value']
            else:
                subject = 'No subject'

            body = ''
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body']['data']
                        body = base64.urlsafe_b64decode(body).decode('utf-8')
                        break

            print(f'Subject: {subject}')
            print(f'Body: {body}')
            print()


def telegramTest(item):
    mobileNumber=item["mobileNumber"]
    mobileCountry=item["mobileCountry"]
    desired_capabilities = {
        "platformName": "Android",
        "appium:deviceName": "Samsung Galaxy S20+",
        "appium:app": r'C:\\Users\\iyad_\\Downloads\\telegram-x-0-26-9-1730-arm64-v8a.apk',
        "appium:automationName": "UiAutomator2"
    }
    print(desired_capabilities)
    device_id =  "Samsung Galaxy S20+"

    # Create the Appium driver
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)

    try:
        driver.implicitly_wait(30)
        driver.find_element(By.ID, value='org.thunderdog.challegram:id/btn_done').click()
        driver.implicitly_wait(10)
        code = driver.find_element(By.ID, value='org.thunderdog.challegram:id/login_code')
        code.clear()
        code.send_keys(mobileCountry)
        phone = driver.find_element(By.ID, value='org.thunderdog.challegram:id/login_phone')
        phone.send_keys(mobileNumber)
        btnDone = driver.find_element(By.ID, value='org.thunderdog.challegram:id/btn_done')
        btnDone.click()
        senario=0
        try:
            # driver.find_element(By.XPATH,value='//android.widget.TextView[@text="Error: Too many requests. Try again in 21 hours. Contact us, if you need help."]')
            driver.find_element(By.XPATH, value='//android.widget.TextView[contains(@text, "Error")]')

            print('wait to 22 hours')
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            imgName = os.path.join(screenshot_dir, f'TelegramError-{dt_string}.png')
            driver.get_screenshot_as_file(imgName)
            print(imgName)

            senario=3

            print(dt_string)
            item["status"]='failed'
            item["time"]=dt_string
            subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
            driver.quit()
        except:
            senario=0
        if senario!=3:
            try:
                driver.find_element(By.XPATH,value='//android.widget.TextView[@text="Enter your email address"]')
                senario=1
            except:

                senario=0
                try:
                    driver.find_element(By.XPATH, value='//android.widget.TextView[contains(@text, "sent an SMS")]')

                    print('done')
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print(dt_string)
                    item["status"] = 'success'
                    item["time"] = dt_string
                    # subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
                    driver.quit()
                except:

                    now = datetime.now()
                    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                    screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)
                    imgName = os.path.join(screenshot_dir, f'TelegramError-{dt_string}.png')

                    driver.get_screenshot_as_file(imgName)
                    item['status']='new case'
                    # subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
                    driver.quit()
            if senario==1:
                emailInput=driver.find_element(By.XPATH,value='//android.widget.EditText')
                emailInput.send_keys('NOC.17.07.24@gmail.com')
                nextBtn=driver.find_element(By.XPATH,value='//android.view.View[@resource-id="org.thunderdog.challegram:id/btn_done"]')
                nextBtn.click()
                time.sleep(10)
                senario=0
                try:
                    driver.find_element(By.XPATH,value='//android.widget.TextView[@text="Code"]')
                    senario=1
                except:
                    print('code page not found')
                    senario=0
                if senario==1:
                    time.sleep(10)
                    service=get_service()
                    code=list_messages(service)
                    codeInput=driver.find_element(By.XPATH,value='//android.widget.EditText')
                    codeInput.send_keys(code)
                    driver.find_element(By.XPATH,value='//android.view.View[@resource-id="org.thunderdog.challegram:id/btn_done"]').click()
                    try:
                        driver.find_element(By.XPATH,value='//android.widget.TextView[contains(@text, "sent an SMS")]')
                        print('success')
                        now = datetime.now()
                        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
                        if not os.path.exists(screenshot_dir):
                            os.makedirs(screenshot_dir)
                        imgName = os.path.join(screenshot_dir, f'TelegramError-{dt_string}.png')

                        driver.get_screenshot_as_file(imgName)
                        item["status"] = 'success'
                        item["time"] = dt_string
                        item['testDate'] = now.date()
                        item['testTime'] = now.time()
                        # subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
                        driver.quit()
                        # return True
                    except:
                        print('email code probleme')
                        now = datetime.now()
                        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
                        if not os.path.exists(screenshot_dir):
                            os.makedirs(screenshot_dir)
                        imgName = os.path.join(screenshot_dir, f'TelegramError-{dt_string}.png')

                        driver.get_screenshot_as_file(imgName)
                        print(imgName)
                        item["status"] = 'failed'
                        item["time"] = dt_string
                        item['testDate'] = now.date()
                        item['testTime'] = now.time()
                        # subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
                        driver.quit()
                        # return False



                elif senario==0:
                    now = datetime.now()
                    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                    screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)
                    imgName = os.path.join(screenshot_dir, f'TelegramError-{dt_string}.png')

                    driver.get_screenshot_as_file(imgName)
                    item["status"] = 'failed'
                    item["time"] = dt_string
                    item['testDate'] = now.date()
                    item['testTime'] = now.time()
                    # subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
                    driver.quit()
                    # return False

    except:
        print('error')
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        imgName = os.path.join(screenshot_dir, f'TelegramError-{dt_string}.png')

        driver.get_screenshot_as_file(imgName)
        print(imgName)

        print(dt_string)
        item["status"] = 'failed'
        item["time"] = dt_string
        item['testDate']=now.date()
        item['testTime']=now.time()
        # subprocess.run(["adb", "-s", device_id, "shell", "pm", "clear", "org.telegram.x"], check=True)
        driver.quit()
        # return False


# telegramTest()
# readGmail()
# readGmailApi()
def microsoftTest(item):
    x = 1
    countryName = item['countryName']
    # countryName='Tunisia'
    # countryName='Egypt'
    coutryCode=item["mobileCountry"]
    # mobile='1228987259'
    mobile=item["mobileNumber"]
    # mobile='56004056'
    desired_capabilities = {
        "platformName": "Android",
        "appium:deviceName": "Samsung Galaxy S20+",
        "appium:app": r'C:\Users\iyad_\Downloads\HoneyPot apk\microsoft-outlook-4-2426-1.apk',
        "appium:automationName": "UiAutomator2"
    }
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    try:

        driver.implicitly_wait(30)
        addAccountBtn = driver.find_element(By.ID, value='com.microsoft.office.outlook:id/btn_primary_button')
        addAccountBtn.click()
        EmailInput = driver.find_element(By.ID, value='com.microsoft.office.outlook:id/auto_complete_input_email')
        EmailInput.send_keys('Amare.Kamari@hotmail.com')
        submitBtn = driver.find_element(By.ID, value='com.microsoft.office.outlook:id/menu_continue')
        submitBtn.click()
        print('step 1 done')
        time.sleep(25)
        passwordInput = driver.find_element(By.XPATH, value='//android.widget.EditText[@resource-id="i0118"]')
        print(passwordInput)
        passwordInput.send_keys('AmjadKaram')
        signInBtn = driver.find_element(By.XPATH, value='//android.widget.Button[@resource-id="idSIButton9"]')
        signInBtn.click()
        time.sleep(5)
        nextBtn = driver.find_element(By.XPATH, value='//android.widget.Button[@resource-id="StartAction"]')
        nextBtn.click()
        time.sleep(5)
        phoneCountry = driver.find_element(By.XPATH, value='//android.view.View[@resource-id="phoneCountry"]')

        phoneCountry.click()
        time.sleep(1)
        listElement = driver.find_element(By.CLASS_NAME, value='android.widget.ListView')
        elements = listElement.find_elements(By.CLASS_NAME, value='android.widget.CheckedTextView')
        print(len(elements))
        try:

            driver.find_element(By.XPATH,f"//android.widget.CheckedTextView[@resource-id='android:id/text1' and contains(@text, '{countryName}')]").click()
            # driver.find_element(By.XPATH,value='//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Vanuatu (+678)"]')
            # // android.widget.CheckedTextView[ @ resource - id = "android:id/text1" and @text="Vanuatu (+678)"]

            print('driver')
        except:
             if x == 1:
                print(elements[0].text[0])
                if countryName[0] < elements[0].text[0]:
                    # actions = ActionChains(driver)

                    while x == 1:

                        # # override as 'touch' pointer action
                        # actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                        # actions.w3c_actions.pointer_action.move_to_location(500, 100)
                        # actions.w3c_actions.pointer_action.pointer_down()
                        # actions.w3c_actions.pointer_action.pause(0.5)
                        # actions.w3c_actions.pointer_action.move_to_location(500, 350)
                        # actions.w3c_actions.pointer_action.release()
                        # actions.perform()
                        #
                        start_x = listElement.size['width'] / 2
                        start_y = listElement.size['height'] * 0.6  # Start from the bottom of the list view
                        end_y = listElement.size['height'] * 0.5  # Scroll to the top of the list view
                        driver.swipe(start_x, end_y, start_x, start_y, 50)  # Swipe vertically

                        ############################
                        elements = listElement.find_elements(By.CLASS_NAME, value='android.widget.CheckedTextView')

                        # time.sleep(2)
                        print(len(elements))
                        # for element in elements:
                        #     print(element.text)
                        #     print(type(element.text))
                        #     print(element.text.split(' ')[1])
                        #     if coutryCode in element.text.split(' ')[-1]:
                        #         x = 0
                        #         element.click()
                        #         break
                        try:
                            driver.find_element(By.XPATH,f"//android.widget.CheckedTextView[@resource-id='android:id/text1' and contains(@text, '{countryName}')]").click()
                            x=0
                        except:
                            continue

                else:
                    # actions = ActionChains(driver)

                    while x == 1:

                        # override as 'touch' pointer action
                        # actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                        # actions.w3c_actions.pointer_action.move_to_location(500, 100)
                        # actions.w3c_actions.pointer_action.pointer_down()
                        # actions.w3c_actions.pointer_action.pause(0.5)
                        # actions.w3c_actions.pointer_action.move_to_location(500, -300)
                        # actions.w3c_actions.pointer_action.release()
                        # actions.perform()
                        ############################
                        start_x = listElement.size['width'] / 2
                        start_y = listElement.size['height'] * 0.6  # Start from the bottom of the list view
                        end_y = listElement.size['height'] * 0.5  # Scroll to the top of the list view
                        driver.swipe(start_x, start_y, start_x, end_y, 50)  # Swipe vertically

                        elements = listElement.find_elements(By.CLASS_NAME, value='android.widget.CheckedTextView')

                        # time.sleep(2)
                        print(len(elements))
                        # for element in elements:
                        #     print(element.text)
                        #     print(type(element.text))
                        #     if coutryCode in element.text.split(' ')[-1]:
                        #         x = 0
                        #         element.click()
                        #         break
                        try:
                            driver.find_element(By.XPATH,f"//android.widget.CheckedTextView[@resource-id='android:id/text1' and contains(@text, '{countryName}')]").click()
                            x = 0
                            break
                        except:
                            continue
        phoneNumber = driver.find_element(By.XPATH, value='//android.widget.EditText[@resource-id="proofField"]')
        phoneNumber.send_keys(mobile)
        # driver.save_screenshot('image1')
        actions = ActionChains(driver)
        # override as 'touch' pointer action
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(500, 100)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(500, 0)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        nextBtn2 = driver.find_element(By.XPATH, value='//android.widget.Button[@resource-id="nextButton"]')
        nextBtn2.click()
        time.sleep(3)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-images'
        try:
            driver.find_element(By.XPATH, value='//android.widget.TextView[@resource-id="serviceAbuseEnterCodeTitle"]')
            print('success')
            print(dt_string)
            item['time']=dt_string
        except:

            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            imgName = os.path.join(screenshot_dir, f'microsoftError-{dt_string}.png')

            driver.get_screenshot_as_file(imgName)
            driver.quit()

    except:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        imgName = os.path.join(screenshot_dir, f'microsoftError-{dt_string}.png')

        driver.get_screenshot_as_file(imgName)
        # ###############################################################
        print('failed')
        driver.quit()

def uberTest():
    phoneNumber='1228987350'
    countryCode='230'
    desired_capabilities = {
        "platformName": "Android",
        "appium:deviceName": "Samsung Galaxy S20+",
        "appium:app": r"C:\\Users\\iyad_\\Downloads\\HoneyPot apk\\uber-4-534-10000.apk",
        "appium:automationName": "UiAutomator2",
        "appium:appWaitForLaunch": False,
    }
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    # try:
    driver.implicitly_wait(30)
    # Deny button handle
    try:
        driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]').click()
        print('Handle Deny Btn')
    except:
        print('location not request')


    time.sleep(5)


    # welcom Button-------------------
    try:
        driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.ubercab:id/welcome_screen_continue"]').click()
    except:
        print('Hello')
    print('befor')
    time.sleep(20)
    countryCodeSelect=driver.find_element(By.XPATH,value='//android.view.View[@resource-id="PHONE_COUNTRY_CODE"]')
    defaultCountryCode=countryCodeSelect.find_element(By.CLASS_NAME,value='android.widget.TextView')
    print(defaultCountryCode.text,defaultCountryCode.text[0])
    defaultText=defaultCountryCode.text
    countryCodeSelect.click()
    print('after click')
    time.sleep(5)

    def scroll_to_element(driver, target_text,direction,countryCode):
        # Get the window size
        window_size = driver.get_window_size()
        start_x = window_size['width'] // 2


        def scroll(direction):
            if direction == 'down':
                start_y = window_size['height'] * 4 // 5
                end_y = window_size['height'] // 5
            else:  # direction == 'up'
                start_y = window_size['height'] // 5
                end_y = window_size['height'] * 4 // 5
            #
            actions = ActionChains(driver)
            # override as 'touch' pointer action
            # actions.w3c_actions.pointer_action.
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.click_and_hold()
            # actions.w3c_actions.pointer_action.pause(2)
            actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            print('action')

            # driver.swipe(start_x, end_y, start_x, start_y, 20)  # Swipe vertically
            # print('swip')
        # Try to scroll down first
        if direction=='down':
            for _ in range(7):  # Adjust the range based on the expected number of scrolls needed
                try:
                    try:
                        # element=driver.find_element(By.XPATH,f"//*[contains(@text, '{countryCode}')]")
                        elements=driver.find_elements(By.CLASS_NAME,value='android.widget.TextView')
                        for element in elements:
                            print(element.text)
                    except:
                        print('not found')
                    return element
                except:
                    scroll('down')

        # If not found, scroll up
        else:
            for _ in range(7):  # Adjust the range based on the expected number of scrolls needed
                try:
                    try:
                        element=driver.find_element(By.XPATH,f"//*[contains(@text, 'Japan')]")
                    except:
                        element=driver.find_element(By.XPATH,f"//*[contains(@text, '{target_text}')]")
                    # time.sleep(2)
                    return element
                except:
                    scroll('up')

        raise Exception(f'Element with text "{target_text}" not found.')

    # Scroll to the desired country code
    # desired_country_code = "EG"
    desired_country_code = "MU"
    # desired_country_code = "US"


    direction='down'
    print(defaultText)
    if defaultText[0]>=desired_country_code[0]:
            direction='down'
            print(direction,defaultText[0],desired_country_code[0])
    else:
        direction='up'
    desired_country_code_element = scroll_to_element(driver, desired_country_code,direction,countryCode)
    print(desired_country_code_element)
    # Click the desired country code
    desired_country_code_element.click()
    print('found')
    phoneNumberField=driver.find_element(By.XPATH,value='//android.widget.EditText[@resource-id="PHONE_NUMBER"]')
    phoneNumberField.send_keys(phoneNumber)
    time.sleep(1)
    continueBtn=driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="forward-button"]')
    continueBtn.click()


def facebookTest():
    desired_capabilities = {
        "platformName": "Android",
        "appium:deviceName": "Samsung Galaxy S20+",
        "appium:app": r"C:\\Users\\iyad_\\Downloads\\HoneyPot apk\\facebook-472-0-0-45-79",
        "appium:automationName": "UiAutomator2",
        "appium:appWaitForLaunch": False,
    }
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    # try:
    driver.implicitly_wait(30)
    accountName="963993991723"
    password="1234Zeyno5678"
    countryName='Egypt'
    mobileNumber='1228987455'
    # login Form
    driver.find_element(By.XPATH,value='(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText').send_keys(accountName)
    driver.find_element(By.XPATH,value='(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.EditText').send_keys(password)
    driver.find_element(By.XPATH,value='//android.view.View[@content-desc="Log in"]').click()
    time.sleep(10)
    # --------------menue Btn
    driver.find_element(By.XPATH,value='//android.view.View[@content-desc="Menu, tab 5 of 5"]').click()
    time.sleep(5)
    # --------------scroll down
    def scrollDown():
        window_size = driver.get_window_size()
        start_x = window_size['width'] // 2
        start_y = window_size['height'] * 4 // 5
        end_y = window_size['height'] // 5
        actions = ActionChains(driver)
        # override as 'touch' pointer action
        # actions.w3c_actions.pointer_action.
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.click_and_hold()
        # actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print('action')
        time.sleep(2)

    scrollDown()
    # ---------------privacy settings
    driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="Settings & privacy, header. Section is collapsed. Double-tap to expand the section."]').click()
    # ---------------privacy center
    driver.find_element(By.XPATH,value='//androidx.recyclerview.widget.RecyclerView[@resource-id="com.facebook.katana:id/(name removed)"]/android.view.ViewGroup[5]/android.view.ViewGroup').click()
    time.sleep(2)
    # -------------scroll down
    scrollDown()
    try:
        driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="Manage your accounts, Accounts Center"]').click()
    except:
        print('need to scroll')
        scrollDown()
        driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="Manage your accounts, Accounts Center"]').click()
    time.sleep(2)
    # ------------personal detailes
    driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="Personal details"]').click()
    time.sleep(2)
    # -------------contact info
    driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="Contact info, +963993991723"]').click()
    time.sleep(2)
    # ------------Add new contact
    driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Add new contact"]/android.view.ViewGroup').click()
    time.sleep(2)
    # -----------Add mobile number
    driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="Add mobile number"]').click()
    time.sleep(2)
    # ----------Change Btn
    driver.find_element(By.XPATH,value='//android.view.View[@content-desc="Change"]').click()
    time.sleep(1)
    # -----------handle drop down list
    for _ in range(10):
        try:
            element = driver.find_element(By.XPATH,value=f'//android.view.View[contains(@content-desc, "{countryName}")]')
            element.click()
            break
        except:
            scrollDown()

    time.sleep(2)
    # --------------------Enter mobile Number
    driver.find_element(By.XPATH,value='//android.widget.EditText').send_keys(mobileNumber)
    # --------------------select Account
    driver.find_element(By.XPATH,value='//android.widget.CompoundButton[@content-desc="Zeyno Zoldic, Facebook"]').click()
    # --------------------next Btn
    driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup')
    time.sleep(2)
    




    # Deny button handle
def facebookLoginTest(item):
    # Use Newtherland siphone
    mobileNumber=item

    def scrollDown():
        window_size = driver.get_window_size()
        start_x = window_size['width'] // 2
        start_y = window_size['height'] * 4 // 5
        end_y = window_size['height'] // 5
        actions = ActionChains(driver)
        # override as 'touch' pointer action
        # actions.w3c_actions.pointer_action.
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.click_and_hold()
        # actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print('action')
        time.sleep(2)


    desired_capabilities = {
  "platformName": "Android",
  "appium:deviceName": "Samsung Galaxy S20+",
  "appium:app": r"C:\\Users\\iyad_\\Downloads\\HoneyPot apk\\facebook-472-0-0-45-79.apk",
  "appium:automationName": "UiAutomator2",
  "appium:appWaitForLaunch": False
}
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    # try:
    driver.implicitly_wait(30)
    time.sleep(20)
    driver.find_element(By.XPATH,value='//android.view.View[@content-desc="Forgot password?"]').click()
    time.sleep(3)
    # -----Deny 1
    driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]').click()
    time.sleep(1)
    #-------Deny 2
    driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]').click()
    time.sleep(1)
    #----------Enter mobile number
    driver.find_element(By.XPATH,value='//android.widget.EditText').send_keys(mobileNumber)
    #----------continue btn
    driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
    time.sleep(3)
    #----------selest way to confirm
    try:
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Try another way"]/android.view.ViewGroup').click()
            time.sleep(2)

        except:
            print('no login page')
        try:
            driver.find_element(By.XPATH,value=f'//android.view.ViewGroup[contains(@content-desc, "SMS") and substring(@content-desc, string-length(@content-desc) - 1) = {mobileNumber[-2:]}]')
        except:
            for _ in range(2):
                scrollDown()
                try:
                    try:
                        driver.find_element(By.XPATH,value='//android.view.ViewGroup[@content-desc="See more"]').click()
                        continue
                    except:
                        driver.find_element(By.XPATH,value=f'//android.view.ViewGroup[contains(@content-desc, "SMS") and substring(@content-desc, string-length(@content-desc) - 1) = {mobileNumber[-2:]}]').click()
                        break
                except:
                    continue
            print('handle see more')
    except:
        #------try another way
        print('new case')
    #--------continue btn
    driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
    time.sleep(5)
    #---------test result
    try:
        driver.find_element(By.XPATH,value='//android.view.View[@content-desc="We sent a code via SMS. Enter that code to confirm your account."]')
        print('success')
    except:
        print('failed')
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        imgName = os.path.join(screenshot_dir, f'facebookError-{dt_string}.png')

        driver.get_screenshot_as_file(imgName)
        print(imgName)


def facebookNewAccountTest(item):
    def scrollDown(x,y):
        window_size = driver.get_window_size()
        start_x = window_size['width'] // 2
        start_x=x
        start_y = y
        end_y = window_size['height'] // 5
        actions = ActionChains(driver)
        # override as 'touch' pointer action
        # actions.w3c_actions.pointer_action.
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.click_and_hold()
        # actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print('action')
        # time.sleep(2)
    def scrollUp(x,y):
        window_size = driver.get_window_size()
        start_x = window_size['width'] // 2
        start_x=x
        start_y = y
        end_y = 1000
        actions = ActionChains(driver)
        # override as 'touch' pointer action
        # actions.w3c_actions.pointer_action.
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.click_and_hold()
        # actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print('action')
        # time.sleep(2)


    countryCode= item["mobileCountry"]
    mobileNumber=item["mobileNumber"]
    first_names = [
        "John", "Mary", "Michael", "Sarah", "David", "Emily",
        "James", "Emma", "Robert", "Olivia", "William", "Ava",
        "Joseph", "Sophia", "Daniel", "Isabella", "Thomas", "Mia",
        "Charles", "Amelia"
    ]
    last_names = [
        "Smith", "Johnson", "Brown", "Williams", "Jones",
        "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]
    days = list(range(1, 29))
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # List of years from 1970 to 2005
    years = list(range(1970, 2006))

    desired_capabilities = {
        "platformName": "Android",
        "appium:deviceName": "Samsung Galaxy S20+",
        "appium:app": r"C:\\Users\\iyad_\\Downloads\\HoneyPot apk\\facebook-472-0-0-45-79.apk",
        "appium:automationName": "UiAutomator2",
        "appium:appWaitForLaunch": False
    }
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    # try:
    driver.implicitly_wait(30)
    time.sleep(30)
    print('start')
    time.sleep(5)
    try:
        #---------create new account btn
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup').click()
        except:
            time.sleep(5)
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup').click()

        time.sleep(1)
        #--------Get started Btn
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Get started"]/android.view.ViewGroup').click()
        time.sleep(1)
        #--------first and last name
        firstName=random.choice(first_names)
        driver.find_element(By.XPATH, value='//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText').send_keys(firstName)
        lastName=random.choice(last_names)
        driver.find_element(By.XPATH, value='//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText').send_keys(lastName)
        #-------Next btn
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
        time.sleep(2)
        #-------handle birthday"August 5,2024"
        current_date = datetime.now()

        # Format the month as abbreviated name (e.g., Aug)
        formatted_month = current_date.strftime("%b")
        formatted_day = current_date.strftime("%d")  # Day of the month as zero-padded decimal (01, 02, ..., 31)
        # formatted_day_without_zero_padding = current_date.strftime("%-d")  # Day of the month without zero padding (1, 2, ..., 31) (This works on Unix-like systems)

        # Format the year
        formatted_year = current_date.strftime("%Y")  # Year with century as a decimal number (2024)
        # formatted_year_short = current_date.strftime("%y")  # Year without century as a zero-padded decimal number (24)

        print(formatted_month)
        print(formatted_day)
        print(formatted_year)
        element=driver.find_element(By.XPATH,value=f'//android.widget.EditText[@resource-id="android:id/numberpicker_input" and @text="{formatted_month}"]')
        # element=driver.find_element(By.XPATH,value='')

        # element=driver.find_element(By.XPATH,value=f'f//android.widget.EditText[@resource-id="android:id/numberpicker_input"')
        location = element.location
        x = location['x']
        y = location['y']
        scrollDown(x,y)

        elementDay=driver.find_element(By.XPATH,value=f'//android.widget.EditText[@resource-id="android:id/numberpicker_input" and @text="{formatted_day}"]')
        location=elementDay.location
        xd = location['x']
        yd = location['y']
        scrollDown(xd, yd)

        elementYear = driver.find_element(By.XPATH,value=f'//android.widget.EditText[@resource-id="android:id/numberpicker_input" and @text="{formatted_year}"]')
        location=elementYear.location
        xy = location['x']
        yy = location['y']
        z=0
        while z<4:
            scrollUp(xy, yy)
            z=z+1

        driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="android:id/button1"]').click()
        # driver.find_element(By.XPATH,value='//android.widget.EditText').clear().send_keys(random.choice(months)+' '+str(random.choice(days))+','+str(random.choice(years)))
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
        time.sleep(3)

        #------handle gender
        gender=['//android.widget.Button[@content-desc="Male"]','//android.view.View[@content-desc="Female"']
        driver.find_element(By.XPATH,value=random.choice(gender)).click()
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
        time.sleep(2)
        #------------handle deny phone manage
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]').click()
        except:
            print('no phone manage')
        #-------------eneter mobile phone
        driver.find_element(By.XPATH,value='//android.widget.EditText').send_keys(countryCode+mobileNumber)
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
        time.sleep(2)
        #-------handle password
        password='123A45#'+firstName[1:3]+'@67Y89'
        driver.find_element(By.XPATH,value='//android.widget.EditText').send_keys(password)
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
        time.sleep(2)
        #-------not save login info
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Not now"]').click()
        time.sleep(2)
        #-------agree poilicies
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="I agree"]/android.view.ViewGroup').click()
        time.sleep(10)
        #---------ask vertification type
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Send code via SMS, Carrier charges may apply"]').click()
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
            time.sleep(5)
        except:
            print('not ask')
        #-------check result
        try:
            now = datetime.now()

            driver.find_element(By.XPATH,value='//android.view.View[@content-desc="Confirmation code"]')
            print('success')
            item['testDate'] = now.date()
            item['testTime'] = now.time()
            item['descriptionTest'] = '--'

            driver.quit()

            return True
        except:
            print('failed')
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
            screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            imgName = os.path.join(screenshot_dir, f'facebookError-{dt_string}.png')

            driver.get_screenshot_as_file(imgName)
            item["status"] = 'failed'
            item["time"] = dt_string
            item['testDate'] = now.date()
            item['testTime'] = now.time()
            item['descriptionTest'] = rf'\whatsappError-{dt_string}.png'
            driver.quit()

            return False
    except:
        print('Error')
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
        screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        imgName = os.path.join(screenshot_dir, f'facebookError-{dt_string}.png')

        driver.get_screenshot_as_file(imgName)
        item["status"] = 'failed'
        item["time"] = dt_string
        item['testDate'] = now.date()
        item['testTime'] = now.time()
        item['descriptionTest'] = rf'\whatsappError-{dt_string}.png'
        driver.quit()

        return False


def instagramCretateAccount(item):
    print('start instagram')
    mobileNumber=item["mobileCountry"]+item["mobileNumber"]

    desired_capabilities = {
        "platformName": "Android",
        "appium:deviceName": "Samsung Galaxy S20+",
        "appium:app": r"C:\\Users\\iyad_\\Downloads\\HoneyPot apk\\instagram-340-0-0-22-109.apk",
        "appium:automationName": "UiAutomator2",
        "appium:appWaitForLaunch": False
    }
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    # try:
    driver.implicitly_wait(30)
    try:
        #------create new account
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup').click()
        time.sleep(2)
        #------deny phone manage
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]').click()
        except:
            print('no phone manage')

        #--------Enter mobile number
        driver.find_element(By.XPATH,value='//android.widget.EditText').send_keys(mobileNumber)
        driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
        time.sleep(2)
        #---------------handle popup create or exist account
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup').click()
            time.sleep(2)
        except:
            print('not ask')
        #-----------send code via sms
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Send code via SMS, Carrier charges may apply"]').click()
            driver.find_element(By.XPATH,value='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
            time.sleep(2)
        except:
            print('diret to result test')
        #----------result test
        try:
            driver.find_element(By.XPATH,value='//android.view.View[@content-desc="Enter the confirmation code"]')
            print('success')
            now = datetime.now()
            item['testDate'] = now.date()
            item['testTime'] = now.time()
            item['descriptionTest'] = '--'

            driver.quit()

            return True
        except:
            print('failed')
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
            screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            imgName = os.path.join(screenshot_dir, f'instagramError-{dt_string}.png')

            driver.get_screenshot_as_file(imgName)
            item["status"] = 'failed'
            item["time"] = dt_string
            item['testDate'] = now.date()
            item['testTime'] = now.time()
            item['descriptionTest'] = rf'\whatsappError-{dt_string}.png'
            driver.quit()

            return False
    except:
        print('error')
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
        screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        imgName = os.path.join(screenshot_dir, f'instagramError-{dt_string}.png')

        driver.get_screenshot_as_file(imgName)
        item["status"] = 'failed'
        item["time"] = dt_string
        item['testDate'] = now.date()
        item['testTime'] = now.time()
        item['descriptionTest'] = rf'\whatsappError-{dt_string}.png'
        driver.quit()
        return False




def whatsAppBuisnessTest(item):
    mobileNumber = item["mobileNumber"]
    mobileCountry = item["mobileCountry"]
    desired_capabilities = {
  "platformName": "Android",
  "appium:deviceName": "Samsung Galaxy S20+",
  "appium:app": r"C:\\Users\\iyad_\\Downloads\\HoneyPot apk\\whatsapp-business-2-24-14-76.apk",
  "appium:automationName": "UiAutomator2",
  "appium:appWaitForLaunch": False

}
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=capabilities_options)
    driver.implicitly_wait(30)
    try:
        #-------ِِِِِAgree Btn
        driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.whatsapp.w4b:id/eula_accept"]').click()
        time.sleep(2)
        #---------enter code and number
        driver.find_element(By.XPATH,value='//android.widget.EditText[@resource-id="com.whatsapp.w4b:id/registration_cc"]').clear().send_keys(mobileCountry)
        driver.find_element(By.XPATH,value='//android.widget.EditText[@resource-id="com.whatsapp.w4b:id/registration_phone"]').send_keys(mobileNumber)
        driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.whatsapp.w4b:id/registration_submit"]').click()
        time.sleep(5)
        #--------handle popup is this correct number
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="android:id/button1"]').click()
        except:
            print('no popup')
        #------handle vertify Another way
        try:
            driver.find_element(By.XPATH,value='//android.widget.Button[@resource-id="com.whatsapp.w4b:id/secondary_button"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH,value='//android.widget.Button[@text="SEND SMS"]').click()
        except:
            print('no popup vertify another way')
        time.sleep(5)

        #-------reult test
        try:
            driver.find_element(By.XPATH,value='//android.widget.TextView[@resource-id="android:id/message"]')
            print('failed')
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            # screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
            screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'

            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            imgName = os.path.join(screenshot_dir, f'whatsappError-{dt_string}.png')

            driver.get_screenshot_as_file(imgName)
            print(imgName)
            item['testDate'] = now.date()
            item['testTime'] = now.time()
            item['descriptionTest']=rf'whatsappError-{dt_string}.png'
            print(item['descriptionTest'])
            driver.quit()

        except:
            try:
                driver.find_element(By.XPATH,value="//*[contains(@text, \"Can't send an SMS\")]")
                print('failed')
                now = datetime.now()
                dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                # screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
                screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'

                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                imgName = os.path.join(screenshot_dir, f'whatsappError-{dt_string}.png')

                driver.get_screenshot_as_file(imgName)
                print(imgName)
                item['testDate'] = now.date()
                item['testTime'] = now.time()
                item['descriptionTest'] =rf'\whatsappError-{dt_string}.png'
                print(item['descriptionTest'])
                driver.quit()

            except:
                print('success')
                now = datetime.now()

                item['testDate'] = now.date()
                item['testTime'] = now.time()
                item['descriptionTest'] ='--'
                driver.quit()


    except:

        now = datetime.now()
        item['testDate'] = now.date()
        item['testTime'] = now.time()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        screenshot_dir = r'C:\Users\iyad_\OneDrive\Desktop\HoneyPot-pythonResults'
        screenshot_dir = r'C:\Users\iyad_\PycharmProjects\pythonProject\static\honeyPotImages'

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        imgName = os.path.join(screenshot_dir, f'whatsappError-{dt_string}.png')
        item['descriptionTest'] =rf'\whatsappError-{dt_string}.png'
        print(item['descriptionTest'])

        driver.get_screenshot_as_file(imgName)
        print(imgName)
        driver.quit()




SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret4.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def list_messages(service, user_id='me'):
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        message_id=messages[0]['id']
        msg = service.users().messages().get(userId=user_id, id=message_id).execute()
        print(msg['snippet'])
        msgPart1=msg['snippet'].split(':')[1]
        msgCode=msgPart1.split('.')[0]
        print('code',msgCode)
        return msgCode

# service = get_service()
# list_messages(service)
def get_mobileNumbers():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="honeypot",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        cursor = db.cursor()
        sql = ("select companyName,countryCode,countryName,telegram,whatsapp,uber,tinder,tiktok,microsoft,"
               "google,facebook,instagram,imo,phone,status,testCounter,mobileNumbers.id"
               " from mobileNumbers inner join company on mobileNumbers.companyId=company.id order by mobilenumbers.testCounter ASC")
        cursor.execute(sql)
        tests = cursor.fetchall()
        cursor.close()
        db.close()
        numberDict={}
        dataList=[]
        companys=[]
        totalDict={}
        for test in tests:
            numberDict={
                        # "mobileNumber":'56004074',
                        "mobileCountry":test[1],
                        "countryName":test[2],
                        "companyName":test[0],
                        "telegram":test[3],
                        "whatsapp":test[4],
                        "uber":test[5],
                        "tinder":test[6],
                        "tiktok":test[7],
                        "microsoft":test[8],
                        "google":test[9],
                "facebook":test[10],
                "instagram":test[11],
                "imo":test[12],
                "mobileNumber":test[13],
                "phoneState":test[14],
                "testCounter":test[15],
                "phoneId":test[16]
            }
            if test[0] in totalDict.keys():
                totalDict[test[0]].append(numberDict)
            else:
                totalDict[test[0]]=[numberDict]
            dataList.append(numberDict)
            companys.append(test[0])

        companys=set(companys)
        return [totalDict,companys]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def insetTest(item):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="honeypot",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        cursor = db.cursor()
        sql = "INSERT INTO tests (phoneId, success, brand, testDate, testTime, descriptionTest) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (item['phoneId'], item['success'], item['brand'], item['testDate'], item['testTime'], item['descriptionTest'])
        cursor.execute(sql,values)
        cursor.execute(f"UPDATE honeypot.mobilenumbers SET testCounter = {item['testCounter']} WHERE mobileNumbers.id={item['phoneId']};")
        # tests = cursor.fetchall()
        cursor.close()
        db.commit()

        db.close()
        print('success')
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


dataList2=[
    {
        "mobileNumber":'56004074',
        "mobileCountry":'216',
        "countryName":'Tunisia',
        "testTime":'',
        "status":''

    },
    {
        "mobileNumber": '1228987330',
        "mobileCountry": '20',
        "countryName": 'Egypt',
        "testTime": '',
        "status": ''

    },

    {
        "mobileNumber": '8496309802',
        "mobileCountry": '1',
        "countryName": 'United States',
        "testTime": '',
        "status": ''

    },
    {
        "mobileNumber": '57389403',
        "mobileCountry": '230',
        "countryName": 'Mauritius',
        "testTime": '',
        "status": ''

    },

]
# for item in dataList:

    # telegramTest(item)
    # whatsAppTest(item)
    # microsoftTest(item)

# # whatsAppTest(dataList[2])
##########################################

def honeyPot(brand):
    total=get_mobileNumbers()
    dataList=total[0]
    companys=total[1]
    print(dataList)
    print(companys)
    if brand=='telegram' or brand=='all':
            for company in companys:
                i=0

                # for item in dataList[company]:
                while(i<4):
                    item=dataList[company][i]

                    i=i+1
                    if item["telegram"]==1:

                        telegramResult=telegramTest(item)
                        try:
                            item["testCounter"]=item["testCounter"]+1
                        except:
                            item["testCounter"]=1
                        item["brand"]="telegram"

                        if telegramResult:
                            print("success telegram")
                            item["success"]=True
                            insertTestResult = insetTest(item)
                            if insertTestResult:
                                print('insert successfuly')
                            else:
                                print('insert Failed ')
                            break
                        else:
                            print('failed telegram')
                            item["success"]=False
                            insertTestResult = insetTest(item)
                            if insertTestResult:
                                print('insert successfuly')
                            else:
                                print('insert Failed ')

                            continue



    if brand=='whatsApp' or brand=='all':

        for company in companys:
            i = 0

            # for item in dataList[company]:
            while (i < 4):
                print(i)
                item = dataList[company][i]
                i=i+1
                if item['whatsapp']==1:

                    whatsAppResult=whatsAppBuisnessTest(item)

                    try:
                        item["testCounter"] = item["testCounter"] + 1
                    except:
                        item["testCounter"] = 1
                    item["brand"] = "whatsApp"
                    if whatsAppResult:
                        print("success whatsapp")
                        item["success"] = True
                        insertTestResult = insetTest(item)
                        if insertTestResult:
                            print('insert successfuly')
                        else:
                            print('insert Failed ')
                        break
                    else:
                        print('failed whatsapp')
                        item["success"] = False
                        insertTestResult = insetTest(item)
                        if insertTestResult:
                            print('insert successfuly')
                        else:
                            print('insert Failed ')

                        continue

    if brand=='facebook' or brand=='all':
        for company in companys:
            i = 0
            while (i < 4):
                item = dataList[company][i]
                # item = dataList[company][i]

                i = i + 1
            # for item in dataList[company]:
                if item["facebook"]==1:
                    facebookResult=facebookNewAccountTest(item)
                    item["brand"]="facebook"
                    if facebookResult:
                        print("success facebbok")
                        item["success"]=True
                        insertTestResult = insetTest(item)
                        if insertTestResult:
                            print('insert successfuly')
                        else:
                            print('insert Failed ')
                        break
                    else:
                        print('failed facebbok')
                        item["success"]=False
                        insertTestResult = insetTest(item)
                        if insertTestResult:
                            print('insert successfuly')
                        else:
                            print('insert Failed ')

                        continue

    if brand=='instagram' or brand=='all':
            for company in companys:
                i=0
                while(i<4):
                    item=dataList[company][i]
                    # item = dataList[company][i]

                    i = i + 1

                # for item in dataList[company]:
                    if item["instagram"] == 1:
                        instagramResult = instagramCretateAccount(item)
                        item["brand"] = "instagram"
                        if instagramResult:
                            print("success instagram")
                            item["success"] = True
                            insertTestResult = insetTest(item)
                            if insertTestResult:
                                print('insert successfuly')
                            else:
                                print('insert Failed ')
                            break
                        else:
                            print('failed instagram')
                            item["success"] = False
                            insertTestResult = insetTest(item)
                            if insertTestResult:
                                print('insert successfuly')
                            else:
                                print('insert Failed ')

                            continue
    if brand == 'microsoft' or brand == 'all':
        for company in companys:
            i = 0
            while (i < 4):
                item = dataList[company][i]
                # item = dataList[company][i]

                i = i + 1

                # for item in dataList[company]:
                if item["microsoft"] == 1:
                    microsoftResult = microsoftTest(item)
                    item["brand"] = "microsoft"
                    if microsoftResult:
                        print("success microsoft")
                        item["success"] = True
                        insertTestResult = insetTest(item)
                        if insertTestResult:
                            print('insert successfuly')
                        else:
                            print('insert Failed ')
                        break
                    else:
                        print('failed microsoft')
                        item["success"] = False
                        insertTestResult = insetTest(item)
                        if insertTestResult:
                            print('insert successfuly')
                        else:
                            print('insert Failed ')

                        continue

# zezo2024t@hotmail.com
#zyk@123456
# item['phoneId'], item['success'], item['brand'], item['testDate'], item['testTime']

# item={
# 'phoneId':1,
#     'success':False,
#     'brand':'whatsApp',
# }
# now = datetime.now()
#
# dt_string = now.strftime("%d_%m_%Y %H:%M:%S")
# item["testDate"] = now.date()
# item["testTime"] = now.time()
# insetTest(item)
# honeyPot('instagram')
# uberTest()
# mobilesList=['18098191698','21656004055','23057430019','201228987350']
# for item in mobilesList:
#     # facebookLoginTest(item)
#     # facebookNewAccountTest(item)
#     instagramCretateAccount(item)
# whatsAppBuisnessTest({"mobileCountry":'20',"mobileNumber":'1228987350'})