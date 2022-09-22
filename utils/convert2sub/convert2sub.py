import re, yaml
import time, os

from sub_convert import sub_convert
from ip_update import geoip_update

# 未测速转clash
input_source_file = './sub/source/sub_merge_base64.txt'
output_nocheck_file = './sub/nocheckClash.yml'

# 已测速转url,base64,clash
input_check_file = './sub/source/check.yaml'    # 需要查看checkclash文件夹里面config配置文件设置的地址
output_url_path = './sub/rx'
output_base64_path =  './sub/rx64'
output_clash_path = './sub/rxClash.yml' 

#备份节点路径
bakup_path = './sub/bakup/'

#转clash用的provider
config_file = './config/provider/config.yml'

#如要备份下面的providers_files需用到，不备份无用
provider_path = './config/provider/'   

class NoAliasDumper(yaml.SafeDumper): # https://ttl255.com/yaml-anchors-and-aliases-and-how-to-disable-them/
    def ignore_aliases(self, data):
        return True

def eternity_convert(file, config, output, provider_file_enabled=True):
    
    file_eternity = open(file, 'r', encoding='utf-8')
    sub_content = file_eternity.read()
    file_eternity.close()
    all_provider = sub_convert.main(sub_content,'content','YAML',custom_set={'dup_rm_enabled': False,'format_name_enabled': True})
    # 创建并写入 provider 
    lines = re.split(r'\n+', all_provider)
    
    proxy_all = []
    cn_proxy = []
    jp_proxy = []
    sg_proxy = []
    us_proxy = []
    other_proxy = []

    for line in lines:
        if line != 'proxies:' and 'plugin' not in line:
            line = '  ' + line
            proxy_all.append(line)    # 如使用，不要忘记去掉上面 `proxy_all = []` 前面的 #

            if 'HK' in line or '香港' in line or 'CN' in line or '中国' in line or 'TW' in line or '台湾' in line:
                cn_proxy.append(line)
            elif 'JP' in line or '日本' in line:
                jp_proxy.append(line)
            elif 'SG' in line or '新加坡' in line:
                sg_proxy.append(line)
            elif 'US' in line or '美国' in line:
                us_proxy.append(line)
            else:
                other_proxy.append(line)
                
    allproxy_provider = 'proxies:\n' + '\n'.join(proxy_all)
    cn_provider = 'proxies:\n' + '\n'.join(cn_proxy)
    jp_provider = 'proxies:\n' + '\n'.join(jp_proxy)
    sg_provider = 'proxies:\n' + '\n'.join(sg_proxy)
    us_provider = 'proxies:\n' + '\n'.join(us_proxy)
    other_provider = 'proxies:\n' + '\n'.join(other_proxy)
    
    if provider_file_enabled:
        """
        #下面备份providers_files要用到
        providers_files = {
            'all': provider_path + 'provider-all.yml',
            'cn': provider_path + 'provider-cn.yml',
            'jp': provider_path + 'provider-jp.yml',
            'sg': provider_path + 'provider-sg.yml',
            'us': provider_path + 'provider-us.yml',
            'other': provider_path + 'provider-other.yml'
            
        }
        """
        eternity_providers = {
            'all': allproxy_provider,
            'cn': cn_provider,
            'jp': jp_provider,
            'sg': sg_provider,
            'us': us_provider,
            'other': us_provider
        }
        """
        #备份providers_files,需要先打开上面 providers_files数据组
        print('Writing content to ./provider/***')
        for key in providers_files.keys():
            provider_all = open(providers_files[key], 'w', encoding= 'utf-8')
            provider_all.write(eternity_providers[key])
            provider_all.close()
        print('./provider/***, Done!\n')
        """

    # 创建完全配置的Eternity.yml
    config_f = open(config_file, 'r', encoding='utf-8')
    config_raw = config_f.read()
    config_f.close()
    
    config = yaml.safe_load(config_raw)

    all_provider_dic = {'proxies': []}
    cn_provider_dic = {'proxies': []}
    jp_provider_dic = {'proxies': []}
    sg_provider_dic = {'proxies': []}
    us_provider_dic = {'proxies': []}
    other_provider_dic = {'proxies': []}
    
    provider_dic = {
        'all': all_provider_dic,
        'cn': cn_provider_dic,
        'jp': jp_provider_dic,
        'sg': sg_provider_dic,
        'us': us_provider_dic,
        'other': other_provider_dic
    }
    for key in eternity_providers.keys(): # 将节点转换为字典形式
        provider_load = yaml.safe_load(eternity_providers[key])
        provider_dic[key].update(provider_load)

    # 创建节点名列表
    all_name = []   
    cn_name = [] 
    jp_name = [] 
    sg_name = []
    us_name = []
    other_name = []
    
    name_dict = {
        'all': all_name,
        'cn': cn_name,
        'jp': jp_name,
        'sg': sg_name,
        'us': us_name,
        'other': us_name
    }
    for key in provider_dic.keys():
        if not provider_dic[key]['proxies'] is None:
            for proxy in provider_dic[key]['proxies']:
                name_dict[key].append(proxy['name'])
        if provider_dic[key]['proxies'] is None:
            name_dict[key].append('DIRECT')
    # 策略分组添加节点名
    proxy_groups = config['proxy-groups']
    proxy_group_fill = []
    for rule in proxy_groups:
        if rule['proxies'] is None: # 不是空集加入待加入名称列表
            proxy_group_fill.append(rule['name'])
    for rule_name in proxy_group_fill:
        for rule in proxy_groups:
            if rule['name'] == rule_name:
                rule.update({'proxies': all_name})
                
                if '香港' in rule_name or '中国' in rule_name or '台湾' in rule_name:
                    rule.update({'proxies': cn_name})
                elif '日本' in rule_name:
                    rule.update({'proxies': jp_name})
                elif '狮城' in rule_name or '新加坡' in rule_name:
                    rule.update({'proxies': sg_name})
                elif '美国' in rule_name:
                    rule.update({'proxies': us_name})
                elif '其他节点' in rule_name:
                    rule.update({'proxies': other_name})
                else:
                    rule.update({'proxies': all_name})
    config.update(all_provider_dic)
    config.update({'proxy-groups': proxy_groups})

    """
    yaml_format = ruamel.yaml.YAML() # https://www.coder.work/article/4975478
    yaml_format.indent(mapping=2, sequence=4, offset=2)
    config_yaml = yaml_format.dump(config, sys.stdout)
    """
    config_yaml = yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True, width=750, indent=2, Dumper=NoAliasDumper)
    
    Eternity_yml = open(output, 'w+', encoding='utf-8')
    Eternity_yml.write(config_yaml)
    Eternity_yml.close()

