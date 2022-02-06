import pandas as pd
import os
from datetime import datetime

# 名称转化专用字典
name_turn = {
    '工号': '销售人员代码',
    '销售员代码': '销售人员代码',
    '营销系列': '营销',
    '营销主管系列': '营销',
    '收展员系列': '收展',
    '收展主管系列': '收展',
    '保单服务专员': '收展'
}


# 输入文件路径，生成列表[文件绝对路径]
class Folder:
    def __init__(self, folder_dir):
        self.folder_dir = folder_dir

    # 遍历文件夹内所有文件，并向下遍历，生成内容为文件绝对路径的列表
    def files(self):
        for folder_dir, folders, files in os.walk(self.folder_dir):
            # 返回一个列表生成器
            return [os.path.join(folder_dir, file_name) for file_name in files]


# 输入列表，处理文件的方法(可添加处理方法,但是命名必须以cui_开头）
class Method:
    @classmethod
    def cui_txt(cls,file_dir):
        return pd.read_table(file_dir, sep=',')

    @classmethod
    def cui_excel(cls,file_dir):
        return pd.read_excel(file_dir, sheet_name=0)

    @classmethod
    def cui_csv(cls,file_dir):
        return pd.read_csv(file_dir, sep=',')


# 输入Files绝对路径列表，根据Method类读取文件内容,生成列标签全不相同的文件列表
class Dealing:
    def __init__(self, files):
        self.method_list = [name for name in dir(Method) if name.startswith('cui')]
        self.file_dir_list = files
        self.file_list = []
        self.new_file_list = []

    # 生成含所有表格的列表
    def reading(self):
        for file_dir in self.file_dir_list:
            for method in self.method_list:
                try:
                    if self.file_list.append(eval('{}.{}({})'.format('Method', method, 'file_dir'))):
                        break
                except ValueError:
                    pass
        return self

    # 处理文件的过程
    # 必须先调用reading的方法，才能调用dealing的方法
    def dealing(self):
        # concat操作
        for df in self.file_list:
            self.file_list.remove(df)
            for df_1 in self.file_list:
                if df.columns.all() == df_1.columns.all():
                    df = pd.concat([df, df_1]).drop_duplicates()
                    self.file_list.remove(df_1)
                else:
                    pass
            # 新的文件列表中所有表格的列标签都不完全一致
            self.new_file_list.append(df)
            return self.dealing()
        return self.new_file_list


# 输入文件绝对路径的列表，读取文件，统一格式，merge处理，生成一个df
class DeepDealing:
    def __init__(self, new_file_list):
        self.list = new_file_list
        self.df_rolling = pd.DataFrame()
        DeepDealing.turn(self.list, self.df_rolling)

    # 修改格式，统一标签名称，merge操作等
    @classmethod
    def turn(cls, file_list, df_rolling):
        for df in file_list:
            df.rename(columns= name_turn,inplace= True)
            df['销售人员代码'] = df['销售人员代码'].apply(lambda x: str(x))
            df.set_index(df.销售人员代码,inplace= True)

            # 处理花名册
            if '人员系列' in df.columns:
                df['渠道'] = df['人员系列'].map(name_turn)
                # 处理销售人员代码和时间格式
                try:
                    df['签约日期'] = df['签约日期'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
                except TypeError:
                    pass

                try:
                    df['预解约日期'] = df['预解约日期'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
                except TypeError:
                    pass

                try:
                    df['解约日期'] = df['解约日期'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
                except TypeError:
                    pass

                df_rolling = pd.merge(df_rolling, df, right_index= True, left_index= True, how='outer')

            # 处理历史职级
            elif '考核前职级' and '确认职级' in df.columns:
                # 处理格式
                try:
                    df['统计日期'] = df['统计日期'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
                except ValueError:
                    pass

                # 转正日期
                df_1 = df[(df['考核前职级'] == '营销员' or '准收展员') | (df['确认职级'] == '业务主任' or '收展员')]
                df_1 = df_1.rename({'统计日期': '转正日期'})

                # 晋组日期
                df_2 = df[(df['占培训控制'] == '是' or '否') | (df['确认职级'] == '组经理' or '金质组经理' or '银质组经理')]
                df_2 = df_2.rename({'统计日期': '晋组日期'}, axis='columns')

                # 晋处部日期
                df_3 = df[(df['占培训控制'] == '是' or '否') | (df['确认职级'] == '处经理' or '部经理')]
                df_3 = df_3.rename({'统计日期': '晋处/部日期'}, axis='columns')

                # merge历史职级
                try:
                    df_rolling = pd.merge(df_rolling, df_1, on='销售人员代码', how='outer')
                    df_rolling = pd.merge(df_rolling, df_2, on='销售人员代码', how='outer')
                    df_rolling = pd.merge(df_rolling, df_3, on='销售人员代码', how='outer')

                except BaseException:
                    pass

            # 处理保单明细，可以继续添加功能
            else:
                pass

        return df_rolling


# 添加一晋、三晋、七留、十三留列
class Assessment:
    def __init__(self, df):
        self.df = df

    def dealing(self):
        Assessment.one(self.df)
        Assessment.three(self.df)
        Assessment.seven_kill(self.df)
        Assessment.thirteen_kill(self.df)

    @classmethod
    def three(cls, df):
        if '签约日期' and '转正日期' in df.columns:
            three_list = []
            for i in range(len(df)):
                if df.iloc[i].转正日期 is None:
                    three_list.append('否')
                else:
                    if (df.iloc[i].转正日期.year*12 + df.iloc[i].转正日期.month - df.iloc[i].签约日期.year*12 - df.iloc[i].签约日期.month) < 4:
                        three_list.append('是')
                    else:
                        three_list.append('否')
            df['是否三晋'] = three_list
            return df
        else:
            return df

    @classmethod
    def one(cls, df):
        if '签约日期' and '转正日期' in df.columns:
            one_list = []
            for i in range(len(df)):
                if df.iloc[i].转正日期 is None:
                    one_list.append('否')
                else:
                    if (df.iloc[i].转正日期.year*12 + df.iloc[i].转正日期.month - df.iloc[i].签约日期.year*12 - df.iloc[i].签约日期.month) < 2:
                        one_list.append('是')
                    else:
                        one_list.append('否')
            df['是否一晋'] = one_list
            return df
        else:
            return df

    @classmethod
    def thirteen_kill(cls, df):
        if '签约日期' and '预解约日期' in df.columns:
            list_13 = []
            for i in range(len(df)):
                if df.iloc[i].预解约日期 is None:
                    list_13.append('是')
                else:
                    if (df.iloc[i].预解约日期.year * 12 + df.iloc[i].预解约日期.month - df.iloc[i].签约日期.year * 12 - df.iloc[i].签约日期.month) < 13:
                        list_13.append('否')
                    else:
                        list_13.append('是')
            df['是否十三留'] = list_13
            return df
        else:
            return df

    @classmethod
    def seven_kill(cls, df):
        if '签约日期' and '预解约日期' in df.columns:
            list_7 = []
            for i in range(len(df)):
                if df.iloc[i].预解约日期 is None:
                    list_7.append('是')
                else:
                    if (df.iloc[i].预解约日期.year * 12 + df.iloc[i].预解约日期.month - df.iloc[i].签约日期.year * 12 - df.iloc[i].签约日期.month) < 7:
                        list_7.append('否')
                    else:
                        list_7.append('是')
            df['是否七留'] = list_7
            return df
        else:
            return df
