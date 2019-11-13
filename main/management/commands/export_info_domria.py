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
from datetime import datetime
import os
import re
os.environ["LANG"] = "en_US.UTF-8"

class Command(BaseCommand):
    args = ''
    help = 'export today parsed'

    def handle(self, *args, **options):
       nw = datetime.now()
       print "here" 
       workbook = xlsxwriter.Workbook("../www/exports/domria_export_%s.xlsx" % str(nw))
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
         "stages":6, 
         "rooms":7, 
         "surface":8,
         "ground":9,
         "material":10, 
         "price":11,
         "phone": 12,
         "date":14,
         "source":15,
         "text": 13
       }
       worksheet.write(i, cols["title"], u"title"  )
   
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
       worksheet.write(i, cols["text"],  "TEXT" )
       worksheet.write(i, cols["date"], "date" )
       worksheet.write(i, cols["source"], "url" )
       i = 1
       
       for item in domria.objects.filter(status="processed"):
          ext_info = None
          seller_info = None       
 
          try:
            ext_info = json.loads(item.ext_info)
            seller_info = json.loads(item.seller_info)
          except :
            print "domria problem object %i " %  item.id
            traceback.print_exc()
            continue
          title = item.title
          item.status = "exported"
          item.export_date = datetime.now()
          item.save()
          phone = ""
          try:
             phone = seller_info["firstPhone"]
          except:
             traceback.print_exc()
             print seller_info
             if not "firstPhone" in seller_info["items"][0]:
                 continue
             phone = seller_info["items"][0]["firstPhone"]
            
             
          #region #city #type #rooms? #stage #surface #ground surface #material #price #phone #date #mark #photo #source #text 
          worksheet.write(i, cols["title"], item.title )
          worksheet.write(i, cols["operation"], ext_info.get("operation","") )
          worksheet.write(i, cols["region"], ext_info.get("region1","") )
          worksheet.write(i, cols["city"], ext_info.get("region2","") )
          worksheet.write(i, cols["type"], ext_info.get("Tip predlozhenija","") )
          worksheet.write(i, cols["rooms"], ext_info.get("Komnat","") )
          worksheet.write(i, cols["stage"], ext_info.get("Etazh","") )
          worksheet.write(i, cols["stages"], ext_info.get("Etazhnost'","") )
          worksheet.write(i, cols["surface"], ext_info.get("Obschaja","") )
          worksheet.write(i, cols["ground"], ext_info.get("Ploschad' uchastka","") )
          worksheet.write(i, cols["material"], ext_info.get("Tip sten","") )
          worksheet.write(i, cols["price"], item.price )
          worksheet.write(i, cols["phone"], phone )
          worksheet.write(i, cols["date"], str(item.pub_date) )
          worksheet.write(i, cols["source"], item.url )
          worksheet.write(i, cols["text"], cleanhtml(ext_info.get("Opisanie", "")) )
          i+=1
       
       workbook.close()
     
      


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext



