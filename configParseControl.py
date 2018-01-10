#coding:utf-8
import ConfigParser  
  
config = ConfigParser.ConfigParser()  
config.read("conf/global.conf")
class globalParam(object):
    phatomjsSreenShotDir = config.get('global', 'phatomjsSreenShotDir')
    username = config.get('global', 'username')
    password = config.get('global', 'password')

