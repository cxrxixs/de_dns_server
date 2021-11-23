import json
from json.decoder import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage, Paginator
from django.http import (HttpResponseBadRequest, HttpResponseServerError,
                         JsonResponse)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import DeDnsServer
from .utils import AuthToken, Validator

# Create your views here.


@csrf_exempt
def api_de_dns_server(request):
    try:

        auth_key = request.headers.get('Auth-Key')
        # Check if Auth-Key is provided in the request
        if not auth_key:
            return JsonResponse(
                data={'error_message': 'Invalid Auth-Key'},
                status=401,
            )

        # Check that Auth-Key is valid and not revoked
        token = AuthToken(auth_key)
        if not token.valid():
            return JsonResponse(
                data={'error_message': 'Invalid Auth-Key'},
                status=401,
            )

        if request.method == 'GET':
            """
            TASK: To update
            Implementation of RESTful API
            """

            as_number = request.GET.get('as_number')
            queries = {}
            if as_number:
                queries['as_number'] = as_number
                # Only allow value that can be converted to number to prevent error at db query

                v = Validator('as_number', as_number)
                if not v.check():
                    return JsonResponse(
                        data={'error_message': 'Invalid as_type'},
                        status=400,
                    )

            checked_at = request.GET.get('checked_at')
            if checked_at:
                queries['checked_at'] = checked_at
                # Only allow value that can be converted to number to prevent error at db query

                v = Validator('checked_at', checked_at)
                if not v.check():
                    return JsonResponse(
                        data={'error_message': 'Invalid as_type'},
                        status=400,
                    )

            sort_term = request.GET.get('sort')
            sort_list = ['id']
            if sort_term:
                sort_by = sort_term.split('.')[0]
                sort_order = sort_term.split('.')[1]

                if sort_by != 'as_number':
                    # Only `as_number` property is currently supported for sorting
                    return JsonResponse(
                        data={'error_message': 'Invalid sort value'},
                        status=400,
                    )

                if sort_order not in ['asc', 'desc']:
                    return JsonResponse(
                        data={'error_message': 'Invalid sort order'},
                        status=400,
                    )

                if sort_order == 'asc':
                    sort_list.insert(0, 'as_number')

                if sort_order == 'desc':
                    sort_list.insert(0, '-as_number')

            obj = DeDnsServer.objects.filter(**queries).order_by(*sort_list).all()

            DEFAULT_PAGE = 1
            page_num = (
                request.GET.get('page', DEFAULT_PAGE)
                if request.GET.get('page', DEFAULT_PAGE) != ''
                else DEFAULT_PAGE
            )
            p = Paginator(obj.values(), 10)
            try:
                dns_servers = p.page(page_num)
            except InvalidPage:
                # Is this good for user exeperience?
                # User might assume that page exist since it returns valid values
                dns_servers = p.page(1)

            next_page = (
                dns_servers.next_page_number() if dns_servers.has_next() else None
            )

            response = {
                'count': len(dns_servers),
                'next_page': next_page,
                'dns_servers_list': [],
            }

            for dns in dns_servers:
                response['dns_servers_list'].append(dns)

            return JsonResponse(response, status=200)

        elif request.method == 'POST':
            """
            TASK: To update
            """

            # Get body parameter
            try:
                data = json.loads(request.body)
                if 'country' in data.keys():
                    # Remove key and replace with countr_code to match db Model
                    data['country_code'] = data.pop('country')

                if not 'country_code' in data.keys():
                    data['country_code'] = 'DE'

                if data['country_code'] == '':
                    # Default to `DE` from requirements
                    data['country_code'] = 'DE'

            except JSONDecodeError:
                # When POST request is not formatted properly
                return JsonResponse(
                    data={'error_message': f'Malformed body parameters'},
                    status=400,
                )

            REQUIRED_PARAMS = [
                'ip_address',
                'as_number',
                'as_org',
                'checked_at',
                'reliability',
            ]
            # Check that required params are present

            for r in REQUIRED_PARAMS:
                if r not in data.keys():
                    return JsonResponse(
                        data={'error_message': f'Missing required parameter {r}'},
                        status=400,
                    )

            for key, val in data.items():
                if key in REQUIRED_PARAMS:
                    if val == None or val == '':
                        return JsonResponse(
                            data={'error_message': f'Missing required parameter {key}'},
                            status=400,
                        )

                    # Validate that parameters are of correct data type
                    v = Validator(key, val)
                    if not v.check():
                        return JsonResponse(
                            data={'error_message': f'Invalid {key} data type'},
                            status=400,
                        )

            dns = DeDnsServer(**data).save()

            response = {
                'success': True,
                'message': 'Add new DNS record',
                'data': dns,
            }

            return JsonResponse(
                data={},
                status=201,
            )

        else:
            return HttpResponseBadRequest()
    except Exception as e:
        print(e)
        return HttpResponseServerError()


def filter_de_dns_server(request):
    try:
        if request.method == 'GET':
            as_number = request.GET.get('as_number')
            checked_at = request.GET.get('checked_at')
            as_org = request.GET.get('as_org')
            as_org_matching = request.GET.get('as_org_matching')

            # When there are no filters applied, sort according to requriements from Task 3
            if not as_number and not checked_at and not as_org:
                # Get all as_number
                unique_as_number = DeDnsServer.objects.filter(error=False).distinct(
                    "as_number"
                )

                # Check if as_number have only one entry then add to exclude list
                exclude_as = []
                for u in unique_as_number:
                    if DeDnsServer.objects.filter(as_number=u.as_number).count() == 1:
                        exclude_as.append(u.as_number)

                # Add ordering by reliability(highest), checked_at(latest), created_at(first)
                dns_servers = (
                    DeDnsServer.objects.exclude(as_number__in=exclude_as)
                    .order_by("-reliability", "-checked_at", "created_at")
                    .values()[:5]
                )

                context = {'dns_servers_list': []}
                for dns_server in dns_servers:
                    context['dns_servers_list'].append(dns_server)

                return render(request, 'index.html', context)

            queries = {}
            if as_number:
                queries['as_number'] = as_number
            if checked_at:
                queries['checked_at'] = checked_at

            matching = {}
            if as_org:
                if as_org_matching == 'exact':
                    matching['as_org__iexact'] = as_org
                else:
                    matching['as_org__icontains'] = as_org

            dns_servers = (
                DeDnsServer.objects.filter(**queries).filter(**matching).values()
            )

            context = {'dns_servers_list': []}
            for dns_server in dns_servers:
                context['dns_servers_list'].append(dns_server)

            return render(request, 'index.html', context)
        else:
            context = {}
            return render(request, 'index.html', context)
    except Exception:
        context = {}
        return render(request, 'index.html', context)


@login_required
def index(request):
    de_dns_servers = DeDnsServer.objects.order_by('-checked_at').values()[:5]
    context = {'dns_servers_list': de_dns_servers}
    return render(request, 'index.html', context)
