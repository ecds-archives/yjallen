import os
import logging
from urllib import urlencode

from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import redirect

from yjallen_app.models import LetterTitle, Letter
from yjallen_app.forms import LetterSearchForm

from eulcommon.djangoextras.http.decorators import content_negotiation
from eulexistdb.query import escape_string
from eulexistdb.exceptions import DoesNotExist # ReturnedMultiple needed also ?
 
def index(request):
  letters = LetterTitle.objects.only('id', 'title', 'date').order_by('date')
  return render_to_response('index.html', {'letters' : letters},context_instance=RequestContext(request))

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
        letter = LetterTitle.objects.get(id__exact=doc_id)
        format = letter.xsl_transform(filename=os.path.join(settings.BASE_DIR, '..', 'yjallen_app', 'xslt', 'form.xsl'))
        return render_to_response('letter_display.html', {'letter': letter, 'format': format.serialize(), 'search_terms': search_terms}, context_instance=RequestContext(request))
    except DoesNotExist:
        raise Http404

def letter_xml(request, doc_id):
  "Display xml of a single issue."
  try:
    doc =LetterTitle.objects.get(id__exact=doc_id)
  except:
    raise Http404
  tei_xml = doc.serializeDocument(pretty=True)
  return HttpResponse(tei_xml, mimetype='application/xml')

def searchbox(request):
    "Search letters by title/author/keyword"
    form = LetterSearchForm(request.GET)
    response_code = None
    context = {'searchbox': form}
    search_opts = {}
    number_of_results = 20
      
    if form.is_valid():
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            search_opts['fulltext_terms'] = '%s' % form.cleaned_data['keyword']
                
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
        
    else:
        response = render(request, 'search.html', {"searchbox": form}, context_instance=RequestContext(request))
       
    if response_code is not None:
        response.status_code = response_code
    return response
