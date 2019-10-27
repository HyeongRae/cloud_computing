from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

import pandas as pd

import json

def index(request):
	achivement={}
	df = pd.read_csv("portfolio/static/data/achivement.csv")
	achivement = df.to_json(orient='split')
	achivement = json.loads(achivement)	
	return render(request, 'index/index.html', {"achivement": achivement})

def info(request):
	context={}
	kname = " "
	ename = " "
	num = " "
	birth = " "
	email = " "
	if request.method == "POST":
		try:
			kname = request.POST.get("kname")
			ename = request.POST.get("ename")
			num = request.POST.get("num")
			birth = request.POST.get("birth")
			email = request.POST.get("email")
			context = {
				"kname": kname,
				"ename": ename,
				"num": num,
				"birth": birth,
				"email": email,
			}
		except Exception as e:
			print(repr(e))
	return render(request,"content/info.html", context)
	
def contact(request):
	content={}
	if request.method == "POST":
		try:
			name = request.POST.get("name")
			number = request.POST.get("number")
			message = request.POST.get("message")
			if name != "" and number != "" and message != "":
				data = {'name':[name],'number':[number],'message':[message]}
				pf = pd.DataFrame(data)
				pf.to_csv("portfolio/static/data/message.csv",mode='a', index=False, header=False)
			else:
				messages.error(request, "WARNING")
		except Exception as e:
			print(repr(e))
	daf = pd.read_csv("portfolio/static/data/message.csv")
	content = daf.to_json(orient='split')
	content = json.loads(content)
	return render(request, 'content/contact.html', {'content': content})

# Create your views here.
