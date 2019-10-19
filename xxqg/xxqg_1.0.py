# -*- coding: utf8 -*-

# -*- coding: utf8 -*-

import requests
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36')
options.add_argument('--no-sandbox')
options.add_argument('disable-infobars')
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])

browser = webdriver.Chrome()
browser.implicitly_wait(60)
browser.maximize_window()

HOME_PAGE = 'https://www.xuexi.cn/'  # 学习强国官方url
LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'  # 登录url
VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html?pageNumber=39'  # 视频url
VIDEO_LINK2 = 'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html#11c4o0tv7nb-5'  # 视频url
# LONG_VIDEO_LINK = 'https://www.xuexi.cn/f65dae4a57fe21fcc36f3506d660891c/b2e5aa79be613aed1f01d261c4a2ae17.html'  # 30分钟以上视频url
# LONG_VIDEO_LINK2 = 'https://www.xuexi.cn/0040db2a403b0b9303a68b9ae5a4cca0/b2e5aa79be613aed1f01d261c4a2ae17.html'  # 备用连接
TEST_VIDEO_LINK = 'https://www.xuexi.cn/8e35a343fca20ee32c79d67e35dfca90/7f9f27c65e84e71e1b7189b7132b4710.html'  # 短视频连接

ARTICLES_LINK = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'
SCORES_LINK = 'https://pc.xuexi.cn/points/my-points.html'  # 分数url


# 等待提示
def wait_key():
    while True:
        message = input('请输入“空格键”继续：')
        if message == ' ':
            break
        print('你输入的是 ' + message + '!')


def login():
    """模拟登录"""
    browser.get(LOGIN_LINK)
    # browser.maximize_window()
    browser.execute_script("var q=document.documentElement.scrollTop=1000")
    # time.sleep(10)
    wait_key()
    browser.get(HOME_PAGE)
    print("模拟登录完毕\n")


def watch_videos():
    """观看视频"""
    browser.get(VIDEO_LINK)
    # xpath_pat = '//*[@id="root"]/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[%d]/div[1]/div/div/div[1]/span'
    xpath_pat = '//*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[%d]/div[%d]/div/div/div[1]/span'
               # //*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[1]/div[2]/div/div/div[1]/span
               # //*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[2]/div[1]/div/div/div[1]/span
               # //*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[1]/div[1]/div/div/div[1]/span
    # //*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[3]/div[1]/div/div/div[1]/span
    #
    #
    #
    # //*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[2]/div[2]/div/div/div[1]/span
    spend_time = 0

    for i in range(1, 4):
        for j in range(1, 3):
            video = browser.find_elements_by_xpath(xpath_pat % (i, j))[0]
            # if i > 6:
            #     break
            video.click()
            all_handles = browser.window_handles
            browser.switch_to.window(all_handles[-1])
            browser.get(browser.current_url)

            # 点击播放
            browser.find_element_by_xpath("//div[@class='outter']").click()
            # 获取视频时长
            video_duration_str = browser.find_element_by_xpath("//span[@class='duration']").get_attribute('innerText')
            video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])
            # 保持学习，直到视频结束
            time.sleep(video_duration + 3)
            spend_time += video_duration + 3
            browser.close()
            browser.switch_to.window(all_handles[0])

    browser.get(TEST_VIDEO_LINK)
    time.sleep(3010 - spend_time)
    print("播放视频完毕\n")


def watch_videos2():
    """观看视频"""
    browser.get(VIDEO_LINK2)
    tab = browser.find_element_by_xpath('//*[@id="0454"]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div')
    tab.click()

    xpath_pat = '//*[@id="1koo357ronk-5"]/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[%d]/div[%d]/section/div/div/div/div/div[1]/div/div/div'
    spend_time = 0

    for i in range(1, 6):
        for j in range(1, 5):
            try:
                video = browser.find_elements_by_xpath(xpath_pat % (i, j))[0]

                video.click()
                all_handles = browser.window_handles
                browser.switch_to.window(all_handles[-1])
                browser.get(browser.current_url)

                # 点击播放
                browser.find_element_by_xpath("//div[@class='outter']").click()
                # 获取视频时长
                video_duration_str = browser.find_element_by_xpath("//span[@class='duration']").get_attribute(
                    'innerText')
                video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])
                # 保持学习，直到视频结束
                time.sleep(video_duration + 3)
                spend_time += video_duration + 3
                browser.close()
                browser.switch_to.window(all_handles[0])
            except Exception:
                print(i, j)

        browser.get(TEST_VIDEO_LINK)
        time.sleep(3010 - spend_time)
        print("播放视频完毕\n")


def read_articles():
    """阅读文章"""
    browser.get(ARTICLES_LINK)
    # articles = browser.find_elements_by_xpath(
    #     '//*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/section/div/div/div[1]/div')
    for index in range(7):
        article = browser.find_element_by_xpath(
            '//*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/section/div/div/div[1]/div/div[{}]/div/div/div[1]/span'.format(
                index + 1))
        try:
            if index > 20:
                break
            article.click()
            all_handles = browser.window_handles
            browser.switch_to.window(all_handles[-1])
            browser.get(browser.current_url)
            for i in range(0, 2000, 100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                browser.execute_script(js_code)
                time.sleep(10)
            for i in range(2000, 0, -100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                browser.execute_script(js_code)
                time.sleep(10)
            time.sleep(80)
            browser.close()
            browser.switch_to.window(all_handles[0])
        except Exception:
            print(index)
    print("阅读文章完毕\n")


def get_scores():
    """获取当前积分"""
    browser.get(SCORES_LINK)
    time.sleep(2)
    gross_score = browser.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]") \
        .get_attribute('innerText')
    today_score = browser.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')
    print("当前总积分：" + str(gross_score))
    print("今日积分：" + str(today_score))
    print("获取积分完毕，即将退出\n")


login()
read_articles()
watch_videos()
watch_videos2()
get_scores()
browser.quit()
