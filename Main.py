from GenerateData import GenerationData
from SolverSAA import SAA, SAA_Test
from SolverDRO import DRO, DRO_Test
import scipy.stats as stats
import numpy as np
import random
import os
import pickle

class TrainAndTest():
    def __init__(self, DisType_Demand, DisParams_Demand, TrainSampleSize, CaseParams, Round):
        self.DisType = DisType_Demand
        self.DisParams_Demand = DisParams_Demand
        self.TrainSampleSize = TrainSampleSize
        self.CaseParams = CaseParams
        self.Round = Round
        self.AvgReward_SAA = []
        self.AvgReward_DRO = []
        self.avgReward_SAA = []
        self.avgReward_DRO = []
        self.train_SAA_ord = 0
        self.train_SAA_profit = 0
        self.train_DRO_ord = 0
        self.train_DRO_profit = 0
        self.Order_SAA = []
        self.Order_DRO = []
        self.Repeat_SAA = 0
        self.Repeat_DRO = 0

    def Train(self):
        TrainSet, _ = GenerationData(self.DisType, self.DisParams_Demand, self.TrainSampleSize)
        SAA_profit, Order_SAA = SAA(self.CaseParams, TrainSet, [0, 300])
        self.train_SAA_ord = Order_SAA
        self.Order_SAA.append(Order_SAA)
        self.train_SAA_profit = SAA_profit
        DRO_profit, Order_DRO = DRO(self.CaseParams, TrainSet)
        self.train_DRO_ord = Order_DRO
        self.Order_DRO.append(Order_DRO)
        self.train_DRO_profit = DRO_profit

    def CleanStore(self):
        self.avgReward_SAA = []
        self.avgReward_DRO = []

    def Test(self):
        _, TestSet = GenerationData(self.DisType, self.DisParams_Demand, self.TrainSampleSize)
        tempReward_SAA = SAA_Test(CaseParams=self.CaseParams, Order=self.train_SAA_ord, TestDemand=TestSet)
        tempReward_DRO = DRO_Test(CaseParams=self.CaseParams, Order=self.train_DRO_ord, TestDemand=TestSet)
        return [tempReward_SAA, tempReward_DRO]

    def StoreProfit(self, input, inner = True):
        if inner == True:
            self.avgReward_SAA.append(input[0])
            self.avgReward_DRO.append(input[1])
        else:
            self.AvgReward_SAA.append(input[0])
            self.AvgReward_DRO.append(input[1])

    def AvgPermance(self):
        m1 = np.mean(self.avgReward_SAA)
        m2 = np.mean(self.avgReward_DRO)
        return [m1, m2]

    def Evaluation(self):
        Temp_SAA = (np.array(self.AvgReward_SAA) / np.array(self.AvgReward_DRO) - 1) * 100
        Mean_SAA_Profit = np.round(np.mean(Temp_SAA), 2)
        ci_SAA_Profit = round(1.96 * np.std(Temp_SAA) / np.sqrt(len(Temp_SAA)), 2)
        self.Repeat_SAA = [Mean_SAA_Profit, ci_SAA_Profit]

    def Print(self):
        print('SAA performance relative to DRO | ', self.Repeat_SAA[0], "±", self.Repeat_SAA[1])
        print(' ')

    def Todo(self):
        for r in range(self.Round):
            self.Train()
            print("Rounnd", r)
            TestResult = self.Test()
            self.StoreProfit(TestResult, inner=True)
            AvgTProfit = self.AvgPermance()
            self.StoreProfit(AvgTProfit, inner=False)
        self.Evaluation()
        self.Print()

