import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from docx import Document

def main(url):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "cookie":"over18=1"
    }
    response=requests.get(url,headers=headers)  #發起請求，獲取網頁內容
    with open("data3.html","w",encoding="utf-8") as f:  #寫入網頁內容到 data3.html 文件
        f.write(response.text)  
        soup=bs4.BeautifulSoup(response.text,"html.parser")  #使用 Beautiful Soup 解析網頁內容
    #尋找標題    
    chapter=soup.find("div",class_="chapter")
    if chapter:
        h3=chapter.find("h3")
        if h3:
            print("-"*30)
            print(h3.text.strip())  #strip(去除前後空白)
    #尋找內文
    content=soup.find("div",class_="chapter")
    if content:
        nr=content.find(id="nr")
        if nr:
            style=nr.find('p', style='color:green;')
            if style:
                style.extract()
            print(nr.text.rstrip())
    with open("直播.txt",mode="a",encoding="utf-8") as file:
        file.write("-"*30+"\n")
        file.write(h3.text.strip()+"\n")
        file.write(nr.text.rstrip()+"\n")

def nextpage(url):
    options=Options()
    options.Chrome_executable_path="G:\Microsoft VS Code\Python traning\chromedriver.exe"
    driver=webdriver.Chrome(options=options)
    driver.get(url)
    next=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID,"btnNext"))
    )
    if next:
        next.click()
    new_url=driver.current_url
    return new_url

first_url="https://h.fkxs.net/book/250599/120526126.html"

i=0
while i<6:
    main(first_url)
    nextpage(first_url)
    first_url=nextpage(first_url)
    if "#google_vignette" in first_url:
        print("跳過這個網址:", first_url)
        continue
    else:
        print("當前:",first_url)
    i+=1