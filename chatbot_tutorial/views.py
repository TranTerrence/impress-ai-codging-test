from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
import spacy


def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message):
    result_message = {
        'type': 'text',
        'text': 'Hi, can you repeat your name please ?'
    }
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(message['text'])
    found = False
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            result_message['text'] = 'Hello ' + ent.text.capitalize()
            found = True
            continue
    if not found:
        # If he can't find the name, we assume that the name is the last noun of the sentence
        nouns = [token.text for token in doc if token.pos_ == 'NOUN']
        if nouns:
            result_message['text'] = 'Hello ' + nouns[-1].capitalize()
        found = True

    return result_message
