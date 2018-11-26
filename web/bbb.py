from flask import Flask,request
from flask import render_template

import requests
from bs4 import BeautifulSoup
import datetime
import random
color_arr=["#FF0F00","#FF6600","#FF9E01","#FCD202","#F8FF01","#B0DE09","#04D215","#0D8ECF","#0D52D1","#2A0CD0","#8A0CCF","#CD0D74"]
# random.shuffle(color_arr)

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])

def index():
    today = datetime.date.today()
    date = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
    keyword = "選舉"


    
    if request.method == 'POST': 
        keyword = request.values['serach']
        print(keyword)
        url="http://learn.iis.sinica.edu.tw:9187/api/sentiment?keyword="+keyword+"&startDate=2018-10-16&endDate="+date+"&wholePost=1"

        headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        r=requests.get(url=url,headers=headers)

        moods=r.json()
        happy=0
        unhappy=0
        happy_json=[]
        unhappy_json=[]
        total=0


        for mood in moods["data"]:
            total+=mood["freq"]
        
        for mood in moods["data"]:
            if mood["type"]=="pos":
                happy+=mood["freq"]
        #         print(mood)
                happy_json.append({"y": mood["freq"],"label": mood["sentiment"]})
            else:
                unhappy+=mood["freq"]
                unhappy_json.append({"y": mood["freq"],"label": mood["sentiment"]})

        if(happy + unhappy!=0):
            happy_percent = happy/(happy+unhappy)*100
        else:
            happy_percent = 0
        # unhappy_percent = unhappy/(happy+unhappy)*100

        # mood_json={"happy":int(happy_percent)},{"unhappy":int(unhappy_percent)}
        # mood_json=int(happy_percent)
        # print(int(happy_percent),100-int(happy_percent))





        url="http://learn.iis.sinica.edu.tw:9187/api/theme?startDate=2018-10-19&endDate="+date+"&keyword="+keyword+"&type=noun&termType=events"
        headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        r=requests.get(url=url,headers=headers)

        events = r.json()

        event=[]
        # for i in range(0,10 if len(events)>10 else len(events)):
        #     event.append(events[i])
        for i in range(0,10 if len(events)>10 else len(events)):
            event.append({"y": events[i]["freq"],"label": events[i]["term"]})


        url="http://learn.iis.sinica.edu.tw:9187/api/theme?startDate=2018-10-19&endDate="+date+"&keyword="+keyword+"&type=noun&termType=active"
        r=requests.get(url=url,headers=headers)
        actives = r.json()
        active=[]
        # for i in range(0,10 if len(actives)>10 else len(actives)):
        #     active.append(actives[i])
        for i in range(0,10 if len(actives)>10 else len(actives)):
            active.append({"y": actives[i]["freq"],"label": actives[i]["term"]})  


        url="http://learn.iis.sinica.edu.tw:9187/api/theme?startDate=2018-10-19&endDate="+date+"&keyword="+keyword+"&type=noun&termType=passive"
        r=requests.get(url=url,headers=headers)
        passives = r.json()
        passive=[]
        random.shuffle(color_arr)

        for i in range(0,10 if len(passives)>10 else len(passives)):
            # passive.append(passives[i])
            passive.append({'term': passives[i]["term"], 'freq': passives[i]["freq"],"color":color_arr[i]})        


        url="http://learn.iis.sinica.edu.tw:9187/api/theme?startDate=2018-10-19&endDate="+date+"&keyword="+keyword+"&type=noun&termType=adj"
        r=requests.get(url=url,headers=headers)
        adjs = r.json()
        adj=[]
        random.shuffle(color_arr)

        for i in range(0,10 if len(adjs)>10 else len(adjs) ):
            # adj.append(adjs[i])
            adj.append({'term': adjs[i]["term"], 'freq': adjs[i]["freq"],"color":color_arr[i]})    


        url="http://learn.iis.sinica.edu.tw:9187/api/time?startDate=2018-10-16&endDate="+date+"&keyword="+keyword+"&type=noun"
        headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        r=requests.get(url=url,headers=headers)
        sorc = r.json()
        tmpdate=""
        tmpnum=0
        new_source=[]
        total_news=0
        for source in sorc["data"]:
            total_news+=source["freq"]
            if(source["date"]!=tmpdate):
                tmpdate = source["date"]
                tmpnum+=source["freq"]
            else:
                tmpdate = source["date"]
                tmpnum+=source["freq"]
                new_source.append({'date':tmpdate , 'source': 'news', 'freq': tmpnum})
                tmpnum=0
    else:

        happy_json=[{'y': 115, 'label': '滿意'},
            {'y': 314, 'label': '喜歡'},
            {'y': 1151, 'label': '注意'},
            {'y': 237, 'label': '喜悅'},
            {'y': 90, 'label': '安心'},
            {'y': 208, 'label': '敬佩'},
            {'y': 10, 'label': '羨慕'},
            {'y': 1060, 'label': '同意'},
            {'y': 13, 'label': '無愧'},
            {'y': 31, 'label': '感激'},
            {'y': 14, 'label': '忠孝'},
            {'y': 19, 'label': '思念'},
            {'y': 14, 'label': '沒羞'}]

        unhappy_json=[{'y': 96, 'label': '惋惜'},
            {'y': 153, 'label': '悲哀'},
            {'y': 20, 'label': '懊悔'},
            {'y': 38, 'label': '仇恨'},
            {'y': 8, 'label': '憐憫'},
            {'y': 132, 'label': '厭惡'},
            {'y': 125, 'label': '驚奇'},
            {'y': 225, 'label': '不滿'},
            {'y': 7, 'label': '憂愁'},
            {'y': 12, 'label': '木然'},
            {'y': 51, 'label': '原諒'},
            {'y': 200, 'label': '不安'},
            {'y': 66, 'label': '為難'},
            {'y': 240, 'label': '害怕'},
            {'y': 94, 'label': '懷疑'},
            {'y': 99, 'label': '生氣'},
            {'y': 330, 'label': '輕視'},
            {'y': 57, 'label': '埋怨'},
            {'y': 69, 'label': '失望'},
            {'y': 43, 'label': '灰心'},
            {'y': 26, 'label': '煩惱'},
            {'y': 17, 'label': '羞愧'},
            {'y': 341, 'label': '著急'},
            {'y': 30, 'label': '抱歉'}]

        happy_percent=87

        event=[{'y': 34, 'label': '進入 階段'},
            {'y': 5, 'label': '新 民調'},
            {'y': 4, 'label': '罷免 投票日'},
            {'y': 4, 'label': '邁入 階段'},
            {'y': 3, 'label': '牽動 發展'},
            {'y': 3, 'label': '原有 人'},
            {'y': 3, 'label': '選到 大家'},
            {'y': 3, 'label': '有 挑戰'},
            {'y': 3, 'label': '讓 政治家 敢'},
            {'y': 3, 'label': '有 特殊性'}]

        active=[{'y': 71, 'label': '進入'},
            {'y': 45, 'label': '倒數'},
            {'y': 38, 'label': '有'},
            {'y': 32, 'label': '登場'},
            {'y': 30, 'label': '舉行'},
            {'y': 22, 'label': '到'},
            {'y': 18, 'label': '在即'},
            {'y': 18, 'label': '結束'},
            {'y': 17, 'label': '投票'},
            {'y': 14, 'label': '新'}]

        passive=[{'term': '是', 'freq': 114, 'color': '#2A0CD0'},
            {'term': '介入', 'freq': 99, 'color': '#FF9E01'},
            {'term': '投入', 'freq': 44, 'color': '#04D215'},
            {'term': '影響', 'freq': 39, 'color': '#F8FF01'},
            {'term': '干預', 'freq': 36, 'color': '#8A0CCF'},
            {'term': '進行', 'freq': 30, 'color': '#FF6600'},
            {'term': '為', 'freq': 27, 'color': '#B0DE09'},
            {'term': '讓', 'freq': 27, 'color': '#CD0D74'},
            {'term': '舉行', 'freq': 26, 'color': '#0D52D1'},
            {'term': '有', 'freq': 24, 'color': '#FF0F00'}]

        adj=[{'term': '期中', 'freq': 611, 'color': '#FCD202'},
            {'term': '美國', 'freq': 273, 'color': '#8A0CCF'},
            {'term': '合一', 'freq': 244, 'color': '#FF0F00'},
            {'term': '九', 'freq': 226, 'color': '#0D52D1'},
            {'term': '這次', 'freq': 170, 'color': '#F8FF01'},
            {'term': '市長', 'freq': 167, 'color': '#0D8ECF'},
            {'term': '台灣', 'freq': 136, 'color': '#2A0CD0'},
            {'term': '地方', 'freq': 128, 'color': '#FF6600'},
            {'term': '年底', 'freq': 123, 'color': '#04D215'},
            {'term': '高雄', 'freq': 88, 'color': '#CD0D74'}]

        new_source=[{'date': '2018-10-16T00:00:00.000Z', 'source': 'news', 'freq': 423},
            {'date': '2018-10-17T00:00:00.000Z', 'source': 'news', 'freq': 153},
            {'date': '2018-10-18T00:00:00.000Z', 'source': 'news', 'freq': 206},
            {'date': '2018-10-19T00:00:00.000Z', 'source': 'news', 'freq': 147},
            {'date': '2018-10-20T00:00:00.000Z', 'source': 'news', 'freq': 339},
            {'date': '2018-10-21T00:00:00.000Z', 'source': 'news', 'freq': 207},
            {'date': '2018-10-22T00:00:00.000Z', 'source': 'news', 'freq': 336},
            {'date': '2018-10-23T00:00:00.000Z', 'source': 'news', 'freq': 358},
            {'date': '2018-10-24T00:00:00.000Z', 'source': 'news', 'freq': 415},
            {'date': '2018-10-25T00:00:00.000Z', 'source': 'news', 'freq': 369},
            {'date': '2018-10-26T00:00:00.000Z', 'source': 'news', 'freq': 319},
            {'date': '2018-10-27T00:00:00.000Z', 'source': 'news', 'freq': 222},
            {'date': '2018-10-28T00:00:00.000Z', 'source': 'news', 'freq': 285},
            {'date': '2018-10-29T00:00:00.000Z', 'source': 'news', 'freq': 306},
            {'date': '2018-10-30T00:00:00.000Z', 'source': 'news', 'freq': 379},
            {'date': '2018-10-31T00:00:00.000Z', 'source': 'news', 'freq': 416},
            {'date': '2018-11-01T00:00:00.000Z', 'source': 'news', 'freq': 499},
            {'date': '2018-11-02T00:00:00.000Z', 'source': 'news', 'freq': 637},
            {'date': '2018-11-03T00:00:00.000Z', 'source': 'news', 'freq': 383},
            {'date': '2018-11-04T00:00:00.000Z', 'source': 'news', 'freq': 358},
            {'date': '2018-11-05T00:00:00.000Z', 'source': 'news', 'freq': 628},
            {'date': '2018-11-06T00:00:00.000Z', 'source': 'news', 'freq': 986},
            {'date': '2018-11-07T00:00:00.000Z', 'source': 'news', 'freq': 852},
            {'date': '2018-11-09T00:00:00.000Z', 'source': 'news', 'freq': 556}]
        total_news = 9478

    
    
    
    return render_template('Admin/index.html', happy_json=happy_json,unhappy_json=unhappy_json,happy=int(happy_percent),events_json=event,active_json=active,passive_json=passive,adj_json=adj,news_json=new_source,total_news=total_news)

if __name__ == '__main__':
    app.debut = True
    app.run()