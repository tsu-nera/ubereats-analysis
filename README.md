# UberEats Analysis

[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/tsu-nera/ubereats-analysis)

- Python 3.7
- Scrapy 1.8
- [See more details at env.yaml(anaconda config file)](https://github.com/tsu-nera/ubereats-analysis/blob/master/env.yaml)

## 概要

武蔵中原のウーバーイーツ加盟店の情報を収集して分析するためリポジトリです。

メンテナンスが大変なので、武蔵中原以外の地域は私の気まぐれで分析します。全国とか、とても対応できません。
このプロジェクトはオープンソースでコードを公開しているので、武蔵中原以外の地域はぜひ仲間になってプロジェクトにコントリビューションしてください！

## データ分析(EDA)

https://github.com/tsu-nera/ubereats-analysis/blob/master/notebooks/shop_analysis.ipynb

## 武蔵中原ウーバーマップ

https://drive.google.com/open?id=1Lt-zlVv4_A1y5v58Efbh9AsFg5Gw8X9q&usp=sharing

## Usage

タスクランナーに [invoke](http://www.pyinvoke.org/)を使用している。

### 店舗情報の取得

武蔵中原駅近辺の店舗情報を`www.ubereats.com`からスクレイピング。 `rawdata/shops`に CSV 形式で保存される。

```
$ inv crawl
```

主な取得項目は、以下のとおり。

- 店名
- レビュー数
- 評価
- 郵便番号
- 住所
- 店舗 URL
- 緯度
- 経度
- 開始時刻
- 終了時刻

人気のチェーン店ほど、検索結果に表示されないことがよくあるため、その場合は個別に取得する。 `rawdata/shops/shop.csv`に 1 レコードが吐き出される。

```
$ inv post [url]
```

### 配達ログの取得

個人の配達ログを`partners.uber.com`から取得。

ログイン認証が必要。 [pit](https://github.com/samzhang111/pit)をつかって UserId とパスワードを外部ファイルから読み出して利用している。 `~/.pit/default.yaml`を作成して、以下を追記する。

```yaml
uber_auth:
  userId: [xxx]
  password: [xxx]
```

日付を引数として渡して、以下でスクリプトを走らせる。 `rawdata/trips`配下にCSVとして出力される。

```
$ inv trip [year] [month] [day]
```

主な取得項目は、以下のとおり。

* 日時
* 曜日
* 時間
* 距離
* ピックアップ時刻
* ピックアップ場所
* 到着時刻
* 支払い額

公開情報以外は、GitHub にデータをアップロードしてはいけない。特にドロップ先の情報は絶対にGitHub にアップロードしてはいけない。

## Authors

[@tsu-nera](https://twitter.com/tsu_nera)
