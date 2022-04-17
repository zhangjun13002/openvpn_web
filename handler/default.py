# -- coding: utf8 --
import json
import time
import base64

from model.default import Admin

from . import BaseHandler


def CheckLogin(func):
    def wrapper(self, *args, **kwargs):
        query = Admin.select().where(Admin.username == self.get_cookie("username")).first()
        if query is not None:
            if self.get_cookie("token") == query.token.strip():
                return func(self, *args, **kwargs)
        self.send_error(status_code=401)
    return wrapper


class LoginHandler(BaseHandler):
    def get(self):
        query = Admin.select().where(Admin.username == self.get_cookie("username")).first()
        if query is not None:
            if self.get_cookie("token") == query.token.strip():
                self.redirect("/")
        else:
            self.render("login.html")

    def post(self):
        try:
            req = json.loads(self.request.body)
            admin = Admin.select().where(Admin.username == req['username']).first()
            if admin is not None:
                if req['password'] == admin.password:
                    token = base64.encodebytes((req['username'] + str(time.time())).encode()).decode()
                    admin = Admin.update({Admin.token: token}).where(Admin.username == req['username'])
                    admin.execute()
                    self.write(json.dumps({"result": "登陆成功", "token": token, "code": 0}))
                else:
                    self.write(json.dumps({"result": "密码不正确", "code": -1}))
            else:
                err_msg = {"result": "{0} 用户不存在".format(req['username'])}
                self.send_error(status_code=500, **err_msg)
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg) 


class MainHandler(BaseHandler):
    def get(self):
        if self.get_cookie("username") is not None:
            self.render("index.html")
        else:
            self.redirect("/login")


class AdminHandler(BaseHandler):
    @CheckLogin
    def post(self):
        try:
            req = json.loads(self.request.body)
            admin = Admin.update({Admin.password: req['password']}).where(Admin.username == "admin")
            admin.execute()
            self.write(json.dumps({"result": "success"}))
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg) 
