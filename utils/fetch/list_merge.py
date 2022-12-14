#!/usr/bin/env python3

# --------------------------------------------------------------------------------------
# 脚本第一行写上 #!/usr/bin/env python3 或者 #!/usr/bin/python3的区别：
# #!/usr/bin/python3 表示 python3 所处的绝对路径就是 /usr/bin/python3
# #!/usr/bin/env/ python3 表示从 "PATH 环境变量"中查找 python3 的位置, 更灵活更具有通用性, 推荐使用这种写法
# 详细介绍了`#!/usr/bin/env python3`这行命令https://www.jianshu.com/p/400c612381dd
# --------------------------------------------------------------------------------------
from ip_update import geoip_update  #更新IP位置数据库,将此行放入需要引用的文件里使用'geoip_update()'即可
from sub_convert import sub_convert # Python 之间互相调用文件https://blog.csdn.net/winycg/article/details/78512300
from list_update import update_url  # 调用list_update文件里的update_url类

import json, re, os                 # Python常用模块https://www.cnblogs.com/Mjonj/p/7499560.html
from urllib import request          # Urllib是python内置的HTTP请求库,urllib.request获取URL的Python模块


# 分析当前项目依赖,生成requirements.txt文件 https://blog.csdn.net/lovedingd/article/details/102522094


# 文件路径定义
readme_file_path = './README.md'              # 说明文件

# 爬取源列表文件
sub_list_json = './config/sub_list.json'    

   
sub_merge_path = './sub/source/'                   # 收集爬取的合集存放目录
sub_merge_url = './sub/source/sub_merge.txt'   
sub_merge_base64 = './sub/source/sub_merge_base64.txt'   
sub_merge_yaml = './sub/source/sub_merge_yaml.yml'   

sublist_content_path = './sub/source/list/'               # 订阅列表备份路径

