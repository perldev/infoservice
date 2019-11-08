# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from datetime import datetime
from main.models import olx
import requests
from lxml import html

import traceback
from libs import get_random_proxy, user_agent_rotator
from dateutil.parser import parse

url = "https://www.olx.ua/nedvizhimost/dnp/"

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
headers = {'accept': 'text/html;q=0.9, */*;q=0.8',
           'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36'}


class Command(BaseCommand):
    args = ''

    def handle(self, *args, **options):

        # Better masquerade here.
        headers['User-agent'] = user_agent_rotator.get_random_user_agent()
        baseproxy = get_random_proxy()
        http_proxy = 'http://'+baseproxy
        https_proxy = 'https://'+baseproxy

        response = requests.get(url, headers=headers, proxies={'http_proxy':http_proxy,'https_proxy':https_proxy})

        rss = response.text
        tree = html.fromstring(rss)

        print dir(tree)
        for entry in tree.cssselect("div.content h3.lheight22"):
            print entry
            title = entry.cssselect("a.marginright5")[0]
            link = title.attrib["href"]
            link = link[:link.find("#")]
            title = title.cssselect("strong")[0].text
            pub_date = datetime.now()
            # print "entry %s %s %s " % (title, link, pub_date)
            try:
                olx.objects.get(url=link)
                print "we have already this element"
            except olx.DoesNotExist:
                print "add new element for working"
                d = olx(url=link, title=title, pub_date=pub_date)
                d.save()
            except:
                print "something strange"
                traceback.print_exc()
