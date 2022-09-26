# fetchProxy

## copy source
> fetch code copy [alanbobs999/TopFreeProxies](https://github.com/alanbobs999/TopFreeProxies)
>
>testspeed code copy [daycat/clashcheck/](https://github.com/daycat/clashcheck/)
>
>转码功能用的的工具[tindy2013/subconverter](https://github.com/tindy2013/subconverter/)
>
>借鉴了这个大哥的好多代码 [/yu-steven/openit](https://github.com/yu-steven/openit)
>
>大佬的测速工具[xxf098/LiteSpeedTest](https://github.com/xxf098/LiteSpeedTest)
>
>ACL4SSR转换规则[ACL4SSR](https://github.com/ACL4SSR/ACL4SSR/tree/master)

虽然是测速筛选过后的节点，但仍然会出现部分节点不可用的情况，遇到这种情况
建议选择`Clash`, `Shadowrocket`之类能自动切换低延迟节点的客户端。

## 节点信息

### 已测速节点
已测速节点数量: `163`

### 所有节点
合并节点总数: `2788`
### 节点来源
- [Pawdroid/Free-servers](https://github.com/Pawdroid/Free-servers), 节点数量: `10`
- [pojiezhiyuanjun/freev2](https://github.com/pojiezhiyuanjun/freev2), 节点数量: `130`
- [Nodefree.org](https://github.com/Fukki-Z/nodefree), 节点数量: `50`
- [xiyaowong/freeFQ](https://github.com/xiyaowong/freeFQ), 节点数量: `143`
- [freefq/free](https://github.com/freefq/free), 节点数量: `26`
- [learnhard-cn/free_proxy_ss](https://github.com/learnhard-cn/free_proxy_ss), 节点数量: `113`
- [vpei/Free-Node-Merge](https://github.com/vpei/Free-Node-Merge), 节点数量: `159`
- [huwo1/proxy_nodes/](https://bitbucket.org/huwo1/proxy_nodes/), 节点数量: `183`
- [oslook/clash-freenode](https://github.com/oslook/clash-freenode), 节点数量: `42`
- [openRunner/clash-freenode](https://github.com/openRunner/clash-freenode), 节点数量: `42`
- [yu-steven/openit](https://github.com/yu-steven/openit), 节点数量: `75`
- [kxswa/k](https://github.com/kxswa/k), 节点数量: `90`
- [ermaozi/get_subscribe](https://github.com/ermaozi/get_subscribe), 节点数量: `50`
- [changfengoss](https://github.com/ronghuaxueleng/get_v2), 节点数量: `5`
- [anaer/Sub](https://github.com/anaer/Sub), 节点数量: `161`
- [mianfeifq/share](https://github.com/mianfeifq/share), 节点数量: `233`
- [free886.herokuapp.com](https://free886.herokuapp.com/), 节点数量: `26`
- [wxshi.top:9090](http://wxshi.top:9090/), 节点数量: `0`
- [proxies.bihai.cf](https://proxies.bihai.cf/), 节点数量: `669`
- [proxypool.918848.xyz](http://proxypool.918848.xyz/), 节点数量: `7`
- [sspool.herokuapp.com](http://sspool.herokuapp.com/ ), 节点数量: `44`
- [hellopool.herokuapp.com](https://hellopool.herokuapp.com/ ), 节点数量: `0`
- [fq.lonxin.net](https://fq.lonxin.net/), 节点数量: `0`
- [paimonhub/Paimonnode/](https://github.com/paimonhub/Paimonnode/), 节点数量: `117`
- [wrfree/free](https://github.com/wrfree/free), 节点数量: `26`
- [Jsnzkpg/Jsnzkpg](https://github.com/Jsnzkpg/Jsnzkpg), 节点数量: `63`
- [aiboboxx/v2rayfree](https://github.com/aiboboxx/v2rayfree), 节点数量: `36`
- [3wking](http://clash.3wking.com:12580), 节点数量: `22`
- [Leon406/SubCrawler](https://github.com/Leon406/SubCrawler), 节点数量: `3583`
- [1808.ga](https://1808.ga/), 节点数量: `7`
- [gitlab.com/univstar1](https://gitlab.com/univstar1/v2ray/), 节点数量: `69`
- [tmp.3320.eu.org/v2ray/](https://tmp.3320.eu.org/v2ray/v2ray.txt), 节点数量: `16`
- [ripaojiedian/freenode](https://github.com/ripaojiedian/freenode), 节点数量: `17`

## 仓库文档
<details>
  <summary>展开查看仓库文档</summary>

```
fetchPorxy.main
├── .github──workflows──fetchProxy.yml(actions Deploy)
├── config
│   ├── provider
│   │   ├── config.yml(转clash订阅用的配置)
│   │   └── rxconfig.ini(转clash订阅用的ACL4SSR配置)
│   └── sub_list.json(订阅列表)   
├── sub
│   ├── source(收集到的源节点文件)
│   │   ├── list──(存放着订阅列表里每个源的节点数据)
│   │   ├── check.yaml(测速后的节点数据，靠此文件转换成订阅文件)
│   │   ├── sub_merge.txt(爬取到的节点合集url格式)
│   │   ├── sub_merge_base64.txt(爬取到的节点合集base64格式)
│   │   └── sub_merge_yaml.yml(爬取到的节点合集YAML格式)
│   ├── checkBakup(lite测速结果备份)
│   │   ├── out.json(lite测速结果)
│   │   └── speedtest.log(lite测速结果日志)
│   ├── nocheckClash.yml(未测速clash订阅文件)
│   ├── rx(url订阅文件)
│   ├── rx64(base64订阅文件)
│   ├── rxClash.yml(测速后订阅文件)
│   ├── literx(lite测速后订阅文件)
│   └── literxClash.yml(lite测速后订阅文件)
├── utils(程序功能模块)
│   ├── fetch(获取)
│   │   ├── ip_update.py(下载country.mmdb文件，默认output->'./country.mmdb')
│   │   ├── list_update.py(更新订阅列表sub_list.json，'有变换订阅地址的需更新')
│   │   ├── list_merge.py(主程序，获取订阅存放到'./sub/source/'里面的3种格式，更新README.md里面的订阅源信息)
│   │   └── sub_convert.py(转换订阅格式的功能模块，用到了'tindy2013/subconverter')
│   ├── checkclash(测速)
│   │   ├── config.yaml(配置文件，里面设置，源文件位置，输出文件位置)
│   │   ├── init.py(里面设置config.yaml文件位置)
│   │   ├── main.py(多线程测速)
│   │   ├── clash.py(main调用模块)
│   │   ├── check.py(main调用模块)
│   │   └── requirements.txt(此模块依赖库)
│   ├── convert2sub(转换成订阅)
│   │   ├── ip_update.py(下载country.mmdb文件，默认output->'./country.mmdb')
│   │   ├── convert2sub.py(转换节点文件到'./sub/'目录下的订阅文件)
│   │   └── sub_convert.py(转换订阅格式的功能模块，用到了'tindy2013/subconverter')
│   ├── litespeedtest(lite测速模块)
│   │   ├── lite2sub -测速完成后转clash订阅
│   │ 	│	├── convert2sub.py(转换节点文件到'./sub/'目录下的订阅文件)
│   │ 	│	└── sub_convert.py(转换订阅格式的功能模块，用到了'tindy2013/subconverter')
│   │   ├── clash_config.yml(clash配置文件，测速要用到)
│   │   ├── lite_config.json(测速lite配置文件，设置测速文件位置等)
│   │   ├── proxychains.conf(Action要用此代理打开lite测速才不会卡住不动)
│   │   ├── speedtest.sh(lite测速运行,输出out.json,speedtest.log)
│   │   └── output.py(将测速结果out.json，转换成url订阅'./sub/literx')
│   └── requirements.txt(依赖库)
└── README.md
```
</details>

### 使用注意
>转码功能用到的`subconverter工具`
>
>测速功能用到的`clash工具`
>
>IP库`country.mmdb`,
>
>测速工具`LiteSpeedTest`
>
>已备份到'rx/all/githubTools'

## 仓库声明
订阅节点仅作学习交流使用，只是对网络上节点的优选排序，用于查找资料，学习知识，不做任何违法行为。所有资源均来自互联网，仅供大家交流学习使用，出现违法问题概不负责。
