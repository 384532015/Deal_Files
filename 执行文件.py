import Cui as C

folder_dir = r'C:\Users\崔晓冰\Desktop\做数'


# 运行过程
def all_progress(folder_dir):
    # 这是一个列表（元素为各文件的绝对路径）
    file_list = C.Folder(folder_dir).files()

    # 这是一个列表（元素为列标签都不相同的DataFrame）
    files = C.Dealing(file_list).reading().dealing()

    # 这是最终的完整的DataFrame（但是没有计算相应指标）
    new_file = C.DeepDealing(files).turn
    new_file.to_excel(r'C:\Users\崔晓冰\Desktop\合并.xlsx')

    # 加入一晋、三晋、七留、十三留的DataFrame
    ultimate_file = C.Assessment(new_file).dealing()
    print(ultimate_file)

    if ('是否一晋' | '是否七留') not in ultimate_file.columns:
        ultimate_file.to_excel(r'C:\Users\崔晓冰\Desktop\合并.xlsx')

    else:
        ultimate_file.drop_duplicates('销售人员代码', inplace=True)
        ultimate_file['渠道'].dropna(inplace=True)

        # 明细表导出
        ultimate_file.to_excel(r'C:\Users\crl\Desktop\处理.xlsx')

        # 数据透视表
        ultimate_file.pivot_table(['是否一晋', '是否三晋'], index='基层销售机构名称', columns='销售人员代码', margins=True)

all_progress(folder_dir)
