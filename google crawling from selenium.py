import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Chrome 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# 검색어 입력
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
search_field = driver.find_element(By.NAME, "q")
name = "강아지"
search_field.send_keys(name)
search_field.send_keys(Keys.RETURN)

# 이미지 저장 폴더 경로
dir_path = name

# 이미지 저장 폴더 생성
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 검색 결과 페이지 URL
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 이미지 다운로드
images = driver.find_elements_by_css_selector(".rg_i")
for i, image in enumerate(images):
    try:
        image.click()
        time.sleep(2)
        original_image_url = None
        elements = driver.find_elements_by_css_selector(".n3VNCb")
        for element in elements:
            if element.get_attribute("src") and element.get_attribute("src").startswith("http"):
                original_image_url = element.get_attribute("src")
                break
        if not original_image_url:
            raise ValueError("Could not find image URL")
        filename = "{}_{}.jpg".format(name, i)
        filepath = os.path.join(dir_path, filename)
        response = requests.get(original_image_url)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("다운로드 완료:", filepath)
    except Exception as e:
        print("에러 발생:", e)
# Chrome 드라이버 종료
driver.quit()