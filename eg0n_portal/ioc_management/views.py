from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

'''
def ip_list(request):
    return render(request, 'ip_list.html')
'''

def domain_list(request):
    return render(request, 'domain_list.html')

