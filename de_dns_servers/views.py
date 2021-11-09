from django.shortcuts import render

# Create your views here.

import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from .models import DeDnsServer
from django.shortcuts import render

def api_de_dns_server(request):
    try:
        if request.method == 'GET':
            '''
            TASK: To update
            '''
            pass
        elif request.method == 'POST':
            '''
            TASK: To update
            '''
            pass
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        print(e)
        return HttpResponseServerError()

def get_de_dns_servers_for_checking(request):
    '''
    TASK: To update
    '''
    pass

def filter_de_dns_server(request):
    try:
        if request.method == 'GET':
            as_number = request.GET.get('as_number')
            checked_at = request.GET.get('checked_at')

            queries = {}
            if as_number:
                queries['as_number'] = as_number
            if checked_at:
                queries['checked_at'] = checked_at

            dns_servers = DeDnsServer.objects.filter(**queries).values()

            context = {
                'dns_servers_list': []
            }
            for dns_server in dns_servers:
                context['dns_servers_list'].append(dns_server)

            return render(request, 'index.html', context)
        else:
            context = {}
            return render(request, 'index.html', context)
    except Exception:
        context = {}
        return render(request, 'index.html', context)

def index(request):
    de_dns_servers = DeDnsServer.objects.order_by('-checked_at').values()[:5]
    context = {
        'dns_servers_list': de_dns_servers
    }
    return render(request, 'index.html', context)
