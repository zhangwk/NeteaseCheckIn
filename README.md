# NeteaseCheckIn

only for Netease check in  (including PC,mobilephone site)  

Thanks to [musicbox](https://github.com/darknessomi/musicbox)
 
[中文说明](https://github.com/zhangwk/NeteaseCheckIn/blob/master/README-zh.md)  
=========================

Requirements
------------
* Python  
* git


Installation
------------
```
git clone git@github.com:zhangwk/NeteaseCheckIn.git NeteaseCheckIn
```
Custom
--------

* Configure account
```python
   cd NeteaseCheckIn
   vim config.py
   
   def getuser():
	      return "12300001111"  # phone number    '12300001111' change it to your PhoneNumber
 

   def getPassword():
	      return "password"  # password     'password' change it to your Password 
```
Discussing
----------
- [submit issue](https://github.com/zhangwk/NeteaseCheckIn/issues/new)
- email: zwk.wilson@foxmail.com

Next Plan
----------
* Nope.

Plus
--------
* You probably will facing some 'encoding format error' in different OS.

* if you missing some library,install it.(google,baidu,whatever helps)

* it works fine on my CentOS ECS of aliyun,so enjoy it!

