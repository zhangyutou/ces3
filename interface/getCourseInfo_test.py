import unittest
from common import huibenpara
from common import commonfunction
from interface import getCoursepage_test



class allCourses(unittest.TestCase):
    ''' 课程详情界面 '''

    @classmethod
    def setUpClass(cls):
        cls.url= huibenpara.host + '/huiben/client/course/getCourseInfo'
        cls.before_result=getCoursepage_test.allcourses().setUpClass()['data']['list']
        cls.api_results=commonfunction.setupRequest().get_result(cls.url, cls.before_result,"id",
                    {'token': 'fb65286c559bf899', 'userId': '215630', 'isVip': '1'}, huibenpara.base_para)
        #print(cls.api_results)
        return cls.api_results

    def test_baseinfo(self):
        ''' 校验课程基本信息"id","price","vipPrice","discountPrice","isVip" '''
        self.basedata = commonfunction.setupBasedata().get_basedatas("plan_course", "id", self.before_result)
        api_data=commonfunction.previewData().get_dict_values('data',self.api_results)
        api_dealresults = commonfunction.previewData().get_dict_datas(["id","price","vipPrice","discountPrice","isVip"], api_data)
        base_dealresults=commonfunction.previewData().get_list_listdict_data(self.basedata,["id","price","vipPrice","discountPrice","isVip"])
        self.assertEqual(api_dealresults, base_dealresults)

    def test_responsetcode(self):
        '''resultCode=0'''
        responsecodes=commonfunction.previewData().get_dict_datas(["resultCode"],self.api_results)
        commonfunction.resultsAssert().assertcircle(responsecodes,"resultCode","0")

    def test_contentnum(self):
        '''验证目录章节个数'''
        api_results=self.api_results
        apicontent=commonfunction.previewData().get_values(api_results,"data")
        self.apicontents=commonfunction.previewData().get_values(apicontent,"planContents")
        self.basecontent=commonfunction.setupBasedata().get_basedatas2("plan_content","id","courseId",self.before_result)
        apilen=commonfunction.previewData().lld_len(self.apicontents)
        baselen=commonfunction.previewData().lld_len(self.basecontent)
        self.assertEqual(apilen,baselen)



