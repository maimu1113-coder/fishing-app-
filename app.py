import os
import feedparser
from flask import Flask, render_template_string

app = Flask(__name__)

RESOURCES = [
    {'cat': 'maker', 'name': 'シマノ', 'url': 'https://fish.shimano.com/ja-JP/news/news-list/jcr:content/root/main/section/news_list.rss'},
    {'cat': 'maker', 'name': 'ダイワ', 'url': 'https://www.daiwa.com/jp/news.xml'},
    {'cat': 'maker', 'name': 'ジャッカル', 'url': 'https://www.jackall.co.jp/bass/feed/'},
    {'cat': 'maker', 'name': 'メジャークラフト', 'url': 'https://www.majorcraft.co.jp/feed'},
    {'cat': 'maker', 'name': 'がまかつ', 'url': 'https://www.gamakatsu.co.jp/feed/'},
    {'cat': 'maker', 'name': 'エバーグリーン', 'url': 'https://www.evergreen-fishing.com/feed'},
    {'cat': 'maker', 'name': 'DUO', 'url': 'https://www.duo-inc.co.jp/feed/'},
    {'cat': 'maker', 'name': 'アブガルシア', 'url': 'https://www.purefishing.jp/product/abugarcia/feed'},
    {'cat': 'shop', 'name': 'TSURINEWS', 'url': 'https://tsurinews.jp/feed/'},
    {'cat': 'shop', 'name': 'ルアマガ', 'url': 'https://plus.luremaga.jp/feed/'}
]

@app.route('/')
def index():
    maker_news, shop_news = [], []
    for res in RESOURCES:
        try:
            feed = feedparser.parse(res['url'])
            for entry in feed.entries[:5]:
                item = {'title': f"【{res['name']}】 {entry.title}", 'link': entry.link, 'date': entry.get('published', '')}
                if res['cat'] == 'maker': maker_news.append(item)
                else: shop_news.append(item)
        except: continue
    
    return render_template_string("""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    body { font-family: sans-serif; background: #000c1d; color: white; padding-bottom: 70px; margin: 0; }
    header { background: #001a33; padding: 15px; text-align: center; border-bottom: 2px solid #00aaff; position: sticky; top: 0; z-index: 100; }
    .card { background: #162435; padding: 15px; margin: 10px; border-radius: 10px; border-left: 5px solid #00aaff; }
    a { text-decoration: none; color: #fff; font-weight: bold; display: block; }
    small { color: #00d4ff; display: block; margin-top: 5px; }
    .tab-bar { position: fixed; bottom: 0; width: 100%; background: #001a33; display: flex; border-top: 2px solid #00aaff; }
    .tab { flex: 1; padding: 15px; text-align: center; cursor: pointer; font-weight: bold; }
    .tab.active { background: #00aaff; color: #001a33; }
    .content { display: none; } .content.active { display: block; }
</style></head><body>
    <header><h3>釣具速報アプリ</h3></header>
    <div id="maker" class="content active">{% for item in maker_news %}<div class="card"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a><small>{{ item.date }}</small></div>{% endfor %}</div>
    <div id="shop" class="content">{% for item in shop_news %}<div class="card"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a><small>{{ item.date }}</small></div>{% endfor %}</div>
    <div class="tab-bar"><div class="tab active" onclick="showTab('maker', this)">メーカー</div><div class="tab" onclick="showTab('shop', this)">ショップ</div></div>
    <script>function showTab(id, el) { document.querySelectorAll(".content").forEach(c => c.classList.remove("active")); document.querySelectorAll(".tab").forEach(t => t.classList.remove("active")); document.getElementById(id).classList.add("active"); el.classList.add("active"); window.scrollTo(0,0); }</script>
</body></html>
""", maker_news=maker_news, shop_news=shop_news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
