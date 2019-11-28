from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http import HttpResponse
import certifi

# Create your views here.

def homepage(request):
	context = {}
	if request.method == "POST":
		data = request.POST.get("paradatao")
		word = request.POST.get("userinput")
		#es = Elasticsearch("http://localhost:9200")
		host = "https://search-assign-tx4wrg5bg72ds5ty6fqbjhtpue.us-east-2.es.amazonaws.com"
		es = Elasticsearch("https://search-assign-tx4wrg5bg72ds5ty6fqbjhtpue.us-east-2.es.amazonaws.com",use_ssl=True, ca_certs=certifi.where())
		
		data=data.lower()
		para=data.split('##&##')
		print(para)
		doc=[0]*len(para)
		for i in range(len(para)):
		    doc[i] = {"sentence" : para[i]}
		    es.index(index="english", doc_type="sentences", id=i, body=doc[i])
		res = es.search(index="english", body={"from":0,"size":9,"query":{"match":{"sentence":word}}})
		lol=res.get('hits').get('hits')
		output = []
		for i in range(len(lol)):
		    lol2=lol[i].get('_source').get('sentence')
		    output.append(lol2)
		context ={
		"data2":output,
		}

	if context == {}:
		return render(request,"main/home.html")
	else:
		return render(request,"main/home.html",context)

	
	





















