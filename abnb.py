#!/usr/bin/python3
from sys import argv
from bs4 import BeautifulSoup
import requests
import urllib.request
import calendar
import datetime

script, ia = argv
if ia == 'sw':
 area = 'South-West-England--UK'
else:
 area = 'south'

airbnb = "https://airbnb.co.uk"

############# Get Dates for the Next Weekend ##########
def GetDateNextSat():
        today = datetime.datetime.today()
        saturday = today + datetime.timedelta((calendar.SATURDAY-today.weekday()) %7)
        return(saturday.strftime('%Y-%m-%d'))

def GetDateNextSun():
        today = datetime.datetime.today()
        sunday = today + datetime.timedelta((calendar.SUNDAY-today.weekday()) %7)
        return(sunday.strftime('%Y-%m-%d'))

checkin = GetDateNextSat()
checkout =  GetDateNextSun()
######################################################

homes = 'homes&current_tab_id=home_tab&selected_tab_id=home_tab'
source = 'source=mc_search_bar&search_type=filter_change&screen_size=large&hide_dates_and_guests_filters=false'

url = airbnb + '/s/' + area + '/homes?refinement_paths%5B%5D=%2F' + homes +'&place_id=ChIJC_d1ROPGakgRpqpEQmUBQ_U&' + source + '&checkin=' + checkin + '&checkout=' + checkout + '&adults=2&room_types%5B%5D=Entire%20home%2Fapt&price_max=275&amenities%5B%5D=25'

result = requests.get(url)
src = result.content
soup = BeautifulSoup(src,features="html.parser")

loc = ("Area : " + area)
cin = (" Checkin : " + checkin)
cout = (" Checkout : " + checkout)
search = loc + cin + cout 

list2 = soup.findAll('div', attrs={'class': "_1ebt2xej"}) #ahrefs
tags = soup.find_all('a', class_="_i24ijs") #descs
list_prices = soup.findAll('div', attrs={'class':"_vsjqit"}) #prices
html = "<html>\n<head>\n<style>p {margin: 0!important }</style>\n<body>"+ search + "\n"
VIS = []
#------------------------------------------------------------
def GenHTML_File():
	with open('htub.html','w+') as file:
		file.write(html +"</body></html>")
		file.close()
#------------------------------------------------------------
def GenScreenInf():
	i = 1
	for link, price in zip(list2,list_prices):
	 VIS.append( (str(i) +" "+ link.text + " " + price.text +"\n") )
	 i = i + 1
	return (VIS)
#-----------------------------------------------------------
def PrScreenInf():
	print ("# Found these in  Area = " + area + "#" + "\n")
	for i in (VIS):
	 print (i)
#-----------------------------------------------------------

# MAIN CODE


print ("Dates = ")
print (GetDateNextSat())
print (GetDateNextSun())



for i,j in zip(tags,list2):
	a = j.text # description
	b = i.text # a href
	c = airbnb + i.get('href') # full url
	print (a +" " + b + c + "\n")
	html += '\n<p>'+'<a href=' + c + '</a>'+a+'</p>\n'

GenScreenInf()
PrScreenInf()
#GenHTML_File()

# Get Pics as BS and save locally to /images
# Loop through list of "c" and get the main image
url2 = 'https://a0.muscache.com/im/pictures/2624c248-e3eb-4c2a-859a-308619cbd574.jpg'
urll = 'https://a0.muscache.com/im/pictures/8c283cfa-3e88-4bf8-8d41-1d8f657ca22f.jpg'

Picture_request = requests.get(url2)
if Picture_request.status_code == 200:
    with open("images/5.jpg", 'wb') as f:
        f.write(Picture_request.content)

