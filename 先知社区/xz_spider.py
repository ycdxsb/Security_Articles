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
        'encoding': "utf-8"
    }

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
    title = title.replace(' - 先知社区','')
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
            url = "https://xz.aliyun.com/t/%d" % id
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

def crawl(number):
    config , options = init()
    ids = [8384, 8789, 5513, 2318, 5425, 8718, 6143, 7018, 8974, 8743, 6916, 2580, 8074, 5721, 4508, 8193, 2413, 2235, 7656, 5603, 5765, 8810, 8890, 8458, 6191, 5709, 9175, 7795, 5536, 6781, 7878, 9302, 4425, 8802, 8902, 1990, 8699, 5759, 9021, 8226, 8786, 5197, 7103, 2301, 9241, 9476, 2691, 7594, 2339, 9311, 2596, 4756, 9371, 8782, 8645, 8730, 7109, 1983, 9143, 5493, 8831, 8746, 8747, 7797, 8774, 6040, 8797, 8894, 3012, 5615]
    crawl_ids(ids,config,options)
    exit(0)
    # process error ids
    if os.path.exists(ERR_FILE):
        with open(ERR_FILE) as f:
            content = f.read()
        err_ids = content.split("\n")
        err_ids = [int(id) for id in err_ids if id!=""]
        crawl_ids(err_ids,config,options)
    
    # process new ids
    files = os.listdir(PDF_PATH)
    ids = [int(f.split("-")[0]) for f in files]
    ids = list((set(range(0,number+1))-set(ids)))
    ids = sorted(ids,reverse=True)
    crawl_ids(ids,config,options)

if __name__ == '__main__':
    argv = sys.argv
    if(len(argv)!=2):
        print("usage: python3 xz_spider.py maxnum")
        exit(-1)
    number = int(sys.argv[1])
    crawl(number)