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

