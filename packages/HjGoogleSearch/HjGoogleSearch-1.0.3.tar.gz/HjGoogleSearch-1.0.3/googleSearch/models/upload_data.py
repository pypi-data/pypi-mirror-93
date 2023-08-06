# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 17:34
# @Author  : Haijun


import os
import random
import ssl
import requests
from urllib.request import Request
from urllib import request
import urllib.request
import urllib.parse
from http.cookiejar import LWPCookieJar
from dynaconf import settings
from googleSearch.utils.logger import logger
from requests_toolbelt.multipart.encoder import MultipartEncoder

home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'  # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass


class NoRedirHandler(request.HTTPRedirectHandler):
    # 禁止302跳转
    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    http_error_301 = http_error_302


class UploadDataForSbi(object):
    """
    以图搜图获取sbi
    """

    def __init__(self):
        self.user_agent = random.choice(settings.USER_AGENT)

    def upload_image_url(self, image_url):
        """
        通过图片在线链接获取sbi
        """
        try:
            url = f'https://www.google.com/searchbyimage?image_url={image_url}&btnG=Search+by+image&encoded_image=&image_content=&filename=&hl=en'
            logger.info(url)
            request = Request(url)
            request.add_header('User-Agent', self.user_agent)
            cookie_jar.add_cookie_header(request)
            opener = urllib.request.build_opener(NoRedirHandler)  # 禁止重定向
            # context = ssl._create_unverified_context()
            response = opener.open(request)
            cookie_jar.extract_cookies(response, request)
            url_with_sbi = response.headers.get('Location')
            logger.info(f'通过图片链接获取sbi===={url_with_sbi}')
            response.close()
            try:
                cookie_jar.save()
            except Exception:
                logger.error('cookiejar保持失败')
            return url_with_sbi
        except Exception as e:
            logger.info(f'通过图片链接获取sbi失败====={e}')
            return None

    def upload_local_image(self, image_url):
        """
        通过上传本地图片获取sbi
        :param file_path: 图片本地路径
        :return:
        """
        try:
            # 目标url
            # file_path = init_data.get('image')
            upload_url = settings.BASE_URL + '/searchbyimage/upload'
            # 打开图片
            fp = open(image_url, 'rb')
            m = MultipartEncoder(
                {'encoded_image': (fp.name, fp, 'image/jpeg'), 'image_url': None, 'image_content': None, 'filename': None,
                 'btnG': None})
            # 此处需要禁止跳转
            response = requests.post(upload_url, data=m,
                                     headers={'Content-Type': m.content_type, 'User-Agent': self.user_agent},
                                     allow_redirects=False)
            url_with_sbi = response.headers.get('Location')
            logger.info(f'通过上传本地图片获取sbi========{url_with_sbi}')
            return url_with_sbi
        except Exception as e:
            logger.info(f'通过上传本地图片获取sbi失败========{e}')
            return None
