from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http      import HttpResponse
from .models import food,order_list
from django.http import JsonResponse
from six0.model import models
import urllib.request
import json
import datetime
from django.db import transaction
from django.utils import timezone
# Create your views here.

appid  = "wx0de42ac8fdc200e4"
secret = "ece154d66fbf5aad8a52700be52bbb03"
code   = ""
Error_Info = {'ErrorCode':'400','ErrorInfo':''}
#Setting
def GetWeChatOpenID(code,appid,secret):
	url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(appid,secret,code)
	res = urllib.request.urlopen(url)
	return res.read()

	
#My Functions

#货物信息
def commodity(request):
	data = {}
	commodity = food.objects.values()
	data['commodity'] = list(commodity)
	fd = food.objects.values()
	print (fd)
	return JsonResponse(data)


#用户认证
@csrf_exempt
def signup(request):
	ur = models.user()
	if(request.method != 'POST'):
		return '404'
	code = request.POST["code"]
	ur.openid = request.POST["openid"]
	#无openid 认证 <'500'>标识
	if(ur.openid == '500'):
		print("----500----")
		#获取openid session_key
		urInfo = GetWeChatOpenID(code,appid,secret)
		print(urInfo)
		str1 = str(urInfo,encoding = "utf-8")
		data = eval(str1)
		ur.openid = data["openid"]
		print(ur.openid)
		#捕获服务器异常
		if(ur.openid == '-1' or ur.openid == '40029' or ur.openid == '45011'):
			return ur.openid
		#openid写入数据库
		ur.Insert()
		resp = {'openid':ur.openid}
		return HttpResponse(json.dumps(resp), content_type="application/json")
	#openid  认证
	else:
		print("---Else---")
		if(len(ur.Select())>0):
			return  HttpResponse("200")
		else:
		#认证过期
			return  HttpResponse("004")


#添加订单
@transaction.atomic
def Order_(request):
# 	if(request.method != 'POST'):
#		models.order_put(request.POST)
#	else:
#		Error_Info['ErrorInfo'] = 'Order could not pull!'
#		HttpResponse(json.dumps(resp), content_type="application/json")
#	with transaction.atomic():
#		fd = food.objects.select_for_update().get(fd_name="A")
#		print(type(fd))
#		print(fd.fd_id)
	data = {"openid":"OPENID&881213","1":"2","333":"5","2222313":"1"}

	#保存点
	sid =  transaction.savepoint()
	orderNum = ""
	for fid in data:
		if(fid == "openid"):
			orderNum = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + data[fid]
			print(orderNum)
			continue
		'''设置保存点用于事务管理'''

		try:
			fd = food.objects.select_for_update().get(fd_id=fid)
		except:
			transaction.savepoint_rollback(sid)
			return HttpResponse('库存错误:'+str(fid))
		
		if(int(fd.fd_count) < int(data[fid])):
			transaction.savepoint_rollback(sid)
			return HttpResponse('库存不足:'+data[fid])
		else:
			try:
				#扣除库存
				fd.fd_count -= int(data[fid])
				#插入订单
				order_list.objects.create(
					openid   	= data["openid"],	#用户标识
					order_num   = orderNum,			#订单编号
					order_state = 0,				#未支付状态
					goods_id 	= fid,				#商品编号
					order_time 	= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),					#订单生成时间
					goods_count = data[fid],		#数量
					goods_price = 100				#价格
#					reserved_State =,				#收货状态
#					reserved_Time  =,               #收货时间
					)
				#保存库存执行
				fd.save()
			except Exception as e:
#				transaction.savepoint_rollback(sid)
				return HttpResponse('写入订单失败！'+str(e))
	#提交
	transaction.atomic()
	
	return HttpResponse('返回订单编号:'+str(orderNum)+" 时间："+str(datetime.datetime.now()))
