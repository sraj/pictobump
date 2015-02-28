# -*- coding:utf-8 -*-
from flask.ext.script import Server, Manager
from conf.settings import Dev, Prod
from pictobump import pictobump_app

app = pictobump_app(Dev)
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=5000))

if __name__ == "__main__":
	manager.run()