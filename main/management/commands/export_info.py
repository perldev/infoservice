# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from main.models import olx,domria
import requests
import traceback 
import sys
import json
from datetime import datetime
import time
from transliterate import translit, get_available_language_codes
import xlsxwriter
from lxml import html
import unicodedata
import sys
from transliterate import translit, get_available_language_codes
import json
import time
from lxml.etree import tostring
from itertools import chain
from libs import user_agent_rotator, get_random_proxy

from datetime import datetime
import os
import re
os.environ["LANG"] = "en_US.UTF-8"
headers = {"accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,de;q=0.5",
                    "cache-control": "max-age=0", 'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36'}


class Command(BaseCommand):
    args = ''
    help = 'export today parsed'

    def handle(self, *args, **options):
       nw = datetime.now()
       print "here" 
       workbook = xlsxwriter.Workbook("../www/exports/olx_export_%s.xlsx" % str(nw))
       worksheet = workbook.add_worksheet()


# Create an new Excel file and add a worksheet.

# Widen the first column to make the text clearer.
#worksheet.set_column('A:A', 20)

# Add a bold format to use to highlight cells.
#bold = workbook.add_format({'bold': True})

# Write some simple text.
#worksheet.write('A1', 'Hello')

# Text with formatting.
#worksheet.write('A2', 'World', bold)

# Write some numbers, with row/column notation.
#worksheet.write(3, 0, 123.456)

# Insert an image.
#worksheet.insert_image('B5', 'logo.png')

#workbook.close()
       i = 0
       cols = {
         "title":0, 
         "region":1, 
         "city":2,
         "operation":3, 
         "type":4, 
         "stage":5, 
         "from": 15, 
         "stages":6, 
         "rooms":7, 
         "surface":8,
         "ground":9,
         "material":10, 
         "price":11,
         "phone": 12,
         "date":14,
         "source":16,
         "text": 13
       }
   
       worksheet.write(i, cols["title"], u"Title"  )
       worksheet.write(i, cols["region"], u"Region"  )
       worksheet.write(i, cols["city"], u"Town/region" )
       worksheet.write(i, cols["operation"], u"Vyberite rubriku"  )
       worksheet.write(i, cols["type"], "Tip" )
       worksheet.write(i, cols["stage"],  "Etazh" )
       worksheet.write(i, cols["stages"], "Etazhnost" )
       worksheet.write(i, cols["rooms"], "Kolichestvo komnat'" )
       worksheet.write(i, cols["surface"], u"Obschaja ploschad'" )
       worksheet.write(i, cols["ground"], "Ploschad' uchastka" )
       worksheet.write(i, cols["material"], "material" )
       worksheet.write(i, cols["price"], "price")
       worksheet.write(i, cols["phone"], "phone" )
       worksheet.write(i, cols["text"],  "description" )
       worksheet.write(i, cols["date"], "date" )
       worksheet.write(i, cols["from"], "Ot" )
       worksheet.write(i, cols["source"], "url" )
       i = 1
       print olx.objects.filter(status="processed").query
       for item in olx.objects.filter(status="processed"):
          #repeat some additional info 
          response = None 
          try:
           # Better masquerade here as well.
           headers['User-agent'] = user_agent_rotator.get_random_user_agent()
           baseproxy = get_random_proxy()
           http_proxy = 'http://' + baseproxy
           https_proxy = 'https://' + baseproxy
           response = requests.get(item.url, headers=headers, proxies={'http_proxy':http_proxy,'https_proxy':https_proxy})
          except:
           # try later
           traceback.print_exc()
           time.sleep(2)
           continue

#         print response.text 
          page = response.text
          print "get parse"
          print item.url
         
          ext_info = None
          seller_info = None
          try:
           
            ext_info = json.loads(item.ext_info)
            seller_info = json.loads(item.seller_info)
          except :
            print "olx problem object %i " % item.id
            traceback.print_exc()
            item.status = "created"
            item.counts = item.counts + 1
            item.save()
            continue
          

          if True:
            tree = html.fromstring(page)
            print tree.cssselect('table.item') 
            #for row in tree.cssselect('table.details tbody tr table.item'):
            for row in tree.cssselect('table.item'):
                print row.cssselect('tr th')
                var1 = row.cssselect('tr th')[0].text
                key =  translit(var1, 'ru', reversed=True)
                #print key
                l1 = row.cssselect('td.value')
                #print "find some attrs"
                #print l1[0].text_content()
                var2 = l1[0].text_content()
                #print "save it"
                key = key.strip()
                ext_info[key] = var2.strip()
          
          if not "phone" in ext_info:
             item.status = "created"
             item.save()
             continue
   
          #item.ext_info = json.dumps(ext_info) 
          #item.save()





          title = item.title
          item.status = "exported"
          item.export_date = datetime.now()
          item.save()
          
          #region #city #type #rooms? #stage #surface #ground surface #material #price #phone #date #mark #photo #source #text 
          worksheet.write(i, cols["title"], item.title )
          worksheet.write(i, cols["region"], ext_info.get("region1","") )
          worksheet.write(i, cols["city"], ext_info.get("region2","") )
          worksheet.write(i, cols["type"], ext_info.get("Tip ob'ekta","") + " " + ext_info.get("Tip doma", "") )
          worksheet.write(i, cols["operation"], ext_info.get("Vyberite rubriku","") )
          worksheet.write(i, cols["stage"], ext_info.get("Etazh","") )
          worksheet.write(i, cols["stages"], ext_info.get("Etazhnost'","") )
          worksheet.write(i, cols["rooms"], ext_info.get("Kolichestvo komnat","") )
          worksheet.write(i, cols["surface"], ext_info.get("Obschaja ploschad'","") )
          worksheet.write(i, cols["ground"], ext_info.get("Ploschad' uchastka","") )
          worksheet.write(i, cols["material"], ext_info.get("Tip sten","") )
          worksheet.write(i, cols["price"], item.price )
          worksheet.write(i, cols["from"],  ext_info.get("Ob'javlenie ot","") )
          worksheet.write(i, cols["phone"], seller_info.get("phone","") )
          worksheet.write(i, cols["date"], str(item.pub_date) )
          worksheet.write(i, cols["source"], item.url )
          worksheet.write(i, cols["text"], cleanhtml(ext_info.get("desc", "")) )
          i+=1
          
       workbook.close()
       return 





def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
 
