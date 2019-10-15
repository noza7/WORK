from selenium import webdriver
from selenium.webdriver.support.select import Select

# 等待加载模块
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as ec
import selenium.webdriver.support.ui as ui
# from selenium.webdriver.support.wait import WebDriverWait

import time

# 自定义模块
# from work.bk import user_info
# from work.bk import data
from baobukao.lib import user_info
from baobukao.temp import data

start_time = time.time()


# 滚动条移动到底部
def scroll_bottom():
    browser.execute_script("window.scrollBy(0,4800)")


def wait_key():
    while True:
        message = input('核对无误请输入“空格”：')
        if message == ' ':
            break
        print('你输入的是 ' + message + '!')


# 一直等待某元素可见，默认超时10秒
def is_visible(locator, timeout=10):
    try:
        ui.WebDriverWait(browser, timeout).until(ec.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


browser = webdriver.Firefox()
# browser = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox/geckodriver.exe')

# 基本信息
url = 'http://121.28.25.166/StationWeb/pages/common/frameset.jsp'
username = user_info.username
password = user_info.password

try:
    # 获取网页信息，发送数据
    browser.get(url)
    a = is_visible('//*[@id="reset1"]')
    # print(a)

    browser.set_window_size(width=1366, height=600)
    browser.find_element_by_css_selector('#veryCode').click()  # 触发验证码焦点事件
    browser.find_element_by_css_selector(
        '#form1 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)').send_keys(
        username)
    browser.find_element_by_css_selector(
        '#form1 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)').send_keys(
        password)
    login_s = browser.find_element_by_css_selector(
        '#form1 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > select:nth-child(1)')  # 获取教学点选择框
    Select(login_s).select_by_value('1300300')  # 选择“秦皇岛电大直属”
    scroll_bottom()

    # 获取验证码
    # path = 'v-code.png'
    # browser.get_screenshot_as_file(path)  # 获取图片并保存
    verification_code = str(input('输入验证码:'))  # 验证码输入

    # 输入验证码，点击登录
    browser.find_element_by_css_selector('#veryCode').send_keys(verification_code)
    browser.find_element_by_css_selector('input.NormalSubmit:nth-child(1)').click()
    print('-' * 90)
    a = is_visible('/html/frameset/frameset')  # 框架定位需要小心，我加了测试，看等待出现是否定位成功
    if a:
        print('登录成功！')
    else:
        print('登录有问题！')

    a = is_visible('/html/frameset/frameset/frame[1]')
    print(a)
    browser.switch_to.frame('contents')  # 定位框架
    browser.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr/td/a/font').click()
    print('点击“考务”')
    browser.find_element_by_xpath('/html/body/div[2]/div[2]/table/tbody/tr[1]/td/a/font').click()
    print('点击“报考”')

    browser.switch_to.parent_frame()  # 返回父框架
    browser.switch_to.frame('main')  # 定位框架
    browser.switch_to.frame('Bar')  # 定位子框架
    browser.find_element_by_css_selector('.top-navigation > a:nth-child(5) > font:nth-child(1)').click()
    print('点击“单个学生报考”')

    browser.switch_to.parent_frame()  # 返回上一层父框架
    browser.switch_to.frame('Info')
    is_visible('/html/body/form/p/font/a/font')
    print('点击“设定考试定义范围”')
    browser.find_element_by_css_selector(
        '.WelcomeData > font:nth-child(1) > a:nth-child(1) > font:nth-child(1)').click()
    print('选择考试学期')
    s = browser.find_element_by_name('examID')
    Select(s).select_by_value('201902')
    # 默认是专科，本科需要开启下面代码-------------------------------------------------------------
    s = browser.find_element_by_name('examKind')
    # 专
    # Select(s).select_by_value('04')
    # 本
    # Select(s).select_by_value('07')
    print('点击“确定”')
    browser.find_element_by_css_selector('.NormalSubmit').click()
    alert = browser.switch_to.alert
    print('接受弹窗{}'.format(alert.text))
    alert.accept()

    browser.switch_to.parent_frame()
    browser.switch_to.frame('Bar')
    print('点击“单个学生报考”')
    browser.find_element_by_css_selector('.top-navigation > a:nth-child(5) > font:nth-child(1)').click()

    browser.switch_to.parent_frame()
    browser.switch_to.frame('Info')
    for i in range(0, len(data.dict_ls)):  # --------------------------------------------------------
        student_num = list(data.dict_ls[i].keys())[0]
        print('输入学号')
        browser.find_element_by_css_selector(
            '.DataInputTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4) > input:nth-child(1)').clear()  # 清空内容
        browser.find_element_by_css_selector(
            '.DataInputTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4) > input:nth-child(1)').send_keys(
            student_num)
        time.sleep(1)
        browser.find_element_by_css_selector('.NormalSubmit').click()  # 点击“查询”
        time.sleep(1)
        browser.find_element_by_css_selector(
            'table.DataInputTable:nth-child(5) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(10) > a:nth-child(1)').click()  # 点击“规则内报考”
        print('跳入包括选择页面')
        time.sleep(3)
        handles = browser.window_handles  # 获得所有窗口句柄
        browser.switch_to.window(handles[-1])  # 取最新的
        time.sleep(1)

        for id_find in data.dict_ls[i][student_num]:
            def try_id_click(id, num):
                '''
                查找课程id号（因为可能出现没有id号的情况，需要跳过继续）
                :param id: 课程id号
                :param num: 1或2(目前只发现这两种情况)
                :return:
                '''
                try:
                    ele = browser.find_element_by_xpath('//input[@value="{}#0.0#{}"]'.format(id, num))
                except Exception:
                    print('{}不存在！'.format(id))
                    with open('log.txt', 'a+') as f:
                        f.write('学号：{}  课程：{}{}{} 出现问题！\n'.format(student_num, id_find[0], id_find[1], id_find[2]))
                else:
                    ele.click()


            try_id_click(id_find[1], 1)
            try_id_click(id_find[1], 2)

        with open('over_log.txt', 'a+') as f:
            f.write('{}  报考成功！\n'.format(student_num))
        browser.find_element_by_css_selector('body > form:nth-child(1) > p:nth-child(5) > input:nth-child(1)').click()
        try:
            alert = browser.switch_to.alert
            print('接受弹窗{}'.format(alert.text))
            alert.accept()
            scroll_bottom()  # 移动到底部
            # wait_key()
            time.sleep(5)
            browser.close()  # 关闭窗口
        except:
            scroll_bottom()  # 移动到底部
            # wait_key()
            time.sleep(5)
            browser.close()  # 关闭窗口

        browser.switch_to.window(handles[0])

    time.sleep(10)
finally:
    time.sleep(10)
    # 关闭页面
    browser.quit()
    # 测试用时
end_time = time.time()
print('用时：{0}秒'.format(end_time - start_time))
