import unittest
import requests
from interface import getContentExercises_test
from common import huibenpara
from common import commonfunction

course_id=getContentExercises_test.ExercisesPage().test_allid()[0]
exercise_id=getContentExercises_test.ExercisesPage().test_allid()[1]
url = huibenpara.host +"/huiben/client/course/getSourceExercisesByExerciseId"


book_workContent=[
  {
    "recordUrl" : "http:\/\/qn.xueduoduo.com\/\/111178_36E4BDEE_xdd20190829153912.mp3",
    "localPath" : "\/var\/mobile\/Containers\/Data\/Application\/20C4357C-A8AA-4BC6-A756-4F0049431F85\/Documents\/upload\/xdd20190829153912.mp3",
    "pageNo" : 2
  },
  {
    "pageNo" : 3,
    "recordUrl" : "http:\/\/qn.xueduoduo.com\/\/111178_2DADD9F5_xdd20190829153921.mp3",
    "localPath" : "\/var\/mobile\/Containers\/Data\/Application\/20C4357C-A8AA-4BC6-A756-4F0049431F85\/Documents\/upload\/xdd20190829153921.mp3"
  },
  {
    "localPath" : "\/var\/mobile\/Containers\/Data\/Application\/20C4357C-A8AA-4BC6-A756-4F0049431F85\/Documents\/upload\/xdd20190829153859.mp3",
    "recordUrl" : "http:\/\/qn.xueduoduo.com\/\/111178_11492259_xdd20190829153859.mp3",
    "pageNo" : 1
  }
]
image_workContent="http://qn.xueduoduo.com//111178_4D0AE779_20190829153205.jpg"
saveWork_url=huibenpara.host +"/huiben/client/course/saveUserWorks"
getWork_url=huibenpara.host+"/client/course/getUserWorks"
saveWork_random = {'userId': '215630'}
getWork_random ={'userId': '215630','pageNo':'1','pageSize':'20'}

