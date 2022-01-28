import pandas as pd
import os,re

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

#描述符
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

#变量名生成器




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
        for path,key,name in self.dic.items(),range(len(self.dic)):
            if key == 'txt':
                name = DataFrame()
                name = eval(self.method[key])(path,sep = ',')
            else:
                name = DataFrame()
                name = eval(self.method[key])(path)
            self.list.append(name)
        return self.list













