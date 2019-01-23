import MySQLdb

class sql:
	db=None;
	cursor=None;
	def __init__(self):
		self.db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='Echosql', db='hkr', charset='utf8')
		self.cursor = self.db.cursor()
	
	def Execute(self,comm = ''):
		try:
#			print(comm)
			self.cursor.execute(comm)
			self.db.commit()
		except:
			self.db.rollback()
		self.db.close()

	def GetData(self,comm = ''):
		try:
#			print(comm)
			self.cursor.execute(comm)
			result = self.cursor.fetchall()
			return result
		except:
			return 'Error <sql.GetData>:Maybe is \'Comm\'!'
		self.db.close()


class user:
	def __init__(self):
		self.id = '0'
		self.openid = '0'
		self.userName ='0'
		self.address = '0'
		self.conn = '0'
		self.power = '0'

	def Insert(self):
		db = sql()
		comm = 'insert into six0_user(openid,userName,address,conn,power)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(self.openid,self.userName,self.address,self.conn,self.power)
		return db.Execute(comm)

	def Select(self):
		db = sql()
		comm = 'select *from six0_user where  openid = \'%s\''%self.openid
		data =  db.GetData(comm)
		print (data)
		return data


class order_put:
	def __init__(self,data):
		self.data = data
		

	#创建订单编号	
	def CreateOrderCode(self):
		pass


	#写入订单信息
	def Insert(self,OrderInfo):
		db = sql()
		comm = 'insert into '


	def CheckCommodity(self):
		#错误信息 
		MSGError = {}
		#初始化数据库连接
		db = sql()
		#获取货物信息
		for fd_id in self.data:
			if(fd_id != 'openid'):
				comm ='select fd_count from six0_food where fd_id=%s'%(fd_id)
				fd_count = db.GetData(comm)	
				if(len(fd_count)!=0):
					#货物出货数量大于库存数量
					if( int(self.data[fd_id])>int(fd_count[0][0])):
						print(fd_id)
						MSGError[fd_id] = "OOS"
					#写入订单信息
					else:
						print("OK")
				#货物编号错误
				else:
					MSGError[fd_id] = "Not_Goods"
		if(len(MSGError)!=0):
			return MSGError
