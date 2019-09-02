import time
from HTMLTestRunner import HTMLTestRunner
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import os

def new_file(test_dir):
    #列举test_dir目录下的所有文件，结果以列表形式返回。
    lists=os.listdir(test_dir)
    #sort按key的关键字进行排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间
    #最后对lists元素，按文件修改时间大小从小到大排序。
    lists.sort(key=lambda fn:os.path.getmtime(test_dir+'\\'+fn))
    #获取最新文件的绝对路径
    file_path=os.path.join(test_dir,lists[-1])
    return file_path

def send_mail():
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 25
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USERNAME'] = '13844681319@163.com'
    app.config['MAIL_PASSWORD'] = 'xdd789'

    mail = Mail(app)
    now_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    msg = Message('测试报告' + str(now_time), sender='13844681319@163.com', recipients=['13844681319@163.com'])

    test_dir = 'C:\\Users\\Administrator\\Desktop\\py文件\\pyrequestUnitest\\report'
    new_report = new_file(test_dir)
    f = open(new_report, 'rb')
    body = f.read()
    f.close()

    msg.html = body
    msg.body = body

    if __name__ == '__main__':

        print(new_report)
        with app.app_context():
            print(mail.send(msg))
