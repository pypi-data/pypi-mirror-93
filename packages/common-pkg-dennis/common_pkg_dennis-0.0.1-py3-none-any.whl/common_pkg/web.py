import requests,time
from lxml import etree
from faker import Faker
import os
from Crypto.Cipher import AES

def get_response(url,conn_timeout=20,read_timeout=20,retry_time=10):
	#可分别设置连接超时时间和读取超时时间、重新发起连接次数

	#生成faker对象
	ua=Faker()

	headers={
		'connection':'close',
		'User-Agent':ua.user_agent()
	}
	i=0

	while i<retry_time:
		try:
			response=requests.get(url,timeout=(conn_timeout,read_timeout),headers=headers)
			return response
		except:
			print('下载失败，第{}次尝试重新下载'.format(i+1),end='    ',flush=True)
			time.sleep(1) #防止请求过于频繁导致其他问题
			i+=1
	else:
		print('所有重试均失败！')
		return False


def get_element_list(url,xpath,conn_timeout=20,read_timeout=20,retry_time=10):
	#url和xpath均需要是字符串，返回xpath命中的标签，列表形式返回
	response=get_response(url,conn_timeout,read_timeout,retry_time)
	if response:
		html=etree.HTML(response.text)
		element_list=html.xpath(xpath)
		if element_list:
			return element_list
		else:
			return False
	else:
		return False



def download_m3u8_video(m3u8_file_path,video_file_path):
	"""
	该函数主要用于将指定m3u8文件内包含的ts文件下载并存储到一个指定视频文件内，并且可兼容经过AES加密后的ts文件的下载
	:m3u8_file_path:m3u8文件读取路径，可为网络路径，也可为本地路径，均需为绝对路径
	:base_url：即下载m3u8文件内包含的ts文件下载地址的基础路径，基础路径后面紧跟ts文件名
	:video_file_path：即将m3u8文件包含的视频下载完毕后，存储的绝对路径，需包含文件后缀
	"""
	ts_file_list=[]
	key=''
	base_url=m3u8_file_path.rsplit('/',1)[0]+'/'
	try:
		#获取ts文件名称列表
		if 'http' in m3u8_file_path:
			#如果是网址
			response=web.get_response(m3u8_file_path)
			if response:
				for line in response.text.splitlines():
					if 'ts' in line :
						ts_file_list.append(line)
					if "#EXT-X-KEY" in line:
						#如果m3u8有加密，则找出解密方式和获取解密key的url地址
						method_pos = line.find("METHOD")
						comma_pos = line.find(",")
						method = line[method_pos:comma_pos].split('=')[1]

						uri_pos = line.find("URI")
						quotation_mark_pos = line.rfind('"')
						key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

						key_url=base_url+key_path
						res = web.get_response(key_url)
						key = res.content

		else:
			if os.path.isfile(m3u8_file_path) and ('m3u8' in m3u8_file_path):
				#如果是本地文件地址
				with open(m3u8_file_path,'r+') as f1:
					for line in f1:
						if 'ts' in line:
							line=line.replace('\n','')
							ts_file_list.append(line)
			else:
				raise ValueError('传入的m3u8文件地址有误')

		#判断传入的视频文件地址是否正确，以及是否存在，如果不存在则创建
		if os.path.isabs(video_file_path):
			dirname=os.path.dirname(video_file_path)
			filename=os.path.basename(video_file_path)
			if not os.access(dirname, os.F_OK):
				os.makedirs(dirname)
		else:
			raise ValueError('传入的存储视频的文件地址需为绝对路径')

		#使用基础链接和ts文件名称拼接出ts文件具体下载地址，逐个下载并写入最终视频文件内
		count=0
		total=len(ts_file_list)
		with open(video_file_path,'wb+') as f2:	
			for ts in ts_file_list:
				count+=1
				file_path=base_url+ts
				response=web.get_response(file_path)
				if response:
					if len(key):
						#如果有加密，则先解密内容，再写入视频文件
						cryptor = AES.new(key, AES.MODE_CBC, key)
						content=cryptor.decrypt(response.content)
					else:
						#如果没有加密，则直接写入视频文件
						content=response.content
					f2.write(content)
					print('已写入{}个ts文件，剩余{}个ts文件'.format(count,total-count))
				else:
					continue

	except ValueError as err:
		print(err)
