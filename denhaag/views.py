from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
from dichter.denhaag.models import *
from django.http import HttpResponse

def index(request, campaign_slug='stop-de-zwarte-lijst'):
	try:
        	c = Campaign.objects.get(title_slug=campaign_slug)
	except Campaign.DoesNotExist:
        	raise Http404

	campaign_list = Campaign.objects.all().order_by('-start_date')[:5]
	t = loader.get_template('index.html')
	return render_to_response('index.html', {'campaign_list': campaign_list, 'STATIC_PREFIX': settings.MEDIA_URL, 'campaign': c})
