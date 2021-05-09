import re
import os
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
    
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.1; ',
    }
    
    WKHTML2PDF_PATH = config['config']['WKHTML2PDF_PATH']
    ERR_FILE = config['config']['ERR_FILE']
    PDF_PATH = config['config']['PDF_PATH']
    
    LOG_FILE = config['log']['LOG_FILE']
    logger.add(LOG_FILE, format="{time} {level} {message}")
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
    # title = re.findall('<h1>(.*)</h1>', content)[0]
    title = re.findall('<title>(.*)</title>', content)[0]
    title = title.replace(" - 安全客，安全资讯平台","")
    title = title.strip()
    return title

def filter(filename):
    string = r'\/:*?"<>|'
    for s in string:
        filename = filename.replace(s, "")
    return(filename)

def crawl_id(id,config,options,filename=None):
    base_url = "https://www.anquanke.com/post/id/%d"
    try:
        url = base_url % id
        logger.info("URL: %s" % url)
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
        filename = os.path.join(PDF_PATH,"%d-%s.pdf" % (id, filename))
            
        html_byte = response.content
        html_byte = html_byte.replace(b"data-original",b"src")
        TMP_FILE = 'tmp.html'
        with open(TMP_FILE,'wb') as f:
            f.write(html_byte)
            
        pdfkit.from_url(TMP_FILE, filename, configuration=config,
                            options=options)
            
        with open(ERR_FILE,'r') as f:
            err_ids = f.read()
        err_ids = err_ids.split("\n")
        err_ids = [int(err_id) for err_id in err_ids if err_id!=""]
        if(id in err_ids):
            err_ids = set(err_ids)-set([id])
            err_ids = sorted(err_ids,reverse=True)
            err_ids = [str(err_id) for err_id in err_ids]
            with open(ERR_FILE,'w') as f:
                f.write("\n".join(err_ids))
    except Exception as e:
        with open(ERR_FILE,'r') as f:
            err_ids = f.read()
        err_ids = err_ids.split("\n")
        err_ids = [int(err_id) for err_id in err_ids if err_id!=""]
        if(id not in err_ids):
            err_ids.append(id)
            err_ids = sorted(err_ids,reverse=True)
            err_ids = [str(err_id) for err_id in err_ids]
            with open(ERR_FILE,'w') as f:
                f.write("\n".join(err_ids))
    

def crawl():
    config , options = init()
    '''
    if os.path.exists(ERR_FILE):
        with open(ERR_FILE) as f:
            content = f.read()
        err_ids = content.split("\n")
        err_ids = [int(id) for id in err_ids if id!=""]
        for err_id in err_ids:
            crawl_id(err_id,config,options)
    '''
    files = os.listdir(PDF_PATH)
    ids = [int(f.split("-")[0]) for f in files]
    url = "https://api.anquanke.com/data/v1/posts?size=20&page=1"
    next_url = 1
    while(next_url!=""):
        logger.info("PAGE_URL: %s" % url)
        response = requests.get(url, headers=headers)
        text = json.loads(response.text)
        next_url = text['next']
        for item in text['data']:
            id = item['id']
            if id in ids:
                continue
            filename = item['title']
            filename = filter(filename)
            crawl_id(id,config,options,filename)
        url = next_url

if __name__=="__main__":
    crawl()