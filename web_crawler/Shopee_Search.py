import requests
import urllib


class ShopeeSpider():    

    def request_get(self,query,keyword):
        
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
            'x-api-source': 'pc',
            'referer': f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}'#urllib.parse.quote對字符串進行URL編碼
        }

        
        s = requests.Session()
        url = 'https://shopee.tw/api/v4/search/product_labels'
        r = s.get(url, headers=headers)
        base_url = 'https://shopee.tw/api/v4/search/search_items'
        
        url = base_url + '?' + query
        r = s.get(url, headers=headers)
        #print(r.url)
        if r.status_code == requests.codes.ok:
            data = r.json()
            
        return data
    def search_products(self,keyword,sort='綜合排名'):
        products = []
        all_by ={
            '綜合排名':'relevancy',
            '最新':'ctime',
            '最熱銷':'sales',
        }
        
        query = f"by={all_by[sort]}&keyword={keyword}&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
        data = self.request_get(query,keyword)
        
        if not data:
            print('請求發生錯誤：')
        if data ['total_count'] <= 0:
            print('找不到有關的產品')
        
        products.extend(data['items'])
        #print(data)
        return products

    def item_spend(self,products,item_id):
        for i in range(5):
            item_id.append(products[i]['itemid'])
        
        return item_id

    
    def shop_spend(self,products,shop_id):
        for i in range(5):
            shop_id.append(products[i]['shopid'])
        
        return shop_id
    
if __name__ == '__main__':
    #keyword = input("請輸入查尋項目:")
    shopee_spider = ShopeeSpider()
    products = shopee_spider.search_products('顯示卡')

    for i in range(5):
        price = str(products[i]['item_basic']['price'])
        Change_price = price.removesuffix('00000')
        price =int(Change_price) 

        
    #print(item_id)
        
        #print(products[i]['item_basic']['name'],Change_price,'/n',item_id,'/n',shop_id)
