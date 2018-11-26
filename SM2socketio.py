#-*- encoding:utf-8 -*-
# from __future__ import print_function
#163.17.136.135:3322
import sys
import re
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import jieba
from opencc import OpenCC
import json
import requests
from bs4 import BeautifulSoup
import jieba.analyse
import subprocess


from threading import Thread
from socketIO_client import SocketIO


import time
import threading






#-*- encoding:utf-8 -*-
# from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import requests
import re
from bs4 import BeautifulSoup
import json

from opencc import OpenCC
import json
import jieba.analyse

import time
from timeit import Timer
import datetime

top_50_keyword=[]
filename_new='data11221523.json'

url="https://www.ptt.cc/bbs/Gossiping/index.html"
headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
# r=requests.get(url=url,headers=headers,cookies={'over18': '1'})





def get_ptt_contents(keywords):
    url="https://www.ptt.cc/bbs/Gossiping/search?q="+keywords
    r=requests.get(url=url,headers=headers,cookies={'over18': '1'})

    content=""
    contents=""

    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')

        #   抓出標題
        post_titles = soup.select('div.r-ent div.title')
        for post_title in post_titles:
        #     print(s)
        # 標題
    #         print("標題：" + post_title.text)
        # 網址
    #         print("網址：" + post_title.a['href'])
            try:
                url = "https://www.ptt.cc"+post_title.a['href']
    #         print(url)


                r2=requests.get(url=url,headers=headers,cookies={'over18': '1'})   
                if r2.status_code == requests.codes.ok:
                    # 以 BeautifulSoup 解析 HTML 程式碼
    #                 soup2 = BeautifulSoup(r2.text, 'html.parser')
    #                 main_content = soup2.find(id="main-content")        
    #                 filtered = [ v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]            

    #             #     content = ' '.join(filtered) 
    #                 content = "".join(filtered[8])
    #                 content = ''.join(re.sub(r'(\s)+', '', content ))

                    soup2 = BeautifulSoup(r2.text, 'html.parser')
                    main_content = soup2.find(id="main-content")
                    filtered = [ v for v in main_content.stripped_strings]
    #                 content=[]
                    for i in range(8,len(filtered)):
                        if filtered[i][:2]==": ":
                            continue
                        if filtered==":":
                            continue
                        if filtered[i][:4]=="※ 引述":
                            continue   
                        if filtered[i][:4] == "http":
                            continue
                        if "Sent from JPTT on" in filtered[i]:
                            break
                        if filtered[i-1][-5:] == "\n\n\n--":
                            break
                        if "※ 發信站"in filtered[i]:
                            break
                        content=''.join(filtered[i])
                    #     print(filtered[i])

                    contents +=content
#             else:
#                 return "連不上網路"
#     else:
#         return "連不上網路"
            
            except:
                pass
        time.sleep(0.1)
    else:
        pass
        
            
            
            
        
    cc = OpenCC('tw2sp')  # convert from  Traditional Chinese to  Simplified Chinese
    # cc.set_conversion('s2tw')
    Simplified = cc.convert(contents)
    
    text = Simplified
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2) 
    news_keywords=[]
    news_phrase=[]
    news_sentence=[]

    cc = OpenCC('s2twp')
    
#     print( '關鍵詞：' )
    for item in tr4w.get_keywords(20, word_min_len=1):
    #     print(item.word, item.weight)
    #         print(item.word)
        news_keywords.append(cc.convert(item.word))

#     print()
#     print( '關鍵短語：' )
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
#         print(phrase)
        news_phrase.append(cc.convert(phrase))


    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

#     print()
#     print( '摘要：' )
    abstracts=[]
    for item in tr4s.get_key_sentences(num=3):
#         print(item.index, item.weight, item.sentence)
    #         print(item.sentence)
        abstracts.append(item.sentence)

    for i in range(0,len(abstracts)):
    #     print(i)
        abstracts[i] = re.sub('[\-\\\\\「\」\）\（\}\{\,\'\"\▼\▲]', '', cc.convert(abstracts[i]))
    # abstracts

    #     for abstract in abstracts:
    #         print(abstract)
    #         print()

