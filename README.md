# タイタニック問題の予測アプリ

## 使用技術
### フロントエンド
- Vue 3.5.13
    - axios 1.8.3
- Vite 6.2.0
    - TypeScript 5.7.2
    - tailwindcss 4.0.14
    - daisyui 5.0.4

### バックエンド
- FastAPI 0.115.11
    - numpy 2.2.3
    - lightgbm 4.6.0
- uvicorn 0.34.0

### その他
- Docker

## 概要
Vue3とFastAPIを使用し、lightgbmベースでタイタニック問題の生存率を推定できるアプリです。

## 再現手順
1. 仮想環境の立ち上げ
    -  `docker-compose up --build`
2. フロントエンド側の処理
    -  `docker-compose exec node bash`
    -  `cd tutorial`
    -  `yarn`
    -  `yarn dev`
3. バックエンド側の処理
    - 特に処理は不要だと思います(一応 コンテナに入るコマンドです)
    -  `docker-compose exec python bash`

## アプリの操作方法
階級、性別、年齢、兄弟姉妹の同伴数、親子の同伴数、運賃の6つの項目を選択し、生存率推定を行えば生存率が表示されます。

<img width="440" alt="26歳男性労働者階級ぼっちの場合" src="https://github.com/user-attachments/assets/5048b4e9-9749-4dff-87a8-36feba19e096" />

### 操作中のGIF
![FastAPIとVueの機械学習アプリ](https://github.com/user-attachments/assets/6cfe634c-b476-4d3d-ab96-8290685a597f)



## 参考文献
- Vue.js FastAPI によるAIアプリ開発入門
- https://zenn.dev/joanofarc/books/085bbef9ea7323
