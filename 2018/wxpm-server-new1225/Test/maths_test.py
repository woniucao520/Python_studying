# coding:utf-8
import datetime
import copy

# children 是该评论下的子评论
# main_list 是主评论

# 根据第一个id进行判断，该子评论位于哪个主评论下，然后追加到主评论下
children_list = [(10, 'hahah', '哎呀', datetime.datetime(2017, 12, 10, 7, 20, 25)),
                 (6, '天气好', '天气好', datetime.datetime(2017, 12, 20, 7, 24, 37)),
                 (6, '哎呦', '哎呦', datetime.datetime(2017, 12, 20, 7, 24, 18))]
main_list = [(6, '6', '6', datetime.datetime(2017, 12, 20, 7, 25, 13)),
             (10, '9', '9', datetime.datetime(2017, 12, 20, 7, 20, 25)),
             (9, '8', '8', datetime.datetime(2017, 12, 20, 7, 20, 20)),
             (7, '7', '7', datetime.datetime(2017, 12, 20, 7, 20, 16)),
             (5, '5', '5', datetime.datetime(2017, 12, 20, 7, 20, 7)),
             (4, '4', '4', datetime.datetime(2017, 12, 20, 7, 20, 3))]

mergeds = []
for m in main_list:
    li = []
    li.append(m)


    for r in children_list:
        if r[0] == m[0]:
            li.append(r)
            #print("*************")
    print(li)
    mergeds.append(li)
# print(mergeds)
    # mergeds.append(li)

# print mergeds
# for i in mergeds:
#     print i

my_list = []
for i in mergeds:
    if len(i)>1:

        i.remove (i[0])
        print (i)
        my_list.append(i)
#print (my_list)

# merged = []
# for m in main_list:
#     li=([],)
#     for r in children_list:
#         if r[0] == m[0]:
#             li[0].append(r)
#     merged.append(m+li)
# print (merged)

# for i in merged:
#      print(i)



# merged = [[(2, '2', '2', datetime.datetime(2017, 12, 21, 16, 30, 37)), (2, '测试', '测试', datetime.datetime(2017, 12, 21, 16, 24, 49)), (2, '你好', '你好', datetime.datetime(2017, 12, 21, 16, 22, 38))], [(7, '7', '7', datetime.datetime(2017, 12, 21, 14, 2, 21))], [(5, '5', '5', datetime.datetime(2017, 12, 21, 14, 0, 46)), (5, '看看bug', '看看bug', datetime.datetime(2017, 12, 21, 16, 25, 29))], [(3, '3', '3', datetime.datetime(2017, 12, 20, 7, 19, 56))], [(1, '1', '1', datetime.datetime(2017, 12, 20, 7, 19, 46))]]
# for m in main_list:
#     li=[]
#     li.append(m)
#     for r in children_list:
#         if r[0] == m[0]:
#             li.append(r)
#     merged.append(li)



# for mylist in merged:
#     if len(mylist)>1:
#         children_list =copy.deepcopy(mylist)

#         children_list.remove(children_list[0])
#         print children_list





