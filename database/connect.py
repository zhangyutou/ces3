import pymysql

def database_query(sentence):
    '''从数据库中取数据（MySQL语句）'''
    conn=pymysql.connect(host="218.78.3.151",user='xueduoduo',password='Xueduoduo@mysql!5788',db="huiben")
    cur=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sentence)
    data=cur.fetchall()
    cur.close()
    conn.close()
    return data



def lineQuery(sentence):
    '''查询数据库某一列保存为list(select 列 from 表)'''
    conn = pymysql.connect(host="218.78.3.151", user='xueduoduo', password='Xueduoduo@mysql!5788', db="huiben",charset='utf8')
    cs1 = conn.cursor()
    cs1.execute(sentence)
    datalist = []
    alldata = cs1.fetchall()
    for s in alldata:
        datalist.append(s[0])
    return datalist



def insertData(shell,line_name,values):
    '''向数据库中插入数据'''
    conn = pymysql.connect(host="218.78.3.151", user='xueduoduo', password='Xueduoduo@mysql!5788', db="huiben",
                           charset='utf8')
    cursor=conn.cursor()
    query = "INSERT INTO "+ shell + line_name + " "+"VALUES" +" "+values
    print(query)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

#p=insertData("plan_user_wroks","(contentId, userId)","(47,111180)")




