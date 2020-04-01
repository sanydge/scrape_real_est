import requests, pandas
from bs4 import BeautifulSoup

l = []
base_url = "http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

for page in range(0, 30, 10):
    print(base_url + str(page) + ".html")
    r = requests.get(base_url + str(page) + ".html", headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "propertyRow"})

    for item in all:
        d = {}
        d["Price"] = item.find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ", "")
        d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text
        d["City, State, ZIP"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
        try:
            d["Area"] = item.find("span", {"class": "infoSqFt"}).text
        except:
            pass

        try:
            d["Beds"] = item.find("span", {"class": "infoBed"}).text
        except:
            pass

        try:
            d["Full Baths"] = item.find("span", {"class": "infoValueFullBath"}).text
        except:
            pass

        try:
            d["Half Baths"] = item.find("span", {"class": "infoValueHalfBath"}).text
        except:
            pass

        for column_group in item.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}),
                                                   column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text.replace(",", "").replace("Under", "<")

        l.append(d)

df = pandas.DataFrame(l)
df.to_csv("Output.csv")