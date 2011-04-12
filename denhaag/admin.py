from dichter.denhaag.models import *
from django.contrib import admin

class PoliticianCampaignInline(admin.TabularInline):
	model = PoliticianCampaign
	extra = 1
	fields = ['politician', 'desc', 'weight']

class PoliticianContactInfoInline(admin.TabularInline):
	model = Politician.contact_info.through
	extra = 1
	# TODO: Set fields = ['bla', 'bla', ...]

class CampaignAdmin(admin.ModelAdmin):
  list_display = ('title', 'start_date', 'end_date')
  search_fields = ('title',)
  ordering = ('title',)
  date_hierarchy = 'start_date'
  inlines = [PoliticianCampaignInline,]
admin.site.register(Campaign, CampaignAdmin)

class PoliticianAdmin(admin.ModelAdmin):
  list_display = ('name', 'party', 'admin_image', 'gender')
  search_fields = ('name', 'party__name')
  ordering = ('name', 'party')
  fieldsets = [(None, {
  	'fields': [
		'name',
		'party',
		'desc',
		'gender',
		'pica',
  ]})]
  inlines = [PoliticianContactInfoInline,]
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
#admin.site.register(PoliticianCampaign, PoliticianCampaignAdmin)

class PoliticianContactInfoAdmin(admin.ModelAdmin):
  list_display = ('contact_method', 'address')
#admin.site.register(PoliticianContactInfo, PoliticianContactInfoAdmin)

class ActionAdmin(admin.ModelAdmin):
	list_display = ('campaign_contact', 'ip')
admin.site.register(Action, ActionAdmin)
admin.site.register(Response)

class StaticAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug')
admin.site.register(Static, StaticAdmin)

# XXX tmp fix
admin.site.register(PoliticianCampaign)

