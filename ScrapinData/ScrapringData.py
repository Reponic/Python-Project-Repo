import requests
import bs4
import pandas as pd
import json
import csv

url = "https://canvs.org/"
hdr = {"user-agent" : "Mozilla/5.0"}
req = requests.get(url, hdr)
if (req.status_code == 200):
    print("Done, Everything is Good!")
    print(req.headers["content-type"])

    # ---- HTML ----

    text = bs4.BeautifulSoup(req.text, "html.parser")
   # print(text)

    # ----- This is what we want the a few extra lines. ------

    results = text.find_all("section", class_="widget widget_text", id="text-7")

    for item in results:
        print(item.get_text())

    # ---- Fun Part ----

    for item in results:
        Data = item.get_text().split("\n")
    Email = ""
    Address = []
    count = 0
    for item in Data:
        if item == "Address:":
            Address.append(Data[count + 1])
            Address.append(Data[count + 2])
        elif item == "Email:":
            Email = Data[count + 1]
        count += 1

    #for item in Address:
     #   print(item)
    #print(Email)

    # ---- Data Frame ----

    data = [
        {'_Email': Email},
        {'_Addres': Address}
    ]

    df = pd.DataFrame(data)
    filename = 'canvs_data.csv'
    df.to_csv(filename, index=False, encoding='utf-8')

    # ---- Building the JSON from the CSV ----

    csvfile = open('canvs_data.csv', 'r')
    jsonfile = open('canvs_data_json.json', 'w')

    fieldnames = ("Address", "Email")
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
         json.dump(row, jsonfile)
         jsonfile.write('\n')




