from django.template import Context, loader
from dichter.denhaag.models import *
from django.http import HttpResponse

def index(request):
	campaign_list = Campaign.objects.all().order_by('-start_date')[:5]
	t = loader.get_template('main.html')
	c = Context({'campaign_list': campaign_list, })
	return HttpResponse(t.render(c))

