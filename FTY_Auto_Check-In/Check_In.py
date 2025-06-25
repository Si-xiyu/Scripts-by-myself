from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import json
import time

# Always save/read config.json in the same folder as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

def load_or_create_config(config_path=config_path):
    config = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        if "email" not in config or "password" not in config:
            raise ValueError("- Config file missing required fields")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print("- Failed to read config file")
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")
        config = {"email": email.strip(), "password": password.strip()}
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("- Configuration saved to config.json")
    return config

# Load account credentials
config = load_or_create_config()
email = config["email"]
password = config["password"]

driver_path = r"E:\software\msedgedriver\msedgedriver.exe"
driver = webdriver.Edge(service=EdgeService(driver_path))

driver.get("https://飞兔.com")
# Wait for page to load
time.sleep(3)

# Login
driver.find_element(By.ID, "regusername").send_keys(email)
driver.find_element(By.ID, "regpassword").send_keys(password)
driver.find_element(By.CLASS_NAME, "loginbutton").click()
# Wait for page update
time.sleep(5)

# Check if login succeeded
try:
    error_box = driver.find_element(By.ID, "tancuowu")
    style = error_box.get_attribute("style")
    if "display: none" not in style:
        error_text = error_box.text.strip()
        if error_text:
            print(f"Login failed, error message: {error_text}")
        else:
            print("Login failed, error box is displayed but contains no message")
        driver.quit()
        exit()
    else:
        print("Error box not displayed, login succeeded or still processing")
except NoSuchElementException:
    print("Error box not found, assuming login succeeded or still processing")

# Try closing the announcement popup if it appears
try:
    time.sleep(3)  # 让弹窗渲染出来
    close_button = driver.find_element(By.CLASS_NAME, "gonggao_tan_button")
    close_button.click()
    print("Closed announcement popup.")
    time.sleep(1)  # 关闭动画时间
except NoSuchElementException:
    print("No announcement popup appeared.")

# Enter check-in page and perform check-in
driver.find_element(By.CLASS_NAME, "qiandao").click()
time.sleep(3)
driver.find_element(By.CLASS_NAME, "invite_get_amount").click()
time.sleep(3)

driver.quit()