from bs4 import BeautifulSoup
import requests as r
import os
import csv

if not os.path.exists("data"):
    os.mkdir("data")

headers = {
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

url = "https://konferencii.ru/"
req = r.get(url, headers=headers).text

soup = BeautifulSoup(req, "lxml")

konf_urls = []
konf_all_data = []
konf_all_data1 = []
page_links = []
cnt = 0

for i in soup.find("div", id="visibleLinks").find_all("a"):
    page_link = "https://konferencii.ru" + i.get("href")
    req = r.get(page_link, headers=headers)
    page_links.append(page_link)
    cnt += 1

    with open(f"data/page{cnt}.html", "w", encoding="utf-8") as file:
        file.write(req.text)

for page in range(1, cnt + 1):
    with open(f"data/page{page}.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")

    content1 = soup.find_all("div", class_="row1 index_cat_1st")
    content2 = soup.find_all("div", class_="row2 index_cat_1st")

    for o in content1:
        konf_url = "https://konferencii.ru" + o.find("div", class_="index_cat_tit").find("a").get("href")
        konf_urls.append(konf_url)
    for o in content2:
        konf_url = "https://konferencii.ru" + o.find("div", class_="index_cat_tit").find("a").get("href")
        konf_urls.append(konf_url)


for konf_url in konf_urls:
    req = r.get(konf_url, headers=headers).text
    soup = BeautifulSoup(req, "lxml")
    konf_data = soup.find("div", class_="content view")

    for j in range(0, 1):

        try:
            name = konf_data.find("h1", class_="inside_h1a").text
        except Exception:
            name = "The name of the conference is not specified"

        try:
            application_deadline = ""
            time = konf_data.find("p").text.strip()
            if "," in time:
                application_deadline = time[time.find(",") + 1:].strip()
                time = time[:time.find(",")].strip()
        except Exception:
            time = "time of the conference is not specified"
            application_deadline = "application deadline is not specified"

        try:
            city = konf_data.find("div", class_="left-col").find("p").text.strip()[:22].strip()
        except Exception:
            city = " city is not specified"

        try:
            language = konf_data.find("div", class_="left-col").find("div", class_="lang").find("a").text
        except Exception:
            language = "language is not specified"

        try:
            form_of_participation = konf_data.find("div", class_="left-col").find_next("p").find_next("p").text[16:].strip()
        except Exception:
            form_of_participation = "form of participation is not specified"

        try:
            last_day = konf_data.find("div", class_="left-col").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").text
            if "(" in last_day:
                last_day = "приём заявок закончен"
            else:
                last_day = last_day[30:]
        except Exception:
            last_day = "last day to submit an application not specified"

        try:
            full_description = konf_data.find("p", class_="p160").text.strip()
            if "\n" in full_description:
                full_description = full_description.replace("\n", " ")
            if "\r" in full_description:
                full_description = full_description.replace("\r", " ")
            if "  " in full_description:
                full_description = full_description.replace("  ", " ")
            if "   " in full_description:
                full_description = full_description.replace("   ", " ")
            full_description.strip()
        except Exception:
            full_description = "description not specified"

        with open("Konf_data.csv", "a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    name,
                    time,
                    application_deadline,
                    city,
                    language,
                    form_of_participation,
                    last_day,
                    full_description
                )
            )
