#coding=utf-8
import re,os
from selenium import webdriver
import cookielib,urllib2,urllib
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.keys import Keys  #需要引入keys包
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
import time
import unittest
##import testCases

js = '''
$.ajax({
  type: 'POST',
  url: "http://kq.chinasoftosg.com/workAttendance/importsExamineAction_getImportsExamine",
  data: "importsExamineVo.page=1&importsExamineVo.pagesize=25",

  dataType: "json"
});
'''
global loginUrl
loginUrl= r'http://ics.chinasoftosg.com/SignOnServlet'
global path_js

path_js = os.path.join(os.path.dirname(__file__),"phantomjs","bin","phantomjs.exe")

global storeDir
def convert2unicode(inputS):
    #input 可以是str，可以是unicode
    if isinstance(inputS,unicode):
        return inputS
    if isinstance(inputS,str):
        return inputS.decode('utf-8')
class downMusic:
    pageNum = 1
    downCount = 0
    global path_js
    global loginUrl


    def __init__(self,name,password,MAXDOWN ):
        self.name=name
        self.password = password
        self.MAXDOWN = int(MAXDOWN)

    def make_cookie(self,domain,name, value):
        return cookielib.Cookie(
            version=0,
            domain=domain,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
            )
    def login(self):
        #登陆，创造cookie
        print "登陆"
        driver=webdriver.PhantomJS(path_js,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        # driver=webdriver.Firefox()
        driver.get(loginUrl)
        driver.maximize_window()
        time.sleep(1)
        driver.get_screenshot_as_file(ur'登陆前.png')
        driver.find_element_by_xpath('//*/input[@name="userName"]').send_keys(self.name)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@onclick="return submitForm(false,false)"]').click()
        time.sleep(3)
        driver.get_screenshot_as_file(ur'登陆后.png')
        print "id=OP"
        driver.find_element_by_xpath('//*[@id="OP"]/a').click()
        self.getRecentSignInDate(driver)
        time.sleep(3)
        phCookieList = driver.get_cookies()

        driverG = driver


        return phCookieList
    def getRecentSignInDate(self,driver):
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
        driver.maximize_window()
        driver.get_screenshot_as_file(ur'OP.png')
        print "考勤"
        driver.find_element_by_xpath('//*[@menuname="考勤"]').click()
        time.sleep(10)
        driver.get_screenshot_as_file(ur'考勤.png')

        for handle in driver.window_handles:
            driver.switch_to.window(handle)
        driver.maximize_window()
        driver.switch_to.frame(2)
        print "年假"
        driver.find_element_by_xpath('//*[@id="accordion1"]/div[2]/a[1]').click()
        time.sleep(10)
        driver.get_screenshot_as_file(ur'年假.png')
        print "个人打卡数据"
        driver.find_element_by_xpath('//*[@id="accordion1"]/div[2]/a[2]').click()
        time.sleep(10)
        driver.get_screenshot_as_file(ur'个人打卡数据.png')

    def phCookie2urlcookie(self,phCookieList):
        ####获取适用于opener.open()的cookie
        print convert2unicode("phCookie2urlcookie is runing \n")
        urlCookie = cookielib.CookieJar()
        print type(phCookieList)
        print phCookieList
        for cookiedir in phCookieList:
            if (cookiedir.has_key('domain')&cookiedir.has_key('name')&cookiedir.has_key('value')):
                urlCookie.set_cookie(self.make_cookie(cookiedir['domain'],cookiedir['name'],cookiedir['value']))
        print urlCookie
        print "this is cookie"
        for i in urlCookie:
            print i
        return urlCookie



    def getPostRes(self, url,urlCookie,data):
        req = urllib2.Request(url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(urlCookie))
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener.addheaders = [headers]
        resp = opener.open(req, data).read()
        print resp
        return None
    def start(self):
        global  driverG
        url = "http://kq.chinasoftosg.com/workAttendance/importsExamineAction_getImportsExamine"
        data = 'importsExamineVo.page=1&importsExamineVo.pagesize=25'
        phCookieList = self.login()
        urlCookie = self.phCookie2urlcookie(phCookieList)
        res = self.getPostRes(url, urlCookie,data)
        print res
if __name__=="__main__":
    account = 'zhanghao'#填写电话号码
    password= 'mima'#填写密码
    k9 = downMusic(account,password,'1000')
    k9.start()




