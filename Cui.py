import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

# 名称转化专用字典
name_turn = {
    '工号': '销售人员代码',
    '销售员代码': '销售人员代码',
    '营销系列': '营销',
    '营销主管系列': '营销',
    '收展员系列': '收展',
    '收展主管系列': '收展',
    '保单服务专员系列': '收展',
    '德州市武城支公司营销发展部': '武城',
    '德州市临邑支公司营销发展部': '临邑',
    '德州市宁津支公司营销发展部': '宁津',
    '德州市庆云支公司营销发展部': '庆云',
    '德州市齐河支公司营销发展部': '齐河',
    '德州市分公司市直营销部（专业化支公司）': '市直营一',
    '德州市分公司个险营销二部': '市直营二',
    '德州市分公司个险营销三部': '市直营三',
    '德州市禹城支公司营销发展部': '禹城',
    '德州市乐陵支公司营销发展部': '乐陵',
    '德州市陵县支公司营销发展部': '陵城',
    '德州市德城区支公司营销发展部': '德城',
    '德州市夏津支公司营销发展部': '夏津',
    '德州市平原支公司营销发展部': '平原',
    '德州市乐陵支公司收展发展部': '乐陵',
    '德州市德城区支公司收展发展部': '德城',
    '德州市禹城支公司收展发展部': '禹城',
    '德州市陵县支公司收展发展部': '陵城',
    '德州市分公司城区收展专业化支公司（专业化支公司）': '收展一支',
    '德州市齐河支公司收展发展部': '齐河',
    '德州市临邑支公司收展发展部': '临邑',
    '德州市武城支公司收展发展部': '武城',
    '德州市平原支公司收展发展部': '平原',
    '德州市庆云支公司收展发展部': '庆云',
    '德州市宁津支公司收展发展部': '宁津',
    '德州市夏津支公司收展发展部': '夏津',
    '德州城区收展第二支公司收展发展部（专业化支公司）': '收展二支',
    '德州市分公司城区收展专业化支公司（专业化': '收展一支',
    '德州市分公司个险营销三部收展部': '德城',
    '德州市分公司市直银行保险部（专业化支公司': '收展二支',
    '德州市分公司庆云支公司银行保险部': '庆云',
    '德州市分公司宁津支公司团险部': '宁津',
    '德州市分公司宁津支公司银行保险部': '宁津',
    '德州市分公司庆云支公司团险部': '庆云',
    '德州市分公司乐陵支公司银行保险部': '乐陵',
    '德州市分公司禹城支公司银行保险部': '禹城',
    '德州市分公司禹城支公司团险部': '禹城',
    '德州市分公司乐陵支公司团险部': '乐陵',
    '德州市分公司德城区支公司银行保险部': '德城',
    '德州市分公司临邑支公司银行保险部': '临邑',
    '德州市分公司齐河支公司银行保险部': '齐河',
    '德州市分公司武城支公司银行保险部': '武城',
    '德州市分公司陵县支公司银行保险部': '陵城',
    '德州市分公司夏津支公司团险部': '夏津',
    '德州市分公司夏津支公司银行保险部': '夏津'
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
    def cui_txt(cls, file_dir):
        # 测试所有编码
        for i in ['GBK', 'ASCII', 'utf-8', 'GB18030', 'latin1', 'ANSI']:
            try:
                return pd.read_table(file_dir, sep=',', encoding=i, low_memory=False)
            except ValueError:
                pass

    @classmethod
    def cui_excel(cls, file_dir):
        return pd.read_excel(file_dir, sheet_name=0)

    @classmethod
    def cui_csv(cls, file_dir):
        return pd.read_csv(file_dir, sep=',')


# 输入Files绝对路径列表，根据Method类读取文件内容,生成列标签全不相同的文件列表
class Concat:
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
        dictionary = dict(zip(list(range(len(self.file_list))), self.file_list))
        remove_list = []
        for i, df in dictionary.items():
            del dictionary[i]
            for j, df_1 in dictionary.items():
                if df.columns.all() == df_1.columns.all():
                    # 保留最新数据，删除工号重复的项
                    if '预解约日期' in df.columns:
                        df = pd.concat([df, df_1]).sort_values(by=['预解约日期'], na_position='last').drop_duplicates(subset=['销售人员代码'], keep='first')
                    else:
                        df = pd.concat([df, df_1]).drop_duplicates()
                    remove_list.append(j)
                else:
                    pass
                
            # 新的文件列表中所有表格的列标签都不完全一致
            self.new_file_list.append(df)
            for k in remove_list:
                del dictionary[k]
            self.file_list = list(dictionary.values())
            # 未处理完self.file_list,返回函数继续运行
            return self.dealing()
        return self.new_file_list


# 输入文件绝对路径的列表，读取文件，统一格式，merge处理，生成一个df
class Data_Cleaning:
    def __init__(self, new_file_list):
        self.list = new_file_list
        self.df_rolling = pd.DataFrame()

    @classmethod
    def date_turn(cls, x):
        try:
            if isinstance(x, str):
                return datetime.strptime(x, '%Y-%m-%d')
            # 浮点型转为时间格式，很重要！
            elif isinstance(x, np.float64):
                time = datetime(year=1900, month=1, day=1) + timedelta(days=x)
                return time
        except:
            return np.nan

    # 修改格式，统一标签名称，merge操作等
    def turn(self):
        for df in self.list:
            df.rename(columns=name_turn, inplace=True)
            df['销售人员代码'] = df['销售人员代码'].fillna(0)
            df['销售人员代码'] = df['销售人员代码'].apply(lambda x: str(int(x)))

            # 处理花名册
            if '人员系列' in df.columns:
                df['渠道'] = df['人员系列'].map(name_turn)
                df['单位'] = df['核算单元名称'].map(name_turn)
                # 处理销售人员代码和时间格式
                df['签约日期'] = df['签约日期'].apply(lambda x: Data_Cleaning.date_turn(x))

                df['预解约日期'] = df['预解约日期'].apply(lambda x: Data_Cleaning.date_turn(x))

                df['解约日期'] = df['解约日期'].apply(lambda x: Data_Cleaning.date_turn(x))

                self.df_rolling = pd.concat([self.df_rolling, df])

            # 处理历史职级
            elif '考核前职级' and '确认职级' in df.columns:
                # 处理格式
                df['统计日期'] = df['统计日期'].apply(lambda x: Data_Cleaning.date_turn(x))

                # 转正日期
                df_1 = df[((df['考核前职级'] == '业务员') | (df['考核前职级'] == '准收展员')) & ((df['确认职级'] == '业务主任') | (df['确认职级'] == '收展员'))]
                df_1 = df_1.rename({'统计日期': '转正日期'}, axis='columns')
                df_1 = df_1.reindex(columns=['销售人员代码', '转正日期'])

                # 晋组日期
                df_2 = df[(pd.notnull(df['占培训控制 '])) & ((df['确认职级'] == '组经理') | (df['确认职级'] == '金质组经理') | (df['确认职级'] == '银质组经理'))]
                df_2 = df_2.rename({'统计日期': '晋组日期'}, axis='columns')
                df_2 = df_2.reindex(columns=['销售人员代码', '晋组日期'])

                # 晋处部日期
                df_3 = df[(pd.notnull(df['占培训控制 '])) & ((df['确认职级'] == '处经理') | (df['确认职级'] == '部经理'))]
                df_3 = df_3.rename({'统计日期': '晋处/部日期'}, axis='columns')
                df_3 = df_3.reindex(columns=['销售人员代码', '晋处/部日期'])

                # merge历史职级
                df_sum = pd.concat([df_1, df_2, df_3])

            # 处理保单明细，可以继续添加功能
            else:
                pass

        self.df_rolling = pd.merge(self.df_rolling, df_sum, on='销售人员代码', how='left')

        return self.df_rolling


# 添加一晋、三晋、七留、十三留列
class Assessment:
    def __init__(self, df):
        self.df = df

    @property
    def three(self):
        if '签约日期' and '转正日期' in self.df.columns:
            three_list = []
            for i in range(len(self.df)):
                if self.df.iloc[i].转正日期 is None:
                    three_list.append('否')
                else:
                    if (self.df.iloc[i].转正日期.year*12 + self.df.iloc[i].转正日期.month - self.df.iloc[i].签约日期.year*12 - self.df.iloc[i].签约日期.month) < 4:
                        three_list.append('是')
                    else:
                        three_list.append('否')
            self.df['是否三晋'] = three_list
            return self.df
        else:
            return self.df

    @property
    def one(self):
        if '签约日期' and '转正日期' in self.df.columns:
            one_list = []
            for i in range(len(self.df)):
                if self.df.iloc[i].转正日期 is None:
                    one_list.append('否')
                else:
                    if (self.df.iloc[i].转正日期.year*12 + self.df.iloc[i].转正日期.month - self.df.iloc[i].签约日期.year*12 - self.df.iloc[i].签约日期.month) < 2:
                        one_list.append('是')
                    else:
                        one_list.append('否')
            self.df['是否一晋'] = one_list
            return self.df
        else:
            return self.df

    @property
    def thirteen_kill(self):
        if '签约日期' and '预解约日期' in self.df.columns:
            list_13 = []
            for i in range(len(self.df)):
                if self.df.iloc[i].预解约日期 is None:
                    list_13.append('是')
                else:
                    if (self.df.iloc[i].预解约日期.year * 12 + self.df.iloc[i].预解约日期.month - self.df.iloc[i].签约日期.year * 12 - self.df.iloc[i].签约日期.month) < 13:
                        list_13.append('否')
                    else:
                        list_13.append('是')
            self.df['是否十三留'] = list_13
            return self.df
        else:
            return self.df

    @property
    def seven_kill(self):
        if '签约日期' and '预解约日期' in self.df.columns:
            list_7 = []
            for i in range(len(self.df)):
                if self.df.iloc[i].预解约日期 is None:
                    list_7.append('是')
                else:
                    if (self.df.iloc[i].预解约日期.year * 12 + self.df.iloc[i].预解约日期.month - self.df.iloc[i].签约日期.year * 12 - self.df.iloc[i].签约日期.month) < 7:
                        list_7.append('否')
                    else:
                        list_7.append('是')
            self.df['是否七留'] = list_7
            return self.df
        else:
            return self.df
