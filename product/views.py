from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib.auth.decorators import login_required
from . import ml
from selenium import webdriver
import time
import re
# from webdriver_manager.chrome import ChromeDriverManager
from wishlist.models import Wishlist,WishlistItem
from django.core.mail import send_mail
# driver = webdriver.Chrome(ChromeDriverManager().install())


def price(request):
    if request.method=='POST':
        name=request.POST.get('name')
        source1 = request.POST.get('source1')
        source2 = request.POST.get('source2')
        flipkart=request.POST.get('flipkart')
        amazon=request.POST.get('amazon')
  
# create a webdriver object for chrome-option and configure
        wait_imp = 10
        CO = webdriver.ChromeOptions()
        CO.add_experimental_option('useAutomationExtension', False)
        CO.add_argument('--ignore-certificate-errors')
        CO.add_argument('--start-maximized')
        wd = webdriver.Chrome(r'C:\Users\pgsou\Desktop\sree\surelwr\chromedriver.exe',options=CO)
        print ("*************************************************************************** \n")
        print("Starting Program, Please wait ..... \n")

        print ("Connecting to Flipkart")
        wd.get(source1)
        wd.implicitly_wait(wait_imp)

        f_price = wd.find_element_by_xpath(flipkart)
        
        # pr_name = wd.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span")
        # product = pr_name.text
        r_price = f_price.text
       
    # print (r_price[1:])
        print (" ---> Successfully retrieved the price from Flipkart \n")
        time.sleep(2)

        print("Connecting to Amazon")
        wd.get(source2)
        wd.implicitly_wait(wait_imp)
    # a_price = wd.find_element_by_id("priceblock_ourprice")
        a_price = wd.find_element_by_xpath(amazon)
        raw_p = a_price.text
    # print (raw_p[2:8])
        print (" ---> Successfully retrieved the price from Amazon \n")
        time.sleep(2)

    # Final display
        print ("#------------------------------------------------------------------------#")
        # print ("Price for [{}] on all websites, Prices are in INR \n".format())
        print("Price available at Flipkart is: "+r_price[1:])
        print("Price available at Amazon is: "+raw_p[2:8])
        #print("Price available at Croma is: "+raw_c[1:7])
        # print(split_domain_port(r_price[1:]))
        a=r_price.replace(''"₹","")
        print(a)
        b=a.replace(''",","")
        print(b)
        print(float(b))
        c=raw_p.replace(''"₹","")
        d=c.replace(''",","")
        print(d)
        Product.objects.create(
            name=name,
            url_flipkart=source1,
            url_amazon=source2,
            price_flipkart_xmlpath=flipkart,
            price_amazon_xmlpath=amazon,
            comapare_flipkart_price=b,
            compare_amazon_price=d,
            slug='_'
        )
        ProductAdd.objects.create(
            comapare_flipkart_price=b,
            compare_amazon_price=d,
            
        )
        print(type(r_price))
        return render(request,'comparison_form.html',{'price':r_price[1:],'price2':raw_p[1:]})

    return render(request,'comparison_form.html')

def product(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = ProductAdd.objects.filter(is_available=True).order_by('-count')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        products = products.filter(category=category)
    page = request.GET.get('page')
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)

    except PageNotAnInteger:
        products = paginator.page(1)

    except EmptyPage:
        products = paginator.page(1)
    is_authenticated = request.user.is_authenticated
    print(is_authenticated)
    if is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)

        return render(
            request,
            'product/product.html',
            {
                'category': category,
                'categories': categories,
                'products': products,
                'wishlist': wishlist
            }
        )

    else:
        return render(
            request,
            'product/product.html',
            {
                'category': category,
                'categories': categories,
                'products': products,
            }
        )

    

def categorysearch(request,id):
    listing = get_object_or_404(Category, id=id)
    print(listing)
    product=ProductAdd.objects.order_by('-created_on').filter(category_id=listing.id)
    return render(request,'product/category_search.html',{'listings':product})


def product_search(request):
    results = None
    try:
        query = request.POST['query']
        results = ProductAdd.objects.filter(name__icontains=query) |\
            ProductAdd.objects.filter(description__icontains=query)
        page = request.GET.get('page')
        paginator = Paginator(results, 6)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(1)
        return render(
            request,
            'product/product.html',
            {'products': results}
        )
    except KeyError:
        wishlist = None
        "KeyError"
        return render(
            request,
            'product/product.html',
            {'products': results}
        )

def product_detail(request, id):

    product = get_object_or_404(
        ProductAdd,
        id=id,
        is_available=True
    )

    return render(
        request,
        'product/detail.html',
        {'product': product}
    )





