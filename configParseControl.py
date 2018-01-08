#coding:utf-8
import ConfigParser  
  
config = ConfigParser.ConfigParser()  
config.read("conf/global.conf")
class globalParam(object):
    phatomjsSreenShotDir = config.get('global', 'phatomjsSreenShotDir')  
