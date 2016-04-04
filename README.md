# Python-SmartisanNotes

Python API Wrapper for http://note.t.tt Service.

利用 Requests、requests_toolbelt 等库模拟浏览器操作，实现[锤子便签网页版](http://note.t.tt)的基本功能。


# 功能介绍

### 基本功能

* 获取便签列表
* 新建便签
* 修改便签
* 删除便签
* 生成锤子便签分享图片
* 生成锤子便签分享网页


### 实验性功能

* 便签备份（导出至 JSON 文件）
* 便签恢复（从 JSON 文件导入）

# 代码说明

### Python 版本要求

Python 2.6 以上版本。

### 第三方库支持

* [requests](http://python-requests.org)
* [requests_toolbelt](https://toolbelt.readthedocs.org)
* [simplejson](http://simplejson.readthedocs.org)

### 演示环境

CrunchBang Linux waldorf (Debian GNU/Linux 7.9)

# 应用示例

### 1. 初始化及登录

```python
from SmartisanNotes import *
username = 'Your Username'
password = 'Your Password'
s = SmartisanNotes(username, password)
# View Account Profile
profile = s.accountProfile()
print profile
```

### 2. 获取便签列表

```python
noteList = s.noteGetList()
print noteList
```

### 3. 新建便签

#### 1) 新建文本便签（支持部分 [Markdown](https://cloud.smartisan.com/apps/note/md.html) 语法）
```python
# noteCreate(detail, [mkd='0', fav='0', note2Img='0'])
# mkd='1' 开启 markdown 功能；fav='1' 添加为收藏；
# note2Img='1' 生成分享图片（返回 URL），同时保存至本地

text = 'Hello, World!\n via Python'
note = s.noteCreate(detail=text, fav='1')
```

![](http://7xslb5.com1.z0.glb.clouddn.com/Python-SmartisanNotes-Demo-01.jpg)

```python
text = '> Hello, World!\n via Python'
note = s.noteCreate(detail=text, mkd='1', note2Img='1')
```

![](http://7xslb5.com1.z0.glb.clouddn.com/Python-SmartisanNotes-Demo-02.jpg)

#### 2）新建图文便签

```python
# imageUpload(imageFile, [describe='', text='', mkd='0', fav='0', note2Img='0'])
# 支持上传本地图片及在线图片，支持 jpeg、png 格式，文件大小不超过 5 MB
# describe 为图片描述，纯 ASCII 字符限 30 字，纯 UTF-8 字符限 15 字，超出将被裁剪

note = s.imageUpload('Octocat.jpg')
```

![](http://7xslb5.com1.z0.glb.clouddn.com/Python-SmartisanNotes-Demo-03.jpg)

```python
imageFile = 'http://image.wufazhuce.com/Fh7OzcpPtSnfC4s60p07sEdvjIzg'
describe = '基因乐趣&人畺 作品'
text = '没人可以永远的活在青春里，但还好，如若有心，我们能见证一代又一代的年轻。这种见证，也便成了一种参与。 by 自由极光\n\n[「ONE · 一个」 VOL.1161]'
s.imageUpload(imageFile, describe=describe, text=text, mkd='1', note2Img='1')
```

![](http://7xslb5.com1.z0.glb.clouddn.com/Python-SmartisanNotes-Demo-04.jpg)

### 4. 修改便签