#     return json.dumps({'news_keywords':news_keywords, 'news_phrase':news_phrase, 'news_sentence':abstracts}, 
#                   ensure_ascii=False)
        
    
    return abstracts








def ptt_cow():
    print("開始ptt爬蟲")
    url="https://www.ptt.cc/bbs/Gossiping/index.html"
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
#     r=requests.get(url=url,headers=headers,cookies={'over18': '1'})
    
    
    
        #爬標題

#     url="https://www.ptt.cc/bbs/Gossiping/index.html"
    titles=''
    for i in range(0,10): 

#         headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        r=requests.get(url=url,headers=headers,cookies={'over18': '1'})

        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            post_titles = soup.select('div.r-ent div.title')
            for post_title in post_titles:
            #     print(s)
                if "本文已被刪除" in post_title.text:
                    continue
                if "討論政治截止線" in post_title.text:
                    continue
                    
                else:
                # 標題
    #                 print(post_title.text[1:])
                    title_tmp = post_title.text[1:]
                    try:
                #         print(title_tmp.split("] ")[1])
                        titles+=title_tmp.split("] ")[1].replace('"',' ')+" \n"
                    except:
                        try:
                #             print(title_tmp.split("］ ")[1])
                            titles+=title_tmp.split("］ ")[1].replace('"',' ')+" \n"
                        except:
                            try:
                #                 print(title_tmp.split("]")[1])
                                titles+=title_tmp.split("]")[1].replace('"',' ')+" \n"
                            except:
                                try:
                #                     print(title_tmp.split("］")[1])
                                    titles+=title_tmp.split("］")[1].replace('"',' ')+" \n"
                                except:
                #                     print(title_tmp)
                                    titles+=title_tmp.replace('"',' ')+" \n"

                #網址
            #         print("網址：" + s.get('href'))
#                 print(titles)
                
            next_page_tmp = soup.select('.action-bar a.btn.wide')    
            next_page ="https://www.ptt.cc"+next_page_tmp[1].get('href')
            url = next_page
    #         print("url",url)
    
    
        #找出關鍵字


    cc = OpenCC('tw2sp')  # convert from Simplified Chinese to Traditional Chinese
    # can also set conversion by calling set_conversion
    # cc.set_conversion('s2tw')
    Simplified = cc.convert(titles)
    jieba.analyse.set_stop_words('stopwords.txt')
    jieba.add_word('柯文哲')
    jieba.add_word('叶克膜')
    jieba.add_word('黄士修')
    jieba.add_word('韩国瑜')
    
    
    cc = OpenCC('s2twp')

    top_50_keyword=[]
    tags = jieba.analyse.extract_tags(Simplified,
                                      topK=50,
                                      withWeight=True
                                     )
    for tag, weight in tags:
    #     print(cc.convert(tag) + "," + str(weight))
        top_50_keyword.append(cc.convert(tag))
    print(top_50_keyword)
        
        
        
        
    output_data=[]

    for i in range(0,50 if len(top_50_keyword)>10 else len(top_50_keyword)):
        if("八卦" in top_50_keyword[i]):
            continue
        output_data.append({"name":top_50_keyword[i],"contents":get_ptt_contents(top_50_keyword[i])})

        # output_data.append({top_50_keyword[i]:get_ptt_contents(top_50_keyword[i])})
        
    
    now = datetime.datetime.now() #現在時間
    time_now=str(now.month)+str(now.day)+str(now.hour)+str(now.minute)
    # Writing JSON data
    global filename_new
    filename_new='data'+time_now+'.json'
    with open(filename_new, 'w') as f:
        try:
            json.dump(output_data, f,ensure_ascii=False)
        except:
            pass
    print('data'+time_now+'.json')
    
    
    # Reading data back
#     with open('data'+time_now+'.json', 'r') as f:
#         data = json.load(f)
    







def ptt_run():  
    print("start")
    ptt_cow()
    timer = threading.Timer(60*60,ptt_run)
    timer.start() 
    
# ptt_run()  






# filename_new='data11212010.json'


def get_new_ptt_keywords():
    return_data=[]

    with open(filename_new, 'r') as f:
        datas = json.load(f)
        for data in datas:
            return_data.append(data["name"])
    # return return_data
    return json.dumps(datas,ensure_ascii=False)




