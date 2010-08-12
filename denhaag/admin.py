from dichter.denhaag.models import *
from django.contrib import admin

class CampaignAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'end_date')
	search_fields = ('title',)
	ordering = ('title',)

class PartyAdmin(admin.ModelAdmin):
	list_display = ('name',)

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Politician)
admin.site.register(Party, PartyAdmin)
admin.site.register(PoliticianCampaign)
admin.site.register(Contact)
admin.site.register(Action)
admin.site.register(Response)
