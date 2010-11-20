#!/usr/bin/python
import csv
import urllib
import os


partycsv = csv.reader(open('kamerleden.csv'), delimiter=';')
partiesoutput = []
parties = {}
i=0
partycsv.next()
for party in partycsv:
  if party[10] not in parties and party[10] is not 'N/A':
    i = i+1
    parties[party[10]] = i
    afko = party[10][party[10].find('(')+1:-1].lower()
    partiesoutput.append("""{
	    "model": "denhaag.Party",
	    "pk": %d,
	    "fields":{
	      "name": "%s",
		    "pica": "images/partij_logos/%s.jpg"
	    }
	  }""" % (i,
	          party[10],
	          afko))
  
print ','.join(partiesoutput)
  
c = csv.reader(open('kamerleden.csv'), delimiter=';')
politicusoutput = []
i=0
c.next()
for politicus in c:
  if politicus[10] is 'N/A':
    continue
  i = i+1
  dstimage = 'politici/%s.jpg' % politicus[1].replace('/', '-')
  if not os.path.exists('static/%s' % dstimage):
    srcimage = urllib.urlopen('http://www.tweedekamer.nl%s' % politicus[0]).read()
    open('static/%s' % dstimage, 'w').write(srcimage)
  politicusoutput.append("""{
    "model": "denhaag.Politician",
    "pk": %d,
    "fields":{
      "name":"%s",
      "party": %d,
      "desc": "Actief in: %s",
      "gender": "%s",
	    "pica": "%s"
    }
  }""" % (i, 
          politicus[1],
          parties[politicus[10]],
          ','.join(politicus[12:31]).rstrip(','),
          politicus[8]  == 'Man' and 'M' or 'F',
          dstimage))
  
print ','.join(politicusoutput)
