# Python-SmartisanNotes

Python API Wrapper for http://note.t.tt Service.

利用 [Requests](http://python-requests.org) 、[requests_toolbelt](https://toolbelt.readthedocs.org) 等库模拟浏览器，实现[锤子便签网页版](http://note.t.tt)的基本操作。

# 基本功能
* 获取便签列表
* 新建便签
* 修改便签
* 生成锤子便签分享图片
* 生成锤子便签分享网页

# 实验性功能
* 便签备份（导出至 JSON 文件）
* 便签恢复（从 JSON 文件导入）

# 使用示例

## 1. 初始化及登录

    from SmartisanNotes import *
    username = 'Your Username'
    password = 'Your Password'
    s = SmartisanNotes(username, password)
    profile = s.accountProfile()
    print profile

    

## 2. 获取便签列表

    noteList = s.noteGetList()
    print noteList

## 3. 新建便签

## 4. 修改便签
