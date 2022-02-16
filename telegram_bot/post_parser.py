import requests
from config import TOKEN_VK, API_V
from bs4 import BeautifulSoup
# from sqlighter import SQLighter
#
# db = SQLighter('db.db')
# res = db.get_all_subscribers("Kronbars")
# print(*res)
# for i in db.get_all_subscribers("Kronbars"):
#     print(i[0])

def parse_itmostudents():
    r = f"https://api.vk.com/method/wall.get?access_token={TOKEN_VK}&v={API_V}&domain=itmostudents&count=1"
    response = requests.get(r)
    data = response.json()['response']['items'][0]
    post_id = data['id']
    post_text = data['text']
    data = data['attachments'][0]
    if data['type'] == 'photo':
        data = data['photo']
    elif data['type'] == 'video':
        data = data['video']
    else:
        return
    post_img_url = data['sizes'][2]['url']
    return post_id, post_text, post_img_url


def parse_kronbars():
    r = f"https://api.vk.com/method/wall.get?access_token={TOKEN_VK}&v={API_V}&domain=kronbars&count=1"
    response = requests.get(r)
    data = response.json()['response']['items'][0]
    post_id = data['id']
    post_text = data['text']
    data = data['attachments'][0]
    if data['type'] == 'photo':
        post_img_url = data['photo']['sizes'][2]['url']
    elif data['type'] == 'video':
        post_img_url = data['video']['image'][2]['url']
    else:
        return
    # post_img_url = data['sizes'][0]['url']
    # post_img_url = data['image'][0]['url']
    return post_id, post_text, post_img_url

def parse_career_news():
    HOST_CAREER = "https://careers.itmo.ru/"
    r = requests.get(HOST_CAREER)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.find('div', class_ = "col-md-3 col-sm-6 active")
    link = str(item.find('a').get("href"))
    post_id = int(link[6:9])
    title = item.find('p', class_ = "news-title").get_text()
    img_url = item.find('img').get("src")
    return post_id, title + '\n\n' + HOST_CAREER + link, HOST_CAREER + img_url
