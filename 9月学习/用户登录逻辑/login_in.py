# encoding=utf-8
import xlrd
import csv
'''

用户登陆
1）用户名与密码都正确，提示：登陆成功
2) 用户是否是黑名单，是的话，就退出
3）用户名不存在，提示 ： 此用户不存在
4) 用户名正确，密码不正确 ， 提示： 密码错误：请重新输入
5）输入3次 错误密码 ： 提示 ： 您输入密码错误已经超过3次

'''
# class Login_in(object):
#     pass
#
# if __name__ == '__main__':
#     object=Login_in()


# 输入用户名与密码  知识点;put 与 raw_input的区别
username= raw_input("plaese input your username:")

password = raw_input("please input your password:")
password = int(password)
# 读取F盘下的 excel表格   知识点：文件的 操作 # 注意反义字符“\\”
file_path= "E:\\test_user\\user_name.xlsx"
sheetname ="Sheet1"
dataresult = []
data_xlsl = xlrd.open_workbook(file_path)
table = data_xlsl.sheet_by_name(sheetname)
for i in range (0,table.nrows):
    dataresult.append(table.row_values(i))
# 将list转换成dict  重点
dict_result = []
for i in range(1,len(dataresult)):
    temp = dict(zip(dataresult[0],dataresult[i]))
    dict_result.append(temp)

n = 0

for news in dict_result:
    # if username==news.values()[1]:
    #     if password == news.values()[0]:
    #         print ("welcome to login")
    #         break
    #     else:
    #         print ("wrong password!")
    #         i = 0
    #         for count in range(0,2):
    #             count =count +1
    #             password2 =raw_input("please input your password again:")
    #             password2=int(password2)
    #             if password2 == news.values()[0]:
    #                 n = n+ 1
    #                 print ("welcome to login")
    #                 break
    #             else:
    #                 i = i +1
    #                 if count < 2:
    #                     n = n + 1
    #                     print("wrong password again")
    #         if i == 2:
    #             print (" password error more than 3 times")
    # if username != news.values()[1]:
    #     # username != news.values()[1]
    #     n=n+1
    #     print("username error")

    # if username != news.values()[1]:
    #     print ("your username is error")


    if password==news.values()[0] and username==news.values()[1]:
        print "username and password successful"

    if username !=news.values()[1] and password == news.values()[0]:

        print("your username or password is not correctly")
    # if username !=news.values()[1] and password != news.values()[0]:
    #     print("your username or password is not correctly")

    count = 0
    if username ==news.values()[1] and password != news.values()[0]:
        print ("your password is not correctly")
        for i in range (0,2):
            count=count+1
            password2 =raw_input("please input your password again:")
            password2=int(password2)
            if password2 == news.values()[0]:
                print ("welcome to login")
                break
            else:
                print ("password error")
            if count == 2:
                print ("password error more than 3 times")






