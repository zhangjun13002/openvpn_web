from peewee import CharField, IntegerField

from . import BaseModel


class Admin(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=50)
    password = CharField(max_length=64)
    token = CharField()

    class Meta:
        table_name = 't_admin'

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=50)
    email = CharField(max_length=100)
    password = CharField(max_length=64)
    active = IntegerField()
    expire = CharField()
    firewall = CharField()
    send = IntegerField()

    class Meta:
        table_name = 't_user'


class Logs(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField()
    local = CharField()
    remote = CharField()
    trusted_ip = CharField()
    trusted_port = CharField()
    logintime = CharField()
    logouttime = CharField()
    received = IntegerField()
    sent = IntegerField()

    class Meta:
        table_name = 't_logs'


class Smtp(BaseModel):
    id = IntegerField()
    server = CharField()
    ssl = IntegerField()
    port = IntegerField()
    user = CharField()
    password = CharField()

    class Meta:
        table_name = 't_smtp'


class Warn(BaseModel):
    id = IntegerField()
    status = IntegerField()
    send_time = IntegerField()
    send_msg = CharField()
    admin_status = IntegerField()
    admin_email = CharField()
    admin_msg = CharField()

    class Meta:
        table_name = 't_warn'

