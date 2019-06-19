# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

STATUS_ORDER = (
    ("created", u"создан"),
    ("get_seller_info", u"получена инфа о продавце"),
    ("get_ext_info", u"получена доп инва"),
    ("processed", u"обработан"),
)

# Create your models here.
class domria(models.Model):
    url = models.CharField(verbose_name=u"URL from", max_length=255, unique=True)
    title = models.CharField(verbose_name=u"название ", max_length=255, )
    pub_date = models.DateTimeField(verbose_name=u"Дата добавления", 
                                    editable=False)
    export_date = models.DateTimeField(blank=True, null=True, 
                                       editable=False)


    seller_info = models.TextField(blank=True, null=True)
    ext_info = models.TextField(blank=True,null=True)
    counts = models.IntegerField(default=0)
    price = models.CharField(default="", max_length=255)
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', editable=False)

  

    class Meta:
        verbose_name = u'domria estate'
        verbose_name_plural = u'domria estate'



# Create your models here.
class olx(models.Model):
    url = models.CharField(verbose_name=u"URL from", max_length=255, unique=True)
    title = models.CharField(verbose_name=u"название ", max_length=255, )
    pub_date = models.DateTimeField(verbose_name=u"�~Tа�~Bа добавлени�~O",
                                    editable=False)
    seller_info = models.TextField(blank=True, null=True)
    ext_info = models.TextField(blank=True,null=True)
    counts = models.IntegerField(default=0)
    price = models.CharField(default="", max_length=255)
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', editable=False)
    export_date = models.DateTimeField(blank=True, null=True, 
                                       editable=False)



    class Meta:
        verbose_name = u'domria estate'
        verbose_name_plural = u'domria estate'


