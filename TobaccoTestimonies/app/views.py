# Create your views here.
from django.views.generic.base import TemplateView
from forms import *
from django.shortcuts import render, redirect
import requests
import json
import shutil

def get_documents(request):
    ids = []
    count = 0
    numDocs = 100
    if request.method == 'GET':
        form = QuerySettingsForm(request.GET)
        if form.is_valid():
            while count <= 1000:
                if count % 100 == 0:
                    url = 'http://solr.industrydocumentslibrary.ucsf.edu/solr/ltdl3/query?q=topic: ' + request.GET['topic'] + '&start=' + str(count) + '&wt=json'
                    result = json.loads(requests.get(url).content)
                if count == 0:
                    numDocs = result['response']['numFound']
                
                documents = result['response']['docs']
                for doc in documents:
                    count = count + 1
                    ids.append(str(doc['id']))

            getDocs(ids)
            return render(request, 'httpResponse.html', {'documents': ids})
            

    template_name = 'index.html'
    form = QuerySettingsForm()
    return render(request, template_name, {'form': form})


def getDocs(docIdList):

    pathLoc = 'home/user/dump'
    shutil.rmtree(pathLoc)

    try:
        if not os.path.exists(pathLoc):
            os.makedirs(pathLoc)
    except OSError:
        print('Error creating directory')

    j = 0
    for docId in docIdList:
        print(docId)
        id1 = docId[0]
        id2 = docId[1]
        id3 = docId[2]
        id4 = docId[3]

        path = '/home/user1/root/' + id1 + '/' + id2 + '/' + id3 + '/' + id4 + '/' + docId
        print(path)

        shutil.copyfile(path + "/" + docId + ".ocr", pathLoc + "/" + docId + ".ocr")

        #docFile = open(path + "/" + docId + ".ocr", "r")
        #docFile.close()

