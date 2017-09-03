#coding:utf-8


# #实力7 如何将一个列表复制到另一个列表
# a = [1,4,7,9,10]
# b=[]
# for i in a:
#     b.append(i)
# print b
# # 使用[:]
# c = a[:]
# print c
#
# #实力8：输出9*9乘法表（分行，列考虑）
# for i in range(1,10):
#     print
#     for j in range(1,i+1):
#         print ('%s * %s = %s')%(i,j,i*j),
'''

如果想要不换行，之前的 2.x 版本可以这样 print x, 在末尾加上 ,
但在 3.x 中这样不起任何作用
要想换行你应该写成 print(x，end = '' )
'''
#实力10  暂停1s，再输出当前时间
# import time
# import datetime
#
# time.sleep(1)
# time_now = datetime.datetime.now()
# print ("当前时间为%s:" % time_now)
#实力11：古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，
# 小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？

# mun=10
# f1 = 1
# f2 =1
# list1 = []
# for i in range(3,mun,2):
#     f1=f1+f2
#     f2 =f1+f2
#     list1.append(f1)
#     # print ("第%s个月总共有%s对兔子") % (i, f1),list1
# a=1
# b=1
# list2=[]
# for i in range(4,mun,2):
#     a=a+b
#     b=a+b
#     list2.append(b)
#     # print ("第%s个月总共有%s对兔子")%(i,b),list2
# list3=[]
# list3=list1+list2
# result = sorted(list3)  #sorted([list])产生一个新对象，有返回值,b.sort()没有产生新的对象，所以返回none
# i =3
# for a in result:
#     print ("第%s个月总共有%s对兔子")%(i,a)
#     i=i+1

#判断101-200之间有多少个素数，并输出所有素数。

for i in range(101,201):
    for j in range(101,i+1):
        if i %2==0 and i%j==0:
            continue

        print i








