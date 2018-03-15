# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 下午 03:18
# @Author  : Yuhsuan
# @File    : clusting_tree_analysis.py
# @Software: PyCharm
import json
import re

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

from log_module import log

def read_json(json_file_path):
    dict = {}
    with open(json_file_path, "r") as openfile:
        dict = json.load(openfile)
    return dict

def analysis_connection(SOURCE_DATA,threshold):
    # 會先依據每天的資料中，往後找到有關連性的群組
    # 比如第一天有三個群組，第一個群組會根據門檻值去尋找有符合的第一個關聯
    # 找到後就跳出換第二個群
    nodes = []
    nodes_brexit = []
    nodes_catalan = []
    nodes_crimea = []
    nodes_gravitational = []
    nodes_hk = []
    nodes_missile = []
    nodes_sewol = []
    nodes_syria = []
    nodes_turkish = []

    edges = []

    for single_day in SOURCE_DATA["daily_data"]:
        # 顯示處理第幾天的資料
        log("第幾天的資料: %s" % single_day["day"])
        # 用來記錄共有多少個要比對的資料
        file_info_len = len(single_day["file_info"])
        compare_day = single_day["compare_day"]
        compare_day_len = len(compare_day)
        log("共有幾個群組資料: %s" % file_info_len)
        # 用來儲存比對出來的資料
        single_day_compare_result = ["" for i in range(file_info_len)]

        # 用來記錄有多少節點的資料
        for i in range(len(single_day["file_info"])):
            pattern = re.compile(".*_(.*)_\d+.txt")
            m = re.match(pattern,single_day["file_info"][i])
            theme = m.group(1)
            if theme == "brexit":
                nodes_brexit.append(str(single_day["day"])+"-"+str(i))
            elif theme == "catalan":
                nodes_catalan.append(str(single_day["day"])+"-"+str(i))
            elif theme == "crimea":
                nodes_crimea.append(str(single_day["day"])+"-"+str(i))
            elif theme == "gravitational":
                nodes_gravitational.append(str(single_day["day"])+"-"+str(i))
            elif theme == "hk":
                nodes_hk.append(str(single_day["day"])+"-"+str(i))
            elif theme == "missile":
                nodes_missile.append(str(single_day["day"])+"-"+str(i))
            elif theme == "sewol":
                nodes_sewol.append(str(single_day["day"])+"-"+str(i))
            elif theme == "syria":
                nodes_syria.append(str(single_day["day"])+"-"+str(i))
            elif theme == "turkish":
                nodes_turkish.append(str(single_day["day"])+"-"+str(i))
            # nodes.append(str(single_day["day"])+"-"+str(i))

        # 從第一個群組開始找相對應符合門檻的資料
        for source_group in range(file_info_len):
            for compare_daily_data in compare_day:
                compare_file_info_len = len(compare_daily_data["file_info"])
                process_group = compare_daily_data["process_group"]
                process_group_len = len(compare_daily_data["process_group"])

                cos = compare_daily_data["cos"]
                tf_idf = compare_daily_data["tf_idf"]
                tf_pdf = compare_daily_data["tf_pdf"]

                for i in range(process_group_len):
                    if process_group[i][0] == source_group and tf_idf[i]>=(threshold/100):
                        if single_day_compare_result[source_group] == "":
                            edges.append((str(single_day["day"])+"-"+str(source_group),str(compare_daily_data["day"])+"-"+str(process_group[i][1])))
                            single_day_compare_result[source_group] = "Source Day: %s, Source Group: %s, Compare Day: %s, Compare Group: %s" % (single_day["day"],source_group,compare_daily_data["day"],process_group[i][1])

        log(single_day_compare_result,lvl="i")

    nodes.append(nodes_brexit)
    nodes.append(nodes_catalan)
    nodes.append(nodes_crimea)
    nodes.append(nodes_gravitational)
    nodes.append(nodes_hk)
    nodes.append(nodes_missile)
    nodes.append(nodes_sewol)
    nodes.append(nodes_syria)
    nodes.append(nodes_turkish)

    # 透過關聯找出分群
    node_list = []
    for i in nodes:
        node_list.extend(i)

    clust_temp = {}
    for i in range(len(node_list)):
        clust_temp[i]=[node_list[i]]

    for relation in edges:
        # 定位第一個元件的位置
        pos1=0
        for i in range(len(node_list)):
            if relation[0] in clust_temp[i]:
                pos1 = i
                break
        # 定位第二個元件的位置
        pos2=0
        for i in range(len(node_list)):
            if relation[1] in clust_temp[i]:
                pos2 = i
                break

        if pos1 != pos2:
            clust_temp[pos1].extend(clust_temp[pos2])
            clust_temp[pos2]=[]
    # print(clust_temp)

    clust_res = {}
    id = 0
    for i in range(len(clust_temp)):
        if clust_temp[i]!=[] and len(clust_temp[i])>1:
            clust_res[id]=clust_temp[i]
            id=id+1

    for i in range(len(clust_res)):
        clust_res[i].sort()
    print(clust_res)
    group_file_list(clust_res,threshold)
    return nodes,edges

