# -*- coding: utf-8 -*-
# @Time    : 2017/12/16 下午11:10
# @Author  : Yuhsuan
# @File    : generate_day_one_samples.py
# @Software: PyCharm

# 將news_documents第一天的資料轉換成文字矩陣

from text_processor import *

# # 這個是將某些特定的的資料產生出來
# # 如果要把所有的資料都打開要把這個關閉
#
# day_one_data = [
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_cr_0.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_cr_1.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_hk_0.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_se_0.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_se_1.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_se_2.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_cr_0.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_hk_0.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_se_0.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_se_1.txt',
#
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_hk_1.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_3.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_4.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_5.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_6.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_7.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_8.txt',
#     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day1_cnn_se_9.txt',
# ]
# # 將第一天的資料產生文字矩陣後，放在news_documents_r中
# format_document(day_one_data)

# 這個是將所有的資料產生出來
# 如果要單一測試一個要把這個關閉
res = get_file_list('/Users/yuhsuan/Desktop/MEMDS/news_documents/')
format_document(res)