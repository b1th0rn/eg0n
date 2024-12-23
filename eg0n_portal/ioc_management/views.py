from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from .models import Vuln

# Create your views here.
def index(request):
  # object_list = Vuln.objects.all().order_by("update_date") 
  # context= {'object_list': object_list}
  # return render(request,"vulns_list.html",context)
  print("-------------------------------------")
  print("request ",request)
  print("request.method ",request.method)
  print("-------------------------------------")
  if request.method == "GET":
    template=loader.get_template("vulns_list.html")
    return HttpResponse(template.render())
  elif request.method == "POST":
    object_list = filter(lambda vuln : vuln.description.text.contains(request.text),Vuln.objects).order_by("update_date")
    response = serializers.serialize('json',object_list)
    return HttpResponse(response)
