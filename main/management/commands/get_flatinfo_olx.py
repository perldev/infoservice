# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import date, timedelta as dt, datetime
import random
from main.models import olx
import requests
import traceback
from lxml import html
import unicodedata
import sys
from transliterate import translit, get_available_language_codes
import os
import json
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from transliterate import translit, get_available_language_codes
from itertools import chain
import random
from libs import user_agent_rotator, get_random_proxy

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
import os

os.environ["LANG"] = "en_US.UTF-8"
headers = {
    "accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,de;q=0.5",
    "cache-control": "max-age=0",
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

class Command(BaseCommand):
    args = ''
    help = 'fix user currency'

    def handle(self, *args, **options):
        # chrome_options = webdriver.ChromeOptions()
        display = Display(visible=0, size=(1600, 900))
        display.start()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
        # chrome_options.add_argument('--user-agent="'+user_agent_rotator.get_random_user_agent()+'"')
        # chrome_options.add_argument('--start-maximized')
        dc = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        # Change the proxy properties of that copy.
        basep = get_random_proxy()
        PROXY = "http://%s" % basep
        PROXYS = "https://%s" % basep
        print "using proxy %s" % PROXY
        os.environ["http_proxy"] = PROXY
        os.environ["https_proxy"] = PROXYS
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        # browser.maximize_window()
        # browser.command_executor._commands.update({
        # 'getAvailableLogTypes': ('GET', '/session/$sessionId/log/types'),
        # 'getLog': ('POST', '/session/$sessionId/log')})
        def try_get_item(item):
            try:
                # Relaunch each time with new user-agent.
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('window-size=1024x768')
                chrome_options.add_argument('user-agent="' + user_agent_rotator.get_random_user_agent() + '"')
                browser = webdriver.Chrome(chrome_options=chrome_options)
                browser.maximize_window()
                browser.command_executor._commands.update({
                    'getAvailableLogTypes': ('GET', '/session/$sessionId/log/types'),
                    'getLog': ('POST', '/session/$sessionId/log')})
                browser.get(item.url)
                browser.implicitly_wait(random.choice((1, 3, 6)))
                browser.save_screenshot("../www/screenshot1_%i.png" % item.id)
                attrs = {}
                all_iframes = browser.find_elements_by_tag_name("iframe")
                if True and len(all_iframes) > 0:
                    print("Ad Found\n")
                    browser.execute_script("""
            var elems = document.getElementsByTagName("iframe"); 
            for(var i = 0, max = elems.length; i < max; i++)
                 {
                     elems[i].hidden=true;
                 }
                              """)
                    print('Total Ads: ' + str(len(all_iframes)))
                else:
                    print('No frames found')

                print "start process link %s %i" % (item.url, item.id)
                print "i'm getting the page"
                print "ok lets gather another info"
                source = browser.page_source
                response = html.fromstring(source)
                for row in response.cssselect('table.details tbody tr table.item'):
                    print row.cssselect('tr th')
                    var1 = row.cssselect('tr th')[0].text
                    key = translit(var1, 'ru', reversed=True)
                    # print key
                    l1 = row.cssselect('td.value')
                    # print "find some attrs"
                    # print l1[0].text_content()
                    var2 = l1[0].text_content()
                    # print "save it"
                    key = key.strip()
                    attrs[key] = var2.strip()

                    """
                    var1 = row.cssselect('tbody tr th')[0].text
                    key =  translit(var1, 'ru', reversed=True)
                    print key
                    l1 = row.cssselect('tbody tr td.value strong')
                    l2 = row.cssselect('tbody tr td.value a')
                    print "find some attrs"
                    if len(l1)>0:
                        var2 = l1[0].text
                    elif len(l2)>0:
                        var2 = l2[0].text
                    print "save it"
                    key = key.strip()
                    attrs[key] = var2.strip()
                    """

                try:
                    attrs["desc"] = response.cssselect("#textContent")[0].text
                    attrs["desc"] = attrs["desc"].strip()

                except:
                    traceback.print_exc()
                    # We did not find even base content. This is bad.
                    return False

                """ 
                for row in response.find_elements_by_css_selector('table.details tbody tr table.item'): 
                      var1 = row.find_elements_by_css_selector('tbody tr th')[0].text
                      key =  translit(var1, 'ru', reversed=True)
                      print key
                      l1 = row.find_elements_by_css_selector('tbody tr td.value strong')
                      l2 = row.find_elements_by_css_selector('tbody tr td.value a')
                      print "find some attrs"
                      if len(l1)>0:
                          var2 = l1[0].text
                      elif len(l2)>0:
                          var2 = l2[0].text
                      print "save it"
                      attrs[key] = var2



                try:
                   attrs["desc"] = response.find_elements_by_css_selector("#textContent")[0].text

                except:
                   traceback.print_exc()
                """
                priceButton = browser.find_elements_by_css_selector('div.price-label')[0]
                item.price = priceButton.text
                # print item.price

                phoneButton = browser.find_elements_by_css_selector('div.link-phone')[0]
                try:
                    print "click cookie"
                    cookieButton = browser.find_elements_by_css_selector('button.cookiesBarClose')[0]
                    cookieButton.click()
                    time.sleep(1)
                except:
                    traceback.print_exc()
                    return False # We can't get click cookie.

                time.sleep(random.choice((1, 3, 5)) + 5)
                print "clicking on phone"

                phoneButton.click()
                print "clicked 1"
                # phoneButton.click()
                # print "clicked 2"
                # phoneButton.click()
                # print "clicked 3"
                time.sleep(random.choice((1, 3, 5)) + 5)
                browser.save_screenshot("../www/screenshot2_%i.png" % item.id)

                phone = phoneButton.find_elements_by_css_selector("strong.xx-large")[0].text
                attrs["phone"] = phone
                print phone
                phone = phone.replace(" ", "")
                if phone.find("xxx") > 0:
                    print 'Profiler log:', browser.execute('getLog')['value']
                    print "can't receive phone"
                    return False
                    # break

                region = browser.find_elements_by_css_selector("a.show-map-link strong")[0].text
                region = region.split(",")
                if len(region) > 0: attrs["region1"] = region[0]
                if len(region) > 1: attrs["region2"] = region[1]
                if len(region) > 2: attrs["region3"] = region[2]

                print attrs
                item.seller_info = json.dumps({"phone": phone})
                item.ext_info = json.dumps(attrs)
                item.status = "processed"
                item.save()
                print attrs
            except:
                return False
                # item.counts = item.counts + 1
                # if item.counts > 4:
                #     item.status = "canceled"
                # item.save()
                # traceback.print_exc()

            try:
                browser.quit()
            except:
                pass

            return True # We got everything!

        yesterday = datetime.now() - dt(days=7)
        for item in olx.objects.filter(status="created", pub_date__gte=yesterday).order_by("-id"):
            ctr = 0
            failed = True
            while ctr < 5:
                result = try_get_item(item)
                ctr += 1
                if result:
                    failed = False
                    break
                item.counts = item.counts + 1
                if item.counts > 4:
                    item.status = "canceled"
                item.save()
            if failed:
                print "[-] Failed item!"
                # traceback.print_exc()


def stringify_children(node):
    parts = ([node.text] +
             list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
             [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))