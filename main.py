import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

try:

    def correct_url(url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        return url


    def scrollDown(browser, numberOfScrollDowns):
        body = browser.find_element(By.TAG_NAME,"body")
        while numberOfScrollDowns >=0:
            body.send_keys(Keys.PAGE_DOWN)
            numberOfScrollDowns -= 1
        return browser


    def crawl_url(url, run_headless=True):

        url = correct_url(url)
        browser =  webdriver.Chrome(executable_path=r'C:\Users\LENOVO\AppData\Local\Temp\Rar$EXa4724.28575\chromedriver.exe')
        browser.get(url)
        browser = scrollDown(browser, 20)
        vegiesArray =[]

        vegiesName = browser.find_elements(By.CLASS_NAME, "Product__DetailContainer-sc-11dk8zk-3")

        for vv in vegiesName:
            obj= {}
            ff=""
            while True:
                try:
                    ff = vv.find_element(By.CLASS_NAME, "variant_text_only").text
                    break
                except:
                    break

            dd = vv.find_element(By.CLASS_NAME,"Product__ProductName-sc-11dk8zk-4").text
            priceDiv = vv.find_element(By.CLASS_NAME, "eJcLXJ")
            obj["name"] = dd
            obj["quantity"] = ff
            obj["price"] = priceDiv.text
            vegiesArray.append(obj)

        for dd in vegiesArray:
            print(dd)

        browser.quit()
        return vegiesArray

    def export_data(data):
        df = pd.DataFrame(data)
        df.to_excel("vegies.xlsx")
        df.to_csv("vegies.csv")

except Exception as e:
    print(e)

if __name__=='__main__':
    url = "https://blinkit.com/cn/vegetables-fruits/fresh-vegetables/cid/1487/1489/"
    data = crawl_url(url)
    export_data(data)