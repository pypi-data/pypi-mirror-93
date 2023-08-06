import os


def main():
    categories = {'1': 'Internet', '2': "Chat", '3': 'Music', '4': 'Video', '5': 'Graphics', '6': 'Games',
                  '7': 'Office', '8': 'Reading', '9': 'Development', '10': 'System'}
    print('请选择分类')
    for i, j in categories.items():
        print(i, j)
    print('其他分类可以直接键入')
    cate = input('')
    if cate in categories:
        category = categories[cate]
    else:
        category = cate

    comment = input('请输入介绍\n')
    exec = input('请输入文件绝对路径\n')
    while True:
        if not os.path.exists(exec):
            print("启动文件路径不正确")
            exec = input('')
        else:
            break
    icon = input('请输入图标文件绝对路径\n')
    while True:
        if not os.path.exists(exec):
            print("图标路径不正确")
            icon = input('')
        else:
            break
    name = input('请输入名称\n')
    text = '''[Desktop Entry]
Categories={categories};
Comment={comment}
Exec="{exec}" %f
Icon={icon}
Name={name}
Terminal=false
Type=Application
Version=1.0
    '''
    text = text.format(categories=category, comment=comment, exec=exec, icon=icon, name=name)
    file_name = name + '.desktop'
    with open(os.path.expanduser('~/.local/share/applications/') + file_name, 'w') as f:
        f.write(text)
    print("生成成功")


if __name__ == '__main__':
    main()
