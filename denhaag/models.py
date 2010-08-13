from django.db import models

class Campaign(models.Model):
	title = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	hashtag = models.CharField(max_length=42)
	desc = models.TextField()
	start_date = models.DateField()
	end_date = models.DateField()
	def __unicode__(self):
		return "%s: %s (%s tot %s)" % (self.title, self.desc, self.start_date, self.end_date)

class Party(models.Model):
	name = models.CharField(max_length=200)

class Politician(models.Model):
	GENDER_CHOICES = (
        	('M', 'Male'),
        	('F', 'Female'),
	)
	name = models.CharField(max_length=200)
	party = models.ForeignKey(Party)
	desc = models.TextField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class PoliticianCampaign(models.Model):
	campaign = models.ForeignKey(Campaign)
	politician = models.ForeignKey(Politician)
	desc = models.TextField()
	weight = models.IntegerField()

class ContactMethod(models.Model):
	name = models.CharField(max_length=25)

class CampaignContact(models.Model):
	campaign = models.ForeignKey(Campaign)
	contact_method = models.ForeignKey(ContactMethod)
	template = models.TextField()

class PoliticianContactInfo(models.Model):
	contact_method = models.ForeignKey(ContactMethod)
	politician = models.ForeignKey(Politician)
	address = models.CharField(max_length=200)

class Action(models.Model):
	campaign_contact = models.ForeignKey(CampaignContact)
	text = models.TextField()
	date = models.DateTimeField(auto_now=True)
	ip = models.IPAddressField()

class Response(models.Model):
	campaign_contact = models.ForeignKey(CampaignContact)
	text = models.TextField()
	date = models.DateTimeField(auto_now=True)
	ip = models.IPAddressField()
	
