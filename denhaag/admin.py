from dichter.denhaag.models import *
from django.contrib import admin

class CampaignAdmin(admin.ModelAdmin):
  list_display = ('title', 'start_date', 'end_date')
  search_fields = ('title',)
  ordering = ('title',)
  date_hierarchy = 'start_date'
admin.site.register(Campaign, CampaignAdmin)

class PoliticianAdmin(admin.ModelAdmin):
  list_display = ('name', 'party')
  search_fields = ('name', 'party')
  ordering = ('name', 'party')
admin.site.register(Politician, PoliticianAdmin)
  
class PartyAdmin(admin.ModelAdmin):
  list_display = ('name', 'admin_image')
admin.site.register(Party, PartyAdmin)

class ContactMethodAdmin(admin.ModelAdmin):
  list_display = ('name','enabled')
admin.site.register(ContactMethod, ContactMethodAdmin)

class CampaignContactAdmin(admin.ModelAdmin):
  list_display = ('campaign', 'contact_method')
admin.site.register(CampaignContact, CampaignContactAdmin)

class PoliticianCampaignAdmin(admin.ModelAdmin):
  list_display = ('politician', 'campaign', 'weight')
admin.site.register(PoliticianCampaign, PoliticianCampaignAdmin)

class PoliticianContactInfoAdmin(admin.ModelAdmin):
  list_display = ('politician', 'address', 'contact_method')
admin.site.register(PoliticianContactInfo, PoliticianContactInfoAdmin)

class ActionAdmin(admin.ModelAdmin):
	list_display = ('campaign_contact', 'ip')
admin.site.register(Action, ActionAdmin)
admin.site.register(Response)

class StaticAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug')
admin.site.register(Static, StaticAdmin)


