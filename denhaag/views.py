from django.template import Context, loader
from django.shortcuts import render_to_response
from dichter.denhaag.models import *
from django.http import HttpResponse

def index(request):
	campaign_list = Campaign.objects.all().order_by('-start_date')[:5]
	t = loader.get_template('index.html')
	return render_to_response('index.html', {'campaign_list': campaign_list, 'STATIC_PREFIX': 'http://127.0.0.1:8000/media/'});

def campaign_detail(request, campaign_id):
    try:
        c = Campaign.objects.get(pk=campaign_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('campaign_detail.html', {'campaign': c})

def send_message_mail(request, politicus):
  try:
    p = Politician.objects.get(name=politicus)
  except Poll.DoesNotExist:
    raise Http404
  return render_to_response('form_mail.html', {'politicus': p})

def send_message_facebook(request, politicus):
  try:
    p = Politician.objects.get(name=politicus)
  except Poll.DoesNotExist:
    raise Http404
  return render_to_response('form_facebook.html', {'politicus': p})

def send_message_hyves(request, politicus):
  try:
    p = Politician.objects.get(name=politicus)
  except Poll.DoesNotExist:
    raise Http404
  return render_to_response('form_hyves.html', {'politicus': p})

