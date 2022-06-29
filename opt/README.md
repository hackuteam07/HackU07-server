# HackU07-サーバー

利用サービス:GCP Run<br>
エンドポイント： https://[参加したイベント名、ヒント:lowercase]7-server-web-zszjj7cu4q-an.a.run.app <br>
region: asia -northeneast01 <br>
CPU: 4 <br>
Memory: 8GB <br>
同時リクエスト数: 10 <br>
リクエストタイムアウト: 300sec <br>
(体感ですがモバイルで使うエンドポイントは2秒弱で帰ってきます、時間が空くとインスタンス生成に10秒くらい＋になります)

## 手順
### ローカル <br>
1: トップディレクトリにてイメージ作成（dockerが立ち上がっていること）
```
$ docker build -t omlette-server .
```
2: ビルド
```
$ docker run -e PORT=8080 -p 8080:8080 omlette-server
```
3: ```localhost:8080``` で確認。スクレイピング＆ML実行は``` localhost:8080/collect```<br>
curl の使用推奨です。(8080ではapplication_jsonで返しているのでブラウザのhtml形式では文字化けします)
### GCP
1: GCP Consoleにログイン（または新規登録）<br>
2: 新規プロジェクト作成 <br>
3: GCP Runの使用をオンにする<br>
4: gcloud sdk のインストール<br>
5: 各種設定（ログイン、プロジェクト移動まで済ませる）<br>
6: ローカルで作成したイメージにタグをつけてGCPにあげる（M1では異なるコマンドでビルドしないといけない、[詳しくは](https://qiita.com/Aruga0918/items/de98169a07b1f61a54ef)）<br>
```
$ docker tag omlette-server asia.gcr.io/[プロジェクトID]/omlette-server:latest 
```

7: プッシュ
```
$ docker push asia.gcr.io/hackuomletteserver/omlette-server:latest 
```
8: GCP Runの画面に行きお好きなように設定、コンテナイメージが選択できるので先ほどプッシュしたものを選ぶ（CPU: 4、メモリ8GBがおすすめです）
