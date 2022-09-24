from sub_convert import sub_convert

if __name__ == '__main__':
    subscribe = 'https://raw.githubusercontent.com/rxsweet/fetchProxy/main/sub/rx64'
    output_path = './output.yml'

    content = sub_convert.convert_remote(subscribe,'clash',sub_convert.use_urlhost())
    file = open(output_path, 'w', encoding= 'utf-8')
    file.write(content)
    file.close()
    print(f'Writing content to output.yml\n')
