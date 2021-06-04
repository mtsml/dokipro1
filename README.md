# dokipro1 せる子
![せる子のロゴ](https://user-images.githubusercontent.com/50922910/120804412-95392200-c57f-11eb-9b7a-e3c453009a97.png)

せる子は会話といくつかのお役立ち機能をお届けするLINE Botです。

![せる子のデモ](https://user-images.githubusercontent.com/50922910/120806555-f661f500-c581-11eb-9050-bb3df5ecfc60.gif)

せる子にできること

- 会話をする
- テクノロジーニュースをお知らせする
- 今日の運勢を占う
- 競馬の結果を予想する

## 使い方
LINEで友達登録をすることで簡単に使いはじめることができます。

**！現在アクセス数制限のためIDは公開していません。**

## 構成図
![せる子の構成図](https://user-images.githubusercontent.com/50922910/120809987-98371100-c585-11eb-9272-ce53c29bc319.png)

### Heroku
本リポジトリのコードがHeroku上にデプロイされており、LINEからのアクションを処理する中核部分です。必要に応じて外部のサービスを呼び出します。

### DynamoDB
ユーザーID、会話回数や親密度といった情報を蓄積します。

### A3RT
ユーザーの会話に対する返答メッセージを生成します。

### mtsml/keiba
競馬の予想結果を提供するAPIを作成する予定です。

## 参考
- [LINE Messeaging API リファレンス](https://developers.line.biz/ja/reference/messaging-api/)
- [Flex Message Simulator](https://developers.line.biz/flex-simulator/?status=success)
- [LINE Messaging API SDK for Python](https://github.com/line/line-bot-sdk-python)
- [TalkAPI | PRODUCT | A3RT](https://a3rt.recruit-tech.co.jp/product/talkAPI/)
- [DynamoDB CRUD処理](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html#GettingStarted.Python.03.03)