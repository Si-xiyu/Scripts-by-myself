from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time

def load_or_create_config(config_path="config.json"):
    config = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        if "email" not in config or "password" not in config:
            raise ValueError("- 配置文件缺字段")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print("- 配置文件读取失败")
        email = input("请输入邮箱：")
        password = input("请输入密码：")
        config = {"email": email.strip(), "password": password.strip()}
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("- 配置已保存至 config.json")
    return config

# 加载账号密码
config = load_or_create_config()
email = config["email"]
password = config["password"]

driver_path = r"E:\software\msedgedriver\msedgedriver.exe"
driver = webdriver.Edge(service=EdgeService(driver_path))

driver.get("https://飞兔.com")
time.sleep(3)

# 登录
driver.find_element(By.ID, "regusername").send_keys(email)
driver.find_element(By.ID, "regpassword").send_keys(password)
driver.find_element(By.CLASS_NAME, "loginbutton").click()

time.sleep(5)

# 进入签到页面并签到
driver.find_element(By.CLASS_NAME, "qiandao").click()
time.sleep(3)
driver.find_element(By.CLASS_NAME, "invite_get_amount").click()
time.sleep(3)

driver.quit()
