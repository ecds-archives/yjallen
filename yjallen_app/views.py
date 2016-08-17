import os
import re
import logging
from urllib import urlencode
from datetime import datetime
import tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
import mimetypes

from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib import messages

from yjallen_app.models import LetterTitle, Letter
from yjallen_app.forms import LetterSearchForm

from eulcommon.djangoextras.http.decorators import content_negotiation
from eulexistdb.query import escape_string
from eulexistdb.exceptions import DoesNotExist # ReturnedMultiple needed also ?
from eulexistdb.db import ExistDBException
 
def index(request):
  context = {}
  labels = {}
  letters_1 = ['College']
  letters_2 = ['Missionary']
  letters_3 = ['Journalism']
  letters_4 = ['Leadership']
  labels = {'College':'College Years, 1854-1858', 'Missionary':'Early Missionary Experience, 1859-1967', 'Journalism':'Journalism Career, 1868-1882', 'Leadership':'Leadership in Methodist Mission, 1883-1906'}
  letters = LetterTitle.objects.only('id', 'head', 'title', 'date', 'date_num').order_by('date_num')
  for letter in letters:
      year = re.search(r'\d\d\d\d', letter.date_num).group(0)
      if int(year) > 1853 and int(year) < 1859:
        letters_1.append(letter)
      if int(year) > 1858 and int(year) < 1868:
        letters_2.append(letter)
      if int(year) > 1867 and int(year) < 1884:
        letters_3.append(letter)
      if int(year) > 1883:
        letters_4.append(letter)
  groups = [letters_1, letters_2, letters_3, letters_4]

  context['letters'] = letters
  context['groups'] = groups
  context['year'] = year
  context['letters_1'] = letters_1
  context['labels'] = labels

        
  return render_to_response('index.html', context, context_instance=RequestContext(request))

def overview(request):
  return render_to_response('overview.html', {'overview' : overview}, context_instance=RequestContext(request))

def letter_display(request, doc_id):
    "Display the contents of a single letter."
    if 'keyword' in request.GET:
        search_terms = request.GET['keyword']
        url_params = '?' + urlencode({'keyword': search_terms})
        filter = {'highlight': search_terms}    
    else:
        url_params = ''
        filter = {}
        search_terms = None
    try:              
        letter = LetterTitle.objects.filter(**filter).get(id__exact=doc_id)
        format = letter.xsl_transform(filename=os.path.join(settings.BASE_DIR, '..', 'yjallen_app', 'xslt', 'form.xsl'))
        return render_to_response('letter_display.html', {'letter': letter, 'format': format.serialize(), 'search_terms': search_terms}, context_instance=RequestContext(request))
    except DoesNotExist:
        raise Http404

def letter_xml(request, doc_id):
  "Display xml of a single issue."
  try:
    doc = LetterTitle.objects.get(id__exact=doc_id)
  except: 
    raise Http404
  tei_xml = doc.serializeDocument(pretty=True)
  return HttpResponse(tei_xml, content_type='application/xml')

def searchbox(request):
    query_error = False
    "Search letters by title/author/keyword"
    form = LetterSearchForm(request.GET)
    response_code = None
    context = {'searchbox': form}
    search_opts = {}
    number_of_results = 20
      
    if form.is_valid():
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            search_opts['fulltext_terms'] = '%s' % form.cleaned_data['keyword']
        
        try:        
            letters = LetterTitle.objects.only("id", "title", "author", "date").filter(**search_opts)

            searchbox_paginator = Paginator(letters, number_of_results)
        
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            # If page request (9999) is out of range, deliver last page of results.
            try:
                searchbox_page = searchbox_paginator.page(page)
            except (EmptyPage, InvalidPage):
                searchbox_page = searchbox_paginator.page(paginator.num_pages)

            context['letters'] = letters
            context['letters_paginated'] = searchbox_page
            context['keyword'] = form.cleaned_data['keyword']
           
            response = render_to_response('search_results.html', context, context_instance=RequestContext(request))
        #no search conducted yet, default form
        except  ExistDBException as e:
            query_error = True
            if 'Cannot parse' in e.message():
                messages.error(request, 'Your search query could not be parsed.  ' + 'Please revise your search and try again.')
            else:
                # generic error message for any other exception
                messages.error(request, 'There was an error processing your search.')
            response = render(request, 'search.html',{'searchbox': form, 'request': request})
        
    else:
        response = render(request, 'search.html', {"searchbox": form}, context_instance=RequestContext(request))
       
    if response_code is not None:
        response.status_code = response_code
    if query_error:
        response.status_code = 400

    return response

def send_file(request, basename):
    if basename == 'yja_letters':
        extension = '.zip'
    else:
        extension = '.txt'
    filepath = 'static/txt/' + re.sub(r'\.\d\d\d', '', basename ) + extension
    filename  = os.path.join(settings.BASE_DIR, filepath )
    download_name = basename + extension
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
