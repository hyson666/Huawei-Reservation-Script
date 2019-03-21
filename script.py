from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import argparse

# import requests
import time
import re
import selenium.common.exceptions

cnt = 0
flag = True

# # Login by requests
# def login():
#     # 取得登陆cookies
#     uid = "uid"
#     pwd = "pwd"
#     actionFlag = "loginAuthenticate"
#     lang = "zh_CN"
#     loginFlag = "byUid"
#     login_info = {"uid": uid, "password": pwd, "actionFlag": actionFlag, "lang": lang, "loginFlag": loginFlag}
#
#     website = "https://uniportal.huawei.com/uniportal/login.do"
#
#     req = requests.post(website, data=login_info)
#
#
#     # 发送预定Post请求
#     city_id = "17"
#     abcs = "r1:1:j_id__ctru75pc2:4:j_id__ctru110pc2:17:selectBooleanRadio1"
#     agree_rule = "t"
#     event = "r1:1:traid1"
#     data = {"r1:1:healthCityId": city_id, "abcs": abcs, "r1:1:agreeRuleId": agree_rule, "event": event,
#             "org.apache.myfaces.trinidad.faces.FORM": "f1", "javax.faces.ViewState": "!c18ht3qe8"}
#     req = requests.post("http://hr-welcometo.huawei.com/wcaportal/faces/home?_adf.ctrl-state=h7agz751t_4",
#                         cookies=req.cookies, data=data)
#     print(req.text)


# Login by selenium
def login2(args):
    global cnt
    global flag

    chrome_options = Options()
    chrome_options.add_argument('window-size=1920x3000')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome("./chromedriver", options=chrome_options)
    driver.get("http://hr-welcometo.huawei.com/wcaportal")
    driver.find_element_by_name("uid").send_keys(args.id)
    driver.find_element_by_name("password").send_keys(args.pwd)
    driver.find_element_by_class_name("login_submit_pwd").click()

    cookies = driver.get_cookies()

    for c in cookies:
        driver.add_cookie(c)

    driver.refresh()
    time.sleep(3)
    driver.find_element_by_id("cil3").click()
    time.sleep(3)
    driver.find_element_by_id("r1:1:cb3").click()
    time.sleep(3)

    while flag:
        try:
            driver.refresh()
            time.sleep(3)
            # Process page source with BeautifulSoup
            page_source = driver.page_source
            bs_obj = BeautifulSoup(page_source, features="html.parser")
        except selenium.common.exceptions.TimeoutException:
            return

        re_key = u"[1-9] " + args.mon
        all_jul_item = bs_obj.find_all(text=re.compile(re_key))

        cnt = cnt + 1
        print("正在进行第" + str(cnt) + "次预约入职")

        for item in all_jul_item:
            date = item.parent.get_text().split('\n')[0]

            status = item.parent.attrs["class"][0]

            button_id = item.parent.attrs["id"]

            if status == "blue":
                driver.find_element_by_id(button_id).click()
                time.sleep(3)
                driver.find_element_by_id("r1:0:agreeRuleId::content").click()
                time.sleep(3)
                driver.find_element_by_id("r1:0:traid1").click()
                time.sleep(5)
                print(date + "可预约入职，已预约")
                flag = False
                break
            elif status == "gray":
                print(date + "暂时不可预约")


if __name__ == '__main__':
    parse = argparse.ArgumentParser(prog="reservation script", description="Huawei reservation script by Hyson")
    parse.add_argument('--id', type=str, required=True, help='Input your user id.')
    parse.add_argument('--pwd', type=str, required=True, help='Input your password')
    parse.add_argument('--mon', type=str, required=True, help='Input your intended reservation month',
                       choices=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Sep', 'Aug', 'Oct', 'Nov', 'Dec'])
    args = parse.parse_args()
    while flag:
        login2(args)