def our_product(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = ProductAdd.objects.filter(is_available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    page = request.GET.get('page')
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(1)
    is_authenticated = request.user.is_authenticated
    print(is_authenticated)
    if is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        return render(
            request,
            'product/our_product.html',
            {
                'category': category,
                'categories': categories,
                'products': products,
                'wishlist': wishlist
            }
        )

    else:
        messages.error(request,'please login to get wishlist')
        return render(
            request,
            'product/our_product.html',
            {
                'category': category,
                'categories': categories,
                'products': products,
            }
        )



a=['best product','Best product','good product','Good product','nice product','Nice product','marvelous product','Marvelous product','marvelous','Marvelous','nice','Nice','good','Good','best','Best','excellent product','Excellent product','excellent','Excellent']

# Create your views here.

# def category_create(request):
#     registerd=False
#     if request.method=='POST':
#         category_form=CategoryForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             registerd=True
#         else:
#             HttpResponse('invalid form')
#     else:
#         category_form=CategoryForm()
#     return render(request,'product/create_category.html',{'registerd':registerd,'category_form':category_form})

def category_list(request):               
    categories=Category.objects.all()
    return render(request,'product/category.html',{'categories': categories})


import csv
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
import pandas as pd
import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import time
from bs4 import BeautifulSoup
import requests


def predict(request):
    if request.method == "POST":
        test = []
        names = []
        flipPrices = []
        prodNames = []
        info,price = [],[]
        url = "https://flipkart.com/search?q="
        q = request.POST.get("nm")
        q = q.replace(" ","+")      
        # response recieved in bytes
        resp = requests.get(url+q)
        # parsing response content using BeautifulSoup class, so that we can perform operations on it.
        parsed_html = bs(resp.content, 'html.parser')
        # data cleaning
        raw_data = parsed_html.find("script", attrs={"id":"is_script"})
        data = raw_data.contents[0].replace("window.__INITIAL_STATE__ = ","").replace(";","")
        json_data = json.loads(data)
        req_data = json_data["pageDataV4"]["page"]["data"]["10003"]   #[10]["widget"]["data"]["products"][3]["productInfo"]
        #req_json_data = json_data["seoMeta"]["answerBox"]["data"]["renderableComponents"][0]["value"]["data"]

        data_list = []
        try:
            for i in range(1, len(req_data)):
                d = {}
                jd = req_data[i]["widget"]["data"]["products"]
                # print(len(jd))
                # print("i: ", i, end="\n")
                for j in range(len(jd)):
                    jd2 = jd[j]["productInfo"]["value"]

                    d["title"] = jd2["titles"]["title"]
                    d["keySpecs"] = jd2["keySpecs"]
                    d["rating"] = jd2["rating"]["average"]
                    d["ratingCount"] = jd2["rating"]["count"]
                    d["price"] = jd2["pricing"]["finalPrice"]["value"]
        #                 d["warranty"] = jd2["warrantySummary"]
                    d["url"] = jd2["smartUrl"]
                data_list.append(d)

        except:
            pass 
        # dumping data to result.json file
        #     print(list(data_list))
        with open("flipkart"+'.json', 'w') as fp:
            json.dump(data_list, fp)

        # Now let us write our data to csv file
        data_file = open("flipkart"+'.csv', 'w') 

        # create the csv writer object 
        csv_writer = csv.writer(data_file) 

        # Counter variable used for writing  
        # headers to the CSV file 
        count = 0

        for data in data_list:
            if count == 0: 

                # Writing headers of CSV file 
                header = data.keys() 
                csv_writer.writerow(header) 
                count += 1
            # Writing data of CSV file 

            csv_writer.writerow(data.values()) 


        with open('flipkart.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            rows = list(reader)
        i,j = 0,2
        while i in range(len(rows)):
            try:
                name = rows[j][0]
                #             name = " ".join(name.split(' ')[0:2])
        #         print(name)
        #         print("name = ",name)
                names.append(name)
                i += 1
                j += 2
            except:
                    break


        print("Best results",len(names))
        #     print(names,len(names))
        if len(names) <= 10:
            flipkart_url = "https://www.flipkart.com/search?q=" + q
            print(flipkart_url)
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            soup = BeautifulSoup(flipkartPage, 'html.parser')
            info = soup.select("[class~=s1Q9rs]")
            if info == []:
                info = soup.select("[class~=IRpwTa]")
            flipPrices = soup.select("[class =_30jeq3]")
            prodNames = [i.get('title') for i in info]
            names = prodNames
            df = pd.DataFrame(list(zip(prodNames, flipPrices)), 
                        columns =['product_name', 'Flipkart_price']) 
            df.to_csv('flipkart.csv')
            print(df)

        else:
            with open('flipkart.csv') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                rows = list(reader)
            i,j = 0,2
            while i in range(len(rows)):
                try:
                    price = rows[j][4]
        #             price = price[i].text
        #             print("price = ",price)
                    flipPrices.append(price)
                    i += 1
                    j += 2
                except:
                    break
            df = pd.DataFrame(list(zip(names, flipPrices)), 
                    columns =['Product_name', 'Flipkart_price'])

            print(df)
            df.to_csv('flipkart.csv')

        data_file.close()

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        amazon=''
        amazonlist = []
        amazonName = []
        i = 0
        while i in range(len(names)):
            print(names[i])
            def amazon(name):
                    try:
                        global amazon
                        name = " ".join(name.split(' ')[0:2])
                        name1 = name.replace(" ","-")
                        name2 = name.replace(" ","+")
                        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
                        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
                        print("\nSearching in amazon:")
                        soup = BeautifulSoup(res.text,'html.parser')
                        amazon_page = soup.select('.a-color-base.a-text-normal')
                        amazon_page_length = int(len(amazon_page))
                        for i in range(0,amazon_page_length):
                            name = name.upper()
                            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                            if name in amazon_name[0:20]:
                                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                                amazonlist.append(amazon_price)
                                print("Amazon:")
                                print(amazon_name)
                                amazonName.append(amazon_name)
                                print("₹"+amazon_price)
                                print("-----------------------")
                                break
                            else:
                                i+=1
                                i=int(i)
                                if i==amazon_page_length:
                                    print("amazon : No product found!")
                                    print("-----------------------")
                                    amazon_price = '0'
                                    amazonlist.append(amazon_price)
                                    amazonName.append("No similar product")
                                    break

                        return amazon_price
                    except:
                        print("amazon: No product found!")
                        print("-----------------------")
                        amazon_price = '0'
                        amazonlist.append(amazon_price)
                        amazonName.append("No similar product")
                    return amazon_price
            amazon_price = amazon(names[i])
            amazon=''
            i += 1
        test = flipPrices
        flip = flipPrices
        idk = []
        for i in range(len(flip)):
        #     x = 
            try:
                x = flip[i].text.replace('₹','')
                print(x)
                idk.append(x)
            except:
                idk = test
        df = pd.DataFrame(list(zip(names,idk,amazonName, amazonlist)), 
                    columns =["Product_name_Flipkart","Flipkart_price",'Product_name_Amazon', 'Amazon_price'])
        print(df)   
        df.to_csv('flipkartandamazon.csv')
        filename = 'flipkartandamazon.csv'
        data = pd.read_csv(filename, header=0)
        stocklist = list(data.values)
        return render(request,'pre.html', {'stocklist':stocklist})
    else:
        return render(request,"pre.html")

def product_list1(request):
    user_instance=request.user
    list=ProductAdd.objects.all().filter(user_id=user_instance)
    return render(request,'product/product_list.html',{'list':list})




def add_review(request,id):
    product=ProductAdd.objects.get(id=id)
    if request.method=='POST':
        form=ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            cp=Review(user=request.user,product=product,review=form.cleaned_data['review'])
            new_text = ml.classifier(title=cp.review,text=cp.review)
            print(new_text[0])
            p=product.count
            if new_text[0] == 'REAL':
                print("yes")
                pro=ProductAdd.objects.update_or_create(id=id,
                defaults={'count':p+10})
            elif cp.review in a:
                print("yes")
                pro=ProductAdd.objects.update_or_create(id=id,
                defaults={'count':p+10})

            else:
                print("no")
                pro=ProductAdd.objects.update_or_create(id=id,
                defaults={'count':p-10})
            print(ml.get_accuracy())
            cp.count=float(ml.get_accuracy())
            cp.save()
            p=product.count
            print(p)
            #pro=ProductAdd.objects.update_or_create(id=id,
            #defaults={'count':p+1})
            messages.success(request,'successfully added')
            return redirect('product')
        else:
            HttpResponse('invalid form')
    else:
        form=ReviewForm()
    return render(request,'product/add_review.html',{'form':form,})




def report_product(reuqest,id):
    product=ProductAdd.objects.get(id=id)
    rp=Report.objects.create(
        product=product
    )
    return redirect('product')





def view_reports(request):
    reports=Report.objects.filter(status=False)
    return render(request,'product/view_reported_products.html',{'reports':reports})


def verify_report(request,id):
    report=Report.objects.get(id=id)
    update_booking_form=ReportForm(instance=report)
    if request.method=="POST":
        update_booking_form=ReportForm(request.POST,request.FILES,instance=report)
        update_booking_form.save()
        registers=Register.objects.all()
        for i in registers:
            send_mail(str(report.product.name)+' this product is reported','This product is reported','shabi960580@gmail.com',[i.user.email])

        return redirect('view_reports')
    return render(request,'product/add_review.html',{'form':ReportForm})
