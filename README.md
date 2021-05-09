# Security Articles

> 爬取安全领域文章(Seebug、先知社区、安全客、freebuf、wooyun等)，转成pdf存到本地，离线学习

- [Seebug](https://paper.seebug.org/)
- [先知社区](https://xz.aliyun.com/)
- [安全客](https://www.anquanke.com/)
- [FreeBuf](https://www.freebuf.com/)

- [Security Articles](#security-articles)
  - [dependence](#dependence)
  - [Seebug Spider](#seebug-spider)
    - [思路](#思路)
    - [Usage](#usage)
  - [XZ Spider](#xz-spider)
    - [思路](#思路-1)
    - [Usage](#usage-1)
  - [Anquanke Spider](#anquanke-spider)
    - [思路](#思路-2)
    - [Usage](#usage-2)
  - [FreeBuf Spider](#freebuf-spider)
    - [思路](#思路-3)
    - [Usage](#usage-3)
  - [](#)

## dependence

- [wkhtmltopdf](https://wkhtmltopdf.org/)

## Seebug Spider

### 思路

遍历id即可

### Usage

安装依赖

```
pip3 install -r requirements.txt
```

修改`config.ini`

```
[config]
ERR_FILE = err_list.txt
WKHTML2PDF_PATH = /usr/local/bin/wkhtmltopdf
PDF_PATH = Seebug

[log]
LOG_FILE = seebug_spider.log
```

- `ERR_FILE`：处理出错的id号
- `WKHTML2PDF_PATH`：wkhtmltopdf二进制文件所在路径
- `PDF_PATH`：存储pdf的目录
- `log`：日志文件

启动爬虫

```
python3 seebug_spider.py maxnum
```

maxnum是当前站点上的博文的最大`id`号，例如当前最新博文链接为`https://paper.seebug.org/1583/`，则最大`id`号为`1583`

## XZ Spider

### 思路

遍历id即可

### Usage

安装依赖

```
pip3 install -r requirements.txt
```

修改`config.ini`

```
[config]
ERR_FILE = err_list.txt
WKHTML2PDF_PATH = /usr/local/bin/wkhtmltopdf
PDF_PATH = xz

[log]
LOG_FILE = xz.log
```

- `ERR_FILE`：处理出错的id号
- `WKHTML2PDF_PATH`：wkhtmltopdf二进制文件所在路径
- `PDF_PATH`：存储pdf的目录
- `log`：日志文件

启动爬虫

```
python3 xz_spider.py maxnum
```

maxnum是当前站点上的博文的最大`id`号，例如当前最新博文链接为`https://xz.aliyun.com/t/9517`，则最大`id`号为`9517`

## Anquanke Spider

### 思路

安全客可以通过API获取文章链接，`https://api.anquanke.com/data/v1/posts?size=20&page=1`，每次返回的结果里会有next_url，因此不断的遍历，直到next_url为空即可

快爬完了发现pdf里的图都是空的，后来发现把html中的img标签中的`data-original`改成src或者加入src就可以了

### Usage

安装依赖

```
pip3 install -r requirements.txt
```

修改`config.ini`

```
[config]
ERR_FILE = err_list.txt
WKHTML2PDF_PATH = /usr/local/bin/wkhtmltopdf
PDF_PATH = anquanke

[log]
LOG_FILE = anquanke.log
```

- `ERR_FILE`：处理出错的id号
- `WKHTML2PDF_PATH`：wkhtmltopdf二进制文件所在路径
- `PDF_PATH`：存储pdf的目录
- `log`：日志文件

启动爬虫

```
python3 anquanke_spider.py
```

## FreeBuf Spider

### 思路

和安全客很像，也是通过api请求数据，但是详细分了类

```
categories = ['network','web','wireless','es','terminal','database',
                'vul','sectool','geek','ics-articles','system','security-management']
```

请求api

```
page_base_url = "https://www.freebuf.com/fapi/frontend/category/list?name=%s&tag=category&limit=20&page=%d&select=0&order=0" % (category,page_id)
```

一直增加页数然后直到某一页返回data_list为空即可

### Usage

安装依赖

```
pip3 install -r requirements.txt
```

修改`config.ini`

```
[config]
ERR_FILE = err_list.txt
WKHTML2PDF_PATH = /usr/local/bin/wkhtmltopdf
PDF_PATH = freebuf
# FreeBuf 分类：
# web安全 web
# 网络安全 network
# 无线安全 wireless
# 企业安全 es
# 终端安全 terminal
# 数据安全 database
# 漏洞 vul
# 工具 sectool
# 极客 geek
# 工控安全 ics-articles
# 系统安全 system
# 安全管理 security-management
CATEGORY = ['network','web','wireless','es','terminal','database','vul','sectool','geek','ics-articles','system','security-management']

[log]
LOG_FILE = freebuf.log
```

- `ERR_FILE`：处理出错的id号
- `WKHTML2PDF_PATH`：wkhtmltopdf二进制文件所在路径
- `CATEGORY`：想要爬取的分类类型
- `PDF_PATH`：存储pdf的目录
- `log`：日志文件

启动爬虫

```
python3 freebuf_spider.py
```

## 