from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.options import Options
import os
import json
import time

# Configure Edge options for headless mode
# options = Options()
# options.add_argument("--headless")           # 开启无头模式
# options.add_argument("--disable-gpu")        # 禁用 GPU（部分系统下防止崩溃）
# options.add_argument("--window-size=1920,1080")  # 指定浏览器分辨率（防止定位失败）

# Always save/read config.json in the same folder as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

# load and create config.json if it can't be loaded
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

# try to log in
def attempt_login(driver, email, password):
    driver.find_element(By.ID, "regusername").clear()
    driver.find_element(By.ID, "regusername").send_keys(email)
    driver.find_element(By.ID, "regpassword").clear()
    driver.find_element(By.ID, "regpassword").send_keys(password)
    driver.find_element(By.CLASS_NAME, "loginbutton").click()
    time.sleep(5)

    # Check if login succeeded
    try:
        error_box = driver.find_element(By.ID, "tancuowu")
        style = error_box.get_attribute("style")
        if "display: none" not in style:
            error_text = error_box.text.strip()
            print(f"Login failed, error message: {error_text or 'Unknown error'}")
            return False
        else:
            print("Login successful (error box hidden)")
            return True
    except NoSuchElementException:
        print("Login successful (error box not found)")
        return True

# Load account credentials
config = load_or_create_config()
email = config["email"]
password = config["password"]

# Initialization for driver
driver_path = r".\Dependencies\msedgedriver\msedgedriver.exe"
driver = webdriver.Edge(service=EdgeService(driver_path))

driver.get("https://飞兔.com")
# Wait for page to load
time.sleep(3)

# Login
# First login attempt
success = attempt_login(driver, email, password)

# Retry once if login failed
if not success:
    print("First login attempt failed, retrying once...")
    time.sleep(2)
    success = attempt_login(driver, email, password)

if not success:
    print("Login failed after retry. Exiting.")
    driver.quit()
    exit()

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
print("Check in successfully!")
time.sleep(100)
driver.quit()