#============#============#============#============#============#============


def google_serach(keyword="巴哈是什麼"):
    # 下載 Yahoo 首頁內容
#     keyword = "巴哈是什麼"
    url="https://www.google.com.tw/search?source=hp&ei=goveW4_cI8ny8AXz2rbgDw&q="+keyword
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    r=requests.get(url=url,headers=headers)
    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')

        #   以 CSS 的 class 抓
        try:
            stories = soup.find_all(class_='kno-rdesc')                 
            print(stories[0].text[:-5])
            return (stories[0].text[:-5])


        except:
            try:
                stories = soup.find_all(class_='LGOjhe')
                print(stories[0].text)
                return (stories[0].text)

            except:
                print("找不到相關搜尋喔！")
                return("找不到相關搜尋喔！")
                
    else:
        print("無法連線到google!!") 
        return ("無法連線到google!!")         

#============#============#============#============#============#============
def get_news_content(keyword="美國&中國"): #取得新聞關鍵內容（包含爬蟲）

    url="https://tw.news.yahoo.com/tag/"+keyword
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    r=requests.get(url=url,headers=headers)
    
    def findkeyword(keyword,text):
        for t in keyword:
            if (t != "&")&(t in text):
                return True
        return False
    
         

    # 去除非關鍵字標題
    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
         # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')

        #以 CSS 的 class 抓出各類頭條新聞
        #stories = soup.find_all('a', class_='D(ib) Ov(h) Whs(nw)')
        stories = soup.select("a.Fw(b).Fz(20px).Lh(23px)")
        textmp=""
        hrefs=[]
        for s in stories:
            tmp = s.text
    #         if keyword in tmp:
            if (findkeyword(keyword,tmp)):
                #新聞標題
    #             print("標題：" + tmp,"連結："+ s.get('href'))
                textmp += tmp
                hrefs.append(s.get('href'))
    # 新聞網址
    #         print("網址：" + s.get('href'))
    
    context =""
    hrefs_num = len(hrefs)
    if (hrefs_num == 0):
        print("無與此關鍵字相關新聞 ")
    if (hrefs_num > 10):
        hrefs_num= int(hrefs_num/2)

    # for url in hrefs:
    for i in range(0,hrefs_num):
        url=hrefs[i]
        news_href = "https://tw.news.yahoo.com/"+url
        r=requests.get(url=news_href,headers=headers)
        # 去除非關鍵字標題
        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(r.text, 'html.parser')

            #以 CSS 的 class 抓出各類頭條新聞
            #stories = soup.find_all('a', class_='D(ib) Ov(h) Whs(nw)')
            stories = soup.select("p.canvas-atom")

            for s in stories:
            #     print(s)
            # 新聞標題
                if "更多上報內容" in s.text or "更多三立新聞網報導" in s.text:
                    break
                context+=s.text +" \n"
    #             print(s.text)
            # 新聞網址
            #print("網址：" + s.get('href'))
            
    
    
    cc = OpenCC('tw2sp')  # convert from Simplified Chinese to Traditional Chinese
    # can also set conversion by calling set_conversion
    # cc.set_conversion('s2tw')
    Simplified = cc.convert(context)
    
    jieba.add_word('国防部', 100, 'n')  # 自定义词库

    text = Simplified
    tr4w = TextRank4Keyword(stop_words_file='stopwords.txt')  # 导入停止词

    # tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2)   # py2中text必須是utf8編碼的str或者unicode對象，py3中必須是utf8編碼的bytes或者str對象
    news_keywords=[]
    news_phrase=[]
    news_sentence=[]
    

    cc = OpenCC('s2twp')

    # print( '關鍵詞：' )
    for item in tr4w.get_keywords(20, word_min_len=1):
    #     print(item.word, item.weight)
#         print(item.word)
        
        news_keywords.append(cc.convert(item.word))

    print()
    # print( '關鍵短語：' )
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
#         print(phrase)

        news_phrase.append(cc.convert(phrase))


    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    print()
    # print( '摘要：' )
    abstracts=[]
    for item in tr4s.get_key_sentences(num=5):
    #     print(item.index, item.weight, item.sentence)
