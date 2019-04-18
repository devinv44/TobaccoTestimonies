# Create your views here.
from django.views.generic.base import TemplateView
from forms import *
from django.shortcuts import render, redirect
import requests
import json

def get_documents(request):
    if request.method == 'GET':
        form = QuerySettingsForm(request.GET)
        if form.is_valid():
            url = 'http://solr.industrydocumentslibrary.ucsf.edu/solr/ltdl3/query?q=author:' + request.GET['person'] + ' AND topic:' + request.GET['topic'] + '&wt=json'
            result = json.loads(requests.get(url).content)
            return render(request, 'httpResponse.html', {'documents': result['response']})

    template_name = 'index.html'
    form = QuerySettingsForm()
    return render(request, template_name, {'form': form})
