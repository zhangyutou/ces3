import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parentdir)
# from db_fixture import test_data

from common import huibenpara


class UserLoginTest(unittest.TestCase):
    ''' 绘本森林登录用例一 '''

    def setUp(self):
        self.base_url =  "https://m.xueduoduo.com/hyun/auth/login"

    # def tearDown(self):
    #     print(self.result)

    def test_user_sign_all_null(self):
        ''' 参数为空 '''
        payload = {"account":"duoduo1","appType":huibenpara.appType, "classId": "", "className": "", "clientPackage":huibenpara.clientPackage, "clientVersion":huibenpara.clientVersion, "grade": "", "gradeName": "", "landIp":huibenpara.landIp, "logoUrl": "", "operatorId": "-999", "password":huibenpara.passWords('123456'), "schoolId": "-9", "schoolName": "", "systemVersion":huibenpara.systemVersion, "token": "c3aeeaa7bd6217ec", "userId": "-999", "userName": "", "userType": "", "version":huibenpara.version}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['resultCode'], '0')
        self.assertEqual(self.result['data']['schoolId'], 226)




if __name__ == '__main__':
    # test_data.init_data() # 初始化接口测试数据
    unittest.main()
