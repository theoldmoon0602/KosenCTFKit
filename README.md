# KosenCTFKit

This is a joke CTF platform inspired of CTFKit.

## 使い方


### セットアップ
1. `git clone https://github.com/theoldmoon0602/KosenCTFKit`
2. `cd KosenCTFKit`
3. `rm -rf challenges`としてダミーを削除した後、`challenges` を配置する (例: `git clone https://github.com/theoldmoon0602/InterKosenCTF2019-challenges challenges`)
3.1. あるいは `docker-compose.yaml`の設定を変更しても良い
4. `ssh`の中身を設定する（このディレクトリは `~/.ssh`相当
4.1. 使用する秘密鍵を配置する
4.2. sshの設定を`ssh/config`に書く
5. `config.py`を編集する
5.1. `SECRET_KEY`を適当な別の文字烈に変える
5.2. `DEBUG = False`とする
5.3. `CATEGORY_SERVERS`を設定する
5.4. `SQLALCHEMY_DATABASE_URI`や`WEBHOOK_URL`を環境に合わせて設定する
6. `ctf_config.yaml`をCTFの設定に合わせて編集する
6.1. `admin`の項目は必ず変更する
7. `src/pages/index.vue`をCTFに合わせて編集する
8. `docker-compose.yaml`を環境に合わせて編集する
8.1
9. `docker-compose up --build -d`

### 登録開始

```
$ docker-compose exec kosenctfkit python3 manage.py open --only-register
```

### CTF開始

注意：この設定が行われていて、かつ`cft_config.yaml`に設定したCTFの開催期間中はCTFが行われます

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

`ctf_config.yaml`に設定した管理ユーザのユーザ名・パスワードでログインして`/admin`にアクセスする


