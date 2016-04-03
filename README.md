# Python-SmartisanNotes

Python API Wrapper for http://note.t.tt Service.

利用 Requests、requests_toolbelt 等库模拟浏览器操作，实现[锤子便签网页版](http://note.t.tt)的基本功能。

# 功能介绍

## 基本功能

* 获取便签列表
* 新建便签
* 修改便签
* 生成锤子便签分享图片
* 生成锤子便签分享网页

## 实验性功能

* 便签备份（导出至 JSON 文件）
* 便签恢复（从 JSON 文件导入）

# 代码说明

## Python 版本要求

Python 2.6+（尚未支持 Python 3+）。

## 第三方库支持

* [requests](http://python-requests.org)
* [requests_toolbelt](https://toolbelt.readthedocs.org)
* [simplejson](http://simplejson.readthedocs.org)

## 演示环境

CrunchBang Linux waldorf (Debian GNU/Linux 7.9)

# 使用示例

## 1. 初始化及登录

    from SmartisanNotes import *
    username = 'Your Username'
    password = 'Your Password'
    s = SmartisanNotes(username, password)
    # Print Account Profile
    profile = s.accountProfile()
    print profile

## 2. 获取便签列表

    noteList = s.noteGetList()
    print noteList

## 3. 新建便签

## 4. 修改便签
