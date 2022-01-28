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

class Files:
    def __init__(self,dic):
        self.dic = dic

    def __repr__(self):
        for path,key in self.dic.items():








