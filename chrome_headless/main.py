from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# 截图
driver.save_screenshot('screenshot.png')

# 滑动验证码
driver.get("https://www.jd.com/")
login_button = driver.find_element_by_class_name('link-login')
login_button.click()
login_type_switch_button = driver.find_element_by_class_name('login-tab-r')
login_type_switch_button.click()
input_username = driver.find_element_by_id("loginname")
input_password = driver.find_element_by_id("nloginpwd")
input_login_button = driver.find_element_by_class_name("login-btn")
input_username.send_keys('username')
input_password.send_keys('password')
input_login_button.click()
# 滑动验证码验证过程
wait = WebDriverWait(driver, 10)
slide_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'JDJRV-slide-btn')))     # 滑块按钮
while True:
    action = ActionChains(driver)            # 实例化一个action对象
    action.click_and_hold(slide_button).perform()  # perform()用来执行ActionChains中存储的行为
    action.reset_actions()
    action.move_by_offset(30, 0).perform()
    action.release().perform()
    time.sleep(0.5)  #等待跳转完成
    # 验证登录是否成功
    print(driver.title)
    if str(driver.title) == '京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！':
        print('滑块验证通过')
        break
    else:
        print('滑块验证失败，重试中')

time.sleep(10)
# 必须有这一步，但是也不能保证关闭
driver.close()
os.system("kill -9 `ps -ef | grep chromedriver | awk '{print $2}' | head -n 1`")
