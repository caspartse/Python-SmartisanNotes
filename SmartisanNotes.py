#!/usr/bin/env python
# -*- coding:utf-8 -*
import sys
import requests
import simplejson as json
from uuid import uuid4
from base64 import b64encode
from time import time, localtime, strftime
import codecs
import re
import imghdr
from requests_toolbelt import MultipartEncoder


ERROR_MAP = {'0': 'OK', '1': 'SYSTEM_MAINTENANCE', '2': 'LOGIC_ERROR', '3': 'FS_READ_ERROR', '4': 'FS_WRITE_ERROR', '5': 'DB_CONNECT_ERROR', '6': 'DB_QUERY_ERROR', '7': 'CACHE_CONNECT_ERROR', '8': 'CACHE_QUERY_ERROR', '1002': 'PARAMETER_ERROR', '1601': 'ILLEGAL_TICKET', '1602': 'INVALID_TICKET', '1101': 'ILLEGAL_UID', '1102': 'ILLEGAL_PASSWORD', '1103': 'ILLEGAL_AVATAR', '1104': 'ILLEGAL_SECQUES', '1105': 'ILLEGAL_SECANS', '1106': 'INVALID_UID', '1107': 'INVALID_PASSWORD', '1108': 'INVALID_SECANS', '1109': 'ALIAS_REQUIRED', '1110': 'PASSWORD_REQUIRED', '1201': 'ILLEGAL_ALIAS',
             '1202': 'INVALID_ALIAS', '1203': 'REGISTERED_ALIAS', '1204': 'ILLEGAL_CELLPHONE', '1205': 'INVALID_CELLPHONE', '1206': 'REGISTERED_CELLPHONE', '1207': 'ILLEGAL_EMAIL', '1208': 'INVALID_EMAIL', '1209': 'REGISTERED_EMAIL', '1210': 'INVALID_NICKNAME', '1211': 'UNREGISTERED_NICKNAME', '1212': 'REGISTERED_NICKNAME', '1213': 'ILLEGAL_NICKNAME', '1301': 'ILLEGAL_VCODE', '1302': 'INVALID_VCODE', '1304': 'VCODE_TOO_OFTEN', '1502': 'CAPTCHA_REQUIRED', '1401': 'ILLEGAL_TOKEN', '1402': 'INVALID_TOKEN', '1701': 'UNAUTHORIZED', '1303': 'REFRECH_VCODE', '1501': 'FAILED_LOGIN_LIMIT'}


