#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:34:57 2017

@author: J. C. Vasquez-Correa
"""

import numpy as np


def prob_list(list_words, list_all, prob_list):
    prob=np.zeros(len(list_words))
    for i in range(len(list_words)):
        chosen_=list_words[i]
        pos_all=0
        for j in range(len(list_all)):
            if list_all[j]==chosen_:
                pos_all=j
                break
        prob[i]=prob_list[pos_all]
    return prob



def compute_prob_city(linea, list_city, list_type_city, prob_linea_city):
    prob_city=np.zeros(len(list_city))
    
    for k in range(len(list_city)):
        foundlinea=False
        chosen_=list_city[k]+" "+linea
        for j in range(len(list_type_city)):
            if list_type_city[j]==chosen_:
                pos_all=j
                foundlinea=True
                break
        if foundlinea:
            prob_city[k]=prob_linea_city[pos_all]
        else: prob_city[k]=0
    return prob_city




def top_list(word_list, number, flag_order=1):
    word_counter = {}
    for word in word_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    if flag_order==1:
        top = popular_words[:number]
    else:
        top1 = popular_words[::-1]
        top=top1[:number]
    return top



def compute_prob(line_list, all_list, flag_prob):
    word_counter = {}
    list_f={}
    counter_rob=np.zeros(len(line_list))
    for word in line_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
            list_f[word]=word
    for i in range(len(line_list)):
        counter_rob[i]=word_counter[line_list[i]]

    if flag_prob:
        prob=np.zeros(len(all_list))
        for j in range(len(all_list)):
            prob[j]=word_counter[all_list[j]]/len(line_list)

    else:
        word_counter_all = {}
        all_listf={}
        for word in all_list:
            if word in word_counter_all:
                word_counter_all[word] += 1
            else:
                word_counter_all[word] = 1
                all_listf[word]=word
        prob=np.zeros(len(all_list))
        for i in range(len(all_list)):
            prob[i]=word_counter_all[all_list[i]]/counter_rob[i]

    return prob
