from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import os
import time

chrome_options = Options()
# 无头模式启动，程序实际运行时启用，调试阶段使用有界面的
# chrome_options.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('disable-infobars')
# 初始化实例
driver = webdriver.Chrome(executable_path='/Applications/Development/chromedriver', chrome_options=chrome_options)

# 请求百度
driver.get("http://www.baidu.com")
# 对于查找元素，使用lxml进行xpath查找效率最高
html = etree.HTML(driver.page_source)
title = html.xpath('/html/head/title/text()')[0]
print(title)

# 表单登录
driver.get("https://www.newrank.cn/")
login_button = driver.find_element_by_class_name('new-header-login')
login_button.click()
login_type_switch_button = driver.find_elements_by_class_name('login-normal-tap')[1]
login_type_switch_button.click()
input_username = driver.find_element_by_id("account_input")
input_password = driver.find_element_by_id("password_input")
input_login_button = driver.find_element_by_id("pwd_confirm")
input_username.send_keys('17031456941')
input_password.send_keys('xkk186137')
input_login_button.click()

# 获取cookie
# 有隐式等待和显式等待，不应该使用time.sleep()，有专门的方法检查元素是否已经加载完成
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# driver = webdriver.Firefox()
# driver.get("http://somedomain/url_that_delays_loading")
# try:
#     wait = WebDriverWait(driver, 10)
#     element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
# finally:
#     driver.quit()
time.sleep(5)
token = driver.get_cookie('token')
print(token['value'])

# 必须有这一步，但是也不能保证关闭
driver.close()
os.system("kill -9 `ps -ef | grep chromedriver | awk '{print $2}' | head -n 1`")
