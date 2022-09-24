import os
from sub_convert import sub_convert

#文件位置
input_source_file = './sub/literx'
output_file = './sub/literxClash.yml'

if __name__ == '__main__':
    #转换
    input_check_file_path = os.path.abspath(input_source_file)  # 获取文件路径
    print（str(input_check_file_path)+'\n'）
    content = sub_convert.convert_remote(input_check_file_path,'clash',sub_convert.use_urlhost())   #转换
    print(content)
    #写入
    file = open(output_file, 'w', encoding= 'utf-8')
    file.write(content)
    file.close()
    print(f'Writing content done！\n')
