from django.db import models
from django.conf import settings

class Campaign(models.Model):
	title = models.CharField(max_length=200)
	title_slug = models.CharField(max_length=200)
	subtitle = models.CharField(max_length=200)
	intro = models.TextField()
	desc = models.TextField()	
	pica = models.ImageField(upload_to='photos/%Y/%m/%d')
	email_subject = models.CharField(max_length=255)	
	email_text = models.TextField()
	phone_text = models.TextField()		
	hashtag = models.CharField(max_length=42)	
	start_date = models.DateField()
	end_date = models.DateField()
	def __unicode__(self):
		return "%s: %s (%s tot %s)" % (self.title, self.desc, self.start_date, self.end_date)

class Party(models.Model):
  name = models.CharField(max_length=200)
  pica = models.ImageField(upload_to='photos/%Y/%m/%d')
  def __unicode__(self):
    return self.name
  def admin_image(self):
    return '<img src="%s" alt="%s"/>' % (self.pica.url, self.name)
  admin_image.allow_tags = True

class Politician(models.Model):
  GENDER_CHOICES = (
        	('M', 'Male'),
        	('F', 'Female'),
  )
  name = models.CharField(max_length=200)
  party = models.ForeignKey(Party)
  desc = models.TextField()
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  pica = models.ImageField(upload_to='photos/%Y/%m/%d')
  contact_info = models.ManyToManyField('PoliticianContactInfo')
  def name_slug(self):
    return sluggify(self.name)

  def __unicode__(self):
    return self.name.decode("utf_8")
  def admin_image(self):
    return u'<img src="%s" alt="%s"/>' % (self.pica.url, self.name)
  admin_image.allow_tags = True
  def contact_email(self):
    return self.contact_info.get(contact_method__name = "email")
  def contact_phone(self):
    return self.contact_info.get(contact_method__name = "phone")
  def contact_twitter(self):
    return self.contact_info.get(contact_method__name = "twitter")

class PoliticianCampaign(models.Model):
    campaign = models.ForeignKey(Campaign)
    politician = models.ForeignKey(Politician)
    desc = models.TextField(blank=True)
    weight = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return '%s - %s ' % (self.politician.name, self.campaign.title)

class ContactMethod(models.Model):
  name = models.CharField(max_length=25)
  enabled = models.BooleanField(default=True)
  prefix = models.CharField(max_length=40, blank=True)
  def __unicode__(self):
    return self.name

class CampaignContact(models.Model):
	campaign = models.ForeignKey(Campaign)
	contact_method = models.ForeignKey(ContactMethod)
	template = models.TextField()

class PoliticianContactInfo(models.Model):
  contact_method = models.ForeignKey(ContactMethod)
  #  politician = models.ForeignKey(Politician)
  address = models.CharField(max_length=200)
  def __unicode__(self):
    return self.contact_method.prefix + self.address


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

class Static(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=200)
	page = models.TextField()

	def __unicode__(self):
		return self.slug


def sluggify(string):
  return string.replace(' ', '_')


def unsluggify(string):
  return string.replace('_', ' ')
