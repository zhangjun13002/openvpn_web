# -- coding: utf8 --
import json
import os
import base64
import subprocess

from config import private_key, public_key

from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from model.default import User, Logs

from . import BaseHandler
from .default import CheckLogin
from utils import send_mail

class KeyHandler(BaseHandler):
    @CheckLogin
    def get(self):
        self.write(public_key)

class UserHandler(BaseHandler):
    @CheckLogin
    def get(self):
        user = self.get_query_arguments("user")[0]
        page = int(self.get_query_arguments("page")[0])
        pagenum = int(self.get_query_arguments("limit")[0])

        result = {"status": 0, "message": "", "total": 0, "data": {}}
        data = {}
        node = []
        if user == "all":
            total = User.select().count()
            result['total'] = total

            query = User.select().order_by(User.id).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                userinfo = {}
                userinfo['id'] = item.id
                userinfo['username'] = item.username
                userinfo['email'] = item.email
                if item.active == 1:
                    userinfo['active'] = True
                else:
                    userinfo['active'] = False
                userinfo['expire'] = item.expire
                userinfo['firewall'] = item.firewall
                node.append(userinfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))
        else:
            total = User.select().where(User.username.contains(user)).count()
            result['total'] = total

            query = User.select().where(User.username.contains(user)).order_by(User.id).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                userinfo = {}
                userinfo['id'] = item.id
                userinfo['username'] = item.username
                userinfo['email'] = item.email
                if item.active == 1:
                    userinfo['active'] = True
                else:
                    userinfo['active'] = False
                userinfo['expire'] = item.expire
                userinfo['firewall'] = item.firewall
                node.append(userinfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))

class AddHandler(BaseHandler):
    @CheckLogin
    def post(self):
        try:
            req = json.loads(self.request.body)
            query = User.select().where(User.username == req['username']).first()
            if query is None:
                req['password'] = MD5.new(req['password'].encode()).hexdigest()
                insert = User.insert(req)
                insert.execute()
                self.write(json.dumps({"result": "success"}))
            else:
                err_msg = {"result": "{0} 已经存在".format(query.username)}
                self.send_error(status_code=500, **err_msg)
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg) 


class GenHandler(BaseHandler):
    @CheckLogin
    def get(self):
        uid = int(self.get_query_arguments("id")[0])
        query = User.select(User.username).where(User.id == uid).first()
        if query:
            result = {"status": 0, "message": "", "total": 0, "data": {}}
            username = query.username
            cmd = os.path.join(self.settings.get('rsa3dir'), "genconf.sh {0}".format(username))
            status = subprocess.call(cmd, shell=True)
            if status == 0:
                src = os.path.join(self.settings.get('rsa3dir'), "{0}.ovpn".format(username))
                dest = os.path.join(self.settings.get('static_path'), "client/{0}.ovpn".format(username))
                os.replace(src, dest)
                url = "/static/client/{0}.ovpn".format(username)
                result["status"] = 0
                result["message"] = "success"
                result["data"]["url"] = url
                self.write(json.dumps(result))
            else:
                result['status'] = status
                result['message'] = "生成配置失败"
                self.write(json.dumps(result))
        else:
            err_msg = {"result": "{0} 不存在".format(query.username)}
            self.send_error(status_code=500, **err_msg)


class UpdateHandler(BaseHandler):
    @CheckLogin
    def post(self):
        try:
            req = json.loads(self.request.body)
            for key, value in req.items():
                if key == 'password':
                    privKey = RSA.import_key(private_key)
                    cipher = PKCS1_v1_5.new(privKey)
                    decrypted = cipher.decrypt(base64.b64decode(value.encode()), None)
                    if decrypted:
                        md5 = MD5.new(decrypted).hexdigest()
                        user = User.update({User.password: md5}).where(User.id == req['id'])
                        user.execute()
                        if req.get('sendmail') == True:
                            query_mail = User.select(User.username, User.email).where(User.id == req['id']).first()
                            if query_mail and query_mail.email != "":
                                username = query_mail.username
                                email = query_mail.email                                
                                title = "VPN用户密码更改"
                                msg = "{0}:\r\n\t        你的VPN用户密码已修改为: {1}.".format(username, decrypted.decode())
                                send_mail.send_mail(email, title=title, message=msg)
                            else:
                                raise ValueError("用户邮箱没有设置.")
                    else:
                        raise ValueError("用户密码错误!")
                if key == 'email':
                    user = User.update({User.email: value}).where(User.id == req['id'])
                    user.execute()
                if key == 'active':
                    user = User.update({User.active: value}).where(User.id == req['id'])
                    user.execute()
                if key == 'expire':
                    user = User.update({User.expire: value, User.send: 0}).where(User.id == req['id'])
                    user.execute()
                if key == 'firewall':
                    user = User.update({User.firewall: value}).where(User.id == req['id'])
                    user.execute()
            self.write(json.dumps({"result": "success"}))
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg)


class DelHandler(BaseHandler):
    @CheckLogin
    def post(self):
        try:
            req = json.loads(self.request.body)
            query = User.select(User.username).where(User.id == req['id']).first()
            user = User.delete().where(User.id == req['id'])
            user.execute()
            if query is not None:
                log = Logs.delete().where(Logs.username == query.username)
                log.execute()
            self.write(json.dumps({"result": "success"}))
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg) 


class LogsHandler(BaseHandler):
    @CheckLogin
    def get(self):
        user = self.get_query_arguments("user")[0]
        page = int(self.get_query_arguments("page")[0])
        pagenum = int(self.get_query_arguments("limit")[0])

        result = {"status": 0, "message": "", "total": 0, "data": {}}
        data = {}
        node = []

        if user == "all":
            total = Logs.select().count()
            result['total'] = total
            query = Logs.select().order_by(Logs.id.desc()).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                loginfo = {}
                loginfo['id'] = item.id
                loginfo['username'] = item.username
                loginfo['local'] = item.local
                loginfo['remote'] = item.remote
                loginfo['trusted_ip'] = item.trusted_ip
                loginfo['trusted_port'] = item.trusted_port
                loginfo['logintime'] = item.logintime
                loginfo['logouttime'] = item.logouttime
                loginfo['received'] = item.received
                loginfo['sent'] = item.sent
                node.append(loginfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))
        else:
            total = Logs.select().where(Logs.username == user).count()
            result['total'] = total
            query = Logs.select().where(Logs.username == user).order_by(Logs.id.desc()).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                loginfo = {}
                loginfo['id'] = item.id
                loginfo['username'] = item.username
                loginfo['local'] = item.local
                loginfo['remote'] = item.remote
                loginfo['trusted_ip'] = item.trusted_ip
                loginfo['trusted_port'] = item.trusted_port
                loginfo['logintime'] = item.logintime
                loginfo['logouttime'] = item.logouttime
                loginfo['received'] = item.received
                loginfo['sent'] = item.sent
                node.append(loginfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))