def backup(file):
    t = time.localtime()
    date = time.strftime('%y%m', t)
    date_day = time.strftime('%y%m%d', t)

    file_eternity = open(file, 'r', encoding='utf-8')
    sub_content = file_eternity.read()
    file_eternity.close()

    try:
        os.mkdir(f'{bakup_path}{date}')
    except FileExistsError:
        pass
    txt_dir = bakup_path + date + '/' + date_day + '.txt' # 生成$MM$DD.txt文件名
    file = open(txt_dir, 'w', encoding= 'utf-8')
    file.write(sub_convert.base64_decode(sub_content))
    file.close()

if __name__ == '__main__':
    #更新IP库
    geoip_update()

#    #将没测速节点直接转成yaml订阅，并备份
#    print('write nocheckClash begin!')
#    eternity_convert(input_source_file, config_file, output=output_nocheck_file)
#    print('write nocheckClash Over!')
#    backup(input_source_file)
#    print('backup done!')

    # 将测速完的check内容转成url节点内容
    input_check_file_path = os.path.abspath(input_check_file)   #python获取绝对路径https://www.jianshu.com/p/1563374e279a
    subContent = sub_convert.convert_remote(input_check_file_path, 'url', 'http://127.0.0.1:25500')
    # 写入url 订阅文件
    print('write rx url sub content!')
    file = open(output_url_path, 'w', encoding= 'utf-8')
    file.write(subContent)
    file.close()

    # 写入base64 订阅文件
    subContent = sub_convert.base64_encode(subContent)
    print('write rx64 sub content!')
    file = open(output_base64_path, 'w', encoding= 'utf-8')
    file.write(subContent)
    file.close()

   # 写入Clash 订阅文件
    print('write RXClash begin!')
    eternity_convert(output_base64_path, config_file, output=output_clash_path)
    print('write RXClash Over!')

