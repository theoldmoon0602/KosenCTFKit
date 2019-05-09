# KosenCTFKit

This is a joke CTF platform inspired of CTFKit.

## How to use

1. edit config.py
1.1. you should change `SECRET_KEY` and make `DEBUG` false
2. edit ctf_config.yaml
2.1. you should change administrator's credential
3. replace `challenges` directory to your own one
4. `docker-compose up --build`
5. `docker exec kosenctfkit /bin/sh`
5.1 `python3 manage.py challange add` to register your challenges to score server
5.2 `python3 manage.py open` to open competition

