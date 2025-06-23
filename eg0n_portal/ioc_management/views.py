from django.db.models import F
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import Vuln, Hash, IpAdd, VulnReview, CodeReview, HashReview, IpAddReview, CodeSnippet
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from collections import Counter

import json

def get_sort_value(obj, key, sort_order):
            value = getattr(obj, key, None)
            if key in ['publish_date', 'update_date'] and value is None:
                return (None,) if sort_order == 'asc' else ('ZZZ',) 
            return value if value is not None else ""

@ensure_csrf_cookie
def vulns(request):    
  if request.method == "GET":
    template=loader.get_template("vulns_list.html")
    return HttpResponse(template.render())
  elif request.method == "POST":
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        page_number = 1 # page_number = int(data.get('pageNumber', 1))
        per_page = 10 # per_page = int(data.get('perPage', 25))
        sort_by = data.get('sortBy', 'publish_date')
        sort_order = data.get('sortOrder', 'asc')

        # Check cache
        cache_key = 'last_10_vulns'
        vulns_data = cache.get(cache_key)
        if not vulns_data:
            # If not in cache, retrieve the last 10 vulnerabilities by publish_date
            last_10_vulns = Vuln.objects.order_by(F('publish_date').desc(nulls_last=True))[:10]
            vulns_data = list(last_10_vulns)
            # Store in cache for 5 minutes
            cache.set(cache_key, vulns_data, timeout=86400)

        # Apply filters on the subset of 10 vulnerabilities
        if text:
           text_lower = text.lower()
           vulns_data = [
              vuln for vuln in vulns_data
              if text_lower in vuln.description.lower() or \
                text_lower in vuln.name.lower() or \
                    text_lower in vuln.name.lower()]
           
        sorted_vulns = sorted(vulns_data,key= lambda vuln: get_sort_value(vuln, sort_by, sort_order), reverse=(sort_order=='desc'))
                
        # Serializzation date in iso 8601 format
        vulnerabilities_data = []
        for vuln in sorted_vulns:
            vulnerabilities_data.append({
                'cve': vuln.cve,
                'name': vuln.name,
                'cvss': vuln.cvss,
                'description': vuln.description,
                'publish_date': vuln.publish_date.isoformat(),
                'update_date': vuln.update_date.isoformat(),
                'slug': vuln.slug,
                'author': vuln.author,
                'lastchange_author': vuln.lastchange_author,
            })
        response_data = {
            'vulnerabilities': vulnerabilities_data,
            'total_pages': 1,
            'current_page': page_number,
            'total_items': len(vulns_data)
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid parameter type'}, status=400)
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
        page_number = 1 # page_number = int(data.get('pageNumber', 1))
        per_page = 10 # per_page = int(data.get('perPage', 25))
        sort_by = data.get('sortBy', 'publish_date')
        sort_order = data.get('sortOrder', 'asc')

        cache_key = 'last_10_hash'
        hash_data = cache.get(cache_key)
        if not hash_data:
            last_10_hash = Hash.objects.order_by(F('publish_date').desc(nulls_last=True))[:10]
            hash_data = list(last_10_hash)
            cache.set(cache_key, hash_data, timeout=86400)

        # Apply filters on the subset of 10 vulnerabilities
        if text:
            text_lower = text.lower()
            hash_data = [
                hash for hash in hash_data 
                if text_lower in hash.filename or \
                    text_lower in hash.description ]

        hash_data = sorted(hash_data, key=lambda hash: get_sort_value(hash, sort_by, sort_order), reverse=(sort_order=='desc'))
    
        # Serializzazione dei dati per la risposta JSON
        response_hash_data = []
        for hash in hash_data:
            response_hash_data.append({
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
            'hash_list': response_hash_data,
            'total_pages': 1,
            'current_page': page_number,
            'total_items': len(hash_data)
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
        page_number = 1 # page_number = int(data.get('pageNumber', 1))
        per_page = 10 # per_page = int(data.get('perPage', 25))
        sort_by = data.get('sortBy', 'publish_date')
        sort_order = data.get('sortOrder', 'asc')
        
        cache_key = 'last_10_ip'
        ip_data = cache.get(cache_key)
        if not ip_data:
            last_10_ip = IpAdd.objects.order_by(F('publish_date').desc(nulls_last=True))[:10]
            ip_data = list(last_10_ip)
            cache.set(cache_key, ip_data, timeout=86400)

        # Apply filters on the subset of 10 vulnerabilities
        if text:
            text_lower= text.lower()
            ip_data = [
                ip for ip in ip_data 
                if text_lower in ip.ip_address or \
                text_lower in ip.url or \
                text_lower in ip.fqdn or \
                text_lower in ip.description
            ]

        # Apply sorting on the filtered subset
        ip_data = sorted(ip_data, key=lambda ip : get_sort_value(ip,sort_by,sort_order),reverse=(sort_by=='desc'))
        # Serializzazione dei dati per la risposta JSON
        ip_address_data = []
        for ipadd in ip_data:
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
            'total_pages': 1,
            'current_page': page_number,
            'total_items': len(ip_data)
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
def scoreboard(request):    
  if request.method == "GET":
    template=loader.get_template("scoreboard.html")
    return HttpResponse(template.render())
  elif request.method == "POST":
    try:
        cache_key = 'scoreboard_cache_key'
        cache_response = cache.get(cache_key)
        if cache_response:
            return JsonResponse(cache_response)
        
        # implicit else, if object is not in cache calculate new scoreboard save in cache and return it 
        # retrive all the authors and reviewers from the DB
        vuln_queryset = Vuln.objects.values('author')
        hash_queryset = Hash.objects.values('author')
        ipadd_queryset = IpAdd.objects.values('author')
        codesnippet_queryset = CodeSnippet.objects.values('author')
        vuln_review_queryset = VulnReview.objects.values('author')
        hash_review_queryset = HashReview.objects.values('author')  
        ipadd_review_queryset = IpAddReview.objects.values('author')
        codesnippet_review_queryset = CodeReview.objects.values('author')
        
        # Combine all the authors and reviewers
        combined_authors = list(vuln_queryset) + list(hash_queryset) + list(ipadd_queryset) + list(codesnippet_queryset)
        combined_reviewers = list(vuln_review_queryset) + list(hash_review_queryset) + list(ipadd_review_queryset) + list(codesnippet_review_queryset)

        # Count the number of contributions by each author and reviewer
        author_counter = Counter([item['author'] for item in combined_authors])
        reviewer_counter = Counter([item['author'] for item in combined_reviewers])
        contributor_counter = author_counter + reviewer_counter

        # Sort authors by count in descending order
        sorted_authors = author_counter.most_common()
        sorted_reviewers = reviewer_counter.most_common()        
        contributor_counter = contributor_counter.most_common()
        
        # Prepare the response data
        top_authors = {}
        for i in range(3):
            if i < len(sorted_authors):
                top_authors[f'author{i+1}'] = sorted_authors[i][0]
            else:
                top_authors[f'author{i+1}'] = ''

        top_reviewers = {}
        for i in range(3):
            if i < len(sorted_reviewers):
                top_reviewers[f'reviewer{i+1}'] = sorted_reviewers[i][0]
            else:
                top_reviewers[f'reviewer{i+1}'] = ''

        top_contributors = {}
        for i in range(3):
            if i < len(contributor_counter):
                top_contributors[f'contributor{i+1}'] = contributor_counter[i][0]
            else:
                top_contributors[f'contributor{i+1}'] = ''


        response_data = {
            'top_authors': top_authors,
            'top_reviewers': top_reviewers,
            'top_contributors': top_contributors,
        }
        cache.set(cache_key, response_data, timeout=86400)
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