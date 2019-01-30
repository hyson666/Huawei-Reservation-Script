from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions

import requests
import time
import re


# Login by requests
def login():
    # 取得登陆cookies
    uid = "hyson1996@163.com"
    pwd = "h1s_wantto10ve"
    actionFlag = "loginAuthenticate"
    lang = "zh_CN"
    loginFlag = "byUid"
    login_info = {"uid": uid, "password": pwd, "actionFlag": actionFlag, "lang": lang, "loginFlag": loginFlag}

    website = "https://uniportal.huawei.com/uniportal/login.do"

    req = requests.post(website, data=login_info)


    # 发送预定Post请求
    city_id = "17"
    abcs = "r1:1:j_id__ctru75pc2:4:j_id__ctru110pc2:17:selectBooleanRadio1"
    agree_rule = "t"
    event = "r1:1:traid1"
    data = {"r1:1:healthCityId": city_id, "abcs": abcs, "r1:1:agreeRuleId": agree_rule, "event": event,
            "org.apache.myfaces.trinidad.faces.FORM": "f1", "javax.faces.ViewState": "!c18ht3qe8"}
    req = requests.post("http://hr-welcometo.huawei.com/wcaportal/faces/home?_adf.ctrl-state=h7agz751t_4",
                        cookies=req.cookies, data=data)
    print(req.text)


# Login by selenium
def login2():
    opt = webdriver.ChromeOptions()
    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")

    driver = webdriver.Chrome("/Users/hyson/Downloads/chromedriver")
    driver.get("http://hr-welcometo.huawei.com/wcaportal")
    driver.find_element_by_name("uid").send_keys("hyson1996@163.com")
    driver.find_element_by_name("password").send_keys("h1s_wantto10ve")
    driver.find_element_by_class_name("login_submit_pwd").click()

    cookies = driver.get_cookies()

    for c in cookies:
        driver.add_cookie(c)

    driver.refresh()
    time.sleep(3)
    driver.find_element_by_id("cil3").click()
    time.sleep(3)
    driver.find_element_by_id("r1:1:cb3").click()

    flag = True

    cnt = 0

    while flag:
        time.sleep(3)
        try:
            driver.refresh()
        except selenium.common.exceptions.TimeoutException:
            driver.refresh()

        # Process page source with BeautifulSoup
        page_source = driver.page_source
        bs_obj = BeautifulSoup(page_source, features="html.parser")

        all_jul_item = bs_obj.find_all(text=re.compile(u"[1-9]+ Jul"))

        cnt = cnt + 1
        print("正在进行第" + str(cnt) + "次预约入职")

        for item in all_jul_item:
            date = item.parent.get_text().split('\n')[0]

            status = item.parent.attrs["class"][0]

            button_id = item.parent.attrs["id"]

            if status == "blue":
                driver.find_element_by_id(button_id).click()
                time.sleep(3)
                driver.find_element_by_id("r1:0:agreeRuleId::content").click() #TODO:查询按钮状态，是False才点击
                time.sleep(3)
                driver.find_element_by_id("r1:0:traid1").click()
                time.sleep(5)
                print(date + "可预约入职，已预约")
                flag = False
                break
            elif status == "gray":
                print(date + "暂时不可预约")



if __name__ == '__main__':
    login2()