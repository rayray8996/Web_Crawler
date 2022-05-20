import requests
import json

class PchomeSpider():
    """PChome線上購物 爬蟲"""
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        }
    def request_get(self, url, params=None, to_json=True):
        
        r = requests.get(url, params)
        #print(r.url)
        if r.status_code != requests.codes.ok:
            print(f'網頁載入發生問題：{url}')
        try:
            if to_json:
                data = r.json()
            else:
                data = r.text
        except Exception as e:
            print('OK')
            return None
        return data
    
    def search_products(self, keyword, max_page=3, shop='全部', sort='有貨優先', price_min=-1, price_max=-1, is_store_pickup=False, is_ipost_pickup=False):
        products = []
        all_shop = {
            '全部': 'all',
            '24h購物': '24h',
            '24h書店': '24b',
            '廠商出貨': 'vdr',
            'PChome旅遊': 'tour',
        }
        all_sort = {
            '有貨優先': 'sale/dc',
            '精準度': 'rnk/dc',
            '價錢由高至低': 'prc/dc',
            '價錢由低至高': 'prc/ac',
            '新上市': 'new/dc',
        }
#https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E9%A1%AF%E7%A4%BA%E5%8D%A1&page=1&sort=sale/dc
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/{all_shop[shop]}/results'
        params = {
            'q': keyword,
            'sort': all_sort[sort],
            'page': 0
        }
        while params['page'] < max_page:
            params['page'] += 1
            data = self.request_get(url, params)
            if not data:
                print(f'請求發生錯誤：{url}{params}')
                break
            if data['totalRows'] <= 0:
                print('找不到有關的產品')
                break
            products.extend(data['prods'])
            if data['totalPage'] <= params['page']:
                break
        return products
 
if __name__ == '__main__':
    pchome_spider = PchomeSpider()
    step = 0
    products = pchome_spider.search_products(keyword='顯示卡')
    print(products)
    
    for i in range(60):
        
        print(products[i]['name'],products[i]['price'],i)

