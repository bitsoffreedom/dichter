from django.template import Context, loader
from django.shortcuts import render_to_response
from dichter.denhaag.models import *
from django.http import HttpResponse

def index(request):
	campaign_list = Campaign.objects.all().order_by('-start_date')[:5]
	t = loader.get_template('main.html')
	return render_to_response('main.html', {'campaign_list': campaign_list});

def campaign_detail(request, campaign_id):
    try:
        c = Campaign.objects.get(pk=campaign_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('campaign_detail.html', {'campaign': c})

