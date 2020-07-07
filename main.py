import requests
import pandas
from bs4 import BeautifulSoup

r = requests.get("https://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content


soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("div", {"class":"propertyRow"})

all[0].find("h4", {"class":"propPrice"}).text.replace("\n", "").replace(" ", "")

pageNr = soup.find_all("a", {"class": "Page"})[-1].text

l = []
base_url = "https://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0, int(pageNr) * 10, 10):
    print(base_url + str(page) + ".html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "propertyRow"})    
    for item in all:
        d = {}
        d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text
        
        try:
            d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
            
        d["Price"] = item.find("h4", {"class", "propPrice"}).text.replace("\n", "").replace(" ", "")

        try:
            d["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"] = None

        try:
            d["Area"] = item.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Baths"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Baths"] = None

        try:
            d["Half Baths"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None
        for colGroup in item.find_all("div", {"class":"columnGroup"}):
            #print(colGroup)
            for featureGroup, featureName in zip(colGroup.find_all("span", {"class": "featureGroup"}), colGroup.find_all("span", {"class": "featureName"})):
                if "Lot Size" in featureGroup.text:
                    d["Lot Size"] = featureName.text
        l.append(d)

df = pandas.DataFrame(l)
print(df)
df.to_csv("Output.csv")