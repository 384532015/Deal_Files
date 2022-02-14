import numpy as np
import pandas as pd
import Cui as C

folder_dir = r'C:\Users\崔晓冰\Desktop\做数'
file_dir = r'C:\Users\崔晓冰\Desktop\处理.xlsx'


# 运行过程
class Progress:
    def __init__(self, folder_dir, file_dir):
        # 文件夹路径
        self.folder_dir = folder_dir
        self.file_dir = file_dir
        # 文件夹内文件绝对路径的列表
        self.file_list = C.Folder(self.folder_dir).files()
        # 合并了之后的文件绝对路径列表（每一个表的列标签都不相同）
        self.files = C.Concat(self.file_list).reading().dealing()
        # 经过concat和merge操作之后的表格
        self.file = C.Data_Cleaning(self.files).turn()
        # # 带有计算结果的明细表
        # self.df = pd.DataFrame()
        # 创建excel对象，写入多个sheet
        self.writer = pd.ExcelWriter(self.file_dir)

    # 生成带有计算结果的明细表
    def roller(self):
        # 实例化
        ultimate_file = C.Assessment(self.file)
        # 经过处理
        ultimate_file.one
        ultimate_file.three
        ultimate_file.seven_kill
        ultimate_file.thirteen_kill
        # 重新给self.file赋值
        self.file = ultimate_file.df

        return self.file

    # 生成数据透视表
    def pivot_df(self):
        if '是否一晋' in self.file.columns:
            # 去重
            self.file.drop_duplicates('销售人员代码', inplace=True)
            self.df['渠道'].dropna(inplace=True)
            # 生成一晋和三晋的数据透视表
            df = pd.pivot_table(self.file, index='单位', columns=['渠道', '签约日期', '是否一晋'], values='销售人员代码', aggfunc='count')
            df_1 = pd.pivot_table(self.file, index='单位', columns=['渠道', '签约日期', '是否三晋'], values='销售人员代码', aggfunc='count')
            # 需要使用@classmethod处理数据透视表
            Progress.dealing(df).to_excel(self.writer, sheet_name='一晋')
            Progress.dealing(df_1).to_excel(self.writer, sheet_name='三晋')
            self.writer.save()


            if '是否七留' in self.file.columns:
                # 生成七留和十三留的数据透视表
                df_2 = pd.pivot_table(self.file, index='单位', columns=['渠道', '签约日期', '是否七留'], values='销售人员代码', aggfunc='count')
                df_3 = pd.pivot_table(self.file, index='单位', columns=['渠道', '签约日期', '是否十三留'], values='销售人员代码', aggfunc='count')
                # 需要使用@classmethod处理数据透视表
                Progress.dealing(df_2).to_excel(self.writer, sheet_name='七留')
                Progress.dealing(df_3).to_excel(self.writer, sheet_name='十三留')
                self.writer.save()
            else:
                pass

        elif '是否七留' in self.file.columns:
            # 生成七留和十三留的数据透视表
            df_2 = pd.pivot_table(self.file, index='单位', columns=['渠道', '签约日期', '是否七留'], values='销售人员代码', aggfunc='count')
            df_3 = pd.pivot_table(self.file, index='单位', columns=['渠道', '签约日期', '是否十三留'], values='销售人员代码', aggfunc='count')
            # 需要使用@classmethod处理数据透视表
            Progress.dealing(df_2).to_excel(self.writer, sheet_name='七留')
            Progress.dealing(df_3).to_excel(self.writer, sheet_name='十三留')
            self.writer.save()

        else:
            self.df.to_excel(self.writer, sheet_name='合并')
            self.writer.save()

    # 处理数据透视表方法
    @classmethod
    def dealing(cls, df):
        if '是否七留' or '是否十三留' in df.columns.names:
            df.rename({'是': '留存人数', '否': '留存率'}, axis=1)
            for channel, date, indicator in df.columns.values:
                df[(channel, date, '入司人数')] = df[(channel, date, '留存率')] + df[(channel, date, '留存人数')]
                df[(channel, date, '留存率')] = df[(channel, date, '留存人数')]/df[(channel, date, '入司人数')]
                df.sort_index(axis=1)
            #返回处理后的表格
            return df

        elif '是否一晋' or '是否三晋' in df.columns.names:
            df.rename({'是': '转正人数', '否': '转正率'}, axis=1)
            for channel, date, indicator in df.columns.values:
                if df[(channel, date, '转正人数')]:
                    df[(channel, date, '入司人数')] = df[(channel, date, '留存率')] + df[(channel, date, '留存人数')]
                    df[(channel, date, '留存率')] = df[(channel, date, '留存人数')]/df[(channel, date, '入司人数')]
                    df.sort_index(axis=1)
                else:
                    df[(channel, date, '转正人数')] = [np.NaN]* len(df.index)
                    df[(channel, date, '入司人数')] = df[(channel, date, '留存率')] + df[(channel, date, '留存人数')]
                    df[(channel, date, '留存率')] = df[(channel, date, '留存人数')] / df[(channel, date, '入司人数')]
                    df.sort_index(axis=1)
            # 返回处理后的表格
            return df


File = Progress(folder_dir,file_dir)
File.roller().pivot_df()

