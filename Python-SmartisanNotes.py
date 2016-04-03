#!/usr/bin/env python
# -*- coding: UTF-8 -*
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import requests
import simplejson as json
from uuid import uuid4
from base64 import b64encode
from time import time, localtime, strftime
import re
import imghdr
from requests_toolbelt import MultipartEncoder
import codecs


class SmartisanNotes(object):
    def __init__(self, username, password):
        super(SmartisanNotes, self).__init__()
        self.session = requests.Session()
        self.uid = str(self.accountLogin(username, password)['uid'])
        self.tabId = b64encode(uuid4().hex)[:8]
        self.markdown = str(self.noteGetList()['setting']['markdown'])

    def accountLogin(self, username, password):
        url = 'https://account.smartisan.com/v2/session/?m=post'
        headers = {
            'Host': 'account.smartisan.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://account.smartisan.com/'
        }
        self.session.headers.update(headers)
        formData = {
            'username': username,
            'password': password,
            'extended_login': '1'
        }
        response = self.session.post(url, data=formData, timeout=60)
        try:
            content = json.loads(response.content)
        except:
            print 'Unknown Error: (%s) %s Try again.' % (response.status_code, response.text)
            sys.exit(0)
        errno = str(content.get('errno'))
        if errno != '0':
            errorMap = {'0': 'OK', '1': 'SYSTEM_MAINTENANCE', '2': 'LOGIC_ERROR', '3': 'FS_READ_ERROR', '4': 'FS_WRITE_ERROR', '5': 'DB_CONNECT_ERROR', '6': 'DB_QUERY_ERROR', '7': 'CACHE_CONNECT_ERROR', '8': 'CACHE_QUERY_ERROR', '1002': 'PARAMETER_ERROR', '1601': 'ILLEGAL_TICKET', '1602': 'INVALID_TICKET', '1101': 'ILLEGAL_UID', '1102': 'ILLEGAL_PASSWORD', '1103': 'ILLEGAL_AVATAR', '1104': 'ILLEGAL_SECQUES', '1105': 'ILLEGAL_SECANS', '1106': 'INVALID_UID', '1107': 'INVALID_PASSWORD', '1108': 'INVALID_SECANS', '1109': 'ALIAS_REQUIRED', '1110': 'PASSWORD_REQUIRED', '1201': 'ILLEGAL_ALIAS', '1202': 'INVALID_ALIAS', '1203': 'REGISTERED_ALIAS', '1204': 'ILLEGAL_CELLPHONE', '1205': 'INVALID_CELLPHONE', '1206': 'REGISTERED_CELLPHONE', '1207': 'ILLEGAL_EMAIL', '1208': 'INVALID_EMAIL', '1209': 'REGISTERED_EMAIL', '1210': 'INVALID_NICKNAME', '1211': 'UNREGISTERED_NICKNAME', '1212': 'REGISTERED_NICKNAME', '1213': 'ILLEGAL_NICKNAME', '1301': 'ILLEGAL_VCODE', '1302': 'INVALID_VCODE', '1304': 'VCODE_TOO_OFTEN', '1502': 'CAPTCHA_REQUIRED', '1401': 'ILLEGAL_TOKEN', '1402': 'INVALID_TOKEN', '1701': 'UNAUTHORIZED', '1303': 'REFRECH_VCODE', '1501': 'FAILED_LOGIN_LIMIT'}
            print 'Error %s: %s. Try again.' % (errno, errorMap[errno])
            sys.exit(0)
        headers = {
            'Host': 'cloud.smartisan.com',
            'Referer': 'https://cloud.smartisan.com/apps/note/'
        }
        self.session.headers.update(headers)
        respData = content['data']
        # return dict
        return respData

    def checkResponse(self, response):
        try:
            content = json.loads(response.content)
        except:
            print 'Unknown Error: (%s) %s Try again.' % (response.status_code, response.text)
            sys.exit(0)
        code = str(content['code'])
        if code == '1':
            for k, v in content['errInfo'].items():
                print 'Error %s: %s. Try again.' % (k, v)
            sys.exit(0)
        return

    def accountProfile(self):
        url = 'https://cloud.smartisan.com/index.php?r=account/login'
        response = self.session.post(url, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        # return dict
        return respData

    def noteGetList(self):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/getList'
        response = self.session.get(url, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        # return dict
        return respData

    def markdownToggle(self, mkd='1'):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/setting'
        formData = {
            'markdown': mkd
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        if str(respData['markdown']) == '1':
            self.markdown = '1'
        else:
            self.markdown = '0'
        # return dict
        return respData

    def noteCreate(self, detail, mkd='0', fav='0', note2Img='0'):
        if (mkd == '1') and (self.markdown == '0'):
            self.markdownToggle(mkd='1')
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/create'
        formData = {
            'detail': detail,
            'markdown': mkd,
            'favorite': fav,
            'tab_id': self.tabId
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        if note2Img == '1':
            syncId = respData['note']['sync_id']
            noteImage = self.note2Image(syncId)
            # return dicts
            return respData, noteImage
        # return dict
        return respData

    def noteUpdate(self, syncId, detail, mkd='0', fav='0', note2Img='0'):
        if (mkd == '1') and (self.markdown == '0'):
            self.markdownToggle(mkd='1')
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/update'
        formData = {
            'sync_id': syncId,
            'detail': detail,
            'markdown': mkd,
            'favorite': fav,
            'tab_id': self.tabId,
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        if note2Img == '1':
            syncId = respData['note']['sync_id']
            noteImage = self.note2Image(syncId)
            # return dicts
            return respData, noteImage
        # return dict
        return respData

    def noteUpdateFav(self, syncId, fav='1', note2Img='0'):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/updateFav'
        formData = {
            'sync_id': syncId,
            'favorite': fav,
            'tab_id': self.tabId,
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        if note2Img == '1':
            syncId = respData['note']['sync_id']
            noteImage = self.note2Image(syncId)
            # return dicts
            return respData, noteImage
        # return dict
        return respData

    def noteUpdateMarkdown(self, syncId, mkd='1', note2Img='0'):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/updateMarkdown'
        formData = {
            'sync_id': syncId,
            'markdown': mkd,
            'tab_id': self.tabId,
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        if note2Img == '1':
            syncId = respData['note']['sync_id']
            noteImage = self.note2Image(syncId)
            # return dicts
            return respData, noteImage
        # return dict
        return respData

    def genChunks(self, srcData, blockSize=5242880):
        while True:
            chunk = srcData.read(blockSize)
            if not chunk:
                break
            yield chunk

    # Supported File Formats: jpeg, png ; Maximum File Size: 5MB
    def imageUpload(self, imageFile, describe='', text='', mkd='0', fav='0', note2Img='0'):
        if re.match(r'[a-zA-z]+://[^\s]*', imageFile):
            # Upload Image from URL
            response = requests.Session().get(
                url=imageFile,
                headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0'},
                timeout=120,
                stream=True,
                verify=False
            )
            fileContent = response.content
            mimeType = response.headers['content-type']
            fileName = '%s.%s' % (uuid4().hex, re.sub(r'image/', '', mimeType))
            formData = MultipartEncoder(fields={'image': (fileName, fileContent, mimeType)})
        else:
            # Upload Image from Local File
            fileContent = codecs.open(imageFile, 'rb')
            mimeType = 'image/%s' % (imghdr.what(fileContent))
            fileName = '%s.%s' % (uuid4().hex, re.sub(r'image/', '', mimeType))
            formData = MultipartEncoder(fields={'image': (fileName, fileContent, mimeType)})
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=image/upload'
        response = self.session.post(
            url=url,
            headers={'Content-Type': formData.content_type},
            data=self.genChunks(formData),
            timeout=120,
            stream=True
        )
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        imageName = respData['file_name']
        width = respData['width']
        height = respData['height']
        # Length Limitations of Describe: ASCII 30, UTF-8 15
        describe = re.sub(r' |\t', '&nbsp;', describe.strip())
        detail = '<image w=%s h=%s describe=%s name=%s>%s' % (width, height, describe, imageName, text)
        note = self.noteCreate(detail, mkd=mkd, fav=mkd, note2Img=note2Img)
        # return dicts
        return respData, note

    # Unfinished Function
    def imageCrop(self, imageName, x, y, width, height):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=image/crop'
        formData = {
            'image_name': imageName,
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        # return dict
        return respData

    def note2Image(self, syncId):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/image&sync_id=%s' % (syncId)
        response = self.session.get(url, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        image = 'https://cloud.smartisan.com/apps/%.f/weiboimage/%s' % (time(), respData['image'])
        respData.update({'image': image})
        # return dict
        return respData

    # Not Available at This Time (System Maintenance)
    def webCreate(self, syncId):
        cloudNoteList = self.noteGetList()['list']
        for note in cloudNoteList:
            if note['sync_id'] == syncId:
                title = note['title']
                detail = note['detail']
                mkd = note['markdown']
                break
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/deleteAll'
        formData = {
            'sync_id': syncId,
            'title': title,
            'content': detail,
            'markdown': mkd
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        # return dict
        return respData

    # ATTENTION!!!
    def noteDelete(self, *syncIds):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/deleteAll'
        formData = {
            'sync_ids': ','.join(syncIds),
            'tab_id': self.tabId
        }
        response = self.session.post(url, data=formData, timeout=60)
        self.checkResponse(response)
        content = json.loads(response.content)
        respData = content['data']
        # return dict
        return respData

    # Experimental Features: Export Notes to JSON File
    def noteBackup(self, fileName=''):
        cloudData = self.noteGetList()
        if fileName == '':
            fileName = 'UID%s_Time%s_Notes%s.json' % (
                self.uid,
                strftime('%Y-%m-%d+%H:%M:%S', localtime(time())),
                len(cloudData['list'])
            )
        with codecs.open(fileName, 'w', 'UTF-8') as f:
            json.dump(cloudData, f, separators=(',', ':'))
        f.close()
        return cloudData

    # Experimental Features: Import Notes from JSON File
    def noteRestore(self, fileName):
        cloudData = self.noteGetList()
        cloudSyncIds = [note['sync_id'] for note in cloudData['list']]
        with codecs.open(fileName, 'rU', 'UTF-8') as f:
            restoreData = json.loads(f.read())
        f.close()
        for note in restoreData['list']:
            syncId = note['sync_id']
            detail = note['detail']
            mkd = note['markdown']
            fav = note['favorite']
            if syncId in cloudSyncIds:
                self.noteUpdate(syncId, detail, mkd=mkd, fav=fav)
            else:
                self.noteCreate(detail, mkd=mkd, fav=fav)
        return self.noteGetList()

if __name__ == '__main__':
    username = 'Your Username'
    password = 'Your Password'
    s = SmartisanNotes(username, password)

