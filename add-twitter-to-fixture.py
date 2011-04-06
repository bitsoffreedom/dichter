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
import json
import os

FIXTURES_FILE = "fixtures"
PARLIAMENT_FILE = "kamerleden.csv"


# If fixtures file is present: load it
if os.path.exists(FIXTURES_FILE):
    old_fixtures = json.load(open(FIXTURES_FILE))
else:
    old_fixtures = []


parliament = csv.reader(open(PARLIAMENT_FILE), delimiter=";")
parties_json = []
party2id = {}
i = 0
for member in parliament:
    afko = member[10][member[10].find('(')+1:-1].lower()
    if not party2id.has_key(afko):
        party2id[afko] = i
        parties_json.append({
            "model": "denhaag.Party",
            "pk": i,
            "fields": {
                "name": member[10],
                "pica": "images/partij_logos/%s.gif" % (afko)
            }
        })
        i += 1




# Write the new fixtures to file
with open(FIXTURES_FILE, "w") as f:
    json.dump(old_fixtures+parties_json, f, indent=4)



