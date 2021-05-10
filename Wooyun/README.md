## Wooyun Spider

### 思路

遍历id

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
PDF_PATH = wooyun

[log]
LOG_FILE = wooyun.log
```

- `ERR_FILE`：处理出错的id号
- `WKHTML2PDF_PATH`：wkhtmltopdf二进制文件所在路径
- `PDF_PATH`：存储pdf的目录
- `log`：日志文件

启动爬虫

```
python3 wooyun_spider.py
```



### 效果

[demo](https://github.com/ycdxsb/Security_Articles/tree/main/Wooyun/demo.pdf)

![image-20210510121557271](https://ycdxsb-1257345996.cos.ap-beijing.myqcloud.com/blog/2021-10-05-image-20210510121557271.png)