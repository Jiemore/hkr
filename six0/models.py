from django.db import models

# Create your models here.

#商品
class food(models.Model):	
	id       = models.AutoField(primary_key=True)					#单纯的计数ID
	fd_id    = models.CharField(max_length=200,unique = True)		#编号(条形码)
	fd_name  = models.CharField(max_length=100)						#名称
	fd_type  = models.CharField(max_length=100)						#类型
	fd_count = models.IntegerField()								#数量
	fd_price = models.DecimalField(max_digits=5, decimal_places=2)	#价格
	fd_picture = models.CharField(max_length=256,default='null')	#图片
	fd_state = models.IntegerField(default=0)						#状态


#分类
class foodtype(models.Model):
	fd_type_id   = models.CharField(max_length=20)					#标识
	fd_type_name = models.CharField(max_length=100)					#名称


#用户
class user(models.Model):
	openid   = models.CharField(max_length=100,unique = True)		#微信用户唯一标识
	userName = models.CharField(max_length=256)						#用户名
	address  = models.CharField(max_length=100)						#地址
	conn     = models.CharField(max_length=100)						#联系方式
	power    = models.IntegerField()								#权限


#订单
class order_list(models.Model):
	openid        = models.CharField(max_length=100)				#微信用户唯一标识
	order_num     = models.CharField(max_length=100)				#订单编号
	order_state   = models.IntegerField()							#订单状态
	order_time    = models.DateTimeField()							#下单时间
	goods_id      = models.CharField(max_length=100)				#商品编号
	goods_count   = models.IntegerField()							#商品下单数量
	goods_price   = models.DecimalField(max_digits=5, decimal_places=2)	#价格
	reserved_State= models.IntegerField(null = True)				#收货状态
	reserved_Time = models.DateTimeField(null = True)				#收货时间
