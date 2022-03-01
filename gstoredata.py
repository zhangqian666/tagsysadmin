# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2022/2/10 下午5:12
"""
# with open("./gstore_data_main.nt", encoding="utf-8", mode="a+") as f:
#     for i in range(100000):
#         f.write("<电影> <名称> <龙虎斗{}> .\n".format(i))
#     for i in range(100000):
#         f.write("<公司> <名称> <字节{}> .\n".format(i))
#
# with open("./gstore_data_other.nt", encoding="utf-8", mode="a+") as f:
#     for j in range(1):
#         for i in range(10000000):
#             f.write("<李白{}> <别名{}> \"李太白{}{}\" .\n".format(i, j, j, i))

# with open("./movie.csv", encoding="utf-8", mode="w") as f:
#     f.write("uuid:ID(movie),name:String,:Label\n")
#     for i in range(100000):
#         f.write("{},\"龙虎斗{}\",\"动作片\"\n".format(i, i))
#
# with open("./person.csv", encoding="utf-8", mode="w") as f:
#     f.write("uuid:ID(user),name:String,:Label\n")
#     for i in range(100000, 600000):
#         f.write("{},\"王明{}\",\"演员\"\n".format(i, i))
#
# with open("./res.csv", encoding="utf-8", mode="w") as f:
#     f.write("uuid:START_ID(movie),uuid:END_ID(user),:TYPE\n")
#
#     for i in range(100000):
#         f.write("{},{},action_in\n".format(i, 100000 + i * 5 + 0))
#         f.write("{},{},action_in\n".format(i, 100000 + i * 5 + 1))
#         f.write("{},{},action_in\n".format(i, 100000 + i * 5 + 2))
#         f.write("{},{},action_in\n".format(i, 100000 + i * 5 + 3))
#         f.write("{},{},action_in\n".format(i, 100000 + i * 5 + 4))
#
#
# with open("./node.csv", encoding="utf-8", mode="w") as f:
#     f.write("uuid:ID(users),name:String,:Label\n")
#     for i in range(2000):
#         f.write("{},\"w\",l\n".format(i))
#
# with open("./res.csv", encoding="utf-8", mode="w") as f:
#     f.write("uuid:START_ID(users),uuid:END_ID(users),:TYPE\n")
#     for j in range(200):
#         for i in range(999):
#             f.write("{},{},R{}\n".format(j, i, j))
with open("./res.txt", encoding="utf-8", mode="w") as f:
    for i in range(200):
        f.write("MATCH (f:l{uuid:\"0\"}),(b:l{uuid:\"%d\"}) with f ,b  CREATE(f)-[:SS]->(b);\n" % i)
