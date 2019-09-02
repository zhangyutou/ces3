import unittest
from common import huibenpara
from common import commonfunction
from interface import getCourseInfo_test
from common import huibenpara
import requests
from database import connect

url = huibenpara.host + '/huiben/client/course/getContentExercises'
before_result = getCourseInfo_test.allCourses().setUpClass()

class ExercisesPage(unittest.TestCase):
    '''课后练习界面'''

    def test_allid(self):
        '''课程id--目录id--练习id 验证'''
        random = {'userId': '215630', 'token': 'f684332d743a72e0'}
        self.courseid_contentid=commonfunction.previewData().lddld_getvalues("data","planContents","id","id",before_result)
        courseid=list(self.courseid_contentid.keys())
        content_results={}
        course_result={}
        nextstep_exerciseid=[]
        nextstep_exerciseids={}

        for i in range(len(courseid)):
            contentidlist=self.courseid_contentid[courseid[i]]
            for j in range(len(contentidlist)):
                contentid=contentidlist[j]
                paras=commonfunction.setupRequest().split_paras("contentId",contentid,random,huibenpara.base_para)
                content_result= requests.post(url,data=paras)
                if content_result.status_code==500:
                    pass
                else:
                    content_result_json=content_result.json()
                    exerciseid=commonfunction.previewData().get_dict_values("id",content_result_json["data"])
                    content_results[contentid]=exerciseid
                    nextstep_exerciseid.extend(exerciseid)
            course_result[courseid[i]]=content_results
            content_results={}
            nextstep_exerciseids[courseid[i]]=nextstep_exerciseid
            nextstep_exerciseid=[]

        base_courses={}
        for i in range(len(courseid)):
            base_content=commonfunction.setupBasedata().get_line_basedatas("plan_content","id","courseid",courseid[i])
            base_courses[courseid[i]]=base_content
            for j in range(len(base_content)):
                base_exercise=commonfunction.setupBasedata().get_line_basedatas("plan_content_exercise","id","contentId",base_content[j])
                base_courses[courseid[i]][base_content[j]]=base_exercise
        #self.assertEqual(course_result,base_courses)
        return courseid,nextstep_exerciseids

    def test_UserStatus(self):
        '''向数据库插入作业完成情况数据，验证接口请求到的数据'''
        #randoms = [{'userId': '215630', 'token': 'f684332d743a72e0'},{'userId': '111178', 'token': 'f684332d743a72e0'},{'userId': '2', 'token': 'f684332d743a72e0'}]
        connect.insertData("plan_user_wroks","(courseId,contentId,exerciseId,userId,status)","(21,29,30,13844681319,'finished')")
        paras = commonfunction.setupRequest().split_paras("contentId", 21, {'userId': '13844681319', 'token': 'f684332d743a72e0'}, huibenpara.base_para)
        content_result = requests.post(url, data=paras).json()
        user_works=content_result["data"]["planUserWorks"]
        for i in range(len(user_works)):
            id=eval(user_works[i]["id"])
            work=user_works[i]
            if id==21 :
                self.assertTrue(work["totalScore"] is not None)
            else :
                print("在数据库中插入的数据，在请求结果中没有找到")
                self.assertEqual(1,2)


