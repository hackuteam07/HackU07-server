from re import U
from flask import Flask, jsonify
import os
import main
import asyncio
import scrapeNews
import json
import codecs

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/collect')
async def collect():
    await scrapeNews.main()
    json_data = json.load(open("articleList.json", "r"))
    articleList = []
    for news in json_data:
        title = news["title"]
        text = news["text"]
        url = news["url"]
        score = await main.predict(title, text)
        articleList.append({"title":title,"url":url, "score": score})
    articleListJson = json.dumps(articleList,ensure_ascii=False )
    fileName = "article_with_score_list.json"
    file = codecs.open(fileName, 'w','utf-8')
    file.write(articleListJson)
    return articleListJson
    

@app.route('/')
async def provide():
    if os.path.isfile("article_with_score_list.json"):
        json_data = json.load(open("article_with_score_list.json", "r", encoding='utf-8'))
        return jsonify(json_data)
    else:
        await collect()
        json_data = json.load(open("article_with_score_list.json", "r", encoding='utf-8'))
        return jsonify(json_data)


# this is previous version 6/23
# async def run_model():
#     # モデルを動かすmain.pyを実行
#     print("Start ...")
#     data = await main.predict()
#     return data

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
