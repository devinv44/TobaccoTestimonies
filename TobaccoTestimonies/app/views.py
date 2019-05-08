# Create your views here.
from django.views.generic.base import TemplateView
from forms import *
from django.shortcuts import render, redirect
import requests
import json
import shutil
import os
from django.views.static import serve

#clustering imports
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import codecs
import nltk
import glob
import errno
import re

def get_documents(request):
    ids = []
    count = 0
    numDocs = 100
    if request.method == 'GET':
        form = QuerySettingsForm(request.GET)
        if form.is_valid():
            while count <= numDocs:
                if count % 100 == 0:
                    url = 'http://solr.industrydocumentslibrary.ucsf.edu/solr/ltdl3/query?q=topic:' + request.GET['topic'] + '&start=' + str(count) + '&wt=json'
                    result = json.loads(requests.get(url).content)
                if count == 0:
                    numDocs = result['response']['numFound']
                
                documents = result['response']['docs']
                for doc in documents:
                    count = count + 1
                    ids.append(str(doc['id']))

            getDocs(ids)
            cluster = cluster_docs()
            cluster_count = display_results(cluster)
            return render(request, 'httpResponse.html', {'num_clusters': cluster_count})
            

    template_name = 'index.html'
    form = QuerySettingsForm()
    return render(request, template_name, {'form': form})


def getDocs(docIdList):

    dirpath = os.getcwd()
    print(dirpath)
    pathLoc = '/home/user1/dump'
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
	exists = os.path.isfile(path + "/" + docId + ".ocr")
	if exists:
        	shutil.copyfile(path + "/" + docId + ".ocr", pathLoc + "/" + docId + ".ocr")
	else:
		print(path + " not found")

        #docFile = open(path + "/" + docId + ".ocr", "r")
        #docFile.close()

def cluster_docs():
    corpus = []
    #filepath to the folder with txt files 
    #this needs to be where all the files pulled from the API are stored
    path = '/home/user1/dump/*.ocr'
    #glob.glob return list of path names as string
    files = glob.glob(path)
    fileIDS = {}
    corpus2 = []
    #https://www.quora.com/How-do-I-read-mutiple-txt-files-from-folder-in-python idea to loop like this to read in files came from here
    #loop through all of the files in the folder
    count = 0
    for name in files:
        try:
            with open(name) as f:
                fileIDS[count] = name[17:len(name) - 4]
    #had an issue with characters not being identified as ascii so use the idea here 
    #https://stackoverflow.com/questions/43358857/how-to-remove-special-characters-except-space-from-a-file-in-python/43358965 
    #to remove them
                final = " ".join(re.findall(r"[a-zA-Z0-9]+", f.read()))
                token = word_tokenize(final)
                #add the text to the corpus
                corpus.append(final)
                corpus2.append(token)
        except IOError as exc:
            #error handling
            if exc.errno != errno.EISDIR:
                raise
        count += 1 

    model = Doc2Vec.load("/home/user1/doc2vecNew.model")


    X=[]
    start_alpha=0.01
    infer_epoch=100
    for d in corpus2:     
        X.append(model.infer_vector(d, alpha=start_alpha, steps=infer_epoch))

    from sklearn.cluster import Birch

    num_clusters = 10
    brc = Birch(branching_factor=50, n_clusters=num_clusters, threshold=0.1, compute_labels=True)
    brc.fit(X)

    clusters = brc.predict(X)

    print ("Clusters: ")
    print (clusters)

    cluster_ids = []

    for i in range(num_clusters):
        c = []
        for j in range(len(clusters)):
            if clusters[j] == i:
                c.append(fileIDS[j])
        cluster_ids.append(c)

    clus_count = 0
    for x in cluster_ids:
        print("Cluster {}:".format(clus_count))
        print(x)
        print("\n")
        clus_count += 1
        
    return cluster_ids

def display_results(clusters):
    pathLoc = 'app/clusters_txt_files'
    shutil.rmtree(pathLoc)
    
    try:
        if not os.path.exists(pathLoc):
            os.makedirs(pathLoc)
    except OSError:
        print('Error creating clusters text files directory')
    
    base_url = "https://www.industrydocuments.ucsf.edu/tobacco/docs/#id="
    
    
    clus_count = 0
    for cluster in clusters:
        clus_count += 1
        text_file = open(pathLoc + "/Cluster_{}.txt".format(clus_count), "w+")
        for doc_id in cluster:
            text_file.write(base_url + doc_id)
            text_file.write("\n")
        text_file.close()
    
    clusters = []
    for clus in range(1, clus_count):
	clusters.append(clus)
    
    return clusters
        

def serve_cluster(request, cluster_count):            
    filepath = '/home/user1/Menu/TobaccoTestimonies/TobaccoTestimonies/app/clusters_txt_files/Cluster_' + str(cluster_count) + '.txt'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
