# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 20:40
# @Author  : Haijun


# -*- coding: utf-8 -*-
# @Time    : 2021/1/22 17:01
# @Author  : Haijun
import re

import aiohttp
import asyncio
import iso8601
import random
from dynaconf import settings
from loguru import logger
from aiostream import stream
from googleSearch.models.site_rank import SiteRank
from googleSearch.models.email import filter_email


class CrawlDetail(object):
    def __init__(self):
        self.headers = {
            'user-agent': random.choice(settings.USER_AGENT),
            'referer': 'https://www.google.com/'
        }

    async def crawl_product(self, expected_url):
        """
        获取最终的产品链接和店铺链接
        :param url:
        :return:
        """
        url = expected_url.get('url')
        image = expected_url.get('image')
        try:
            logger.info(f'开始爬取详情数据url==============={url}')
            async with aiohttp.TCPConnector(limit=10, verify_ssl=False) as tc:
                async with aiohttp.ClientSession(connector=tc) as session:
                    async with session.get(url=url, headers=self.headers, timeout=15) as req:
                        if req.status in [200, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 305, 306, 307]:
                            logger.info(f'详情页状态====={req.status} ===== 请求url==={url}=====响应url======{req.url}')
                            source = await req.text()
                            return await self.parse(source, image, str(req.url))
        except Exception as e:
            return []

    async def parse(self, res_text, image, res_url=None):
        # try:
        domain = re.findall(r'(.*?://.*?/)', res_url)[0]
        # 匹配商品上架时间
        _published_time = list()
        if 'Shopify.shop' in res_text or 'Shopify.theme' in res_text or \
                'Shopify.cdnHost' in res_text or 'Powered by Shopify' in res_text:
            if 'published_at":"' in res_text:
                p_at = re.findall(r'published_at":"(.*?)"', res_text)
                _published_time.extend(p_at)
            # elif 'created_at":"' in res_text:
            #     p_at = re.findall(r'created_at":"(.*?)"', res_text)
            #     _published_time.extend(p_at)
            elif 'created_at&quot;:&quot;' in res_text:
                p_at = re.findall(r'created_at&quot;:&quot;(.*?)&quot', res_text)
                _published_time.extend(p_at)
            elif '"datePublished":"' in res_text:
                p_at = re.findall(r'datePublished":"(.*?)"', res_text)
                _published_time.extend(p_at)
            published_time = self.create_time(_published_time)
            return await  self.source_filter_key(res_text, domain, image, res_url, 'shopify', published_time)
        elif 'content="WooCommerce' in res_text or 'woocommerce_params' in res_text or \
                'woocommerce-product-gallery' in res_text:
            if 'datePublished":"' in res_text:
                p_at = re.findall(r'datePublished":"(.*?)"', res_text)
                _published_time.extend(p_at)
            if 'modified_time" content="' in res_text:
                p_at = re.findall(r'modified_time" content="(.*?)"', res_text)
                _published_time.extend(p_at)
            if '"dateModified":"' in res_text:
                p_at = re.findall(r'"dateModified":"(.*?)"', res_text)
                _published_time.extend(p_at)
            published_time = self.create_time(_published_time)
            return await self.source_filter_key(res_text, domain, image, res_url, 'woocommerce', published_time)
        # except Exception as e:
        #     logger.error(f'爬取详情数据失败==============={res_url}===={e}')
        #     pass

    def create_time(self, p_time):
        """
        iso8601
        时间转换
        2020-06-05T15:01:50-04:00
        """
        published_time = None
        if p_time:
            published_time = p_time[0]
            t = iso8601.parse_date(published_time)
            published_time = t.strftime("%Y-%m-%d %H:%M:%S")
        return published_time

    async def source_filter_key(self, res_text, domain, image, res_url, source_key, published_time):
        try:
            # 当前页邮箱
            o_m = re.findall(r'([a-z][a-z0-9]*[-_]?[a-z0-9]*@[a-z0-9]*[-_]?[a-z0-9]*[\.][a-z]{2,3}[\.]?[a-z]{0,2})',
                             res_text)
            # 联系页邮箱
            xs = stream.iterate([f'{domain}pages/contact-us', f'{domain}pages/contact', f'{domain}pages/about-us',
                                 f'{domain}contact-us', f'{domain}contact', f'{domain}about-us'])
            # async for
            async for t in xs:
                email = await filter_email(t)
                if email:
                    o_m.append(email)
            _email = []
            if o_m:
                for i in o_m:
                    # 去除尾部的'.'
                    j = '.'.join([k for k in i.split('.') if k])
                    _email.append(j)
                # 去重
                o_m = list(set(_email))
                # 去除图片 xxx@xxx.jpg, xxx@xxx.png
                o_m = await self.wipe_email(o_m, 'png')
                o_m = await self.wipe_email(o_m, 'jpg')
                o_m = await self.wipe_email(o_m, 'jpeg')
                o_m = await self.wipe_email(o_m, 'webp')
                o_m = await self.wipe_email(o_m, 'gif')
                o_m = await self.wipe_email(o_m, 'bmp')

            # 排名 涉及到请求频次问题，此处省略，单独爬取
            # rank_data = await SiteRank().parse(domain) or None
            url_dict = {
                'host': domain,
                'image': image,
                'product_url': res_url,
                'tool_name': source_key,
                'email': o_m,
                'world_rank': None,  # 排名
                'published_time': published_time
            }
            logger.info(f'过滤后爬取数据结束============={url_dict}')
            return url_dict
        except Exception as e:
            print(e)

    async def wipe_email(self, e_l, i_type):
        """
        去除图片后缀的邮箱
        xxx@xxx.jpg
        :param e_l: 邮箱列表
        :param i_type: 图片格式
        :return:
        """
        expected_mail = list(
            set([i.strip() for i in e_l if i_type not in i and len(i) < 50]))
        return expected_mail


if __name__ == '__main__':
    data = {
        'image': 'https://cdn.shopify.com/s/files/1/0446/5108/5973/products/product-image-1434797904_480x480@2x.jpg?v%3D1598031340',
        'url': 'https://carolestore.com/products/led-makeup-mirror-light'
    }
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete(CrawlDetail().crawl_product(data))
    print(r)
