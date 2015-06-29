#coding=utf-8
import requests
import StringIO
import re
import base64

class PJ():
	def __init__(self):
		self.white = 'iVBORw0KGgoAAAANSUhEUgAAAJYAAAAZCAIAAABchUC4AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3wYdAgYerV4wMwAAAD9JREFUaN7t0QENAAAIwzDAv+ejg9BJWDtJ6XJjAUIhFEKEQiiEQohQCIVQCBEKoRAKIUIhFEIhRCiEQiiEL1sX+wMvfsLvYwAAAABJRU5ErkJggg=='
		self.RefreshAll()

	def Login(self, usr, pwd, vcode):
		postdata = {
			"operation":"",
			"usercode_text":usr,
			"userpwd_text":pwd,
			"checkcode_text":vcode,
			"submittype":"\xC8\xB7 \xC8\xCF"
		}
		try:
			content = self.Session.post("http://222.30.32.10/stdloginAction.do", data = postdata).content.decode("gb2312")
		except:
			return {"Err":True, "Val":"NetWork Error!"}
		if content.find("stdtop") != -1:
			return {"Err":False, "Val":"Login Success"}
		elif (content.find(u"请输入正确的验证码") != -1):
			return {"Err":True, "Val":"ValidateCode Error!"}
		elif (content.find(u"用户不存在或密码错误") != -1):
			return {"Err":True, "Val":"User Name or Password Error!"}
		elif (content.find(u"忙") != -1 or content.find(u"负载") != -1):
			return {"Err":True, "Val":"System Busy!"}
		else:
			return {"Err":True, "Val":"UnknownError!"}
	
	def GetVcode(self):
		Q = self.Session.get("http://222.30.32.10/ValidateCode")
		if Q.status_code != 200:
			return None
		else:
			return StringIO.StringIO(Q.content)

	
	def RefreshAll(self):
		print "Refreshed"
		self.Session = requests.session()
		#self.Session.proxies = {"http":"127.0.0.1:8888"}
		self.vcode = StringIO.StringIO(base64.b64decode(self.white))
		self.NetWork = False
		try:
			self.Session.get("http://222.30.32.10")
			M = self.GetVcode()
			if M:
				self.vcode = M
				self.NetWork = True
			else:
				pass		
		except:
			pass
	
	def PJ(self):
		try:
			G = self.Session.get("http://222.30.32.10/evaluate/stdevatea/queryCourseAction.do")
		except :
			return {"Err":True, "Val":"NetWork Error!"}
		if G.url == "http://222.30.32.10/stdlogin.jsp":
			return {"Err":True, "Val":"Please Login First!"}
		else:
			num=int(re.findall(u"共 ([0-9]*) 项", G.content.decode("gb2312"))[0])
			failcount=0
			for i in range(num):
				Add = "http://222.30.32.10/evaluate/stdevatea/queryTargetAction.do?operation=target&index=%s"%str(i)
				D = self.Session.get(Add).content.decode("gb2312")
				D = D.replace(u"该教师给你的总体印象",u"该教师给你的总体印象（10）")
				item=re.findall(u"（([0-9]*)）", D)
				params="operation=Store"
				for j in range(len(item)):  
					params+=("&array["+str(j)+"]="+item[j])
				params+="&opinion="
				E = self.Session.post("http://222.30.32.10/evaluate/stdevatea/queryTargetAction.do", headers = {"Referer":Add}, data = params).content.decode("gb2312")
				if -1==E.find(u"成功保存！"):failcount+=1
			return {"Err":False, "Val":"Total: %s  Success: %s"%(num, num-failcount)}


