import os
def mkdir(path):
	#创建文件目录
	if not os.path.exists(path):
		#支持递归创建文件夹
		os.makedirs(path)

