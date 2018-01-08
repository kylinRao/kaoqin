#coding=utf-8
import re,os
from selenium import webdriver
import cookielib,urllib2,urllib
#from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.keys import Keys  #需要引入keys包
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
import time
import unittest
from logControl import logControl
import logging
import sys
import configParseControl
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
	#pageNum = 1
	#downCount = 0
	
	#global path_js
	#global loginUrl
	
	logger = logControl().getLogger()
	##phatomjsSreenShotDir = configParseControl.globalParam.phatomjsSreenShotDir


	def __init__(self,name,password,MAXDOWN ):
		self.name=name
		self.password = password
		self.MAXDOWN = int(MAXDOWN)

	def make_cookie(self,domain,name, value): 
		self.logger.debug("make_cookie working:domain:{domain},name:{name},value:{value}".format(domain=domain,name=name,value=value))
		return cookielib.Cookie(
			version=0,
			# domain=domain,
			domain = ".chinasoftosg.com",
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
		global allowco
		global goodCookie
		#登陆，创造cookie
		self.logger.info("输入账号和密码，进行登录操作")
		driver=webdriver.PhantomJS(path_js,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
		# driver=webdriver.Firefox()
		driver.get(loginUrl)
		driver.maximize_window()
		time.sleep(1)




		driver.get_screenshot_as_file(os.path.join(configParseControl.globalParam.phatomjsSreenShotDir,ur'登陆前.png'))
		driver.find_element_by_xpath('//*/input[@name="userName"]').send_keys(self.name)
		driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
		driver.find_element_by_xpath('//*[@onclick="return submitForm(false,false)"]').click()
		time.sleep(3)
		driver.get_screenshot_as_file(os.path.join(configParseControl.globalParam.phatomjsSreenShotDir,ur'登陆后.png'))

		self.logCookie(driver)
		goodCookie = driver.get_cookies()

        #
		# self.logger.info("点击id=op进入新OA页面")
		# driver.find_element_by_xpath('//*[@id="OP"]/a').click()
        #
        #
		# goodCookie = self.getRecentSignInDate(driver)
		# time.sleep(3)
        #
        #
		# phCookieList = driver.get_cookies()
		# self.logCookie(driver)
        #
		# self.logger.info("phCookieList is:")
		# for i in phCookieList:
		# 	self.logger.info(type(i))
		# 	self.logger.info(i)
		# 	for c in i:
		# 		self.logger.info(i['name'],i['value'])
        #
		# driverG = driver


		return goodCookie
	def logCookie(self,driver):
		for ck in driver.get_cookies():
			if ck["domain"]:
				self.logger.debug("【domain】:{domain}--【name】:{name}--【value】:{value}".format(domain=ck["domain"],name=ck["name"],value=ck["value"]))
	def getRecentSignInDate(self,driver):
		time.sleep(4)
		for handle in driver.window_handles:

			driver.switch_to.window(handle)
			self.logger.debug("当前handler的driver的cookie")
			self.logCookie(driver)
		driver.maximize_window()

		goodCookie  =  driver.get_cookies()



		driver.get_screenshot_as_file(os.path.join(configParseControl.globalParam.phatomjsSreenShotDir,ur'OP.png'))
		#print "考勤"
		self.logger.info("进入考勤iframe")
		driver.find_element_by_xpath('//*[@menuname="考勤"]').click()
		time.sleep(10)
		driver.get_screenshot_as_file(os.path.join(configParseControl.globalParam.phatomjsSreenShotDir,ur'考勤.png'))
		self.logCookie(driver)


		self.logger.info("进入考勤页面时的phCookieList is:")


		for handle in driver.window_handles:
			driver.switch_to.window(handle)
		driver.maximize_window()
		driver.switch_to.frame(2)
		#print "年假"
		self.logger.info("进入年假TAB，并提供当前年假信息")
		driver.find_element_by_xpath('//*[@id="accordion1"]/div[2]/a[1]').click()
		time.sleep(10)
		self.logCookie(driver)


		driver.get_screenshot_as_file(os.path.join(configParseControl.globalParam.phatomjsSreenShotDir,ur'年假.png'))
		#print "个人打卡数据"
		self.logger.info("进入个人打卡数据TAB，并记录当前考勤信息")
		driver.find_element_by_xpath('//*[@id="accordion1"]/div[2]/a[2]').click()
		time.sleep(10)
		driver.get_screenshot_as_file(os.path.join(configParseControl.globalParam.phatomjsSreenShotDir,ur'个人打卡数据.png'))
		self.logCookie(driver)

		return goodCookie

	def phCookie2urlcookie(self,phCookieList):
		####获取适用于opener.open()的cookie
		print convert2unicode("phCookie2urlcookie is runing \n")
		urlCookie = cookielib.CookieJar()
		#print type(phCookieList)
		#print phCookieList
		self.logger.info("如下cookie转换中：")
		for cookiedir in phCookieList:

			if (cookiedir.has_key('domain')&cookiedir.has_key('name')&cookiedir.has_key('value')):
				urlCookie.set_cookie(self.make_cookie(cookiedir['domain'],cookiedir['name'],cookiedir['value']))

				#self.logger.info("domain:{domain},name:{name},value:{value}".format(domain=cookiedir['domain'],name=cookiedir['name'],value=cookiedir['value']))

		return urlCookie



	def getPostRes(self, url,urlCookie,data):
		for ck in urlCookie:
			self.logger.debug("post 请求使用到的cookie信息如下：domain:{domain}name:{name},value:{value}".format(domain=ck.domain,name=ck.name,value=ck.value))
		req = urllib2.Request(url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(urlCookie))
		headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
		opener.addheaders = [headers]
		resp = opener.open(req, data).read()
		self.logger.debug("http请求的返回消息：")
		self.logger.debug(resp)
		return None
	def start(self):
		global  driverG
		url = "http://kq.chinasoftosg.com/workAttendance/importsExamineAction_getImportsExamine"
		data = 'importsExamineVo.page=1&importsExamineVo.pagesize=25'
		phCookieList = self.login()
		urlCookie = self.phCookie2urlcookie(goodCookie)
		res = self.getPostRes(url, urlCookie,data)
		print res
if __name__=="__main__":
	account = '68104'#填写电话号码
	password= 'Rql*34704'#填写密码
	k9 = downMusic(account,password,'1000')
	k9.start()