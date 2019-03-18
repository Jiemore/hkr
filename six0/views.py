from django.shortcuts import redirect
#登录
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http      import HttpResponse
#Models
from .models import (
					food,
					order_list,
					Userprofile)
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

#_______________小程序接口
#
#


#货物信息
def commodity(request):
	data = {}
	commodity = food.objects.values()
	data['commodity'] = list(commodity)
	fd = food.objects.values()
	return JsonResponse(data)


#用户认证
@csrf_exempt
def signup(request):
	ur = models.user()
	if(request.method != 'POST'):
		return '204'
	try:
		code = request.POST["code"]
		ur.openid = request.POST["openid"]
	except:
		return HttpResponse(json.dumps({"Error":"201","info":"not "}), content_type="application/json")
	#无openid 认证 <'500'>标识
	if(ur.openid == '555'):
		#获取openid session_key
		urInfo = GetWeChatOpenID(code,appid,secret)
		print(urInfo)
		str1 = str(urInfo,encoding = "utf-8")
		data = eval(str1)
		ur.openid = data["openid"]
		print(ur.openid)
		#捕获服务器异常
		if(ur.openid == '-1' or ur.openid == '40029' or ur.openid == '45011'):
			return HttpResponse(json.dumps({"Error":ur.openid,"info":"Wechat Server Error"}),content_type="application/json")
		#openid写入数据库
		ur.Insert()
		resp = {'openid':ur.openid}
		return HttpResponse(json.dumps(resp), content_type="application/json")
	#openid  认证
	else:
		if(len(ur.Select())>0):
			return HttpResponse(json.dumps(resp), content_type="application/json")
		else:
		#认证过期
			return  HttpResponse("004")


#添加订单
@csrf_exempt
@transaction.atomic
def Order_(request):
	if(not "openid" in request.POST):
		return HttpResponse(json.dumps({"info" :"error","Error":"309"}),content_type="application/json")
#	data = {"openid":"OPENID&881213","1":"2","333":"1","2222313":"1"}
	data = request.POST
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
			return HttpResponse(json.dumps({"Error":"301",
											"info":"库存错误",
											"fid":str(fid)}),content_type="application/json")
		
		if(int(fd.fd_count) < int(data[fid])):
			transaction.savepoint_rollback(sid)
			return HttpResponse(json.dumps({"Error":"302",
											"info" :"库存不足！",
											"fid"  :str(fid),
											"num":data[fid]}),content_type="application/json")
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
				return HttpResponse(json.dumps({"infor":"写入订单失败！",
												"e":str(e),
												"Error":"303"
												}),content_type="application/json")
	#提交
	transaction.atomic()
	
	return HttpResponse(json.dumps({"orderNum":orderNum,
									"info"    :"succeed",
									"Error"   :"300"}),content_type="application/json")


#支付
def Pay(request):
	if(not ("openid" in request.POST and "ordernum" in request.POST)):
		return HttpResponse(json.dumps({"info" :"error",
                                 "Error":"409"}),content_type="application/json")

	if(request.method=='POST'):
		openId=request.POST['openid']
		orderNum=request.POST['ordernum']
		try:
			order_list.objects.get(openid=openId,order_num=orderNum).update(order_state='1')
			#响应后台
			return HttpResponse(json.dumps({"Error":"400",
											"error_msg" :"succeed",
											"ordernum":orderNum
											}),content_type="application/json")
		except:
			return HttpResponse(json.dumps({"openid":openId,
											"ordernum":orderNum,
											"Error":"401",
											"error_msg" :"支付失败!"}), content_type="application/json")
	else:
		return HttpResponse('pay error')

#
#________________ 后台管理页面
#
#


def session_test(request):
	show='first'
	if request.session.get('h1'):
		show='again'
	request.session['h1']='hello'
	h1=request.session.get('h1')
	return HttpResponse('write session:'+h1+'  '+show)


def query(request):
	msg=food.objects.values_list()
#	print(msg)
	return render(request,'test.html',{'result':msg})


@login_required
def Index(request):
	return render(request,'index.html',{'msg':'ok'})


def Login(request):
	User = get_user_model()
	#userss = User.objects.create_user(username='admin',password='root')
	if  request.method=="POST":
		#读取账户和密码
		UserName = request.POST.get("user")
		Password = request.POST.get("pwd")
		
		#检测账户和密码是否正确
		user = auth.authenticate(username=UserName,password=Password)
		if user:

			session = User.objects.filter(username=UserName).values()[0]["session"]

			#session 删除之前存在的会话
			if not session=='None':
				request.session.delete(session)

			#写入session
			auth.login(request,user)
			request.session["user"] = UserName
			session_key = request.session.session_key
			User.objects.filter(username=UserName).update(session=session_key)
			return redirect('/background/index/')

		else:
			error_msg = {'error_msg':'账户或密码错误'}
			return render(request,'login.html',error_msg)#错误的用户或者密码
	else:
		pass#错误请求

	#登录
	error_msg = {'error_msg':'Login'}
	return render(request,'login.html',error_msg)


def Logout(request):
	#del request.session['state']
	request.session.clear()
	return redirect('/login/')