#         print(item.sentence)
        abstracts.append(item.sentence)
        
    cc = OpenCC('s2twp')
    for i in range(0,len(abstracts)):
    #     print(i)
        abstracts[i] = re.sub('[\「\」\）\（\}\{\,\'\"\▼\▲]', '', cc.convert(abstracts[i]))
    # abstracts
    
#     for abstract in abstracts:
# #         print(abstract)
# #         print()
    try:
        return json.dumps({'news_keywords':news_keywords, 'news_phrase':news_phrase, 'news_sentence':abstracts}, 
                  ensure_ascii=False).encode()
    except:
        return json.dumps({'news_keywords':"null", 'news_phrase':"null", 'news_sentence':"null"}, 
                  ensure_ascii=False).encode()

#============#============#============#============#============#============#============#============#============#============



#============#============#============#============#============#============#============#============#============#============
filename = "Gossiping-39285-39385.json"

def getkeywords(num):
    # load ptt posts

    with open(filename,encoding = 'utf8') as f:
        posts = json.load(f)
    #     print(posts)
    titles=""
    for post in posts["articles"]:
    #     print(post["article_title"])
        title_tmp = post["article_title"]

    #     title_tmp = pattern.findall(title_tmp)
    #     if( title_tmp[0][1] == " "):
    #         title_tmp[0] = title_tmp[0][1:].lstrip();
    #     print(title_tmp[0])


        try:
    #         print(title_tmp.split("] ")[1])
            titles+=title_tmp.split("] ")[1].replace('"',' ')+" \n"
        except:
            try:
    #             print(title_tmp.split("］ ")[1])
                titles+=title_tmp.split("］ ")[1].replace('"',' ')+" \n"
            except:
                try:
    #                 print(title_tmp.split("]")[1])
                    titles+=title_tmp.split("]")[1].replace('"',' ')+" \n"
                except:
                    try:
    #                     print(title_tmp.split("］")[1])
                        titles+=title_tmp.split("］")[1].replace('"',' ')+" \n"
                    except:
    #                     print(title_tmp)
                        titles+=title_tmp.replace('"',' ')+" \n"
    from opencc import OpenCC
    cc = OpenCC('tw2sp')  # convert from Simplified Chinese to Traditional Chinese
    # can also set conversion by calling set_conversion
    # cc.set_conversion('s2tw')
    Simplified = cc.convert(titles)
    # print(Simplified)
    jieba.analyse.set_stop_words('stopwords.txt')
    jieba.add_word('柯文哲')
    jieba.add_word('叶克膜')
    jieba.add_word('黄士修')
    jieba.add_word('林佳龙')
    cc = OpenCC('s2twp')
    result = ''.join(i for i in Simplified if not i.isdigit()) #去除數字
    tags = jieba.analyse.extract_tags(result,
                                      topK=num,
                                      withWeight=True
                                     )
    keywords = []
    for tag, weight in tags:
        keywords.append(cc.convert(tag))
#         print(cc.convert(tag) + "," + str(weight))
    return keywords

#============#============#============#============#============#============#============#============#============#============


#取得最新頁數
def getlastpage():
    url="https://www.ptt.cc/bbs/Gossiping/index.html"
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    r=requests.get(url=url,headers=headers, cookies={'over18': '1'})
    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        stories = soup.select("a.btn.wide")
        for s in stories:
            if (s.text == "‹ 上頁"):
                return (s.get('href')) #/bbs/Gossiping/index39048.html


Crawler_flag = 0


def packJsonReturn(retCode=0, retMsg='ok', retData=None):
    return json.dumps({'Crawler_flag':Crawler_flag,'retCode':retCode, 'retMsg':retMsg, 'retData':retData}, 
                      ensure_ascii=False).encode()

def keywords(number):
    keywords = getkeywords(int(number))
    return packJsonReturn(0, 'ok', keywords)

def CrawlerThread(page):

    lastpage = getlastpage()[20:25]
#     page = 3
#     filename = "Gossiping-39285-39385.json"
    cmd  = subprocess.getoutput("python ptt-web-crawler/PttWebCrawler/crawler.py -b Gossiping -i "+ str(int(lastpage) - int(page)) +" "+ str(lastpage))
    # os.system("python test.py")
    if cmd == "end Crawler":
        global filename 
        filename = "Gossiping-"+str(int(lastpage) - int(page))+"-"+str(lastpage)+".json"
        print("爬蟲結束...好累好累")
    print(cmd)
    print(filename)
    global Crawler_flag 
    Crawler_flag = 0