# get_paras1 = commonfunction.setupRequest().split_paras("exerciseId", 85,getWork_random,huibenpara.base_para)
# get_paras = {**get_paras1, **{"courseId": "35"}}
# get_result = requests.post(url, data=get_paras)
# print(get_result.json())
# get_paras= commonfunction.setupRequest().split_paras("exerciseId", 89,getWork_random,huibenpara.base_para)
# get_result = requests.post(url, data=get_paras).json()
# print(get_result)
class exercise(unittest.TestCase):
    '''查看、保存练习'''

    def test_allExercise(self):
        '''验证所有课后练习都能正常查看'''
        for j in range(len(course_id)):
            now_courseid=course_id[j]
            for i in range(len(exercise_id[now_courseid])):
                exercise=exercise_id[now_courseid][i]
                random_paras={"userId":"111178"}
                paras = commonfunction.setupRequest().split_paras("exerciseId",exercise_id[now_courseid][i],random_paras,huibenpara.base_para)
                result=requests.post(url,data=paras)
                if result.status_code != 200:
                    print("获取课后练习信息失败:%d" % (exercise_id[now_courseid][i]))
                    continue
                else:
                    result_text = result.json()["data"]
                    if "userWorks"in result_text.keys():

                        if "exerciseId"  in result_text["userWorks"][0].keys():
                            print("查询到需订正或已完成的作业:%d" % (exercise_id[now_courseid][i]))
                            result=result_text["userWorks"][0]
                            self.assertEqual(result["exerciseId"],exercise_id[now_courseid][i])
                        else:
                            print("数据异常：%d" % (exercise_id[now_courseid][i]))
                            continue
                    elif type(result_text["exercises"])==dict:
                        print("查询到未完成的作业：%d" % (exercise_id[now_courseid][i]))
                        self.assertEqual(result_text["exercises"]["id"], exercise_id[now_courseid][i])
                        work_type=result_text["exercises"]["type"]
                        if work_type == "book":
                            save_paras1 = commonfunction.setupRequest().split_paras("exerciseId", exercise_id[now_courseid][i],
                                                                                        saveWork_random,
                                                                                        huibenpara.base_para)
                            save_para2 = {**save_paras1, **{"courseId": str(now_courseid)}}
                            save_paras3={**save_para2,**{"workType":str(work_type)}}
                            save_paras={**save_paras3,**{"workContent":str(book_workContent)}}
                            save_result = requests.post(saveWork_url, data=save_paras).json()
                            self.assertEqual(save_result["resultCode"], '0')
                                #exercise=exercise_id[now_courseid][i]
                            get_paras= commonfunction.setupRequest().split_paras("exerciseId",exercise,getWork_random,huibenpara.base_para)
                            #print('xdd=%s'%get_paras)
                            get_result = requests.post(url, data=get_paras).json()
                            self.assertEqual(get_result["data"]["userWorks"][0]["exerciseId"],exercise_id[now_courseid][i])
                        else:
                            save_paras1 = commonfunction.setupRequest().split_paras("exerciseId",
                                                                                        exercise_id[now_courseid][i],
                                                                                        saveWork_random,
                                                                                        huibenpara.base_para)
                            save_paras2 = {**save_paras1, **{"courseId": str(now_courseid)}}
                            save_paras3 = {**save_paras2, **{"workType": str(work_type)}}
                            save_paras = {**save_paras3, **{"workContent": str(image_workContent)}}
                            save_result = requests.post(saveWork_url, data=save_paras).json()
                            self.assertEqual(save_result["resultCode"], '0')
                            #exercise = exercise_id[now_courseid][i]
                            get_paras1 = commonfunction.setupRequest().split_paras("exerciseId",exercise,getWork_random,huibenpara.base_para)
                            get_paras = {**get_paras1, **{"courseId": str(now_courseid)}}
                            get_result = requests.post(url, data=get_paras).json()
                            self.assertEqual(get_result["data"]["userWorks"][0]["exerciseId"],exercise_id[now_courseid][i])

                        # except:
                        #     '''数据异常'''
                        #     print("数据异常:%d" % (exercise_id[now_courseid][i]))
                    elif type(result_text["exercises"])==list:
                        try:
                            print("查询到未完成的作业：%d" % (exercise_id[now_courseid][i]))
                            self.assertEqual(result_text["exercises"][0]["id"], exercise_id[now_courseid][i])
                            work_type = result_text["exercises"][0]["type"]
                            #*********************************
                            if work_type == "book":
                                save_paras1 = commonfunction.setupRequest().split_paras("exerciseId",
                                                                                        exercise_id[now_courseid][i],
                                                                                        saveWork_random,
                                                                                        huibenpara.base_para)
                                save_para2 = {**save_paras1, **{"courseId": str(now_courseid)}}
                                save_paras3 = {**save_para2, **{"workType": str(work_type)}}
                                save_paras = {**save_paras3, **{"workContent": str(book_workContent)}}
                                save_result = requests.post(saveWork_url, data=save_paras).json()
                                self.assertEqual(save_result["resultCode"], '0')
                                # exercise=exercise_id[now_courseid][i]
                                get_paras = commonfunction.setupRequest().split_paras("exerciseId", exercise,
                                                                                      getWork_random,
                                                                                      huibenpara.base_para)
                                # print('xdd=%s'%get_paras)
                                get_result = requests.post(url, data=get_paras).json()
                                self.assertEqual(get_result["data"]["userWorks"][0]["exerciseId"],
                                                 exercise_id[now_courseid][i])
                            else:
                                save_paras1 = commonfunction.setupRequest().split_paras("exerciseId",
                                                                                        exercise_id[now_courseid][i],
                                                                                        saveWork_random,
                                                                                        huibenpara.base_para)
                                save_paras2 = {**save_paras1, **{"courseId": str(now_courseid)}}
                                save_paras3 = {**save_paras2, **{"workType": str(work_type)}}
                                save_paras = {**save_paras3, **{"workContent": str(image_workContent)}}
                                save_result = requests.post(saveWork_url, data=save_paras).json()
                                self.assertEqual(save_result["resultCode"], '0')
                                # exercise = exercise_id[now_courseid][i]
                                get_paras1 = commonfunction.setupRequest().split_paras("exerciseId", exercise,
                                                                                       getWork_random,
                                                                                       huibenpara.base_para)
                                get_paras = {**get_paras1, **{"courseId": str(now_courseid)}}
                                get_result = requests.post(url, data=get_paras).json()
                                self.assertEqual(get_result["data"]["userWorks"][0]["exerciseId"],
                                                 exercise_id[now_courseid][i])
                        except:
                            '''数据异常'''
                            print("数据异常:%d" % (exercise_id[now_courseid][i]))
                    else:
                        print("查询到未完成的作业：%d" % (exercise_id[now_courseid][i]))
                        self.assertEqual(result_text["exercises"]["id"],exercise_id[now_courseid][i])
                        work_type = result_text["exercises"]["type"]
                        #**************************************
                        if work_type == "book":
                            save_paras1 = commonfunction.setupRequest().split_paras("exerciseId", exercise_id[now_courseid][i],
                                                                                        saveWork_random,
                                                                                        huibenpara.base_para)
                            save_para2 = {**save_paras1, **{"courseId": str(now_courseid)}}
                            save_paras3={**save_para2,**{"workType":str(work_type)}}
                            save_paras={**save_paras3,**{"workContent":str(book_workContent)}}
                            save_result = requests.post(saveWork_url, data=save_paras).json()
                            self.assertEqual(save_result["resultCode"], '0')
                                #exercise=exercise_id[now_courseid][i]
                            get_paras= commonfunction.setupRequest().split_paras("exerciseId",exercise,getWork_random,huibenpara.base_para)
                            #print('xdd=%s'%get_paras)
                            get_result = requests.post(url, data=get_paras).json()
                            self.assertEqual(get_result["data"]["userWorks"][0]["exerciseId"],exercise_id[now_courseid][i])
                        else:
                            save_paras1 = commonfunction.setupRequest().split_paras("exerciseId",
                                                                                        exercise_id[now_courseid][i],
                                                                                        saveWork_random,
                                                                                        huibenpara.base_para)
                            save_paras2 = {**save_paras1, **{"courseId": str(now_courseid)}}
                            save_paras3 = {**save_paras2, **{"workType": str(work_type)}}
                            save_paras = {**save_paras3, **{"workContent": str(image_workContent)}}
                            save_result = requests.post(saveWork_url, data=save_paras).json()
                            self.assertEqual(save_result["resultCode"], '0')
                            #exercise = exercise_id[now_courseid][i]
                            get_paras1 = commonfunction.setupRequest().split_paras("exerciseId",exercise,getWork_random,huibenpara.base_para)
                            get_paras = {**get_paras1, **{"courseId": str(now_courseid)}}
                            get_result = requests.post(url, data=get_paras).json()
                            self.assertEqual(get_result["data"]["userWorks"][0]["exerciseId"],exercise_id[now_courseid][i])
    # @classmethod
    # def tearDown(self):



