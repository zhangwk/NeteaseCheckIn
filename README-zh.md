# NeteaseCheckIn

仅用于网易云音乐 手机端与PC端签到

感谢 [musicbox](https://github.com/darknessomi/musicbox)
 
[English](https://github.com/zhangwk/NeteaseCheckIn/blob/master/README.md)  
=========================

需求
------------
* Python  
* git


安装
------------
```
git clone git@github.com:zhangwk/NeteaseCheckIn.git NeteaseCheckIn
```
定制
--------

* 填你的账号
```python
   cd NeteaseCheckIn
   vim Netease.py
   
   ne.phone_login(
   12345678910,     =>手机号码
   'yourpassword'   =>对应的密码
   )
```
下一步
----------
添加邮箱登陆，忘了，忘了

讨论
----------
- [submit issue](https://github.com/zhangwk/NeteaseCheckIn/issues/new)
- email: zwk.wilson@foxmail.com


还有
--------
如果在IDE中运行，你应该能看到所缺少的库。  
此py在我的云服务器上运行正常，CentOs 7.  
配合定时任务（Crontab）运行，每天自动签到。

