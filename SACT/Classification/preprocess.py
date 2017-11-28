import argparse
import json
import sys

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import pandas as pd
import numpy
from random import shuffle
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer


def get_service():
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    return discovery.build('language', 'v1beta1', http=http)


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def analyze_syntax(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extract_syntax': True,
        },
        'encodingType': encoding,
    }

    service = get_service()

    request = service.documents().annotateText(body=body)
    response = request.execute()
    sentence = ''
    for i in range(len(response["tokens"])):
        sentence += response["tokens"][i]['text']['content']+'/'+response["tokens"][i]['partOfSpeech']['tag']+' '
    # '/'+response["tokens"][i]['dependencyEdge']['label']+
    return sentence

cachedStopWords = stopwords.words("english")

def bow(path):
	file = pd.read_csv(path, delimiter='\t')
	sentences = []
	for i in range(len(file)):
		sentences.append(re.sub("[^a-zA-Z]", " ", file['text'][i]))
		sentences[i] = sentences[i].lower()
	target = file['class']
	stri = ""
	sntncs = []
	wnl = WordNetLemmatizer()
	for i in range(len(sentences)):
		tkns = sentences[i].split()

		jaffa = []
		for wd in tkns:
			if wd not in cachedStopWords:
				# jaffa.append(wnl.lemmatize(wd))
				jaffa.append(wd)

		sentences[i] = " ".join(jaffa)
		sentences[i] = analyze_syntax(sentences[i])	
		stri+= sentences[i]+"\t"+str(target[i])+"\n"

	with open('Dataset/nlapi_classify.txt', 'w') as f:
			f.write(stri)
	return(sentences, target)




