# Security Articles

> 爬取安全领域文章(Seebug、先知社区、安全客、freebuf、wooyun等)，转成pdf存到本地，离线学习

- [Seebug](https://paper.seebug.org/)
- [先知社区](https://xz.aliyun.com/)



## dependence

- [wkhtmltopdf](https://wkhtmltopdf.org/)

## Seebug Spider

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

