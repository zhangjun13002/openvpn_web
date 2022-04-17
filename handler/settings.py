# -- coding: utf8 --
import json

from model.default import Smtp, Warn

from . import BaseHandler
from .default import CheckLogin


class SmtpHandler(BaseHandler):
    @CheckLogin
    def get(self):
        query = Smtp().select().first()
        if query:
            result = {}
            result["server"] = query.server
            result["ssl"] = query.ssl
            result["port"] = query.port
            result["user"] = query.user
            self.write(json.dumps(result))
        else:
            err_msg = {"result": "获取邮箱参数错误"}
            self.send_error(status_code=500, **err_msg) 

    @CheckLogin
    def post(self):
        try:
            req = json.loads(self.request.body)
            if req['password'] == "":
                query = Smtp.update({Smtp.server: req['server'], Smtp.ssl: req['ssl'], Smtp.port: req['port'], Smtp.user: req['user']}).where(Smtp.id==1)
            else:
                query = Smtp.update({Smtp.server: req['server'], Smtp.ssl: req['ssl'], Smtp.port: req['port'], Smtp.user: req['user'], Smtp.password: req['password']}).where(Smtp.id==1)
            query.execute()
            self.write(json.dumps({"result": "success"}))
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg) 

class WarnHandler(BaseHandler):
    @CheckLogin
    def get(self):
        query = Warn().select().first()
        if query:
            result = {}
            result["status"] = query.status
            result["send_time"] = query.send_time
            result["send_msg"] = query.send_msg
            result["admin_status"] = query.admin_status
            result["admin_email"] = query.admin_email
            self.write(json.dumps(result))
        else:
            err_msg = {"result": "获取提醒参数错误"}
            self.send_error(status_code=500, **err_msg) 

    @CheckLogin
    def post(self):
        try:
            req = json.loads(self.request.body)
            if req['status'] == 0:
                query = Warn.update({Warn.status: req['status']}).where(Warn.id==1)
            elif req['admin_status'] == 0:
                query = Warn.update({Warn.status: req['status'], Warn.send_time: int(req['send_time']), Warn.send_msg: req['send_msg'], Warn.admin_status: req['admin_status']}).where(Warn.id==1)
            else:
                query = Warn.update({Warn.status: req['status'], Warn.send_time: int(req['send_time']), Warn.send_msg: req['send_msg'], Warn.admin_status: req['admin_status'], Warn.admin_email: req['admin_email']}).where(Warn.id==1)
            query.execute()
            self.write(json.dumps({"result": "success"}))
        except Exception as e:
            err_msg = {"result": "{0}".format(str(e))}
            self.send_error(status_code=500, **err_msg) 