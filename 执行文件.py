import pandas as pd
import Cui as C
from pandas import Period


# 描述符，规范输入值的范围
class year:
    def __init__(self, data):
        self.data = data

    def __set__(self, instance, value):
        if value >= 2015:
            instance.__dict__[self.data] = value
        else:
            raise ValueError('统计年份必须大于等于2015年')


# 运行过程
class Progress:
    year = year('year')
    def __init__(self, folder_dir, file_dir, year, content):
        # 文件夹路径
        self.folder_dir = folder_dir
        self.file_dir = file_dir
        # 文件夹内文件绝对路径的列表
        self.file_list = C.Folder(self.folder_dir).files()
        # 合并了之后的文件绝对路径列表（每一个表的列标签都不相同）
        self.files = C.Concat(self.file_list).reading().dealing()
        # 经过concat和merge操作之后的表格
        self.file = C.Data_Cleaning(self.files).turn()
        # 明细表筛选列
        self.content = content
        # 创建excel对象，写入多个sheet
        self.writer = pd.ExcelWriter(self.file_dir)
        self.year = year
        self.period = pd.Period(self.year, freq='M')

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

    # 调整表格顺序
    @staticmethod
    def reorder(df):
        columns = list(df.columns.sort_values())
        df = df[columns]
        return df


    # 生成数据透视表
    def pivot_df(self):
        self.file[self.content].to_excel(self.writer, sheet_name='基础表')
        self.writer.save()
        self.file = self.file.set_index('签约日期').to_period('M').reset_index()
        if '是否一晋' in self.file.columns:
            # 去重
            self.file.drop_duplicates('销售人员代码', inplace=True)
            self.file['渠道'].dropna()
            # 生成一晋和三晋的数据透视表
            df = pd.pivot_table(self.file[(self.file['签约日期']>=self.period) & (self.file['签约日期']<(self.period+12))], index=['单位'], columns=['渠道', '签约日期', '是否一晋'], values=['销售人员代码'], aggfunc='count')
            df_1 = pd.pivot_table(self.file[(self.file['签约日期']>=(self.period-3)) & (self.file['签约日期']<(self.period+9))], index=['单位'], columns=['渠道', '签约日期', '是否三晋'], values=['销售人员代码'], aggfunc='count')

            # 需要使用@classmethod处理数据透视表
            Progress.dealing(df).to_excel(self.writer, sheet_name='一晋')
            Progress.dealing(df_1).to_excel(self.writer, sheet_name='三晋')
            self.writer.save()

            if '是否七留' in self.file.columns:
                # 生成七留和十三留的数据透视表
                df_2 = pd.pivot_table(self.file[(self.file['签约日期']>=(self.period-6)) & (self.file['签约日期']<(self.period+6))], index='单位', columns=['渠道', '签约日期', '是否七留'], values='销售人员代码', aggfunc='count')
                df_3 = pd.pivot_table(self.file[(self.file['签约日期']>=(self.period-12)) & (self.file['签约日期']<(self.period))], index='单位', columns=['渠道', '签约日期', '是否十三留'], values='销售人员代码', aggfunc='count')

                # 需要使用@classmethod处理数据透视表
                Progress.dealing(df_2).to_excel(self.writer, sheet_name='七留')
                Progress.dealing(df_3).to_excel(self.writer, sheet_name='十三留')
                self.writer.save()
            else:
                pass

        elif '是否七留' in self.file.columns:
            # 生成七留和十三留的数据透视表
            df_2 = pd.pivot_table(
                self.file[self.file['签约日期'] >= (self.period - 6) and self.file['签约日期'] < (self.period + 6)], index='单位',
                columns=['渠道', '签约日期', '是否七留'], values='销售人员代码', aggfunc='count')
            df_3 = pd.pivot_table(
                self.file[self.file['签约日期'] >= (self.period) and self.file['签约日期'] < (self.period + 12)], index='单位',
                columns=['渠道', '签约日期', '是否十三留'], values='销售人员代码', aggfunc='count')

            # 需要使用@classmethod处理数据透视表
            Progress.dealing(df_2).to_excel(self.writer, sheet_name='七留')
            Progress.dealing(df_3).to_excel(self.writer, sheet_name='十三留')
            self.writer.save()

        # 没有相应指标，返回合并的表格
        else:
            pass

    # 处理数据透视表方法
    @classmethod
    def dealing(cls, df):
        if '是否七留' in df.columns.names or '是否十三留' in df.columns.names:
            df = df.rename({'是': '留存人数', '否': '未留存人数'}, axis=1)
            # 选取最下层标签
            for *content, indicator in df.columns.values:
                if '留存人数' in df[tuple(content)].columns and '未留存人数' in df[tuple(content)].columns:
                    df = df.fillna(0)
                    df[(*content, '入司人数')] = df[(*content, '留存人数')] + df[(*content, '未留存人数')]
                    df[(*content, '留存率')] = df[(*content, '留存人数')]/df[(*content, '入司人数')]
                    df[(*content, '留存率')] = df[(*content, '留存率')].apply(lambda x: format(x, '.2%'))
                    # del df[(*content, '未留存人数')]
                    df[tuple(content)] = df[tuple(content)].reindex(['留存率', '留存人数', '未留存人数', '入司人数'], axis=1)
                else:
                    if '未留存人数' not in df[tuple(content)].columns:
                        df[(*content, '未留存人数')] = [0]* len(df.index)
                        df = df.fillna(0)
                        df[(*content, '入司人数')] = df[(*content, '未留存人数')] + df[(*content, '留存人数')]
                        df[(*content, '留存率')] = df[(*content, '留存人数')] / df[(*content, '入司人数')]
                        df[(*content, '留存率')] = df[(*content, '留存率')].apply(lambda x: format(x, '.2%'))
                        # del df[(*content, '未留存人数')]
                        df[tuple(content)] = df[tuple(content)].reindex(['留存率', '留存人数', '未留存人数', '入司人数'], axis=1)
                    else:
                        df[(*content, '留存人数')] = [0] * len(df.index)
                        df = df.fillna(0)
                        df[(*content, '入司人数')] = df[(*content, '未留存人数')] + df[(*content, '留存人数')]
                        df[(*content, '留存率')] = df[(*content, '留存人数')] / df[(*content, '入司人数')]
                        df[(*content, '留存率')] = df[(*content, '留存率')].apply(lambda x: format(x, '.2%'))
                        # del df[(*content, '未留存人数')]
                        df[tuple(content)] = df[tuple(content)].reindex(['留存率', '留存人数', '未留存人数', '入司人数'], axis=1)

            # 返回处理后的表格
            return Progress.reorder(df)

        elif '是否一晋' in df.columns.names or '是否三晋' in df.columns.names:
            df = df.rename({'是': '转正人数', '否': '未转正人数'}, axis=1)
            for *content, indicator in df.columns.values:
                if '转正人数' in df[tuple(content)].columns and '未转正人数' in df[tuple(content)].columns:
                    df = df.fillna(0)
                    df[(*content, '入司人数')] = df[(*content, '未转正人数')] + df[(*content, '转正人数')]
                    df[(*content, '转正率')] = df[(*content, '转正人数')]/df[(*content, '入司人数')]
                    df[(*content, '转正率')] = df[(*content, '转正率')].apply(lambda x: format(x, '.2%'))
                    # del df[(*content, '未转正人数')]
                    df[tuple(content)] = df[tuple(content)].reindex(['转正率', '转正人数', '未转正人数', '入司人数'], axis=1)
                else:
                    if '转正人数' not in df[tuple(content)].columns:
                        df[(*content, '转正人数')] = [0] * len(df.index)
                        df = df.fillna(0)
                        df[(*content, '入司人数')] = df[(*content, '未转正人数')] + df[(*content, '转正人数')]
                        df[(*content, '转正率')] = df[(*content, '转正人数')] / df[(*content, '入司人数')]
                        df[(*content, '转正率')] = df[(*content, '转正率')].apply(lambda x: format(x, '.2%'))
                        # del df[(*content, '未转正人数')]
                        df[tuple(content)] = df[tuple(content)].reindex(['转正率', '转正人数', '未转正人数', '入司人数'], axis=1)
                    else:
                        df[(*content, '未转正人数')] = [0] * len(df.index)
                        df = df.fillna(0)
                        df[(*content, '入司人数')] = df[(*content, '未转正人数')] + df[(*content, '转正人数')]
                        df[(*content, '转正率')] = df[(*content, '转正人数')] / df[(*content, '入司人数')]
                        df[(*content, '转正率')] = df[(*content, '转正率')].apply(lambda x: format(x, '.2%'))
                        # del df[(*content, '未转正人数')]
                        df[tuple(content)] = df[tuple(content)].reindex(['转正率', '转正人数', '未转正人数', '入司人数'], axis=1)
            # 返回处理后的表格
            return Progress.reorder(df)
        else:
            pass



# 设置需要处理的文件夹
# folder_dir = input('请输入需要处理的文件夹的绝对路径')
folder_dir = r'C:\Users\崔晓冰\Desktop\做数'
# 设置输出的文件
file_dir = r'C:\Users\崔晓冰\Desktop\处理.xlsx'
# 设置选取的年份
# year = input('请输入需查询的年份')
year = 2021
# 设置明细表需要显示的列,如果不需要筛选，content = [:]
content = ['单位', '渠道', '职场名称',  '销售人员代码', '姓名', '签约日期', '是否一晋', '是否三晋', '是否七留', '是否十三留']

# 运算过程
File = Progress(folder_dir, file_dir, year, content)
File.roller()
File.pivot_df()

