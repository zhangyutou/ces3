import requests
from database import connect
import unittest



class setupRequest():

    def connect_paras(self,base_para,random_paras):
        '''拼接固定变量和随机变量'''
        paras={**base_para,**random_paras}
        return  paras

    def split_keypara(self,datalist,key,url_paras):    #
        '''拼接口参数'''
        if type(datalist)==list:
            values = []
            for i in range(len(datalist)):
                value = datalist[i][key]
                values.append(value)
            paras = []
            for i in range(len(datalist)):
                para = {**{key: str(values[i])}, **url_paras}
                paras.append(para)
            return paras
        else:
            print("split_keypara Error:(list,str,dict)")

    def get_result(self,url,before_datalist,key,url_paras,base_paras):
        '''取request结果'''
        paras=[]
        results=[]
        u_p=setupRequest().split_keypara(before_datalist,key,url_paras)
        for i in range(len(u_p)):
            random_paras = u_p[i]
            para = setupRequest().connect_paras(base_paras,random_paras)
            paras.append(para)
        for i in range(len(u_p)):
            result = requests.post(url, data=paras[i]).json()
            results.append(result)
        return results

    def split_paras(self,key,key_para,url_para,base_para):
        '''拼接key_para、url_para、base_url'''
        random_paras = {**{key: str(key_para)}, **url_para}
        paras = {**base_para, **random_paras}
        return paras




class previewData():

    def get_dict_data(self,para,data):
        '''把字典中的指定键值对取出来'''
        if type(data)==dict and type(para)==list:
            api_dealdata ={}
            self.para=para
            self.data=data
            for j in range(len(self.para)):
                api_dealdata_key=para[j]
                api_dealdata[api_dealdata_key]=self.data[api_dealdata_key]
            return api_dealdata
        else:
             print("get_dict_data Error:([key1,key2...]，dict)")

    def get_dict_datas(self,para,data):  #
        '''循环取list（多个字典）中的键值对'''
        if type(para)==list and type(data)==list :
            test_datas = []
            for i in range(len(data)):
                test_data = previewData().get_dict_data(para,data[i])
                test_datas.append(test_data)
            return test_datas
        else:
            print("get_dict_datas Error:([key1,key2...],[dict1,dict2...])")

    def get_dict_values(self,key,datalist):         #
        '''循环取list中某个键对应的值([{'a':{'b':'c'}},{'a':{'a':'d'}}])'''
        values=[]
        for i in range(len(datalist)):
            data=datalist[i]
            value=data[key]
            values.append(value)
        return values

    def get_values(self,data,key):
        '''取出list中多个字典中指定key对应的值'''
        values = []
        for i in range(len(data)):
            value = data[i][key]
            values.append(value)
        return values

    def get_list_listdict_data(self,data,key):
        '''取键值对[[{'a':'c'}}],[{'a':'d'}]]'''
        test_datas = []
        for i in range(len(data)):
            test_data = previewData.get_dict_data(self,key,data[i][0])
            test_datas.append(test_data)
        return test_datas

    def lld_len(self,list):
        '''查看元素个数（list含list）'''
        lists=[]
        for i in range(len(list)):
            llist=len(list[i])
            lists.append(llist)
        return lists

    def lld_getvalues(self,key,list):
        '''[{'c':'d'},{'c':'e'}]，取"c"对应的值'''
        values=[]
        for i in range(len(list)):
            value1=list[i]
            value2=value1[key]
            values.append(value2)
        return values

    def lddld_getvalues(self,first_key,second_key,key,value_key,data):
        '''把b作为键，从[{a:{m:n,b:[{c:d},{c:e}]}},{}]中取c对应的值'''
        value={}
        for i in range(len(data)):
            value1=data[i][first_key]
            value2=value1[second_key]
            value3=previewData().lld_getvalues(value_key,value2)
            turnkey=value1[key]
            value[turnkey]=value3
        return value

# a=[{'a':{'m':'35','b':[{'c':'d'},{'c':'e'}]}},{'a':{'m':'34','b':[{'c':'d'},{'c':'e'}]}}]
# b=previewData().lddld_getvalues('a','b','m','c',a)
# print(b)

class setupBasedata():

    def split_sentence(self,shell,key,values):
        '''拼接MySQL语句（指定shell、key:值）'''
        if len(values)==1:
            sentence = "select * from" + shell + "where" + key + "=" + str(values)
            return sentence
        else:
            sentences=[]
            for i in range(len(values)):
                sentence="select * from " + shell + " where " + key + "=" + str(values[i])
                sentences.append(sentence)
            return sentences

    def get_basedatas(self,shell,key,data):
        '''从数据库中取数据'''
        baseDatas=[]
        values=previewData().get_values(data,key)
        sentences=setupBasedata().split_sentence(shell,key,values)
        for i in range(len(values)):
            baseData=connect.database_query(sentences[i])
            baseDatas.append(baseData)
        return baseDatas

    def get_basedatas2(self,shell,apikey,basekey,data):
        '''从数据库中取数据apikey!=bsekey，data：list中含多个字典'''
        baseDatas=[]
        values=previewData().get_values(data,apikey)
        sentences = setupBasedata().split_sentence(shell, basekey, values)
        for i in range(len(values)):
            baseData = connect.database_query(sentences[i])
            baseDatas.append(baseData)
        return baseDatas

    def split_nolimit_sentence(self,shell,content,key,values):
        '''拼接MySQL语句（指定shell、key:值）'''
        sentence="select"+ " " + content + " " + "from" + " "+ shell + " where " + key + "=" +  str(values)
        return sentence

    def get_line_basedatas(self,shell,content,key,data):
        '''从数据库中取某列数据'''
        baseDatas=[]
        sentences=setupBasedata().split_nolimit_sentence(shell,content,key,data)
        baseData=connect.lineQuery(sentences)
        return baseData



class resultsAssert(unittest.TestCase):

    def assertcircle(self,codes,key,hope):
        '''多对一时循环断言([{'a':'0'},{'a':'0'}],'a','0')'''
        for i in range(len(codes)):
            self.assertEquals(codes[i][key],hope)
        return


