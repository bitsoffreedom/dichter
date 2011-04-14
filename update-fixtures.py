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
import json
import os
import urllib2

FIXTURES_FILE = "fixtures"
PARLIAMENT_FILE = "kamerleden.csv"
TWITTER_URL = "http://politieklive.nl/~dbdhcsv.php"


# If fixtures file is present: load it
if os.path.exists(FIXTURES_FILE):
    old_fixtures = json.load(open(FIXTURES_FILE))
else:
    old_fixtures = []


parliament = csv.reader(open(PARLIAMENT_FILE), delimiter=";")
parties_json = []
parties = {}
partyid = 1
members_json = []
members = {}
memberid = 1
contact_json = []
for member in parliament:
    # Skip header
    if member[0] == "image": continue
    afko = member[10][member[10].find('(')+1:-1].lower()
    if not parties.has_key(afko):
        parties[afko] = partyid
        parties_json.append({
            "model": "denhaag.Party",
            "pk": partyid,
            "fields": {
                "name": member[10],
                "pica": "images/partij_logos/%s.gif" % (afko)
            }
        })
        partyid += 1
    dstimage = 'politici/%s.jpg' % member[1].replace('/', '-')
    if not os.path.exists('static/%s' % dstimage):
        print 'http://www.tweedekamer.nl%s' % (member[0])
        srcimage = urllib2.urlopen('http://www.tweedekamer.nl%s' % member[0]).read()
        open('static/%s' % dstimage, 'w').write(srcimage)
    contact_json.append({
        "model": "denhaag.PoliticianContactInfo",
        "pk": memberid,
        "fields": {
            "contact_method": 1,
            "address": member[9].lower()
        }
    })
    members[member[1]] = memberid
    members_json.append({
        "model": "denhaag.Politician",
        "pk": memberid,
        "fields": {
            "name": member[1],
            "party": parties[afko],
            "desc": "Actief in: " + ",".join(member[12:31]).rstrip(","),
            "gender": member[8]  == 'Man' and 'M' or 'F',
            "pica": dstimage,
            "contact_info": [memberid, ]
        }
    })
    memberid += 1

# Now add the twitter accounts
twitter_csv = csv.reader(urllib2.urlopen(TWITTER_URL), delimiter=",")
for tweep in twitter_csv:
    if len(tweep) == 2: # Has twitter account
        match = difflib.get_close_matches(tweep[0], members.keys())
        if not match: continue
        match = match[0]
        for i in range(len(members_json)):
            if members_json[i]["pk"] == members[match]:
                members_json[i]["fields"]["contact_info"].append(memberid)
                break
        contact_json.append({
            "model": "denhaag.PoliticianContactInfo",
            "pk": memberid,
            "fields": {
                "contact_method": 2,
                "address": tweep[1]
            }
        })
        memberid += 1

new_json = old_fixtures + parties_json + members_json + contact_json



# Write the new fixtures to file
with open(FIXTURES_FILE, "w") as f:
    json.dump(new_json, f, indent=4)



