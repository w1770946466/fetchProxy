import os
from sub_convert import sub_convert

#文件位置
# 未测速转clash
input_source_file = './sub/source/sub_merge_base64.txt'
output_nocheck_file = './sub/nocheckClash.yml'

# 已测速转url,base64,clash
input_check_file = './sub/source/check.yaml'    # 需要查看checkclash文件夹里面config配置文件设置的地址
output_url_path = './sub/rx'
output_base64_path =  './sub/rx64'
output_clash_path = './sub/rxClash.yml' 

#--Code begin-------------------------------------------------------------

# 写入文件模块
def write_file(file,content):
    f = open(file, 'w', encoding= 'utf-8')
    f.write(content)
    f.close()

if __name__ == '__main__':
    ## 将未测速的节点内容转成clash订阅
    input_source_file_path = os.path.abspath(input_source_file)  #python获取绝对路径https://www.jianshu.com/p/1563374e279a
    #转换
    content = sub_convert.convert_remote(input_source_file_path,'clash')   
    #写入nocheckClash.yml
    write_file(output_nocheck_file,content)
    
    ## 将测速完的check内容转成url节点内容
    input_check_file_path = os.path.abspath(input_check_file)   #python获取绝对路径https://www.jianshu.com/p/1563374e279a
    #转换
    content = sub_convert.convert_remote(input_check_file_path,'clash')   
    # 写入rxClash.yml 订阅文件
    print('write rxClash.yml content!')
    write_file(output_clash_path,content)
    
    # 写入url 订阅文件
    print('write rx url sub content!')
    content = sub_convert.convert_remote(input_check_file_path,'url')
    write_file(output_url_path,content)

    # 写入base64 订阅文件
    content = sub_convert.base64_encode(content)
    print('write rx64 sub content!')
    write_file(output_base64_path,content)

    
