import pandas as pd
import os,re
from collections import abc

#输入文件路径，生成字典{绝对路径：文件后缀名}
class Folder:
    def __init__(self,Folder_dir):
        self.Folder_dir = Folder_dir
        self.dic = {}

    #实例返回一个字典
    def __repr__(self):
        Folder.Dealing(self.Folder_dir)
        return self.dic

    #遍历文件夹内所有文件，并向下遍历，{绝对路径：文件后缀名}
    @classmethod
    def Dealing(cls,files):
        files = os.scandir(files)
        for file in files:
            if file.is_file():
                self.dic[file.path] = file.name.split('.')[-1]
            else:
                return Folder.Dealing(file)

#描述符（还是不会！），用于储存多个数据
class DataFrame:
    __count = 0
    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__count
        self.storage_name =  '{}_{}'.format(prefix,index)
        __count += 1

    def __get__(self,instance,owner):
        return getattr(instance,self.storage_name)

    def __set__(self,instance,value):
        setattr(instance, self.storage_name, value)

#输入字典，生成元素为DataFrame的变量名的列表
class Files:
    def __init__(self,dic):
        self.dic = dic
        self.method = {
            "txt":"pd.read_table",
            "xls":"pd.read_excel",
            "xlxs":"pd.read_excel",
            "csv":"pd.read_csv"
        }
        self.list = []

    def __repr__(self):
        #用数字作为变量名！！！！
        #目前只能处理一级标题的表格
        for path,key,name in self.dic.items(),range(len(self.dic)):
            if key == 'txt':
                name = DataFrame()
                #根据不同的文件类型，采用不同的方法
                name = eval(self.method[key])(path,sep = ',')
            else:
                name = DataFrame()
                name = eval(self.method[key])(path)
            self.list.append(name)
        return self.list

#用于处理文件,输入文件列表，根据文件内容，选择concat或者merge的处理方法
class Dealing:
    def __init__(self,file_list):
        self.file_list_1 = file_list.pop(0)
        self.file_list = file_list
        self.list_merge = []
        self.merge = DataFrame()
        self.concat = DataFrame()

    @classmethod
    def Dealing(cls,files):
        concat_list = []
        #遍历分类
        if isinstance(files,abc.MutableSequence):
            file_1 = files.pop(0)
            for file in files:
                if len(file.colums - file_1.columns) <= 2:
                    concat_list.append(file)
                    files.remove(file)
                else:
                    pass
            df_concat = pd.concat(concat_list)




