def find_files(item,DICT):
    group_file_list = []
    pattern = "(\d+)-(\d+)"
    pattern = re.compile(pattern)
    m = re.match(pattern,item)

    number_day = m.group(1)
    number_group = m.group(2)

    for i in DICT:
        if i['day'] == int(number_day):
            file_list = i['group'][number_group]
            for file in file_list:
                # print(i['file_list'][(file-1)])
                group_file_list.append(i['file_list'][(file-1)])
    return group_file_list


def group_file_list(group_list,threshold):
    GROUP_FILE_LISTS = {}
    group_file_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\first_clusting_result.json"
    file_reference_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\file_reference.json"
    DICT = read_json(group_file_path)
    for i in group_list:
        GROUP_FILE_LISTS[i]=[]
        for j in group_list[i]:
            # print("j: %s" % j)
            res = find_files(j,DICT)
            GROUP_FILE_LISTS[i].extend(res)

    # 最後分群出來的檔案們
    log("GROUP_FILE_LISTS:\n%s" % GROUP_FILE_LISTS,lvl="i")

    # 儲存一份還沒轉換前的資料
    group_file_result_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\final_group_file_reference\\"+str(threshold)+".json"
    with open(group_file_result_path, "w") as file:
        json.dump(GROUP_FILE_LISTS, file)

    # 載入比對的檔案們
    file_reference = []
    with open(file_reference_path,"r") as file:
        file_reference = json.load(file)
    log("file_reference:\n%s" % file_reference, lvl="i")


    # 進行最後的檔案轉換
    for i in GROUP_FILE_LISTS:
        for file_list in range(len(GROUP_FILE_LISTS[i])):
            for reference in file_reference:
                # print(reference[1].replace("\\","/"))
                # print(GROUP_FILE_LISTS[i][file_list])
                pattern = ".*\/(.*.txt)"
                pattern = re.compile(pattern)
                m = re.match(pattern,GROUP_FILE_LISTS[i][file_list])
                if m.group(1) in reference[1].replace("\\","/"):
                    GROUP_FILE_LISTS[i][file_list] = reference[0]
    print(GROUP_FILE_LISTS)

    group_file_result_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\final_group_file\\"+str(threshold)+".json"
    with open(group_file_result_path,"w") as file:
        json.dump(GROUP_FILE_LISTS,file)

def draw_tree(nodes, edges,threshold):
    # pos = nx.get_node_attributes(G, 'pos')
    # print(pos)
    # nodes = [(1,0),"1-1","1-2","2-1","2-3"]
    # edges = [((1,0),"1-1"),((1,0),"2-3")]
    # labels = nodes
    # G.add_nodes_from(nodes,labels=labels)
    # G.add_edges_from(edges)
    #
    # pos = {}
    # for i in nodes:
    #     # pos[i] = [int(i[0]),int(i[2])]
    #     if type(i) is tuple:
    #         pos[i] = [i[0],i[1]]
    #     else:
    #         pos[i] = [(i[0]), (i[2])]
    # pos = nx.get_node_attributes(G, 'pos')
    # pos = nx.spring_layout(G)
    # nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_nodes(G, pos)
    # nx.draw_networkx_labels(G, pos)

    G = nx.Graph()

    pos = {}

    pattern = "(\d+)\-(\d+)"
    pattern = re.compile(pattern)

    # print("mcolors: %s" % mcolors)
    colors = list(dict(**mcolors.CSS4_COLORS))
    for node in range(len(nodes)):
        color = colors[node*2-2]
        G.add_nodes_from(nodes[node])

        for i in nodes[node]:
            m = re.match(pattern,i)
            if int(m.group(1))%2 == 1:
                pos[i] = [int(m.group(1)),int(m.group(2))*2-0.3]
            else:
                pos[i] = [int(m.group(1)), int(m.group(2))+0.5]
        print(nodes[node])
        point = nx.draw_networkx_nodes(G,pos,nodelist=nodes[node],node_color=color)
        point.set_edgecolor('#000000')

    print(pos)
    print(edges)
    G.add_edges_from(edges)

    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    # nx.draw(G, pos,with_labels=True)

    fig = plt.gcf()
    fig.set_size_inches(100,20)
    plt.axis('off')
    plt.savefig('C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\file\\'+str(threshold)+'.jpg', dpi=100)
    # plt.show()
    # plt.cla()

def main(json_file_path,threshold):
    SOURCE_DATA = read_json(json_file_path)
    nodes, edges = analysis_connection(SOURCE_DATA,threshold)
    # print(edges)
    draw_tree(nodes, edges,threshold)

if __name__ == "__main__":
    json_file_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\clusting_tree_values.json"
    for i in range(1,100):
        threshold = i
        main(json_file_path,threshold)
