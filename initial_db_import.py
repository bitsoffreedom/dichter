#!/usr/bin/env python
###############################################################################
# Copyright (c) 2011, Floor Terra <floort@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
###############################################################################

import csv
import difflib
import os, sys
import urllib2

os.environ["DJANGO_SETTINGS_MODULE"] = "dichter.settings"

import django
from django.core.management import setup_environ
import settings
setup_environ(settings)
from denhaag.models import *

FIXTURES_FILE = "fixtures"
PARLIAMENT_FILE = "kamerleden.csv"
TWITTER_URL = "http://politieklive.nl/~dbdhcsv.php"


# Setup default stuff
twitter_cm = ContactMethod(id=1, name="twitter", prefix="@")
twitter_cm.save()
email_cm = ContactMethod(id=2, name="email", prefix="")
email_cm.save()


parliament = csv.reader(open(PARLIAMENT_FILE), delimiter=";")
parties = {}
members = {}
for member in parliament:
    # Skip header
    if member[0] == "image": continue
    afko = member[10][member[10].find('(')+1:-1].lower()
    if not parties.has_key(afko):
        p = Party(name=member[10], pica="images/partij_logos/%s.gif" %(afko))
        p.save()
        parties[afko] = p.id
    dstimage = 'politici/%s.jpg' % member[1].replace('/', '-')
    if not os.path.exists('static/%s' % dstimage):
        print 'http://www.tweedekamer.nl%s' % (member[0])
        srcimage = urllib2.urlopen('http://www.tweedekamer.nl%s' % member[0]).read()
        open('static/%s' % dstimage, 'w').write(srcimage)
    pci = PoliticianContactInfo(
        contact_method = email_cm,
        address = member[9].lower()
    )
    pci.save()
    p = Politician(
        name = member[1],
        party = Party.objects.get(id=parties[afko]),
        desc = "Actief in: " + ",".join(member[12:31]).rstrip(","),
        gender = member[8]  == 'Man' and 'M' or 'F',
        pica = dstimage,
    )
    p.save()
    p.contact_info.add(pci)
    p.save()
    members[member[1]] = p.id

# Now add the twitter accounts
twitter_csv = csv.reader(urllib2.urlopen(TWITTER_URL), delimiter=",")
for tweep in twitter_csv:
    if len(tweep) == 2: # Has twitter account
        if not tweep[1]: continue
        match = difflib.get_close_matches(tweep[0], members.keys())
        if not match: continue
        match = match[0]
        pci = PoliticianContactInfo(
            contact_method = twitter_cm,
            address = tweep[1]
        )
        pci.save()
        p = Politician.objects.get(id=members[match])
        p.contact_info.add(pci)
        p.save()


