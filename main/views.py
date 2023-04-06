from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
import json
import requests
from .models import Newsdata,Contactus,Comments
import requests
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime  as dt
from django.conf import settings
from django.core.mail import send_mail
from . forms import ContactForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import NewsdataSerializers

class NewsdataView(APIView):
    def get(self,request,*args , **kwargs):
        result = Newsdata.objects.all()
        serializers = NewsdataSerializers(result , many =True)
        return Response({'status':'success' , 'students' : serializers.data} , status=200)

# import news.wsgi
# application = news.wsgi.application

# import imp
# import os
# import sys

def axtar(request):
    x = request.POST['sorgu']
    newsdata=Newsdata.objects.filter(metn__contains = x)
    template=loader.get_template('main/index.html')
    data={'newsdata':newsdata,'x':x}
    return HttpResponse(template.render(data,request))

def index(request):
    
    api = Newsdata.objects.all()
    blok1 = Newsdata.objects.all().order_by('-id')[0:1]
    blok2 = Newsdata.objects.all().order_by('-id')[1:6]
    blok3 = Newsdata.objects.raw('SELECT * FROM main_newsdata GROUP BY basliq ORDER BY id DESC LIMIT 6,5')
    blok4 = Newsdata.objects.all().order_by('-id')[11:17]
    blok5 = Newsdata.objects.all().order_by('-id')[19:20]
    blok = Newsdata.objects.raw('SELECT * FROM main_newsdata GROUP BY kateqoriya LIMIT 0,8')
    blok6 = Newsdata.objects.all().order_by('-id')[20:22]
    blok7 = Newsdata.objects.all().order_by('-id')[22:34]
    blok8 = Newsdata.objects.all().order_by('-id')[22:28]
    idman = Newsdata.objects.raw('SELECT * FROM main_newsdata WHERE kateqoriya = "İdman" LIMIT 0,6 ')
    nsay = Newsdata.objects.values_list("basliq").count()
    
    
    news_all = Newsdata.objects.all()

    obj_paginator = Paginator(news_all, 12)
    first_page = obj_paginator.page(1).object_list
    # range iterator of page numbers
    page_range = obj_paginator.page_range
    
    context = {"nsay":nsay, "blok1":blok1, "blok2":blok2, "blok3":blok3, "blok4":blok4, "blok5":blok5,
    "blok":blok,'blok6':blok6,'blok7':blok7,'blok8':blok8,'api':api,'idman':idman,'first_page':first_page
    ,'page_range':page_range,'obj_paginator':obj_paginator}
    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None) 
        results = list(obj_paginator.page(page_no).object_list.values('id', 'link','basliq','foto', 'metn','kateqoriya', 'tarix' , 'temp'))
        return JsonResponse({"results":results})
    return render(request,('main/index.html'),context)

def xeber(request):
    my_news=Newsdata.objects.all()
    nsay = Newsdata.objects.values_list("basliq").count()

    template = loader.get_template("main/xeber.html")
    data = {"my_news": my_news, 'nsay':nsay}
    return HttpResponse(template.render(data,request))

def addnews(request):

    req = requests.get("https://metbuat.az/")
    soup = BeautifulSoup(req.text, 'html.parser')
    sayt= soup.find_all('a',attrs={"class":"news_box"})
 
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Baku,az&APPID=99714fa04d3d562ec0eb037231496d65")
    data = response.text
        
    data  = json.loads(data)
    # print(data)
    temp = (data['main']['temp'] - 272.15 )
    temp = int(temp)
    for i in sayt:
        link1= 'https://metbuat.az' + i["href"]
        data = requests.get(link1)
        soup = BeautifulSoup(data.content,'html.parser')
        # Kateqoriya
        w = soup.find('span',class_='news_in_catg')
        if w is not None:
            kat = w.text
        else:
            kat = None

        # Metn
        w = soup.find('article',class_='normal-text')
        if w is not None:
            m = w.text
            metn = m.replace('You must enable Javascript on your browser for the site to work optimally and display sections completely.','')
        else:
            metn = None

        # Sekiller
        image= i.find("img")
        image = 'https://metbuat.az/' + image["src"]

        # Basliq
        w= i.find("h4",class_='news_box_ttl')
        if w is not None:
            title = w.text
        else:
            title = None
        
        # Linkler
        now = dt.now().date()

        add = Newsdata(link=link1, basliq=title, foto=image, metn=metn, tarix=now, kateqoriya=kat,temp = temp)
        add.save()
    messages.success(request, 'Xeber uğurla əlavə edildi')

    return HttpResponseRedirect(reverse('xeber'))

def delete(self):
    Newsdata.objects.all().delete()
    return HttpResponseRedirect(reverse('xeber'))

def singlepage(request, id):
    if request.method=='POST':
        comment = request.POST['comment']
        name = request.POST['name']
        email = request.POST['email']
        website = request.POST['website']
        meqale_id = request.POST['id']
        daxil_et = Comments(comment=comment,name=name,email=email,website=website,meqale_id=meqale_id)
        daxil_et.save()
    news = Newsdata.objects.filter(id=id)
    comments = Comments.objects.filter(meqale_id=id).order_by('-id')
    return render(request,('main/singlepage.html'),{"news":news,'comments':comments,'id':id})

def categori(request, id):
    r = Newsdata.objects.get(id=id)
    kat = r.kateqoriya
    news = Newsdata.objects.filter(kateqoriya=kat)
    
    return render(request,('main/categori.html'),{"news":news})
    
def contact(request):
    form = ContactForm()
    comm = Contactus.objects.all().order_by('-id')
    return render(request,'main/contact.html',{"comm":comm,'form':form})

def addcontact(request):
    
    # daxil_et = Contactus(message=message,name=name,email=email,subject=subject)
    # daxil_et.save()
    # sbjct = 'Bildiris'
    # msg = 'HELLO'
    
    msg = request.POST['message']
    name = request.POST['name']
    email = request.POST['email']
    sbjct = request.POST['subject']

    subject= [request.POST['name'], request.POST['subject'], request.POST['email']  ]
    message = "Hörmetli, "+ name+ " göndərdiyiniz "+ sbjct+ " -email müraciətə baxilacaq. Tezlikle sizə geri dönüş ediləcək. Köməyə ehtiyacınız varsa, lütfən, marketinq sualları üçün [e-poçt və telefon nömrəsi] ilə və ya mühasibat sualları üçün [e-poçt və telefon nömrəsi] ilə əlaqə saxlayın."
    
    email_from = settings.EMAIL_HOST_USER
    qebul_eden = [email,]
    qebul = ["horadiztorpag2017@gmail.com",]
    
    send_mail(sbjct,message,email_from,qebul_eden)
     
    send_mail(subject, msg, email_from, qebul)
   
    return HttpResponseRedirect(reverse('contact'))

def about(request):
    blok = Newsdata.objects.raw('SELECT * FROM main_newsdata GROUP BY kateqoriya LIMIT 0,8')
    return render(request,'main/about.html',{'blok':blok})



