from django.shortcuts import render
from .forms import DataForm
from lxml.html import fromstring
from urllib.parse import urlencode, urlparse, parse_qs
from requests import get
import requests
from bs4 import BeautifulSoup
import random
import re, math
from .models import Data
from django.views import View

# def home(request):
#     return render(request,'index.html',{})
browsers = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
            ]



headers={
	'User-Agent': browsers[random.randint(0, len(browsers) - 1)],
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5'
	}

def geturls(req,text):
    urllist = []
    abstractlist = []
    list3 = []
    count = len(re.findall(r'\w+', text))
    print (count)
    raw = get("https://www.google.com/search?q=%s"%(text),headers=headers,verify=False).text
    page = fromstring(raw)
    for result in page.cssselect(".r a"):
        url = result.get("href")
        if url.startswith("/url?"):
            url = parse_qs(urlparse(url).query)['q']
        print(url[0])

        urllist.append(url[0].strip('https://'))
    soup = BeautifulSoup(raw, "lxml")

    for s in soup.findAll('span', {'class': 'st'}):
        print(s.text)
        abstractlist.append(s.text)
        list3 = list(zip(urllist,abstractlist))
    # result = dataextract(urllist,text)
    print(urllist)
    return render(req,'links1.html',{'links':list3})



class Check(View):
    def get(self, request, *args, **kwargs):
        #bg_image = 'https://upload.wikimedia.org/wikipedia/commons/0/05/20100726_Kalamitsi_Beach_Ionian_Sea_Lefkada_island_Greece.jpg'
        return render(request,'index.html',{})
        #return render(request, "shortener/home.html", {}) # Try Django 1.8 & 1.9 http://joincfe.com/youtube

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.method == "POST":
            print(request.POST)
            form = DataForm(request.POST)
            if form.is_valid():
                post = form.save(commit =False)
                post.user = request.user
                post.save()
                cd = form.cleaned_data

                text1 = cd['data']
                # text1 = re.sub(r'[^\w]', ' ', text1)
                # text1 = ''.join([i for i in text1 if not i.isdigit()])
                # text1 = " ".join(text1.split())
                print("\n\n\n cleaned text")
                print(text1)
                return geturls(request,text = text1)





                # return geturls(request,text = text1)
        else:
            form = DataForm()

        return render(request,'index.html',{'form':form},{'links':list3})
