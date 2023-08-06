import pymysql,pexpect


def get_dbconn(config):
	#根据配置文件连接数据库并返回connection句柄
	try:
		return pymysql.connect(**config) #使用**将字典解包成key=value
	except :
		#如果连接异常，则可能是服务器未启动，则启动MYSQL服务器，并使用pexpect库进行判断并自动输入所需密码
		cmd='sudo /usr/local/mysql/support-files/mysql.server start'
		process=pexpect.spawn(cmd)
		keyword_index=process.expect(['Password:',pexpect.EOF,pexpect.TIMEOUT])
		if keyword_index==0:
			#自动填入密码及回车
			process.sendline('0704baijun')#传入密码，同时传入换行符（回车）
			keyword_index=process.expect(['SUCCESS!.{0,10}$','try again',pexpect.EOF,pexpect.TIMEOUT])
			if keyword_index==0:
				print('链接数据库成功')
				return pymysql.connect(**config)
			#匹配到其他，直接返回false，此时代表服务器未连接成功
			elif keyword_index==1:
				print('密码错误，请修改并重试！')
				return False
			else:
				return False
		#未出现输入Password时，可能是超时或命令错误
		else:
			return False
		process.close()

def db_shutdown():
	#关闭当前开启的MYSQL服务器
	cmd='sudo /usr/local/mysql/support-files/mysql.server stop'
	process=pexpect.spawn(cmd)
	expect_list=['Password:',pexpect.EOF,pexpect.TIMEOUT]
	keyword_index=process.expect(expect_list)
	process.setecho(False) #禁止在终端展示所有输入输出
	if keyword_index==0:
		#自动填入密码及回车
		process.sendline('0704baijun')#传入密码，同时传入换行符（回车）
		keyword_index=process.expect(['SUCCESS!.{0,10}$','try again',pexpect.EOF,pexpect.TIMEOUT])
		#清空此次匹配之前所有的缓存，便于读取before时，保证是此次匹配成功后，终端输出的内容，而不是累计的全部匹配输出的内容
		#因为每次只有匹配到之后，才会将当前终端展示的输出（send命令执行结果）append到缓存中
		# handle.buffer=''
		if keyword_index==0:
			#处于开启状态，关闭成功
			print('当前处于开启状态，关闭成功')
			return True
		elif keyword_index==1:
			print('密码错误，请修改并重试！')
			return False
		elif keyword_index==2:
			#EOF代表子程序终止，before为命令结果，after为
			if 'PID' in str(process.before):
				print('MYSQL服务器已经处于关闭状态')

class Mysql(object):
	#将数据库连接、数据库增删改查，封装为一个类，并进行单例模式开发，确保全局只创建一个数据库的连接
	def __new__(cls,*agrs1,**args2):
		if not hasattr(cls,'__instance'):
			cls.__instance=super(Mysql,cls).__new__(cls)
			return cls.__instance
	def __init__(self,connector,auto_commit=False):
		#初始化时，注意将自动提交关闭
		self.conn=connector
		self.cursor=self.conn.cursor()
		self.conn.autocommit(auto_commit)
	def __del__(self):
		try:
			self.cursor.close();self.conn.close()
		except:
			pass
		finally:
			del self.cursor;del self.conn
	def insert(self,sql_str,data_list):
		#插入方法，包含回滚机制，返回插入行数，可以通过返回值的True或False判断是否执行成功
		try:
			rows=self.cursor.executemany(sql_str,data_list)
		except Exception as err:
			self.conn.rollback()
			print('写入失败，已回滚，失败原因：{}'.format(err))
			return False
		else:
			self.conn.commit()
			if rows==0:
				return True
			return rows
	def query(self,sql_str,data_list=None):
		#查询方法，返回查询的行数以及查询结果，结果为列表类型，列表元素为字典:[{'column_name':data},]
		try:
			if data_list==None:
				rows=self.cursor.execute(sql_str)
			else:
				rows=self.cursor.executemany(sql_str,data_list)
		except Exception as err:
			print('查询失败，请重试，失败原因：{}'.format(err))
			return False
		else:
			return [rows,self.cursor.fetchall()]

	def update(self,sql_str,data_list):
		#更新方法，返回影响的行数量，如果更新发生错误，则回滚
		try:
			rows=self.cursor.executemany(sql_str,data_list)
		except Exception as err:
			self.conn.rollback()
			return False
			print('更新失败，已回滚，失败原因：{}'.format(err))
		else:
			self.conn.commit()
			return rows
	def delete(self,sql_str,data_list):
		#更新方法，返回影响的行数量，如果更新发生错误，则回滚
		try:
			rows=self.cursor.executemany(sql_str,data_list)
		except Exception as err:
			self.conn.rollback()
			return False
			print('删除失败，已回滚，失败原因：{}'.format(err))
		else:
			self.conn.commit()
			return ro


