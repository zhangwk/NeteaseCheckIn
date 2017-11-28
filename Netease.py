from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import chr
from builtins import int
from builtins import map
from builtins import open
from builtins import pow
from builtins import range
from builtins import str

from future import standard_library

standard_library.install_aliases()

import re
import os
import json
import time
import hashlib
import base64
import binascii

from Crypto.Cipher import AES
from http.cookiejar import LWPCookieJar

import requests

from storage import Storage

import logger

default_timeout = 10

log = logger.getLogger(__name__)

modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


def createSecretKey(size):
	return binascii.hexlify(os.urandom(size))[:16]


def encrypted_request(text):
	text = json.dumps(text)
	secKey = createSecretKey(16)
	encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
	encSecKey = rsaEncrypt(secKey, pubKey, modulus)
	data = {'params': encText, 'encSecKey': encSecKey}
	return data


def aesEncrypt(text, secKey):
	pad = 16 - len(text) % 16
	text = text + chr(pad) * pad
	encryptor = AES.new(secKey, 2, '0102030405060708')
	ciphertext = encryptor.encrypt(text)
	ciphertext = base64.b64encode(ciphertext).decode('utf-8')
	return ciphertext


def rsaEncrypt(text, pubKey, modulus):
	text = text[::-1]
	rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
	return format(rs, 'x').zfill(256)


def login(self, username, password):
	pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
	if pattern.match(username):
		return self.phone_login(username, password)
	action = 'https://music.163.com/weapi/login?csrf_token='
	self.session.cookies.load()
	text = {
		'username': username,
		'password': password,
		'rememberLogin': 'true'
	}
	data = encrypted_request(text)
	try:
		return self.httpRequest('Login_POST', action, data)
	except requests.exceptions.RequestException as e:
		log.error(e)
		return {'code': 501}


class NetEase(object):
	def __init__(self):
		self.header = {
			'Accept': '*/*',
			'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Host': 'music.163.com',
			'Referer': 'http://music.163.com/search/',
			'User-Agent':
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
			# NOQA
		}
		self.cookies = {'appver': '1.5.2'}
		self.playlist_class_dict = {}
		self.session = requests.Session()
		self.storage = Storage()
		self.session.cookies = LWPCookieJar(self.storage.cookie_path)
		try:
			self.session.cookies.load()
			cookie = ''
			if os.path.isfile(self.storage.cookie_path):
				self.file = open(self.storage.cookie_path, 'r')
				cookie = self.file.read()
				self.file.close()
			expire_time = re.compile(r'\d{4}-\d{2}-\d{2}').findall(cookie)
			if expire_time:
				if expire_time[0] < time.strftime('%Y-%m-%d', time.localtime(time.time())):
					self.storage.database['user'] = {
						'username': '',
						'password': '',
						'user_id': '',
						'nickname': '',
					}
					self.storage.save()
					os.remove(self.storage.cookie_path)
		except IOError as e:
			log.error(e)
			self.session.cookies.save()
		# 登录

	def httpRequest(self,
	                method,
	                action,
	                query=None,
	                urlencoded=None,
	                callback=None,
	                timeout=None):

		connection = json.loads(
			self.rawHttpRequest(method, action, query, urlencoded, callback, timeout)
		)

		return connection

	def rawHttpRequest(self,
	                   method,
	                   action,
	                   query=None,
	                   urlencoded=None,
	                   callback=None,
	                   timeout=None):
		if method == 'GET':
			url = action if query is None else action + '?' + query
			connection = self.session.get(url,
			                              headers=self.header,
			                              timeout=default_timeout)

		elif method == 'POST':
			connection = self.session.post(action,
			                               data=query,
			                               headers=self.header,
			                               timeout=default_timeout)

		elif method == 'Login_POST':
			connection = self.session.post(action,
			                               data=query,
			                               headers=self.header,
			                               timeout=default_timeout)
			self.session.cookies.save()
		connection.encoding = 'utf-8'
		print(connection.text)
		return connection.text

	# if connection.status_code==200:





	# 手机登录

	def phone_login(self, username, password):

		action = 'https://music.163.com/weapi/login/cellphone'

		mpassword = hashlib.md5(password.encode()).hexdigest()

		text = {
			'phone': username,
			'password': mpassword,
			'rememberLogin': 'true'
		}

		data = encrypted_request(text)
		try:
			return self.httpRequest('Login_POST', action, data)

		except requests.exceptions.RequestException as e:
			log.error(e)
		return {'code': 501}

	# 每日签到


	def daily_signin(self, type):
		action = 'http://music.163.com/weapi/point/dailyTask'
		text = {'type': type}
		data = encrypted_request(text)
		try:
			return self.httpRequest('POST', action, data)
		except requests.exceptions.RequestException as e:
			log.error(e)
			return -1

	def writeToFile(self, data):
		with open(('qiandaoRecord' + '.txt'), 'a', encoding='utf-8') as file:
			file.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + str(data) + '\n')


ne = NetEase()
ne.phone_login('yourPhoneNum','password' )
time.sleep(1)
# mobilesignin = \
mobilesignin = ne.daily_signin(0)
if mobilesignin != -1 and mobilesignin['code'] not in (-2, 301):
	print('移动端签到成功')
	ne.writeToFile('移动端签到成功')
else:
	print('移动签到失败')
	ne.writeToFile('移动签到失败')
time.sleep(1)
pcsignin = ne.daily_signin(1)
if pcsignin != -1 and pcsignin['code'] not in (-2, 301):
	print('PC端签到成功')
	ne.writeToFile('PC端签到成功')
else:
	print('PC签到失败')
	ne.writeToFile('PC端签到失败')