class SmartisanNotes(object):

    def __init__(self, username, password):
        super(SmartisanNotes, self).__init__()
        self.session = requests.Session()
        # For Debug
        # self.session.verify = False
        self.uid = str(self.accountLogin(username, password)['uid'])
        self.tabId = b64encode(uuid4().hex)[:8]

    def accountLogin(self, username, password):
        url = 'https://account.smartisan.com/v2/session/?m=post'
        headers = {
            'Host': 'account.smartisan.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer': 'https://account.smartisan.com/'
        }
        self.session.headers.update(headers)
        payload = {
            'username': username,
            'password': password,
            'extended_login': '1'
        }
        resp = self.session.post(url, data=payload, timeout=100)
        try:
            content = json.loads(resp.content)
        except:
            print 'Unknown Error: (%s) %s Try again.' % (resp.status_code, resp.text)
            sys.exit(1)
        errno = str(content.get('errno'))
        if errno != '0':
            print 'Error %s: %s. Try again.' % (errno, ERROR_MAP[errno])
            sys.exit(1)
        respData = content['data']
        headers = {
            'Host': 'cloud.smartisan.com',
            'Referer': 'https://cloud.smartisan.com/apps/note/'
        }
        self.session.headers.update(headers)
        # return dict
        return respData

    def checkResponse(self, resp):
        try:
            content = json.loads(resp.content)
        except:
            print 'Unknown Error: (%s) %s Try again.' % (resp.status_code, resp.text)
            sys.exit(1)
        code = str(content['code'])
        if code == '1':
            for k, v in content['errInfo'].iteritems():
                print 'Error %s: %s. Try again.' % (k, v)
            sys.exit(1)
        return

    def noteGetList(self):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=v2/getList'
        resp = self.session.get(url, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        # return dict
        return respData

    def noteCreate(self, detail, mode='2', fav='0', note2Img='0'):
        # formatting mode: 0 (Text) / 1 (Rich Text Format) / 2 (Markdown)
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/create'
        payload = {
            'detail': detail,
            'favorite': fav,
            'markdown': '0',
            'folderId': '',
            'formatting_mode': mode,
            'title': '',
            'tab_id': self.tabId
        }
        resp = self.session.post(url, data=payload, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        if note2Img == '1':
            syncId = respData['note']['sync_id']
            noteImage = self.note2Image(syncId, detail)
            # return dicts
            return respData, noteImage
        # return dict
        return respData

    def noteUpdate(self, syncId, detail, mode='2', fav='0', note2Img='0'):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/update'
        payload = {
            'detail': detail,
            'favorite': fav,
            'markdown': '0',
            'folderId': '',
            'formatting_mode': mode,
            'title': '',
            'tab_id': self.tabId
        }
        resp = self.session.post(url, data=payload, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        if note2Img == '1':
            syncId = respData['note']['sync_id']
            noteImage = self.note2Image(syncId, detail)
            # return dicts
            return respData, noteImage
        # return dict
        return respData

    def noteUpdateFav(self, syncId, fav='1'):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/updateFav'
        payload = {
            'sync_id': syncId,
            'favorite': fav,
            'tab_id': self.tabId,
        }
        resp = self.session.post(url, data=payload, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        # return dict
        return respData

    def noteUpdateFormattingMode(self, syncId, mode):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/updateFormattingMode'
        payload = {
            'sync_id': syncId,
            'formatting_mode': mode,
            'tab_id': self.tabId,
        }
        resp = self.session.post(url, data=payload, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        # return dict
        return respData

    def genChunks(self, srcData, blockSize=5242880):
        while True:
            chunk = srcData.read(blockSize)
            if not chunk:
                break
            yield chunk

    # Supported File Formats: jpeg, png ; Maximum File Size: 5MB
    def imageUploadOnly(self, imageFile):
        if re.match(r'[a-zA-z]+://[^\s]*', imageFile):
            # Upload Image from URL
            resp = requests.Session().get(
                url=imageFile,
                headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'},
                timeout=120,
                stream=True,
                verify=False
            )
            fileContent = resp.content
            mimeType = resp.headers['content-type']
            fileName = '%s.%s' % (uuid4().hex, re.sub(r'image/', '', mimeType))
            payload = MultipartEncoder(
                fields={'image': (fileName, fileContent, mimeType)})
        else:
            # Upload Image from Local File
            fileContent = codecs.open(imageFile, 'rb')
            mimeType = 'image/%s' % (imghdr.what(fileContent))
            fileName = '%s.%s' % (uuid4().hex, re.sub(r'image/', '', mimeType))
            payload = MultipartEncoder(
                fields={'image': (fileName, fileContent, mimeType)})
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=image/upload'
        resp = self.session.post(
            url=url,
            headers={'Content-Type': payload.content_type},
            data=self.genChunks(payload),
            timeout=120,
            stream=True
        )
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        return respData

    # Supported File Formats: jpeg, png ; Maximum File Size: 5MB
    def imageUpload(self, imageFile, describe='', text='', reverse='0', mode='2', fav='0', note2Img='0'):
        respData = self.imageUploadOnly(imageFile)
        imageName = respData['file_name']
        width = respData['width']
        height = respData['height']
        # Length Limitations of Describe: ASCII 30, UTF-8 15
        describe = re.sub(r' |\t', '&nbsp;', describe.strip())
        if reverse == '1':
            detail = '%s<image w=%s h=%s describe=%s name=%s>' % (
                text, width, height, describe, imageName)
        else:
            detail = '<image w=%s h=%s describe=%s name=%s>%s' % (
                width, height, describe, imageName, text)
        note = self.noteCreate(detail, mode=mode, fav=fav, note2Img=note2Img)
        # return dicts
        return respData, note

    # Inserting an Image Just Like Markdown: ![describe](imageFile)
    def noteArticle(self, detail, mode='2', fav='0', note2Img='0'):
        while True:
            imgElements = re.findall(r'\!\[[\s\S]*?\]\([^\s]+?\)', detail)
            if len(imgElements) == 0:
                break
            describe, imageFile = re.findall(
                r'\!\[([\s\S]*?)\]\(([^\s]+?)\)', imgElements[0])[0]
            image = self.imageUploadOnly(imageFile)
            describe = re.sub(r' |\t', '&nbsp;', describe.strip())
            imgTage = '<image w=%s h=%s describe=%s name=%s>' % (
                image['width'], image['height'], describe, image['file_name'])
            detail = detail.replace(imgElements[0], imgTage)
        note = self.noteCreate(detail=detail, mode=mode, fav=fav, note2Img='1')
        return note

    def note2Image(self, syncId, detail):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/image'
        payload = {
            'detail': detail,
            'sync_id': syncId,
            'rtf_style': '',
            'formatting_mode': '2',
            'tab_id': self.tabId
        }
        resp = self.session.post(url, data=payload, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
        respData = content['data']
        imageName = respData['image']
        image = 'https://cloud.smartisan.com/apps/%.f/weiboimage/%s' % (
            time(), imageName)
        respData.update({'image': image})
        # Save Image
        r = self.session.get(image, timeout=100, stream=True)
        if r.status_code == 200:
            with codecs.open(imageName, 'wb') as f:
                for chunk in r.iter_content(20480):
                    f.write(chunk)
            f.close()
        else:
            pass
        # return dict
        return respData

    # ATTENTION!!!
    def noteDelete(self, *syncIds):
        url = 'https://cloud.smartisan.com/apps/note/index.php?r=note/deleteAll'
        payload = {
            'sync_ids': ','.join(syncIds),
            'tab_id': self.tabId
        }
        resp = self.session.post(url, data=payload, timeout=100)
        self.checkResponse(resp)
        content = json.loads(resp.content)
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
                len(cloudData['note'])
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
    pass
