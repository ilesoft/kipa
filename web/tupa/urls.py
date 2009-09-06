from django.conf.urls.defaults import *
from models import *
from django.contrib import admin
admin.autodiscover()
from django.views.generic.simple import direct_to_template
from django.conf import settings

genericViews = patterns('django.views.generic.list_detail',        
                        (r'^$','object_list', 
                        {'template_name': 'tupa/index.html', 
                        'queryset': Kisa.objects.all() } ),) 

urlpatterns = genericViews +  patterns('web.tupa.views.',
        (r'^admin/(.*)', admin.site.root ),
        (r'^(?P<kisa_nimi>\w+)/tallenna/$', 'tallennaKisa'), 
        (r'^kantaan/$', 'tietokantaan'), 
        (r'^(?P<kisa_nimi>\w+)/$', 'kisa'),
        (r'^uusiKisa/maarita/$', 'maaritaKisa'),
        (r'^(?P<kisa_nimi>\w+)/maarita/$', 'maaritaKisa'),
        (r'^(?P<kisa_nimi>\w+)/maarita/tehtava/$', 'maaritaValitseTehtava'),
        (r'^(?P<kisa_nimi>\w+)/maarita/tehtava/uusi/sarja/(?P<sarja_id>\d+)/$', 'maaritaTehtava'),
        (r'^(?P<kisa_nimi>\w+)/maarita/tehtava/(?P<tehtava_id>\d+)/$', 'maaritaTehtava'),
        (r'^(?P<kisa_nimi>\w+)/maarita/vartiot/', 'maaritaVartiot'),
        (r'^(?P<kisa_nimi>\w+)/maarita/tehtava/kopioi/sarjaan/(?P<sarja_id>\d+)/$', 'kopioiTehtavia'),
        (r'^(?P<kisa_nimi>\w+)/maarita/testitulos/$', 'testiTulos'),
        (r'^(?P<kisa_nimi>\w+)/syota/$', 'syotaKisa'),
        (r'^(?P<kisa_nimi>\w+)/syota/tehtava/(?P<tehtava_id>\d+)/$', 'syotaTehtava'),
        (r'^(?P<kisa_nimi>\w+)/tulosta/$', 'tulosta'),
        (r'^(?P<kisa_nimi>\w+)/tulosta/sarja/(?P<sarja_id>\d+)/$', 'tulostaSarja'),
        (r'^(?P<kisa_nimi>\w+)/tulosta/piirit/$', 'piirit'), )

if settings.DEBUG :
        urlpatterns += patterns('',
                (r'^kipamedia/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_DOC_ROOT}),)
