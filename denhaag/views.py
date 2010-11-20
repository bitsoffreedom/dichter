from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
from dichter.denhaag.models import *
from django.http import HttpResponse, Http404

# non django imports
import datetime

def index(request, campaign_slug=None):
  today = datetime.date.today().isoformat()
  try:
    if not campaign_slug:
      c = Campaign.objects.filter(start_date__lte = today, end_date__gte = today).order_by('-start_date')[:1]
    else:
      c = Campaign.objects.filter(start_date__lte = today, end_date__gte = today).get(title_slug=campaign_slug)
  except Campaign.DoesNotExist:
    raise Http404

  campaign_list = Campaign.objects.filter(start_date__lte = today, end_date__gte = today).order_by('-start_date')
  politici_list = Politician.objects.all()
  for politicus in politici_list:
    politicus.contact_methods = PoliticianContactInfo.objects.filter(politician=politicus)

  return render_to_response('index.html', {'campaign_list': campaign_list, 'politici_list': politici_list, 'STATIC_PREFIX': settings.MEDIA_URL, 'campaign': c})

def send_message_mail(request, politicus):
  try:
    p = Politician.objects.get(name=politicus)
  except Politician.DoesNotExist:
    raise Http404
  return render_to_response('form_mail.html', {'politicus': p})

def send_message_facebook(request, politicus):
  try:
    p = Politician.objects.get(name=politicus)
  except Politician.DoesNotExist:
    raise Http404
  return render_to_response('form_facebook.html', {'politicus': p})

def send_message_hyves(request, politicus):
  try:
    p = Politician.objects.get(name=politicus)
  except Politician.DoesNotExist:
    raise Http404
  return render_to_response('form_hyves.html', {'politicus': p})


def static(request, slug):
	try:
		p = Static.objects.get(slug=slug)
		print p.slug
	except Static.DoesNotExist:
		raise Http404
	return render_to_response('static.html', {
		'page': p,
		'STATIC_PREFIX': settings.MEDIA_URL,
	})

