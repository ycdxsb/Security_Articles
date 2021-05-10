<h1 align="center">Security Article</h1>

> 爬取安全领域文章(Seebug、先知社区、安全客、freebuf等)，转成pdf存到本地

## 原因

一些比较老的博文中的一些关键的图片会由于图片服务器错误（不提供图片）加载失败，但是又毫无办法。

有人选择把图片和文章内容全部爬下来存进数据库重新组织，但是对我个人不是很有必要，直接存成pdf反而更方便我阅读。

考虑到版权等问题，只提供代码，不提供pdf文档

**PS**：在找解决方案的时候看到了一个去年完成的项目[Security Search](http://helosec.com/)，主要是实现信息聚合搜索的功能，内容很全也一直在更新。

## 站点

|                站点                 |                             脚本                             |  进度  |
| :---------------------------------: | :----------------------------------------------------------: | :----: |
| [Seebug](https://paper.seebug.org/) | [Spider](https://github.com/ycdxsb/Security_Articles/tree/main/Seebug) | 已完成 |
| [先知社区](https://xz.aliyun.com/)  | [Spider](https://github.com/ycdxsb/Security_Articles/tree/main/%E5%85%88%E7%9F%A5%E7%A4%BE%E5%8C%BA) | 已完成 |
| [安全客](https://www.anquanke.com/) | [Spider](https://github.com/ycdxsb/Security_Articles/tree/main/%E5%AE%89%E5%85%A8%E5%AE%A2) | 已完成 |
| [FreeBuf](https://www.freebuf.com/) | [Spider](https://github.com/ycdxsb/Security_Articles/tree/main/FreeBuf) |  已完成  |
| [Wooyun](http://www.vuln.cn/wooyundrops) | [Spider](https://github.com/ycdxsb/Security_Articles/tree/main/Wooyun) | 已完成 |
| [嘶吼](https://www.4hou.com/) |  |  |

## TODO
- 本地存空间有点费，使用[nodedrive](https://github.com/notechats/notedrive)对接百度云

## 依赖

- [wkhtmltopdf](https://wkhtmltopdf.org/)