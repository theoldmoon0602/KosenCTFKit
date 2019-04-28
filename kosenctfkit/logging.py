from kosenctfkit.models import db, Log
import requests
import json


class CTFLogger:
    def init(self, webhook_url=None):
        self.webhook_url = webhook_url

    def log(self, text):
        log = Log(text=text)
        db.session.add(log)
        db.session.commit()
        if self.webhook_url:
            try:
                requests.post(
                    self.webhook_url,
                    data=json.dumps(
                        {"text": text, "username": "CTF Log", "icon_emoji": ":memo:"}
                    ),
                )
            except:
                pass


logger = CTFLogger()
