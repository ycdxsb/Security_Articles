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



### 效果

[demo](https://github.com/ycdxsb/Security_Articles/tree/main/FreeBuf/demo.pdf)

Freebuf的效果有点问题，左侧边栏会对文章首部有所遮挡，但是不太影响阅读

![image-20210510121809435](https://ycdxsb-1257345996.cos.ap-beijing.myqcloud.com/blog/2021-10-05-image-20210510121809435.png)



### 问题

发现wkhtmltopdf有的页面会有超时，比如https://www.freebuf.com/network/225926，拉进url黑名单处理，或者改pdfkit接口加入timeout，参考：https://github.com/JazzCore/python-pdfkit/pull/151