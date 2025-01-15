from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import Vuln, Hash, IpAdd

import json

# Create your views here.

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def vulns(request):    
  if request.method == "GET":
    template=loader.get_template("vulns_list.html")
    return HttpResponse(template.render())
  elif request.method == "POST":
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        page_number = int(data.get('pageNumber', 1))
        per_page = int(data.get('perPage', 25))
        sort_by = data.get('sortBy', 'publish_date')
        sort_order = data.get('sortOrder', 'asc')

        queryset = Vuln.objects.all()
        if text:
            queryset = queryset.filter(
                Q(description__icontains=text) |
                Q(name__icontains=text) |
                Q(cve__icontains=text)
            )

        # Gestione dell'ordinamento
        if sort_order == 'desc':
            queryset = queryset.order_by(F(sort_by).desc(nulls_last=True)) #gestione dei valori nulli
        else:
            queryset = queryset.order_by(F(sort_by).asc(nulls_last=True))#gestione dei valori nulli

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page_number)

        # Serializzazione dei dati per la risposta JSON
        vulnerabilities_data = []
        for vuln in page_obj.object_list:
            vulnerabilities_data.append({
                'cve': vuln.cve,
                'name': vuln.name,
                'cvss': vuln.cvss,
                'description': vuln.description,
                'publish_date': vuln.publish_date.isoformat(),  # Formatta la data in ISO 8601
                'update_date': vuln.update_date.isoformat(),
                'slug': vuln.slug,
                'author': vuln.author,
                'lastchange_author': vuln.lastchange_author,
            })
        response_data = {
            'vulnerabilities': vulnerabilities_data,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'total_items': paginator.count
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid parameter type'}, status=400) #gestione di parametri non validi come stringhe al posto di interi
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An error occurred'}, status=500)
  else:
    return JsonResponse({'error': 'Invalid request method'}, status=405)
  
@ensure_csrf_cookie
def hash(request):    
  if request.method == "GET":
    template=loader.get_template("hash_list.html")
    return HttpResponse(template.render())
  elif request.method == "POST":
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        page_number = int(data.get('pageNumber', 1))
        per_page = int(data.get('perPage', 25))
        sort_by = data.get('sortBy', 'publish_date')
        sort_order = data.get('sortOrder', 'asc')

        queryset = Hash.objects.all()
        if text:
            queryset = queryset.filter(
                Q(filename__icontains=text) |
                Q(description__icontains=text)
            )

        # Gestione dell'ordinamento
        if sort_order == 'desc':
            queryset = queryset.order_by(F(sort_by).desc(nulls_last=True)) #gestione dei valori nulli
        else:
            queryset = queryset.order_by(F(sort_by).asc(nulls_last=True))#gestione dei valori nulli

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page_number)

        # Serializzazione dei dati per la risposta JSON
        hash_data = []
        for hash in page_obj.object_list:
            hash_data.append({
                'filename': hash.filename,
                'platform': hash.platform,
                'sha256': hash.sha256,
                'sha1': hash.sha1,
                'md5': hash.md5,
                'website': hash.website,
                'confidence': hash.confidence,
                'description': hash.description,
                'publish_date': hash.publish_date.isoformat(),  # Formatta la data in ISO 8601
                'update_date': hash.update_date.isoformat(),
                'expire_date': hash.expire_date.isoformat(),
                'author': hash.author,
                'lastchange_author': hash.lastchange_author,
            })
        response_data = {
            'hash_list': hash_data,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'total_items': paginator.count
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid parameter type'}, status=400) #gestione di parametri non validi come stringhe al posto di interi
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An error occurred'}, status=500)
  else:
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@ensure_csrf_cookie
def ipadd(request):    
  if request.method == "GET":
    template=loader.get_template("ipadd_list.html")
    return HttpResponse(template.render())
  elif request.method == "POST":
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        page_number = int(data.get('pageNumber', 1))
        per_page = int(data.get('perPage', 25))
        sort_by = data.get('sortBy', 'publish_date')
        sort_order = data.get('sortOrder', 'asc')

        queryset = IpAdd.objects.all()
        if text:
            queryset = queryset.filter(
                Q(ip_address__icontains=text) |
                Q(url__icontains=text) |
                Q(fqdn__icontains=text) |
                Q(description__icontains=text)
            )

        # Gestione dell'ordinamento
        if sort_order == 'desc':
            queryset = queryset.order_by(F(sort_by).desc(nulls_last=True)) #gestione dei valori nulli
        else:
            queryset = queryset.order_by(F(sort_by).asc(nulls_last=True))#gestione dei valori nulli

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page_number)

        # Serializzazione dei dati per la risposta JSON
        ip_address_data = []
        for ipadd in page_obj.object_list:
            ip_address_data.append({
                'ip_address': ipadd.ip_address,
                'url': ipadd.url,
                'fqdn': ipadd.fqdn,
                'confidence': ipadd.confidence,
                'description': ipadd.description,
                'publish_date': ipadd.publish_date.isoformat(),  # Formatta la data in ISO 8601
                'update_date': ipadd.update_date.isoformat(),
                'expire_date': ipadd.expire_date.isoformat(),
                'author': ipadd.author,
                'lastchange_author': ipadd.lastchange_author,
            })
        response_data = {
            'ip_address_list': ip_address_data,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'total_items': paginator.count
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid parameter type'}, status=400) #gestione di parametri non validi come stringhe al posto di interi
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An error occurred'}, status=500)
  else:
    return JsonResponse({'error': 'Invalid request method'}, status=405)
