# KosenCTFKit

This is a joke CTF platform inspired of CTFKit.

## Settings

### CTF settings

Edit `ctf-config.yaml`. Regards score-expr, V is the challenge's base_score and N is number of solved.

### Application settings

By editing `config.py`, you can set the url for database and more settings. In production, you should change the `SECRET_KEY`.


## Build

You can use docker and docker-compose to build this app or not.

### Docker and docker-compose

simply run `docker-compose build`.


### By your hand

follow this script.

```
$ yarn install
$ yarn build
$ pipenv install
$ pipenv run python app.py
```

## Manage the competition

Use `manage.py`. It can

- open/close CTF and registration
- add/open/list challenges

To see more details, run `python manage.py help`.

