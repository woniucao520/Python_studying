# encoding:utf-8
#实力13:打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。
# 例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。
# for i in range (100,1000):
#     a = (i/100) #取百位
#     b =(i/10)%10 #取上位  # '/'取商,'%'取余数
#     c=i%10 # 取个位
#     s1=a**3 + b**3 +c**3
#     s2 = 100*a +10 *b +c
#     if s1 == s2:
#         print i

# 判断101-200之间有多少个素数，并输出所有素数
#只有1和本身
# list =[]
#
# for i in range (101,201,2):
#     for j in range(2,15):
#         if i % j == 0:
#            # leap = 0
#            break
#     else:
#         print i
'''
方法二
'''
import math

# def sushu():
#     result = []
#     for i in range (101,201,2):
#         flag = True
#         k = math.sqrt(i)
#         k = int(k)
#         for j in range(2,k+1):
#             if i % j ==0:
#                 flag= False
#                 continue
#         if flag == True:
#             result.append(i)
#             print result
# sushu()

# 实例15:利用条件运算符的嵌套来完成此题：学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。
# def score():
#     number = int(raw_input("please input the number:\n" ))
#     if number>= 90:
#         print ("该同学得到的等级为A")
#     elif 60<=number<=89:
#         print ("该同学得到的等级为B")
#     else:
#         print('该同学得到的等级为C')
# score()

#实例16: 输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。
# import re
# def count():
#     strNum= (raw_input("please input the string:\n" ))
#     strNum = ''.join(strNum)
#     zimu =re.findall(r'[a-zA-Z]',strNum)
#     shuzi = re.findall(r'[0-9]',strNum)
#     blank = re.findall(' ',strNum)
#     other =len(strNum)- len(zimu)-len(shuzi)-len(blank)
#     print ("字母的个数为%s")%(len(zimu))
#     print ("数字的个数为%s") % (len(shuzi))
#     print ("空格的个数为%s") % (len(blank))
#     print ("其他的特殊字符个数为%s") % (other)
# count()
# 实力17求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字
def SumNum():
    a = (raw_input("输入需要加的数字:\n" ))
    a=int(a)
    sum=a
    b = (raw_input("输入需要循环的次数:\n" ))
    b=int(b)
    list = []
    for i in range(1,b+1):
        n=sum
        sum = 10*n + a
        list.append(n)
    all = 0
    for j in list:
        all  = all+j
        print all
SumNum()


