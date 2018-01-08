#coding=utf-8
####定义单例的日志logger模块

import  logging
import logging.config
class logControl:
	logging.config.fileConfig(r"conf/logger.conf")
	##create logger
	def getLogger(self):
		logger = logging.getLogger('run')
		return logger