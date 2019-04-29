# Create your views here.
from django.views.generic.base import TemplateView
from forms import *
from django.shortcuts import render, redirect
import requests
import json

def get_documents(request):
    ids = []
    count = 0
    if request.method == 'GET':
        form = QuerySettingsForm(request.GET)
        if form.is_valid():
            url = 'http://solr.industrydocumentslibrary.ucsf.edu/solr/ltdl3/query?q=' + request.GET['topic'] + '&wt=json'
            result = json.loads(requests.get(url).content)
            #documents = result['response']['docs']
            #for doc in documents:
                #count = count + 1
                #ids.append(str(doc['id']))
            #count = count + 1
            return render(request, 'httpResponse.html', {'documents': result})
            #docFound = result['response']['numFound']
            #while count < docFound:
                #if count % 100 == 0:
                    #sec_url = 'http://solr.industrydocumentslibrary.ucsf.edu/solr/ltdl3/query?q=topic:' + request.GET['topic'] + '&start=' + str(count) + '&wt=json'
                    #sec_result = json.loads(requests.get(sec_url).content)
                    #sec_doc = sec_result['response']['docs']

    template_name = 'index.html'
    form = QuerySettingsForm()
    return render(request, template_name, {'form': form})
