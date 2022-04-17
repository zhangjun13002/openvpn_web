import time
from apscheduler.schedulers.tornado import TornadoScheduler

from model import db
from model.default import User
from model.default import Warn

from utils.send_mail import send_mail

def check_expire():
    try:
        if db.is_closed():
            db.connect()
        query = Warn.select().first()
        if query:
            if query.status == 1:
                times = query.send_time
                message = query.send_msg
                admin_status = query.admin_status
                admin_email = query.admin_email
                now = time.time()
                last_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now + (times - 1) * 86400))
                next_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now + times * 86400))       
                q_user = User.select(User.id, User.username, User.email, User.expire, User.send).where(User.expire > last_time and User.expire < next_time)
                all_user = ""
                if q_user:
                    for item in q_user:
                        if item.send == 0 and item.email != "":
                            msg = message.format(username=item.username, time=item.expire)
                            send_mail(item.email, title="VPN用户即将到期", message=msg)
                            q_user = User.update({User.send: 1}).where(User.id == item.id)
                            q_user.execute()
                            all_user = all_user + item.username + ", "

                if admin_status == 1 and admin_email != "" and all_user != "":
                    msg = "管理员: \r\n\t    VPN用户: {0} 即将到期。".format(all_user)
                    send_mail(admin_email, title="VPN用户即将到期", message=msg)
        db.close()
    except Exception as e:
        print("Error:", str(e))

def sche_init():
    scheduler = TornadoScheduler()
    scheduler.add_job(check_expire, 'cron', day="*", hour="01", minute="00", id="check_expire")
    scheduler.start()