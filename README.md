# KosenCTFKit

This is a joke CTF platform inspired of CTFKit.

## 使い方


### セットアップ
- `git clone https://github.com/theoldmoon0602/KosenCTFKit`
- `cd KosenCTFKit`
- `rm -rf challenges`としてダミーを削除した後、`challenges` を配置する (例: `git clone https://github.com/theoldmoon0602/InterKosenCTF2019-challenges challenges`)
    + あるいは `docker-compose.yaml`の設定を変更しても良い
- `ssh`の中身を設定する（このディレクトリは `~/.ssh`相当
    + 使用する秘密鍵を配置する
    + sshの設定を`ssh/config`に書く
- `config.py`を編集する
    + `SECRET_KEY`を適当な別の文字烈に変える
    + `DEBUG = False`とする
    + `CATEGORY_SERVERS`を設定する
    + `SQLALCHEMY_DATABASE_URI`や`WEBHOOK_URL`を環境に合わせて設定する
    + `admin`の項目は必ず変更する
- `src/pages/`をCTFに合わせて編集する
- `docker-compose.yaml`を環境に合わせて編集する
- `docker-compose up --build -d`

### 登録開始

```
$ docker-compose exec kosenctfkit python3 manage.py open --only-register
```

### CTF開始

注意：この設定が行われていて、かつ`config.py`に設定したCTFの開催期間中はCTFが行われます

```
$ docker-compose exec kosenctfkit python3 manage.py open
```

### 問題のデプロイ

注意：複数の問題を一度にデプロイすることはできない

```
$ docker-compose exec kosenctfkit python3 manage.py challenge deploy <問題名>
```

問題が解けることの確認も同時に行う場合

```
$ docker-compose exec kosenctfkit python3 manage.py challenge deploy <問題名> --check
```


問題が解けることの確認のみを行う場合

```
$ docker-compose exec kosenctfkit python3 manage.py challenge check <問題名>
```

### 問題の公開

- `--all` オプションを使うと全ての問題を対象にできる
- `--close` オプションを使うと問題を非公開にできる

```
$ docker-compose exec kosenctfkit python3 manage.py challenge open "<問題名1>" "<問題名2>"
```

### adminとして色々を管理

`config.py`に設定した管理ユーザのユーザ名・パスワードでログインして`/admin`にアクセスする


