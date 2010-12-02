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
    campaign = Campaign.objects.filter(
        start_date__lte=today, end_date__gte=today)
    if not campaign_slug:
      campaign = campaign.order_by('-start_date')[:1]
    else:
      campaign = campaign.get(title_slug=campaign_slug)
  except Campaign.DoesNotExist:
    raise Http404

  campaign_list = Campaign.objects.filter(
      start_date__lte=today, end_date__gte=today).order_by('-start_date')
  politicians_list = PoliticianCampaign.objects.filter(campaign=campaign)

  return render_to_response(
      'index.html',
      {'campaign_list': campaign_list, 'politicians_list': politicians_list,
       'STATIC_PREFIX': settings.MEDIA_URL, 'campaign': campaign})

def politician_info(request, politician=''):
  politician = Politician.objects.get(name=unsluggify(politician))
  if not politician:
    raise Http404
  return render_to_response(
      'politician.html',
      {'STATIC_PREFIX': settings.MEDIA_URL, 'politician': politician})

def send_message_mail(request, politician):
  try:
    politician = Politician.objects.get(name=politician)
  except Politician.DoesNotExist:
    raise Http404
  return render_to_response('form_mail.html', {'politician': politician})

def send_message_facebook(request, politician):
  try:
    politician = Politician.objects.get(name=politician)
  except Politician.DoesNotExist:
    raise Http404
  return render_to_response('form_facebook.html', {'politician': politician})

def send_message_hyves(request, politician):
  try:
    politician = Politician.objects.get(name=politician)
  except Politician.DoesNotExist:
    raise Http404
  return render_to_response('form_hyves.html', {'politician': politician})


def static(request, slug):
  try:
    politician = Static.objects.get(slug=slug)
    print politician.slug
  except Static.DoesNotExist:
    raise Http404
  return render_to_response(
      'static.html',
      {'page': politician, 'STATIC_PREFIX': settings.MEDIA_URL})
