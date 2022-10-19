import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os
import requests
import time
from googleapiclient.http import MediaFileUpload
from Google import Create_Service

try:

    def correct_url(url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        return url


    def scrollDown(browser, numberOfScrollDowns):
        body = browser.find_element(By.TAG_NAME, "body")
        while numberOfScrollDowns >= 0:
            body.send_keys(Keys.PAGE_DOWN)
            numberOfScrollDowns -= 1
        return browser


    def crawl_blinkit_url(url, run_headless=True):

        url = correct_url(url)
        browser = webdriver.Chrome(
            executable_path=r'C:\Users\LENOVO\AppData\Local\Temp\Rar$EXa4724.28575\chromedriver.exe')
        browser.get(url)
        browser = scrollDown(browser, 20)
        vegiesArray = []

        vegiesName = browser.find_elements(By.CLASS_NAME, "Product__DetailContainer-sc-11dk8zk-3")

        for vv in vegiesName:
            obj = {}
            ff = ""
            while True:
                try:
                    ff = vv.find_element(By.CLASS_NAME, "variant_text_only").text
                    break
                except:
                    break

            dd = vv.find_element(By.CLASS_NAME, "Product__ProductName-sc-11dk8zk-4").text
            priceDiv = vv.find_element(By.CLASS_NAME, "eJcLXJ")
            obj["name"] = dd
            obj["quantity"] = ff
            obj["price"] = priceDiv.text
            vegiesArray.append(obj)

        for dd in vegiesArray:
            print(dd)

        browser.quit()
        return vegiesArray


    def crawl_lots_data(url, run_headless=True):
        pageNumber =1
        lotVegiesArray = []
        while pageNumber<=2:
            jsonData ={
                "assortOrderStoreCode": "101",
                "assortPriceStoreCode": "101",
                "hierarchies": [{"level": 1, "selectedHId1": []}],
                "loadHierarchy": "true",
                "locale": "en_US",
                "menuId": 100712,
                "nonAssortOrderStoreCode": "101",
                'nonAssortPriceStoreCode': "101",
                "page": pageNumber,
                "pageSize": 60,
                "priceFilters": [],
                "reloadPrice": "true",
                "sorting": "SORTING_MENU_INDEX"
            }
            response = requests.post(url, json=jsonData)
            arrayData = response.json()["content"]

            for data in arrayData:
                obj ={}
                obj["name"] = data["productName"]
                obj["quantity"] = data["pricingRecords"][0]["quantity"]
                obj["price"] = data["pricingRecords"][0]["retailPrice"]
                lotVegiesArray.append(obj)
            pageNumber = pageNumber+1
            time.sleep(10)
        print(len(lotVegiesArray))
        for dd in lotVegiesArray:
            print(dd)
        return lotVegiesArray


    def export_data(data, excelFilePath, csvFilePath):
        df = pd.DataFrame(data)
        df.to_excel(excelFilePath)
        df.to_csv(csvFilePath)


    def excel_converter(file_path: str, folder_ids: list = None):
        CLIENT_SECRET_FILE = './secret_key/secret_key.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        print((service))

        if not os.path.exists(file_path):
            print(f'{file_path} not found')
            return
        try:
            print(os.path.splitext(os.path.basename(file_path))[0])
            file_metadata = {
                'name': os.path.splitext(os.path.basename(file_path))[0],
                'mimeType': 'application/vnd.google-apps.spreadsheet',
                'parents': folder_ids
            }
            print(file_path)
            media = MediaFileUpload(filename=file_path,
                                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response = service.files().create(
                media_body=media,
                body=file_metadata
            ).execute()

            print(response)
            return (response)
        except Exception as e:
            print(e)
            return

except Exception as e:
    print(e)

if __name__ == '__main__':
    url = "https://blinkit.com/cn/vegetables-fruits/fresh-vegetables/cid/1487/1489/"
    data = crawl_blinkit_url(url)
    export_data(data, "../excels/vegies.xlsx", "./csv/vegies.csv")

    lotsData =crawl_lots_data("https://api.lotswholesale.com/next-product/public/api/product/search")
    export_data(lotsData, "../excels/lotsVegies.xlsx", "./csv/lotsVegies.csv")

    excel_files= os.listdir('../excels')
    for excel_file in excel_files:
        excel_converter(os.path.join('../excels/', excel_file))
