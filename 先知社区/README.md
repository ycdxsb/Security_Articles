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

### 效果

[demo](https://github.com/ycdxsb/Security_Articles/tree/main/%E5%85%88%E7%9F%A5%E7%A4%BE%E5%8C%BA/demo.pdf)

![image-20210510111414900](https://ycdxsb-1257345996.cos.ap-beijing.myqcloud.com/blog/2021-10-05-image-20210510111414900.png)

