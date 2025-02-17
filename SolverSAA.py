import numpy as np
import os
import pickle

def SAA(CaseParams, demand, FeasibleSolRange):
    p1 = CaseParams[0]
    p2 = CaseParams[1]
    s1 = CaseParams[2]
    l1 = CaseParams[3]
    s2 = CaseParams[4]
    l2 = CaseParams[5]
    c = CaseParams[6]
    demand_1 = demand[0]
    demand_2 = demand[1]
    FeasibleSolLow = FeasibleSolRange[0]
    FeasibleSolUp = FeasibleSolRange[1]
    SAA_profit = 0
    SAA_order = 0
    for cur_x in range(FeasibleSolLow, FeasibleSolUp + 1):
        cur_f = 0
        for cur_d1_index in range(len(demand_1)):
            cur_f += p1 * min(cur_x, demand_1[cur_d1_index]) +p2 * min(cur_x, demand_2[cur_d1_index])+ s1 * max(cur_x - demand_1[cur_d1_index], 0)+ s2 * max(cur_x - demand_2[cur_d1_index], 0)- l1 * max(demand_1[cur_d1_index]-cur_x, 0)- l2 * max(demand_2[cur_d1_index]-cur_x, 0) - c * cur_x
        if cur_f > SAA_profit:
            SAA_profit = cur_f
            SAA_order = cur_x
    SAA_profit = 0
    for cur_d1_index in range(len(demand_1)):
        SAA_profit += p1 * min(SAA_order, demand_1[cur_d1_index]) + p2 * min(SAA_order, demand_2[cur_d1_index]) + s1 * max(
            SAA_order - demand_1[cur_d1_index], 0) + s2 * max(SAA_order - demand_2[cur_d1_index], 0) - l1 * max(
            demand_1[cur_d1_index] - SAA_order, 0) - l2 * max(demand_2[cur_d1_index] - SAA_order, 0) - c * SAA_order
    return SAA_profit/len(demand_1), SAA_order

def SAA_Opt(CaseParams, demand, FeasibleSolRange):
    p1 = CaseParams[0]
    p2 = CaseParams[1]
    s1 = CaseParams[2]
    l1 = CaseParams[3]
    s2 = CaseParams[4]
    l2 = CaseParams[5]
    c = CaseParams[6]
    demand_1 = demand[0]
    demand_2 = demand[1]
    FeasibleSolLow = FeasibleSolRange[0]
    FeasibleSolUp = FeasibleSolRange[1]
    SAA_profit = 0
    SAA_order = 0
    for cur_x in range(FeasibleSolLow, FeasibleSolUp + 1):
        cur_f = 0
        for cur_d1_index in range(len(demand_1)):
            cur_f += p1 * min(cur_x, demand_1[cur_d1_index]) +p2 * min(cur_x, demand_2[cur_d1_index])+ s1 * max(cur_x - demand_1[cur_d1_index], 0)+ s2 * max(cur_x - demand_2[cur_d1_index], 0)- l1 * max(demand_1[cur_d1_index]-cur_x, 0)- l2 * max(demand_2[cur_d1_index]-cur_x, 0) - c * cur_x
        if cur_f > SAA_profit:
            SAA_profit = cur_f
            SAA_order = cur_x
    SAA_profit = 0
    for cur_d1_index in range(len(demand_1)):
        SAA_profit += p1 * min(SAA_order, demand_1[cur_d1_index]) + p2 * min(SAA_order, demand_2[cur_d1_index]) + s1 * max(
            SAA_order - demand_1[cur_d1_index], 0) + s2 * max(SAA_order - demand_2[cur_d1_index], 0) - l1 * max(
            demand_1[cur_d1_index] - SAA_order, 0) - l2 * max(demand_2[cur_d1_index] - SAA_order, 0) - c * SAA_order
    return SAA_order

def SAA_Test(CaseParams, Order, TestDemand):
    p1 = CaseParams[0]
    p2 = CaseParams[1]
    s1 = CaseParams[2]
    l1 = CaseParams[3]
    s2 = CaseParams[4]
    l2 = CaseParams[5]
    c = CaseParams[6]
    demand_1 = TestDemand[0]
    demand_2 = TestDemand[1]
    SAA_profit = 0
    for i in range(len(demand_1)):
        SAA_profit += p1 * min(Order, demand_1[i]) +p2 * min(Order, demand_2[i])+ s1 * max(Order - demand_1[i], 0)+s2 * max(Order - demand_2[i], 0)- l1 * max(demand_1[i]-Order, 0)- l2 * max(demand_2[i]-Order, 0) - c * Order
    return SAA_profit/len(demand_1)

def SaveSAARes(SAA_Results, filename, path):
    file_path = os.path.join(path, filename)
    with open(file_path, 'wb') as file:
        pickle.dump(SAA_Results, file)
