import pandas as pd
import os


# 输入文件路径，生成列表[文件绝对路径]
class Folder:
    def __init__(self, folder_dir):
        self.folder_dir = folder_dir

    # 遍历文件夹内所有文件，并向下遍历，生成内容为文件绝对路径的列表
    def files(self):
        for folder_dir, folders, files in os.walk(self.folder_dir):
            # 返回一个列表生成器
            return [os.path.join(folder_dir, file_name) for file_name in files]


# 输入列表，处理文件的方法(可编辑,但是命名必须以cui_开头）
class Files:
    def __init__(self, file_list):
        self.list = file_list

    @staticmethod
    def cui_txt(file_dir):
        return pd.read_table(file_dir, sep=',')

    @staticmethod
    def cui_excel(file_dir):
        return pd.read_excel(file_dir, sheet_name=0)

    @staticmethod
    def cui_csv(file_dir):
        return pd.read_csv(file_dir, sep=',')


# 输入Files(实例化)对象，读取文件内容,生成包含文件内容的列表
class Reading:
    def __init__(self, classes):
        self.object = classes
        self.method_list = [name for name in dir(self.object) if name.startswith('cui')]
        self.file_dir_list = self.object.list
        self.file_list = []
        self.new_file_list = []

    def reading(self):
        for file_dir in self.file_dir_list:
            for method in self.method_list:
                try:
                    if self.file_list.append(eval('{}.{}({})'.format(self.object, method, file_dir))):
                        break
                except BaseException:
                    pass

    # 处理文件的过程
    # 必须先调用reading的方法，才能调用dealing的方法
    def dealing(self):
        # concat操作
        count = len(self.file_list)
        for i in range(count):
            df = self.file_list.pop(0)
            for j in range(len(self.file_list)):
                if df.colums == self.file_list[j].columns:
                    df = pd.concat([df, self.file_list[j]]).drop_duplicates()
                    del self.file_list[j]
                else:
                    pass
            # 新的文件列表中所有表格的列标签都不完全一致
            self.new_file_list.append(df)

        if len(self.new_file_list) == 1:
            pd.to_excel()