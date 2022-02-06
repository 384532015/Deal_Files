import Cui as c

folder_dir = r'C:\Users\crl\Desktop\处理表格'


# 运行过程
# 这是一个列表（元素为各文件的绝对路径）
file_list = c.Folder(folder_dir).files()

# 这是一个列表（元素为列标签都不相同的DataFrame）
files = c.Dealing(file_list).reading().dealing()

# 这是最终的完整的DataFrame（但是没有计算相应指标）
new_file = c.Deep_dealing(files)





