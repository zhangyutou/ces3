import time, sys
sys.path.append('./interface')
# sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader
# from db_fixture import test_data
from common import sendEmail



# 指定测试用例为当前文件夹下的 interface 目录
test_dir = './interface'
testsuit = defaultTestLoader.discover(test_dir, pattern='*_test.py')


if __name__ == "__main__":
    # test_data.init_data() # 初始化接口测试数据
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='绘本森林测试报告',
                            description='运行环境: Requests, unittest ')
    runner.run(testsuit)
    fp.close()
    sendEmail.send_mail()
