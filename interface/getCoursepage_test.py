import unittest
import requests
from common import huibenpara
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parentdir)
from database import connect

class allcourses(unittest.TestCase):
    ''' 全部课程界面 '''

    @classmethod
    def setUpClass(cls):
        cls.url= huibenpara.host + '/huiben/client/course/getCoursePage'
        random_para={'pageNo':'1','pageSize':'20','userId':'215630','token':'fed07d2a84febd37'}
        cls.para={**huibenpara.base_para, **random_para}
        cls.result=requests.post(cls.url,data=cls.para).json()
        return cls.result

    def test_resultcode(self):
        self.assertEqual(self.result['resultCode'], '0')

    def test_bookid(self):
        '''验证上线的课程id'''
        list1 = self.result['data']['list']
        bookids=[]
        for i in range(len(list1)):
            bookid=list1[i]["id"]
            bookids.append(bookid)
        base_bookids=connect.lineQuery("select id from plan_course WHERE status=1")
        self.assertListEqual(sorted(bookids),sorted(base_bookids))




if __name__ == '__main__':
    unittest.main()