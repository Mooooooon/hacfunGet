# hacfun.py
# -*- coding: utf-8 -*-
import pycurl
import StringIO
import json
import urllib
import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")
# 封装CURL操作
def start(url):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) ' \
         'AppleWebKit/537.36 (KHTML, like Gecko) ' \
         'Chrome/36.0.1985.143 Safari/537.36'
    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.TIMEOUT, 300)
    c.setopt(pycurl.USERAGENT, ua)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.perform()
    get_info = b.getvalue()
    c.close()
    return get_info


# 转码
def u(string):
    return string.decode('utf-8')


while True:
    number = raw_input("请输入要下载的串号：")
    if number:
        url = 'http://h.acfun.tv/t/' + number + '.json'
        get_json = start(url)
        info = json.loads(get_json)
        success = info[u("success")]
        if success == True:
            size = info[u("page")][u("size")]
            img_sum = 1
            error = 0
            isExists = os.path.exists(str(number))
            if not isExists:
                os.makedirs(str(number))
            for i in range(size):
                url = 'http://h.acfun.tv/t/' + number + '.json?page=' + str(i + 1)
                get_json = start(url)
                info = json.loads(get_json)
                replys = info[u("replys")]
                fileHandle = open(str(number) + "/" + 'error.txt', 'a')
                for j in range(len(replys)):
                    image = replys[j][u("image")]
                    if image:
                        image_url = "http://static.acfun.mm111.net/h" + image
                        image_url_split = image.split('.')
                        ext = image_url_split[-1]
                        file_name = image_url_split[-2].split('/')[-1]
                        try:
                            urllib.urlretrieve(image_url, str(number) + "/" + file_name + "." + ext)
                            print "第" + str(img_sum) + "张下载完毕"
                            img_sum += 1
                            error = 0
                        except:
                            error += 1
                            if error < 5:
                                print "第" + str(img_sum) + "张下载失败，重试"
                                img_sum -= 1
                            else:
                                print "第" + str(img_sum) + "张下载失败，放弃"
                                fileHandle.write(image_url + "\n")
                fileHandle.close()
            print '串号' + number + '下载完毕，按回车关闭程序，或输入串号继续下载'
        else:
            print '获取失败，请确认串号输入正确'
    else:
        break