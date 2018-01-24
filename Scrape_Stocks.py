#Declare Libraries
import urllib2
from bs4 import BeautifulSoup  
from lxml import html
import requests

#Grabs html tree, seaches for identifer of earnings table, grows next year est growth
page = requests.get('https://finance.yahoo.com/quote/MMM/analysts?p=MMM')
tree = html.fromstring(page.content)
values = tree.xpath('//td[@class="Ta(end) Py(10px)"]/text()')

#This is the next year growth rate
print(float(values[12].replace("%","")))

#The Dividend URL page
url = "https://finance.yahoo.com/quote/MMM/history?period1=1279598400&period2=1500523200&interval=1mo&filter=history&frequency=1mo"
r = requests.get(url)

# Turn the HTML into a Beautiful Soup object, strip out items into list with dividend identifier
soup = BeautifulSoup(r.text, 'lxml')
table = soup.find_all(class_='Ta(c) Py(10px)')

#Parse out the number values
i = 0
dividends = []
while (i < len(table)):
  #Protect from stock splits
  if ("Stock Split" not in str(table[i])):
    #Some parsing to get to the number using common tags
    string = str(table[i])
    string = string[string.index("strong data-reactid="):]
    string = string[string.index(">") + 1:]
    string = float(string[:string.index("<")])
    #Find growth rate quartley, however it is published
    if ( i >= 1):
      dividends.extend([temp / string])
    temp = string
  else:
    pass 
  i = i + 1

#Average growth rate to get our estimate
print(sum(dividends)/len(dividends))