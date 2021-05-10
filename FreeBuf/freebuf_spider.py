import re
import os
import ast
import json
import requests

from configparser import ConfigParser
from html import unescape

import chardet
import pdfkit
from loguru import logger

def init():
    cwd = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.abspath(os.path.join(cwd, 'config.ini'))
    config = ConfigParser()
    config.read(config_path)
    
    global headers 
    global WKHTML2PDF_PATH
    global ERR_FILE
    global PDF_PATH
    global LOG_FILE
    global categories
    
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.1; ',
    }
    
    WKHTML2PDF_PATH = config['config']['WKHTML2PDF_PATH']
    ERR_FILE = config['config']['ERR_FILE']
    PDF_PATH = config['config']['PDF_PATH']
    
    LOG_FILE = config['log']['LOG_FILE']
    logger.add(LOG_FILE, format="{time} {level} {message}")
    categories = ast.literal_eval(config['config']['CATEGORY'])
    if(not os.path.exists(PDF_PATH)):
        os.mkdir(PDF_PATH)
    if(not os.path.exists(ERR_FILE)):
        file = open(ERR_FILE,'w') 
        file.close()
    config = pdfkit.configuration(wkhtmltopdf=WKHTML2PDF_PATH)

    options = {
        'encoding': "utf-8",
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '0mm',
        'margin-left': '10mm'
    }
    return config,options

def get_filename(response):
    html_byte = response.content
    charset = chardet.detect(html_byte)['encoding']
    if (charset.lower() == "gb2312" or charset.lower() == "gbk"):
        response.encoding = 'gbk'
    else:
        response.encoding = 'utf-8'
    content = response.text
    content = content.replace("\n","")
    title = re.findall('<title>(.*)</title>', content)[0]
    title = title.replace(" - FreeBuf网络安全行业门户","")
    title = title.strip()
    return title

def filter(filename):
    string = r'\/:*?"<>|'
    for s in string:
        filename = filename.replace(s, "")
    return(filename)

def crawl_id(id,category,config,options,filename=None):
    base_url = "https://www.freebuf.com/%s/%d"
    url = base_url % (category,id)
    logger.info("URL: %s" % url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404 or str(response.status_code)[0:2] == "40":
            logger.debug("status: %d" % response.status_code)
            return
        if(filename==None):
            filename = get_filename(response)
        logger.info("FILE_NAME: %s" % filename)
        filename = unescape(filename)
        filename = filter(filename)
        logger.info("FILE_NAME: %s" % filename)
        filename = os.path.join(PDF_PATH,category,"%d-%s.pdf" % (id, filename))
        pdfkit.from_url(url, filename, configuration=config,
                            options=options)
        with open(ERR_FILE,'r') as f:
            err_urls = f.read()
        err_urls = err_urls.split("\n")
        err_urls = [err_url for err_url in err_urls if err_url!=""]
        if(url in err_urls):
            err_urls = list(set(err_urls)-set([url]))
            with open(ERR_FILE,'w') as f:
                f.write("\n".join(err_urls))
    except Exception as e:
        with open(ERR_FILE,'r') as f:
            err_urls = f.read()
        err_urls = err_urls.split("\n")
        err_urls = [err_url for err_url in err_urls if err_url!=""]
        if(url not in err_urls):
            err_urls.append(url)
            with open(ERR_FILE,'w') as f:
                f.write("\n".join(err_urls))
    

def crawl_url(url,config,options):
    id = url.split('/')[-1]
    category = url.split('/')[-2]
    crawl_id(id,category,config,options)

def crawl():
    config , options = init()
    '''
    if os.path.exists(ERR_FILE):
        with open(ERR_FILE) as f:
            content = f.read()
        err_urls = content.split("\n")
        err_urls = [err_url for err_url in err_urls if err_url!=""]
        for err_url in err_urls:
            crawl_url(err_url,config,options)
    '''
    page_base_url = "https://www.freebuf.com/fapi/frontend/category/list?name=%s&tag=category&limit=20&page=%d&select=0&order=0"
    #categories = ['network','web','wireless','es','terminal','database','vul','sectool','geek','ics-articles','system','security-management']
    
    for category in categories:
        page_id = 1
        category_path = os.path.join(PDF_PATH,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        files = os.listdir(category_path)
        ids = [int(f.split("-")[0]) for f in files]
        while(True):
            url = page_base_url %(category,page_id)
            logger.info("PAGE_URL: %s" % url)
            response = requests.get(url, headers=headers)
            text = json.loads(response.text)
            if len(text['data']['data_list'])==0:
                break
            for item in text['data']['data_list']:
                id = int(item["ID"])
                if(id in ids):
                    continue
                filename = item["post_title"]
                filename = filter(filename)
                crawl_id(id,category,config,options,filename)
            page_id += 1

if __name__== '__main__':
    crawl()