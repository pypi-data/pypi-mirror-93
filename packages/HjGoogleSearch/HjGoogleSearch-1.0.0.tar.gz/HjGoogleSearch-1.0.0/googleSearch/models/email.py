# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 15:44
# @Author  : Haijun

import re
import aiohttp
import asyncio

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}

async def filter_email(url):
    async with aiohttp.TCPConnector(limit=5, verify_ssl=False) as tc:
        async with aiohttp.ClientSession(connector=tc) as session:
            try:
                async with session.get(url=url, headers=headers, timeout=15) as req:
                    if req.status in [200, 301, 302]:
                        res_text = await req.text()
                        o_m = re.findall(
                            r'([A-Za-z][A-Za-z0-9]*[-_]?[A-Za-z0-9]*@[A-Za-z0-9]*[-_]?[A-Za-z0-9]*[\.][A-Za-z]{2,5}[\.]?[A-Za-z]{0,3})',
                            res_text)
                        return o_m
                    return False
            except Exception as e:
                return False