# host = '172.22.100.200'
host = "127.0.0.1"
port = 81
        

class TwoWayClient(object):
    def on_event(self, event):
        print ("event",event)
        
    def connect(self, event):
        print ("connect",event)
        self.socketio.emit('handshake1', "001")

    def handshake2(self, event):
        print ("handshake2",event)
        self.socketio.emit('service', "401")

    # def getkeywords(self, num):
    #     print ("getkeywords",getkeywords(int(num)))
    #     # self.socketio.emit('service', getkeywords(int(num)))
    #     self.socketio.emit('801', getkeywords(int(num)))

    def getkeywords(self, num):
        print ("getkeywords",get_new_ptt_keywords())
        # self.socketio.emit('service', getkeywords(int(num)))
        self.socketio.emit('801', get_new_ptt_keywords())
        
    def Crawler(self, event):
        print ("Crawler",event)
        print ("開始爬蟲......")
        
        global Crawler_flag
        Crawler_flag = 1
        thr = Thread(target=CrawlerThread, args=[event])
        thr.start()

        
        
    def showfilename(self, event): 
        # global Crawler_flag
        # global filename 
        global filename_new
        # print ("showfilename",filename)
        print ("showfilename",filename_new)

        # self.socketio.emit('service', filename)
        # self.socketio.emit('803', filename)
        self.socketio.emit('803', filename_new)


 
    def CrawlerFlag(self, event):
        global Crawler_flag
        print ("CrawlerFlag",event,Crawler_flag)
        # self.socketio.emit('service', Crawler_flag)
        self.socketio.emit('804', Crawler_flag)

        

    def get_news(self, keywords):
        print ("get_news",keywords)
        print ("對新聞爬蟲＆分析中 請稍等")
        
        # self.socketio.emit('service', get_news_content(keywords).decode('utf-8'))
        self.socketio.emit('805', get_news_content(keywords).decode('utf-8'))
    
    def get_google(self, keywords):
        print ("get_google",keywords)
        print ("查詢google中")
        self.socketio.emit('806', google_serach(keywords))



    def ptt_Crawler(self,keywords):
        print ("ptt爬蟲開始")
        global Crawler_flag
        if (Crawler_flag == 1):
            print("已經在爬蟲了")
        else:
            ptt_run()  








    def __init__(self):
#         while(1):
#             try:
#                 print("connecting SocketIO server")
#                 socket = SocketIO(host, port, wait_for_connection=False)
#                 print("connect success")
# #                 socket.wait()
#             except:
#                 print('The server is down. Try again later.')
#                 time.sleep(5) 
        print("connect")
        
        self.socketio = SocketIO(host, port)
        self.socketio.on('events', self.on_event)

        self.socketio.on('connect', self.connect)            
        self.socketio.emit('handshake1', "001")
        self.socketio.on('handshake2', self.handshake2)  
        self.socketio.on('service', self.on_event)  
        
        self.socketio.on('801', self.getkeywords)
        #self.socketio.on('802', self.Crawler)
        self.socketio.on('802', self.ptt_Crawler)


        self.socketio.on('803', self.showfilename)
        self.socketio.on('804', self.CrawlerFlag)
        self.socketio.on('805', self.get_news)
        self.socketio.on('806', self.get_google)

        
#         self.socketio.emit('service', getkeywords(10))
        self.receive_events_thread = Thread(target=self._receive_events_thread)
        self.receive_events_thread.daemon = True
        self.receive_events_thread.start()

        while True:
            some_input = input()
            if (some_input == "802"):
                ptt_run()
                global Crawler_flag
                Crawler_flag = 1
            self.socketio.emit('service', some_input)
            

    def _receive_events_thread(self):

        self.socketio.wait()


def main():
    error_con = 0
    while(error_con<10):
        try:
            TwoWayClient()
            print("程式出錯誤 嘗試重新啟動")
        except:
#             TwoWayClient()
            error_con+=1
            time.sleep(5)
    


if __name__ == "__main__":
    main()
