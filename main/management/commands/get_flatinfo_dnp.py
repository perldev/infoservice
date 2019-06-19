# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from main.models import domria
import requests
import traceback 
from lxml import html
import unicodedata
import sys
from transliterate import translit, get_available_language_codes
import json
import time
from lxml.etree import tostring
from itertools import chain
#    url = models.CharField(verbose_name=u"URL from", max_length=255, unique=True)
#    title = models.CharField(verbose_name=u"название ", max_length=255, )
#    pub_date = models.DateTimeField(verbose_name=u"�~Tа�~Bа добавлени�~O",
#                                    editable=False)
#    seller_info = models.TextField(blank=True, null=True)
#    ext_info = models.TextField(blank=True,null=True)
#    status = models.CharField(max_length=40,
#                              choices=STATUS_ORDER,
#                              default='created', editable=False)


"""
<title>
продажа 3к Квартира &nbsp; 2 082 192 грн. / 33 041 грн. Комнат 3 Площадь 63 Этаж 2/5, к
</title>
<link>
https://dom.ria.com/ru/realty-perevireno-prodaja-kvartira-dnepropetrovsk-pobeda-mandryikovskaya-ulitsa-15374930.html
</link>
<pubDate>Fri, 29 Mar 2019 15:49:38</pubDate>
<enclosure url="https://cdn.riastatic.com/photos/dom/photo/9607/960788/96078857/96078857b.jpg" type="image/jpeg"/>
<description>
<![CDATA[
Изящная квартира в действительно качественном доме. Ул. Мадрыковская 6...
]]>
</description>
</item>
"""

class Command(BaseCommand):
    args = ''
    help = 'fix user currency'

    def handle(self, *args, **options):
      for item_domria in domria.objects.filter(status='created'):
       try:
         headers = {"accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,de;q=0.5",
                    "cache-control": "max-age=0", 'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36'}
         url = item_domria.url
         url  = url.replace(".html", ".amp.html")
         print "getting information about object"
         print "process link %s" % url
         try:
           response = requests.get(url, headers=headers)
         except:
           # try later
           traceback.print_exc()
           time.sleep(10)
           continue
            
#         print response.text 
         rss = response.text
         #rss = rss.encode('ascii', 'xmlcharrefreplace')
         tree = html.fromstring(rss)
         print "get price"
         price = tree.cssselect("div.price-seller span.price")[0]
         price_1 = stringify_children(price)
         try:
            price = tree.cssselect("div.price-seller span.inline-wrap")[0]
            price_2 = stringify_children(price)
            item_domria.price = price_1 +" "+ price_2
         except:
            traceback.print_exc()
            item_domria.price = price_1
         
         try: 
            e = tree.xpath("//amp-list")[0] 
         except:
            # if we can receive this it's possible  that estate is bought 
            traceback.print_exc()
            item_domria.status='canceled'
            item_domria.save()
            continue
            
         infourl = e.attrib["src"]
         #HACK for receivin info about seller &__amp_source_origin=https%3A%2F%2Fdom.ria.com
         print "getting information about seller"
         try:
            info  = requests.get(infourl+ "&__amp_source_origin=https%3A%2F%2Fdom.ria.com", headers=headers)
            item_domria.seller_info  = info.text
            item_domria.save()
         except:
            # try later
            traceback.print_exc()
            time.sleep(10)
            continue
                   
         labels = tree.xpath("//dl[@class=\"unstyle\"]/dd")
         print labels
         #labels = tree.xpath("//dl[@class=\"unstyle\"]/dd/span[@class=\"label\"]/text()")
         #print labels
         #arguments = tree.xpath("//dl[@class=\"unstyle\"]/dd/span[@class=\"argument\"]/text()")
         
         #print arguments
         try:
            description = tree.xpath("//p[@id=\"realtyDescriptionText\"]/text()")[0]
         except:
            description = ""
            traceback.print_exc()
         res_dict = {}
         try:
           print "getting params "
           for item in labels: 
             #print stringify_children(i)
             keystr  =''.join(item.itertext()).strip()
             keystr = keystr.split(":")
            # key ="".join(item.xpath("//text()")).strip()
             #print key
             key = keystr[0]
 
             key = translit(key.strip(), 'ru', reversed=True)
             key = key.replace(":","")
             res_dict[key] = keystr[1].strip()
         except:
             traceback.print_exc()

         region =  stringify_children(tree.cssselect("h1.head")[0])
         item_domria.title = region
         region  =  region.split(",")
         print region

         if len(region)>2: res_dict["region1"] = region[2]
         if len(region)>3: res_dict["region2"] = region[3]
         if len(region)>4: res_dict["region3"] = region[4]
         res_dict["operation"] = translit(region[0], 'ru', reversed=True)
          

         item_domria.status = "processed"    
         item_domria.ext_info  = json.dumps(res_dict)
         item_domria.save()
         print "seems ok! continue"
         time.sleep(10)
       except:
         item_domria.counts = item_domria.counts + 1
         if item_domria.counts>4:
             item_domria.status="canceled"
         item_domria.save()
         traceback.print_exc()


def stringify_children(node):
   return ''.join(node.itertext()).strip()