class sub_merge():
    def sub_merge(url_list): # 将转换后的所有 Url 链接内容合并转换 YAML or Base64, ，并输出文件，输入订阅列表。

        content_list = []
        for t in os.walk(sublist_content_path):    # 遍历文件夹
            for f in t[2]:
                f = t[0]+f
                os.remove(f)                # 删除所有的备份

        for index in range(len(url_list)):
            content = sub_convert.convert_remote(url_list[index]['url'],'url','http://127.0.0.1:25500') # 将爬取源url地址爬取的内容存放到content
            ids = url_list[index]['id']
            remarks = url_list[index]['remarks']
            if content == 'Url 解析错误':
                content = sub_convert.main(sub_merge.read_list(sub_list_json)[index]['url'],'url','YAML')
                if content != 'Url 解析错误':
                    content_list.append(content)
                    print(f'Writing content of {remarks} to {ids:0>2d}.txt\n')
                else:
                    print(f'Writing error of {remarks} to {ids:0>2d}.txt\n')
                file = open(f'{sublist_content_path}{ids:0>2d}.txt', 'w+', encoding= 'utf-8')
                file.write('Url 解析错误')
                file.close()
            elif content == 'Url 订阅内容无法解析':
                file = open(f'{sublist_content_path}{ids:0>2d}.txt', 'w+', encoding= 'utf-8')
                file.write('Url 订阅内容无法解析')
                file.close()
                print(f'Writing error of {remarks} to {ids:0>2d}.txt\n')
            elif content != None:
                content_list.append(content)
                file = open(f'{sublist_content_path}{ids:0>2d}.txt', 'w+', encoding= 'utf-8')
                file.write(content)
                file.close()
                print(f'Writing content of {remarks} to {ids:0>2d}.txt\n')
            else:
                file = open(f'{sublist_content_path}{ids:0>2d}.txt', 'w+', encoding= 'utf-8')
                file.write('Url 订阅内容无法解析')
                file.close()
                print(f'Writing error of {remarks} to {ids:0>2d}.txt\n')
                
        print('Merging nodes...\n')
        content_raw = ''.join(content_list) # https://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p14_combine_and_concatenate_strings.html
        content_yaml = sub_convert.main(content_raw,'content','YAML',{'dup_rm_enabled': True, 'format_name_enabled': False})
        with open(sub_merge_yaml, 'w+', encoding='utf-8') as f:
            f.write(content_yaml)
            f.close()
        sub_merge_yaml_ptch = os.path.abspath(sub_merge_yaml)  #python获取绝对路径https://www.jianshu.com/p/1563374e279a
        content_raw = sub_convert.convert_remote(sub_merge_yaml_ptch, output_type='url', host='http://127.0.0.1:25500')
        content_base64 = sub_convert.base64_encode(content_raw)
        content = content_raw
        file = open(f'{sub_merge_url}', 'w+', encoding= 'utf-8')
        file.write(content_raw)
        file.close()
        with open(sub_merge_base64, 'w+', encoding='utf-8') as f:
            f.write(content_base64)
            f.close()

    def read_list(json_file,remote=False):  # 将 sub_list.json    爬取源Url内容读取为列表
        with open(json_file, 'r', encoding='utf-8') as f:
            raw_list = json.load(f)         # json格式获取list内容，暂时存放到raw_list
        input_list = []
        for index in range(len(raw_list)):
            if raw_list[index]['enabled']:  # 如果enabled启用 == true （根据节点源的好坏，决定是否启用）
                if remote == False:         # 如果 remote偏僻，遥远 == False
                    urls = re.split('\|',raw_list[index]['url'])    # 多订阅地址的爬取源，只取第一个地址？
                else:
                    urls = raw_list[index]['url']                   # 多订阅地址的爬取源所有地址都添加
                raw_list[index]['url'] = urls
                input_list.append(raw_list[index])
        return input_list                   # 将sub_list.json里面的所有url存放到input_list返回

    def readme_update(readme_file=readme_file_path, sub_list=[]): # 更新 README 节点信息
        print('更新 README.md 中')
        with open(readme_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            f.close()
        # 获得当前名单及各仓库节点数量
        with open(sub_merge_url, 'r', encoding='utf-8') as f:
            total = len(f.readlines())
            total = f'合并节点总数: `{total}`\n'
            thanks = []
            repo_amount_dic = {}
            for repo in sub_list:
                line = ''
                if repo['enabled'] == True:
                    id = repo['id']
                    remarks = repo['remarks']
                    repo_site = repo['site']

                    sub_file = f'{sublist_content_path}{id:0>2d}.txt'
                    with open(sub_file, 'r', encoding='utf-8') as f:
                        proxies = f.readlines()
                        if proxies == ['Url 解析错误'] or proxies == ['订阅内容解析错误']:
                            amount = 0
                        else:
                            amount = len(proxies)
                        f.close()
                    repo_amount_dic.setdefault(id, amount)
                    line = f'- [{remarks}]({repo_site}), 节点数量: `{amount}`\n'
                if remarks != "alanbobs999/TopFreeProxies":
                    thanks.append(line)
            f.close()
        """
        # 高速节点打印
        for index in range(len(lines)):
            if lines[index] == '### 高速节点\n': # 目标行内容
                # 清除旧内容
                lines.pop(index+1) # 删除节点数量
                while lines[index+4] != '\n':
                    lines.pop(index+4)

                with open('./Eternity', 'r', encoding='utf-8') as f:
                    proxies_base64 = f.read()
                    proxies = sub_convert.base64_decode(proxies_base64)
                    proxies = proxies.split('\n')
                    proxies = ['    '+proxy for proxy in proxies]
                    proxies = [proxy+'\n' for proxy in proxies]
                top_amount = len(proxies)
                
                lines.insert(index+1, f'高速节点数量: `{top_amount}`\n')
                index += 4
                for i in proxies:
                    index += 1
                    lines.insert(index, i)
                break
        """
        # 所有节点打印
        for index in range(len(lines)):
            if lines[index] == '### 所有节点\n': # 目标行内容
                # 清除旧内容
                lines.pop(index+1) # 删除节点数量

                with open(sub_merge_url, 'r', encoding='utf-8') as f:
                    proxies = f.read()
                    proxies = proxies.split('\n')
                    top_amount = len(proxies) - 1
                    f.close()
                lines.insert(index+1, f'合并节点总数: `{top_amount}`\n')
                """
                with open('./sub/sub_merge.txt', 'r', encoding='utf-8') as f:
                    proxies = f.read()
                    proxies = proxies.split('\n')
                    proxies = ['    '+proxy for proxy in proxies]
                    proxies = [proxy+'\n' for proxy in proxies]
                top_amount = len(proxies) - 1
                
                lines.insert(index+1, f'合并节点数量: `{top_amount}`\n')
                
                index += 5
                for i in proxies:
                    index += 1
                    lines.insert(index, i)
                """
                break
        # 节点来源打印
        for index in range(len(lines)):
            if lines[index] == '### 节点来源\n':
                # 清除旧内容
                while lines[index+1] != '\n':
                    lines.pop(index+1)

                for i in thanks:
                    index +=1
                    lines.insert(index, i)
                break


        # 写入 README 内容
        with open(readme_file, 'w', encoding='utf-8') as f:
            data = ''.join(lines)
            print('README.md write 完成!\n')
            f.write(data)

# if __name__ == '__main__'当模块被直接运行时以下代码块将被运行，当模块是被导入时，代码块不被运行
# 详细讲解：https://blog.konghy.cn/2017/04/24/python-entry-program/
if __name__ == '__main__':
# 准备工作
    update_url.update_main()                                    # 更新爬取源sub_list_json
    geoip_update()                                              # 更新IP位置数据库
# 开始正题
    sub_list = sub_merge.read_list(sub_list_json)               # 从sub_list_json读取爬取源的url放入sub_list
    sub_list_remote = sub_merge.read_list(sub_list_json,True)   # 多订阅地址的爬取源所有url都添加到sub_list_remote列表
    sub_merge.sub_merge(sub_list_remote)                        # 转换后的所有 Url 链接内容合并转换 YAML or Base64, 并输出文件sub_merge.txt，sub_merge_base64.txt，sub_merge_yaml.yml
#    sub_merge.readme_update(readme_file_path,sub_list)                    # 更新 README 节点信息
