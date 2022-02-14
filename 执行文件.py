import Cui as C
import pandas as pd

folder_dir = r'C:\Users\崔晓冰\Desktop\做数'


# 运行过程
def all_progress(folder_dir):
    # 这是一个列表（元素为各文件的绝对路径）
    file_list = C.Folder(folder_dir).files()

    # 这是一个列表（元素为列标签都不相同的DataFrame）
    files = C.Concat(file_list).reading().dealing()

    # 这是最终的完整的DataFrame（但是没有计算相应指标）
    new_file = C.Data_Cleaning(files).turn()

    # 加入一晋、三晋、七留、十三留的DataFrame
    ultimate_file = C.Assessment(new_file)
    ultimate_file.one
    ultimate_file.three
    ultimate_file.seven_kill
    ultimate_file.thirteen_kill

    global df
    df = ultimate_file.df

    if '是否一晋' not in df.columns:
        if '是否七留' not in df.columns:
            df.to_excel(r'C:\Users\崔晓冰\Desktop\合并.xlsx')

    else:
        df.drop_duplicates('销售人员代码', inplace=True)
        df['渠道'].dropna(inplace=True)

        # 明细表导出
        # df.to_excel(r'C:\Users\崔晓冰\Desktop\处理.xlsx')

        # 数据透视表
        df = df.set_index('签约日期')
        df.to_excel(r'C:\Users\崔晓冰\Desktop\处理.xlsx')
        df = df.to_period('M')
        df_pivot = pd.pivot_table(df[df['签约日期']>='2021-10-01'], index=['单位'], columns=['渠道', '签约日期', '是否三晋'], values=['销售人员代码'], aggfunc='count')
        df_pivot = df_pivot.rename({'是':'三晋人数', '否':'三晋率'}, axis=1)
        print(df_pivot)


all_progress(folder_dir)

