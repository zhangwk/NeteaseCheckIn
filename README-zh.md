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

* Configure account
```python
   cd NeteaseCheckIn
   vim Netease.py
   
   ne.phone_login(
   12345678910,     =>Your phoneNumber
   'yourpassword'   =>Your password
   )
```
讨论
----------
- [submit issue](https://github.com/zhangwk/NeteaseCheckIn/issues/new)
- email: zwk.wilson@foxmail.com


还有
--------
如果在IDE中运行，你应该能看到所缺少的库。
此py在我的云服务器上运行正常，CentOs 7.
使用定时任务运行，Crontab，每天签到。

