from selenium import webdriver
from pyvirtualdisplay import Display
 
 
display = Display(visible=0, size=(800,600))
display.start()
driver = webdriver.Chrome("./chromedriver")
driver.get("http://www.baidu.com")
print(driver.page_source)

driver.quit()
display.stop()
