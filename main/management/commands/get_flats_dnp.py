# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from main.models import domria
import requests
from xml.etree import ElementTree as etree
import traceback 
from dateutil.parser import parse

urls =  [
#"https://dom.ria.com/ru/search/rss/?category=1&realty_type=2&operation_type=1&fullCategoryOperation=1_2_1&page=1&state_id=11&city_id=11&limit=100&from_realty_id=&to_realty_id=&sort=inspected_sort&user_id=&characteristic%5B209%5D%5Bfrom%5D=&characteristic%5B209%5D%5Bto%5D=&characteristic%5B214%5D%5Bfrom%5D=&characteristic%5B214%5D%5Bto%5D=&characteristic%5B216%5D%5Bfrom%5D=&characteristic%5B216%5D%5Bto%5D=&characteristic%5B218%5D%5Bfrom%5D=&characteristic%5B218%5D%5Bto%5D=&characteristic%5B227%5D%5Bfrom%5D=&characteristic%5B227%5D%5Bto%5D=&characteristic%5B228%5D%5Bfrom%5D=&characteristic%5B228%5D%5Bto%5D=&characteristic%5B1607%5D%5Bfrom%5D=&characteristic%5B1607%5D%5Bto%5D=&characteristic%5B1608%5D%5Bfrom%5D=&characteristic%5B1608%5D%5Bto%5D=&characteristic%5B234%5D%5Bfrom%5D=&characteristic%5B234%5D%5Bto%5D=&characteristic%5B242%5D=239&characteristic%5B247%5D=252&characteristic%5B265%5D=0&realty_id_only=&date_from=&date_to=&with_phone=&exclude_my=&new_housing_only=&banks_only=&exclude_realty_id=&_csrf=A8rf63Wj-6ZhvCXPeFSLWziOBnHljySz_NQY&reviewText=&email=&period=per_day", 
"https://dom.ria.com/ru/search/rss/?category=0&realty_type=0&operation_type=0&fullCategoryOperation=0&page=1&state_id=11&city_id=11&limit=100&from_realty_id=&to_realty_id=&sort=inspected_sort&user_id=&characteristic%5B209%5D%5Bfrom%5D=&characteristic%5B209%5D%5Bto%5D=&characteristic%5B215%5D%5Bfrom%5D=&characteristic%5B215%5D%5Bto%5D=&characteristic%5B216%5D%5Bfrom%5D=&characteristic%5B216%5D%5Bto%5D=&characteristic%5B218%5D%5Bfrom%5D=&characteristic%5B218%5D%5Bto%5D=&characteristic%5B219%5D%5Bfrom%5D=&characteristic%5B219%5D%5Bto%5D=&characteristic%5B226%5D=0&characteristic%5B229%5D%5Bfrom%5D=&characteristic%5B229%5D%5Bto%5D=&characteristic%5B234%5D%5Bfrom%5D=&characteristic%5B234%5D%5Bto%5D=&characteristic%5B242%5D=239&characteristic%5B265%5D=0&realty_id_only=&date_from=&date_to=&with_phone=&exclude_my=&new_housing_only=&banks_only=&exclude_realty_id=&_csrf=IQE7RDXp-EMidyb0Zzj3W-ximko35JnqavlE&reviewText=&email=&period=per_allday"

]

# Create your models here.
#    url = models.CharField(verbose_name=u"URL from", max_length=255, unique=True)
#    title = models.CharField(verbose_name=u"название ", max_length=255, )
#    pub_date = models.DateTimeField(verbose_name=u"�~Tа�~Bа добавлени�~O",
#                                    editable=False)
#    seller_info = models.TextField(blank=True, null=True)
#    ext_info = models.TextField(blank=True,null=True)
#    status = models.CharField(max_length=40,
#                              choices=STATUS_ORDER,
#                              default='created', editable=False)
headers = {'accept': 'application/xml;q=0.9, */*;q=0.8', 'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36'}


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
      for url in urls: 
         response = requests.get(url, headers=headers)
         rss = response.text
         rss = rss.encode('ascii', 'xmlcharrefreplace')
         reddit_root = etree.fromstring(rss)
         item = reddit_root.findall('channel/item')
         for entry in item:
            title = entry.findtext('title')  
            link = entry.findtext('link') 
            pub_date = parse(entry.findtext('pubDate'))
            try:
                domria.objects.get(url=link)
            except domria.DoesNotExist:
                d = domria(url=link, title=title, pub_date=pub_date)
                d.save()
            except:
                traceback.print_exc()
    



