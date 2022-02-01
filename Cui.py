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
        for folder_dir,folders,files in os.walk(files):
            for file_name in files:
                self.dic[os.path.join(folder_dir,file_name)] = file_name.split('.')[-1]

#输入字典，将具有相同列标签的表concai合并，生成{[列标签]:表内容}的字典
class Files:
    def __init__(self,dic):
        self.dic = dic
        self.method = {
            "txt":"pd.read_table",
            "xls":"pd.read_excel",
            "xlxs":"pd.read_excel",
            "csv":"pd.read_csv"
        }
        self.dictionary = {}

    def __repr__(self):
        #用数字作为变量名！！！！
        #目前只能处理一级标题的表格
        for path,key in self.dic.items():
            # 根据不同的文件类型，采用不同的方法
            if key == 'txt':
                if eval(self.method[key])(path,sep = ',').columns not in self.dictionary.keys():
                    self.dictionary[eval(self.method[key])(path,sep = ',').columns] = eval(self.method[key])(path,sep = ',')
                else:
                    self.dictionary[eval(self.method[key])(path,sep = ',').columns] = pd.concat(
                        [self.dictionary[eval(self.method[key])(path,sep = ',').columns],
                         self.dictionary[eval(self.method[key])(path,sep = ',')]])
            else:
                if eval(self.method[key])(path, sep=',').columns not in self.dictionary.keys():
                    self.dictionary[eval(self.method[key])(path).columns] = eval(self.method[key])(path)
                else:
                    self.dictionary[eval(self.method[key])(path).columns] = pd.concat(
                        [self.dictionary[eval(self.method[key])(path).columns],
                         self.dictionary[eval(self.method[key])(path)]])
        return self.dictionary

#用于处理文件,输入字典，根据文件内容，选择concat或者merge的处理方法
class Dealing:
    def __init__(self,dictionary):
        self.dictionary = dictionary

    def dealing(self):






















