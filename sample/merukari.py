from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

item_ls = []
item_url_ls = []

# ブラウザの設定
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ブラウザの起動
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)

# キーワード設定
KEYWORD = '大学'

def get_url():
    url = f'https://jp.mercari.com/search?keyword={KEYWORD}'
    browser.get(url)
    browser.implicitly_wait(5)

    # 商品の詳細ページのURLを取得する
    item_box = browser.find_elements(By.CSS_SELECTOR, '#item-grid > ul > li')
    for item_elem in item_box:
        item_url_ls.append(item_elem.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

def get_data():
    # 商品情報の詳細を取得する
    for item_url in item_url_ls:
        browser.get(item_url)
        time.sleep(3)
        
        # 商品名
        item_name = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > mer-heading').text
        
        # Shadow DOMの要素にアクセスするにはJavaScriptを実行する
        shadow_root = browser.execute_script("return arguments[0].shadowRoot", browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(2) > mer-show-more'))
        item_ex = shadow_root.find_element(By.CSS_SELECTOR, 'div.content.clamp').text
        
        # 画像URLの取得も同様にShadow DOMを考慮
        src_shadow = browser.execute_script("return arguments[0].shadowRoot", browser.find_element(By.CSS_SELECTOR, '#main > article > ... > mer-item-thumbnail'))
        src = src_shadow.find_element(By.CSS_SELECTOR, 'div > figure > div.image-container > picture > img').get_attribute('src')
        
        # 価格の取得も同様
        shadow_root1 = browser.execute_script("return arguments[0].shadowRoot", browser.find_element(By.CSS_SELECTOR, '#item-grid > ul > li:nth-child(1) > a > mer-item-thumbnail'))
        price_shadow = shadow_root1.find_element(By.CSS_SELECTOR, 'div > figure > div.price-container > mer-price')
        item_price = price_shadow.find_element(By.CSS_SELECTOR, 'span.number').text
        
        data = {
            '商品名': item_name,
            '商品説明': item_ex,
            '価格': item_price,
            'URL': item_url,
            '画像URL': src
        }

        item_ls.append(data)

def main():
    get_url()
    get_data()
    pd.DataFrame(item_ls).to_csv(f'merukari_{KEYWORD}.csv')

if __name__ == '__main__':
    main()
