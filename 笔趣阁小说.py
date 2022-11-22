#笔趣阁小说获取
#网址：https://www.bbiquge.net/
import re
import threading
import requests
from bs4 import BeautifulSoup
import os
import shutil

if not os.path.exists('./小说'):
    os.mkdir('./小说')
else:
    shutil.rmtree('./小说')
    os.mkdir('./小说')

if not os.path.exists('./log'):
    os.mkdir('./log')
else:
    shutil.rmtree('./log')
    os.mkdir('./log')
log = open('./log/error.txt', mode='a+')
log.write('123')


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
}

charset = 'gbk'
classify = {
    '1': 492,
    '2': 111,
    '3': 974,
    '4': 1377,
    '5': 281,
    '6': 114,
}

count = 0
def c_b(chapter_name, chapter_test_url):
    try:
        global count
        count = count + 1
        # print(chapter_test_url, chapter_name)
        test_html = requests.get(url=chapter_test_url, headers=headers)
        test_html.encoding = charset
        soup2 = BeautifulSoup(test_html.text, 'lxml')
        test_c = soup2.select('#content')
        c = str(test_c)
        test = re.findall('<br/> (.*?)<', c)[0:]
        f = open(f'./小说/{book_name}/{count}-{chapter_name}.txt', mode='a+', encoding='utf-8')
        f.write('@@' + chapter_name + '\n')
        for t in test:
            d = t.replace('\xa0', '')
            f.write("  " + d + '\n')
        f.close()
        print(f'            {chapter_name}保存成功！')
    except:
        log.write(f'            {chapter_name} {chapter_name}保存失败！\n')


for i in range(1, 6):
    try:
        for j in range(1, classify[str(i)]):
            try:
                page_url = f'https://www.bbiquge.net/fenlei/{i}_{j}/'
                page_html = requests.get(url=page_url, headers=headers)
                page_html.encoding = charset
                soup = BeautifulSoup(page_html.text, 'lxml')
                detailsOfTheNovel = soup.select('#tlist > ul > li'[:40])
                for novel in detailsOfTheNovel:
                    a = str(novel)
                    # print(a)
                    chapter_url = re.findall('href="(.*?)"', a)[0]
                    book_name = re.findall('title="(.*?)"', a)[0]
                    try:
                        chapter_html = requests.get(url=chapter_url, headers=headers)
                        chapter_html.encoding = charset
                        soup5 = BeautifulSoup(chapter_html.text, 'lxml')
                        conut = soup5.select('body > div.zjbox > div > select > option'[0:])
                        if not os.path.exists(f'./小说/{book_name}'):
                            os.mkdir(f'./小说/{book_name}')
                        else:
                            shutil.rmtree(f'./小说/{book_name}')
                            os.mkdir(f'./小说/{book_name}')
                        for k in range(1, len(conut)):
                            url_1 = chapter_url + f'/index_{k}.html'
                            chapter_html_1 = requests.get(url=url_1, headers=headers)
                            chapter_html_1.encoding = charset
                            soup1 = BeautifulSoup(chapter_html_1.text, 'lxml')
                            chapter_list = soup1.select('dd'[0:])
                            for chapter_test in chapter_list:
                                b = str(chapter_test)
                                chapter_test_url = chapter_url + re.findall('href="(.*?)"', b)[0]
                                chapter_name = re.findall('">(.*?)<', b)[0]
                                max_xc = threading.Semaphore(5)
                                n_c = threading.Thread(target=c_b, args=(chapter_name, chapter_test_url))
                                n_c.start()
                    except:
                        log.write(f'      {book_name}保存失败！\n')
                        continue
                    print(f'        {book_name}保存成功！')
            except:
                log.write(f'  {i}类保存失败！\n')
                continue
            print(f'    {i}类保存成功！')
    except:
        log.write(f'全部保存失败！\n')
        continue
    print('全部保存成功！')
log.close()

