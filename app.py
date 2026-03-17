import os
import feedparser
from flask import Flask, render_template_string

app = Flask(__name__)

# ★BlueBlue、deps、ガンクラフト、ヤマガブランクス等を追加しました！
RESOURCES = [
    # メーカー（ソルト・バス混在）
    {'cat': 'maker', 'name': 'BlueBlue', 'url': 'https://www.bluebluefishing.com/rss'},
    {'cat': 'maker', 'name': 'SHIMANO', 'url': 'https://fish.shimano.com/ja-JP/news/news-list/jcr:content/root/main/section/news_list.rss'},
    {'cat': 'maker', 'name': 'DAIWA', 'url': 'https://www.daiwa.com/jp/news.xml'},
    {'cat': 'maker', 'name': 'deps', 'url': 'https://www.depsweb.co.jp/feed/'},
    {'cat': 'maker', 'name': 'JACKALL', 'url': 'https://www.jackall.co.jp/bass/feed/'},
    {'cat': 'maker', 'name': 'Megabass', 'url': 'https://www.megabass.co.jp/site/feed/'},
    {'cat': 'maker', 'name': 'GAN CRAFT', 'url': 'https://gancraft.com/feed/'},
    {'cat': 'maker', 'name': 'YAMAGA Blanks', 'url': 'https://yamaga-blanks.com/feed/'},
    {'cat': 'maker', 'name': 'MajorCraft', 'url': 'https://www.majorcraft.co.jp/feed'},
    {'cat': 'maker', 'name': 'がまかつ', 'url': 'https://www.gamakatsu.co.jp/feed/'},
    {'cat': 'maker', 'name': 'EverGreen', 'url': 'https://www.evergreen-fishing.com/feed'},
    {'cat': 'maker', 'name': 'DUO', 'url': 'https://www.duo-inc.co.jp/feed/'},
    {'cat': 'maker', 'name': 'AbuGarcia', 'url': 'https://www.purefishing.jp/product/abugarcia/feed'},
    {'cat': 'maker', 'name': 'RAID JAPAN', 'url': 'http://raidjapan.com/?feed=rss2'},
    {'cat': 'maker', 'name': 'O.S.P', 'url': 'https://www.osp-lures.com/feed/'},
    {'cat': 'maker', 'name': 'issei', 'url': 'https://issei.tv/feed'},
    {'cat': 'maker', 'name': 'Nories', 'url': 'https://www.nories.com/feed'},
    {'cat': 'maker', 'name': 'Smith', 'url': 'https://www.smith.jp/feed'},
    {'cat': 'maker', 'name': 'APIA', 'url': 'https://www.apiajapan.com/news/index.xml'},
    
    # ニュース・ショップ
    {'cat': 'shop', 'name': 'TSURINEWS', 'url': 'https://tsurinews.jp/feed/'},
    {'cat': 'shop', 'name': 'ルアマガプラス', 'url': 'https://plus.luremaga.jp/feed/'},
    {'cat': 'shop', 'name': '釣果の窓', 'url': 'https://choka-win.com/feed/'},
    {'cat': 'shop', 'name': '釣りの総合ニュース', 'url': 'https://www.fishing-v.jp/news/rss.php'}
]

@app.route('/')
def index():
    maker_news, shop_news = [], []
    for res in RESOURCES:
        try:
            feed = feedparser.parse(res['url'])
            # ニュースがないメーカーを飛ばすための処理
            if not feed.entries: continue
            for entry in feed.entries[:3]:
                date = entry.get('published', '')[:16]
                item = {'title': entry.title, 'source': res['name'], 'link': entry.link, 'date': date}
                if res['cat'] == 'maker': maker_news.append(item)
                else: shop_news.append(item)
        except: continue

    return render_template_string("""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FISHING NEWS PRO</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-color: #050a0f;
            --card-bg: #111a24;
            --accent-color: #00f2ff;
            --text-main: #f0f5f9;
            --text-sub: #8b9eb0;
        }
        body {
            font-family: 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding-bottom: 90px;
        }
        header {
            background: rgba(5, 10, 15, 0.9);
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid var(--accent-color);
            position: sticky; top: 0; z-index: 100;
            backdrop-filter: blur(15px);
        }
        header h1 {
            margin: 0; font-size: 1.3rem; letter-spacing: 3px; color: var(--accent-color);
            font-style: italic; text-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
        }
        .container { padding: 15px; max-width: 650px; margin: auto; }
        .card {
            background: var(--card-bg);
            margin-bottom: 15px;
            padding: 18px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
            border: 1px solid rgba(0, 242, 255, 0.1);
        }
        .card a { text-decoration: none; color: var(--text-main); font-size: 1rem; font-weight: 600; line-height: 1.5; display: block; }
        .info { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
        .source-tag { 
            background: linear-gradient(90deg, #00f2ff, #0072ff); 
            color: #000; padding: 3px 10px; border-radius: 50px; font-size: 0.7rem; font-weight: 800;
        }
        .date-text { font-size: 0.75rem; color: var(--text-sub); }
        
        .tab-bar {
            position: fixed; bottom: 0; width: 100%; height: 75px;
            background: rgba(5, 10, 15, 0.95);
            display: flex; justify-content: space-around; align-items: center;
            border-top: 1px solid rgba(0, 242, 255, 0.3); backdrop-filter: blur(15px);
        }
        .tab {
            text-align: center; color: var(--text-sub); flex: 1; transition: 0.3s;
            font-size: 0.75rem;
        }
        .tab i { font-size: 1.4rem; display: block; margin-bottom: 5px; }
        .tab.active { color: var(--accent-color); transform: translateY(-5px); }

        .content { display: none; animation: slideUp 0.4s ease; }
        .content.active { display: block; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <header><h1><i class="fas fa-water"></i> FISHING PRO</h1></header>
    
    <div class="container">
        <div id="maker" class="content active">
            {% for item in maker_news %}
            <div class="card">
                <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
                <div class="info">
                    <span class="source-tag">{{ item.source }}</span>
                    <span class="date-text">{{ item.date }}</span>
                </div>
            </div>
            {% endfor %}
        </div>

        <div id="shop" class="content">
            {% for item in shop_news %}
            <div class="card">
                <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
                <div class="info">
                    <span class="source-tag">{{ item.source }}</span>
                    <span class="date-text">{{ item.date }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="tab-bar">
        <div class="tab active" id="tab-maker" onclick="showTab('maker')">
            <i class="fas fa-tools"></i>メーカー
        </div>
        <div class="tab" id="tab-shop" onclick="showTab('shop')">
            <i class="fas fa-rss"></i>ニュース
        </div>
    </div>

    <script>
        function showTab(id) {
            document.querySelectorAll(".content").forEach(c => c.classList.remove("active"));
            document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
            document.getElementById(id).classList.add("active");
            if(id === 'maker') document.getElementById('tab-maker').classList.add("active");
            else document.getElementById('tab-shop').classList.add("active");
            window.scrollTo(0,0);
        }
    </script>
</body>
</html>
""", maker_news=maker_news, shop_news=shop_news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
