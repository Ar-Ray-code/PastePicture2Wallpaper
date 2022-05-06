# PastePicture2Wallpaper

キャラクターをUbuntu風の壁紙に貼り付けるプログラム。

![](./images_for_readme/urara-ubuntu-wallpaper.jpg)

## 1. 画像をColabで深度画像に変換する

Midasを用いて画像を単眼深度推定を行います。PCのリソースが厳しいのでGoogle Colabパワーを使います。（適宜画像パスは工夫してください）

[export_depth.ipynb (Colaboratry)](https://colab.research.google.com/github/Ar-Ray-code/PastePicture2Wallpaper/blob/main/export_depth.ipynb)をチェックしてください。

<br>

一通り実行すると、`depth_result.png`が出力されます。

<br>

## 2. 画像を閾値を指定して距離を指定

> PyQtの使い方下手過ぎて申し訳ないです…

[`convert.py`](./convert.py)を用いて深度の閾値を変更します。デフォルトでは150なので、そのまま`convertion`ボタンを押してもOKです。

### オプション

- `-i` : 画像パス
- `-d` : `depth_result.png`を指定

> 画像は同じサイズにしてください（何も変換しなければ問題無いです）

```bash
python3 convert.py -i ~/Downloads/image.jpg -d ~/Downloads/depth_result.png
```

変換終了後に次のファイルがコマンド入力をしたディレクトリに出力されます。

- edges_check.jpg : エッジ検出後の画像（確認用）
- edges.png : エッジ検出後の合成用画像。線に少し透明度があり、背景が透過されています。

<br>

残念ながら完璧な線画は出力できないので、適宜修正してください。

<br>

## 3. Gimpなどを使って合成

壁紙をGimpなどで作ってください。

- [使用した画像（StackExchange）](https://askubuntu.com/questions/1187569/where-to-find-default-ubuntu-purple-wallpaper-without-animals)

<br>

## パラメータ

現在は閾値のみ直接扱えます。パラメータもっと増やします…

<br>

## 参考

https://axross-recipe.com/recipes/404 by [Kazuhito00](https://github.com/Kazuhito00/)