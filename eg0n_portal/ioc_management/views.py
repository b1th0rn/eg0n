from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import (
    Vuln,
    Hash,
    IpAdd,
    VulnReview,
    CodeReview,
    HashReview,
    IpAddReview,
    CodeSnippet,
)
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from collections import Counter
from .viewsHelper import get_cached_filterd_data_async
from asgiref.sync import sync_to_async

import json


@ensure_csrf_cookie
async def vulns(request):
    """
    Summary:
        Handles GET and POST requests for vulnerabilities.
        - GET: Renders the vulnerabilities list template.
        - POST: Returns the last 10 vulnerabilities (cached for 24h), filtered and sorted by user parameters.
    """
    if request.method == "GET":
        # Render the vulnerabilities list page using the template system
        template = loader.get_template("vulns_list.html")
        return HttpResponse(template.render())
    elif request.method == "POST":
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)
            text = data.get("text", "")  # Text filter for searching
            page_number = 1  # Pagination is fixed to 1 page of 10 items
            per_page = 10  # Only the last 10 vulnerabilities are shown
            sort_by = data.get("sortBy", "publish_date")  # Field to sort by
            sort_order = data.get("sortOrder", "asc")  # Sort order (asc/desc)

            # Prepare cache key and query for last 10 vulns (ordered by publish_date)
            cache_key = "last_10_vulns"
            last_10_vulns = Vuln.objects.order_by(
                F("publish_date").desc(nulls_last=True)
            )[:per_page]

            # Define filter function for vulnerabilities
            # This function will be used to filter the cached/queryset data
            def filter_vuln(text_filter, value):
                # Check if the filter text is present in description or name (case-insensitive)
                return (
                    text_filter in (value.description or "").lower()
                    or text_filter in (value.name or "").lower()
                )

            # Retrieve, cache, filter, and sort vulnerabilities
            # - If not cached, fetch from DB and cache for 24h
            # - Apply filter and sorting on the cached/queryset data
            values_data = await get_cached_filterd_data_async(
                text.lower(), last_10_vulns, cache_key, filter_vuln, sort_by, sort_order
            )

            # Serialize vulnerabilities for JSON response
            vulnerabilities_data = []
            for vuln in values_data:
                # Convert each Vuln object to a dictionary, formatting dates as ISO 8601
                vulnerabilities_data.append(
                    {
                        "cve": vuln.cve,
                        "name": vuln.name,
                        "cvss": vuln.cvss,
                        "description": vuln.description,
                        "publish_date": (
                            vuln.publish_date.isoformat() if vuln.publish_date else None
                        ),
                        "update_date": (
                            vuln.update_date.isoformat() if vuln.update_date else None
                        ),
                        "slug": vuln.slug,
                        "author": vuln.author,
                        "lastchange_author": vuln.lastchange_author,
                    }
                )
            # Prepare the response with pagination info (always 1 page of 10 items)
            response_data = {
                "vulnerabilities": vulnerabilities_data,
                "total_pages": 1,
                "current_page": page_number,
                "total_items": len(vulnerabilities_data),
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            # Handle invalid JSON in request
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError:
            # Handle invalid parameter types
            return JsonResponse({"error": "Invalid parameter type"}, status=400)
        except Exception as e:
            # Catch-all for unexpected errors
            print(e)
            return JsonResponse({"error": "An error occurred"}, status=500)
    else:
        # Only GET and POST are allowed
        return JsonResponse({"error": "Invalid request method"}, status=405)


@ensure_csrf_cookie
async def hash(request):
    """
    Summary:
        Handles GET and POST requests for hashes.
        - GET: Renders the hash list template.
        - POST: Returns the last 10 hashes (cached for 24h), filtered and sorted by user parameters.
    """
    if request.method == "GET":
        # Render the hash list page using the template system
        template = loader.get_template("hash_list.html")
        return HttpResponse(template.render())
    elif request.method == "POST":
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)
            text = data.get("text", "")  # Text filter for searching
            page_number = 1
            per_page = 10
            sort_by = data.get("sortBy", "publish_date")
            sort_order = data.get("sortOrder", "asc")

            # Prepare cache key and query for last 10 hashes (ordered by publish_date)
            cache_key = "last_10_hash"
            last_10_hash = Hash.objects.order_by(
                F("publish_date").desc(nulls_last=True)
            )[:per_page]

            # Define filter function for hashes
            # Checks if the filter text is present in filename or description
            def filter_hash_text(text_filter, value):
                return (
                    text_filter in (value.filename or "").lower()
                    or text_filter in (value.description or "").lower()
                    or text_filter in (value.md5 or "").lower()
                    or text_filter in (value.sha1 or "").lower()
                    or text_filter in (value.sha256 or "").lower()
                )

            # Retrieve, cache, filter, and sort hashes
            values_data = await get_cached_filterd_data_async(
                text.lower(),
                last_10_hash,
                cache_key,
                filter_hash_text,
                sort_by,
                sort_order,
            )

            # Serialize hashes for JSON response
            response_hash_data = []
            for hash in values_data:
                response_hash_data.append(
                    {
                        "filename": hash.filename,
                        "platform": hash.platform,
                        "sha256": hash.sha256,
                        "sha1": hash.sha1,
                        "md5": hash.md5,
                        "website": hash.website,
                        "confidence": hash.confidence,
                        "description": hash.description,
                        "publish_date": (
                            hash.publish_date.isoformat() if hash.publish_date else None
                        ),
                        "update_date": (
                            hash.update_date.isoformat() if hash.update_date else None
                        ),
                        "expire_date": (
                            hash.expire_date.isoformat() if hash.expire_date else None
                        ),
                        "author": hash.author,
                        "lastchange_author": hash.lastchange_author,
                    }
                )

            # Prepare the response with pagination info (always 1 page of 10 items)
            response_data = {
                "hash_list": response_hash_data,
                "total_pages": 1,
                "current_page": page_number,
                "total_items": len(response_hash_data),
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            # Handle invalid JSON in request
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError:
            # Handle invalid parameter types
            return JsonResponse({"error": "Invalid parameter type"}, status=400)
        except Exception as e:
            # Catch-all for unexpected errors
            print(e)
            return JsonResponse({"error": "An error occurred"}, status=500)
    else:
        # Only GET and POST are allowed
        return JsonResponse({"error": "Invalid request method"}, status=405)


@ensure_csrf_cookie
async def ipadd(request):
    """
    Summary:
        Handles GET and POST requests for IP addresses.
        - GET: Renders the IP address list template.
        - POST: Returns the last 10 IP addresses (cached for 24h), filtered and sorted by user parameters.
    """
    if request.method == "GET":
        # Render the IP address list page using the template system
        template = loader.get_template("ipadd_list.html")
        return HttpResponse(template.render())
    elif request.method == "POST":
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)
            text = data.get("text", "")  # Text filter for searching
            page_number = 1
            per_page = 10
            sort_by = data.get("sortBy", "publish_date")
            sort_order = data.get("sortOrder", "asc")

            # Prepare cache key and query for last 10 IP addresses (ordered by publish_date)
            cache_key = "last_10_ip"
            last_10_ip = IpAdd.objects.order_by(
                F("publish_date").desc(nulls_last=True)
            )[:per_page]

            # Define filter function for IP addresses
            # Checks if the filter text is present in ip_address, url, fqdn, or description
            def filter_ip_text(text_filter, value):
                return (
                    text_filter in (value.ip_address or "").lower()
                    or text_filter in (value.url or "").lower()
                    or text_filter in (value.fqdn or "").lower()
                    or text_filter in (value.description or "").lower()
                )

            # Retrieve, cache, filter, and sort IP addresses
            values_data = await get_cached_filterd_data_async(
                text.lower(), last_10_ip, cache_key, filter_ip_text, sort_by, sort_order
            )

            # Serialize IP addresses for JSON response
            ip_address_data = []
            for ipadd in values_data:
                ip_address_data.append(
                    {
                        "ip_address": ipadd.ip_address,
                        "url": ipadd.url,
                        "fqdn": ipadd.fqdn,
                        "confidence": ipadd.confidence,
                        "description": ipadd.description,
                        "publish_date": (
                            ipadd.publish_date.isoformat()
                            if ipadd.publish_date
                            else None
                        ),
                        "update_date": (
                            ipadd.update_date.isoformat() if ipadd.update_date else None
                        ),
                        "expire_date": (
                            ipadd.expire_date.isoformat() if ipadd.expire_date else None
                        ),
                        "author": ipadd.author,
                        "lastchange_author": ipadd.lastchange_author,
                    }
                )
            # Prepare the response with pagination info (always 1 page of 10 items)
            response_data = {
                "ip_address_list": ip_address_data,
                "total_pages": 1,
                "current_page": page_number,
                "total_items": len(ip_address_data),
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            # Handle invalid JSON in request
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError:
            # Handle invalid parameter types
            return JsonResponse({"error": "Invalid parameter type"}, status=400)
        except Exception as e:
            # Catch-all for unexpected errors
            print(e)
            return JsonResponse({"error": "An error occurred"}, status=500)
    else:
        # Only GET and POST are allowed
        return JsonResponse({"error": "Invalid request method"}, status=405)


@ensure_csrf_cookie
async def scoreboard(request):
    """
    Summary:
        Handles GET and POST requests for the scoreboard.
        - GET: Renders the scoreboard template.
        - POST: Returns the top 3 authors, reviewers, and contributors, using cache for 24h.
    """
    if request.method == "GET":
        # Render the scoreboard page using the template system
        template = loader.get_template("scoreboard.html")
        return HttpResponse(template.render())
    elif request.method == "POST":
        try:
            cache_key = "scoreboard_cache_key"
            # Try to get scoreboard data from cache (to avoid heavy DB queries)
            response_data = cache.get(cache_key)
            if response_data:
                # If cached, return immediately
                return JsonResponse(response_data)

            # Acquire a lock to prevent race conditions (multiple requests at once)
            lock_key = ("lock_" + cache_key,)
            lock_acquired = await sync_to_async(cache.add)(lock_key, "lock", 10)
            if lock_acquired:
                try:
                    # Double-check cache after acquiring lock (another request may have set it)
                    response_data = cache.get(cache_key)
                    if response_data:
                        return JsonResponse(response_data)
                    # Retrieve all authors and reviewers from DB for each model
                    vuln_queryset = Vuln.objects.values("author")
                    hash_queryset = Hash.objects.values("author")
                    ipadd_queryset = IpAdd.objects.values("author")
                    codesnippet_queryset = CodeSnippet.objects.values("author")
                    vuln_review_queryset = VulnReview.objects.values("author")
                    hash_review_queryset = HashReview.objects.values("author")
                    ipadd_review_queryset = IpAddReview.objects.values("author")
                    codesnippet_review_queryset = CodeReview.objects.values("author")

                    # Combine all authors and reviewers into lists
                    combined_authors = (
                        await sync_to_async(list)(vuln_queryset)
                        + await sync_to_async(list)(hash_queryset)
                        + await sync_to_async(list)(ipadd_queryset)
                        + await sync_to_async(list)(codesnippet_queryset)
                    )
                    combined_reviewers = (
                        await sync_to_async(list)(vuln_review_queryset)
                        + await sync_to_async(list)(hash_review_queryset)
                        + await sync_to_async(list)(ipadd_review_queryset)
                        + await sync_to_async(list)(codesnippet_review_queryset)
                    )

                    # Count contributions by each author and reviewer
                    author_counter = Counter(
                        [item["author"] for item in combined_authors]
                    )
                    reviewer_counter = Counter(
                        [item["author"] for item in combined_reviewers]
                    )
                    contributor_counter = author_counter + reviewer_counter

                    # Sort authors, reviewers, and contributors by count (descending)
                    sorted_authors = author_counter.most_common()
                    sorted_reviewers = reviewer_counter.most_common()
                    contributor_counter = contributor_counter.most_common()

                    # Prepare top 3 authors, reviewers, and contributors for the response
                    top_authors = {}
                    for i in range(3):
                        if i < len(sorted_authors):
                            top_authors[f"author{i+1}"] = sorted_authors[i][0]
                        else:
                            top_authors[f"author{i+1}"] = ""

                    top_reviewers = {}
                    for i in range(3):
                        if i < len(sorted_reviewers):
                            top_reviewers[f"reviewer{i+1}"] = sorted_reviewers[i][0]
                        else:
                            top_reviewers[f"reviewer{i+1}"] = ""

                    top_contributors = {}
                    for i in range(3):
                        if i < len(contributor_counter):
                            top_contributors[f"contributor{i+1}"] = contributor_counter[
                                i
                            ][0]
                        else:
                            top_contributors[f"contributor{i+1}"] = ""
                    # Build the final response data
                    response_data = {
                        "top_authors": top_authors,
                        "top_reviewers": top_reviewers,
                        "top_contributors": top_contributors,
                    }
                    # Cache the scoreboard for 24 hours (86400 seconds)
                    cache.set(cache_key, response_data, timeout=86400)
                finally:
                    # Release the lock so other requests can proceed
                    await sync_to_async(cache.delete)(lock_key)

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            # Handle invalid JSON in request
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError:
            # Handle invalid parameter types
            return JsonResponse({"error": "Invalid parameter type"}, status=400)
        except Exception as e:
            # Catch-all for unexpected errors
            print(e)
            return JsonResponse({"error": "An error occurred"}, status=500)
    else:
        # Only GET and POST are allowed
        return JsonResponse({"error": "Invalid request method"}, status=405)
