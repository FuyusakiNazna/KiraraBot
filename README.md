# KiraraBot
TAOのレア敵を通知するBOTです。

# メモ:
```
マイナンバー親の許可がもらえなかったのでこの部分だけ載せます
動作確認よろしく 不要な部分削っただけだから多分動く
```

# インストール:
```
パッケージをインストール
config.tomlにtokenとprefix書き込む
-python run.py
```

# 動作環境(2020/11/27)
全部installすれば動くんじゃね
| パッケージ名 | version |  | パッケージ名 | version | 
|:-----------|:------------:| ------------ |:-----------|:------------:| 
| "Python" | 3.8.1 | | "discord.py" | 1.5.1 |
| "ImageHash" | 4.1.0 | | "intent" | 0.0.4 |
| "requests" | 2.24.0 | |  |  |

# データベースの中身:
| テーブル名:  | カラム名: | カラム名: | カラム名: | カラム名: | カラム名: |  カラム名: |
|:-----------|:------------|:------------:|:-----------|:------------|:------------:|:------------:|
| "tao_enemy" | name(text) | id(text) | rank(text) | attribute(text) | time(text) | url(text) |