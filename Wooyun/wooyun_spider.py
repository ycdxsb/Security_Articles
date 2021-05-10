import re
import os
import sys
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
    title = re.findall('<title>(.*)</title>', content)[0]
    title = title.replace(' | 漏洞人生','')
    title = title.strip()
    return title

def filter(filename):
    string = r'\/:*?"<>|'
    for s in string:
        filename = filename.replace(s, "")
    return(filename)

def crawl_ids(ids,config,options):
    for id in ids:
        try:
            url = "http://www.vuln.cn/%d" % id
            logger.info("URL: %s" % url)
            response = requests.get(url, headers=headers)
            if response.status_code == 404 or str(response.status_code)[0:2] == "40":
                logger.debug("status: %d" % response.status_code)
                continue
            filename = get_filename(response)
            logger.info("FILE_NAME: %s" % filename)
            filename = unescape(filename)
            filename = filter(filename)
            logger.info("FILE_NAME: %s" % filename)
            filename = os.path.join(PDF_PATH,"%d-%s.pdf" % (id, filename))
            pdfkit.from_url(url, filename, configuration=config,
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
            pass

def crawl():
    config , options = init()
    '''
    # process error ids
    if os.path.exists(ERR_FILE):
        with open(ERR_FILE) as f:
            content = f.read()
        err_ids = content.split("\n")
        err_ids = [int(id) for id in err_ids if id!=""]
        crawl_ids(err_ids,config,options)
    '''
    # process wooyun
    files = os.listdir(PDF_PATH)
    ids = [int(f.split("-")[0]) for f in files]
    ids = list((set(range(6000,7154+1))-set(ids)))
    ids = sorted(ids,reverse=True)
    crawl_ids(ids,config,options)
    
    # process wooyun zone
    files = os.listdir(PDF_PATH)
    ids = [int(f.split("-")[0]) for f in files]
    ids = list((set(range(8001,8289+1))-set(ids)))
    ids = sorted(ids,reverse=True)
    crawl_ids(ids,config,options)

if __name__ == '__main__':
    crawl()