
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ddddocr import DdddOcr
from time import sleep
import json


try:
    with open("config.json", encoding="utf-8") as f:
        data = json.loads(f.read())
except Exception as e:
    print("读取配置文件config.json错误 请检查是否信息齐全 详细错误为：")
    print(e)

browser = webdriver.Chrome("chromedriver.exe")


def main():
    browser.get("https://i.hzmbus.com/webhtml/login")
    try:
        username = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入邮箱地址']"))
        )
        password = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入密码']"))
        )
        username.send_keys(str(data['mail']))
        password.send_keys(str(data['pwd']))
        browser.find_element(By.CLASS_NAME, "login_btn").click()

        ticket = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@class='get_to' and text()='{str(data['destination'])}']"))
        )
        ticket.click()

        name = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@maxlength='20']"))
        )
        idBox = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@maxlength='40']"))
        )
        name.send_keys(str(data['nameStr']))
        idBox.send_keys(str(data['idNumber']))

        print("开始验证码识别，请等待5秒验证码刷新时间")
        sleep(5)
        image = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='验证码']"))
        )
        img_bytes = image.screenshot_as_png

        ocr = DdddOcr()
        res = ocr.classification(img_bytes=img_bytes)
        print(f'验证码结果为：{res}')
        captcha = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='验证码']"))
        )
        captcha.send_keys(str(res))

        agree = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hint_icon"))
        )
        agree.click()

        confirm = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='确认购票']"))
        )

        print(f"每等待{data['interval']}秒刷新一次，默认为10秒")
        while (confirm):
            sleep(data['interval'])
            confirm.click()

    except Exception as e:
        print(f"出现异常：{e}")


if __name__ == '__main__':
    main()
