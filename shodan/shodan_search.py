#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shodan
import json
import sys


SHODAN_API_KEY = "FWZjuMGUas6ZCBItqiWMJKDf9e2r5A18"
limit = 200
counter = 0

try:
        api = shodan.Shodan(SHODAN_API_KEY)

        results = api.search_cursor('mongodb')
        for result in results:
            print(result['ip_str'])
            counter += 1
            if counter >= limit:
                break

except shodan.APIError, e:
    print 'Error: %s' % e

except KeyboardInterrupt:
    print 'Interrupted'
    sys.exit(0)

