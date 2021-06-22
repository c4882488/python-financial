# -*- coding: UTF-8 -*-

# 載入函數
from styem.GetOriginalData import getKbar
import datetime
from talib import SMA,STDDEV
import numpy as np

class GetData():
    def tradingtrends(stock,sdate,edate,d1,d2,c1,c2,c3):
        # 取得資料
        KBar=getKbar('./styem/'+stock+'.csv')

        # 計算移動平均線 、 標準差 、 低點 、 高點
        KBar['MA'] = SMA(KBar['close'], timeperiod= 120)
        KBar['STD'] = STDDEV(KBar['close'], timeperiod= 120)
        KBar['BD'] = KBar['MA']-0.75*KBar['STD']
        KBar['BU'] = KBar['MA']+0.75*KBar['STD']

        # 初始資金
        InitCapital=1000000
        # 進場價格 、 進場數量
        OrderPrice = None
        OrderQty = 0
        # 出場價格
        CoverPrice = None
        # 停損 、 停利價
        StopLoss = None
        TakeProfit = None
        # 總獲利 、 交易次數
        TotalProfit = []
        TotalTreadeNum = 0
        data = {
                '買進時間': [], 
                '買進原因': [],
                '買進價格': [],
                '售出時間': [],
                '售出價格': [],
                '售出原因': [],
                '數量': [],
                '獲利': [],#[(CoverPrice-OrderPrice)*OrderQty*1000],
                '累積獲利':[]
                }

        for i in range(len(KBar['date'])):
            Date = KBar['date'][i]
            Close = KBar['close'][i]
            LastClose = KBar['close'][i-1]
            MA = KBar['MA'][i]
            LastMA = KBar['MA'][i-1]
            BD = KBar['BD'][i]
            LastBD = KBar['BD'][i-1]
            BU = KBar['BU'][i]
            LastBU = KBar['BU'][i-1]
            # 進場條件
            if LastClose < LastBD and Close >= BD and OrderQty == 0  and d1 == 1:
                # 進場時間、價格、數量
                OrderDate = KBar['date'][i+1]
                OrderPrice = KBar['open'][i+1]
                OrderQty = int(InitCapital/(Close)/1000)
                # 停損價、停利價
                StopLoss = OrderPrice *0.8
                TakeProfit = OrderPrice *1.6
                #print( '低點 買進時間:', OrderDate.strftime('%Y/%m/%d') , '買進價格:',OrderPrice , '買進數量:' ,OrderQty )
                status = ' 低點 '
                data['買進時間'].append(OrderDate.strftime('%Y/%m/%d')) #字典的append（新增)鍵值
                data['買進原因'].append(status)
                data['買進價格'].append(OrderPrice)
                data['數量'].append(OrderQty)
            # 順勢 進場條件
            if LastClose < LastMA and Close >= MA*1.01 and OrderQty == 0 and d2 == 1:
                # 進場時間、價格、數量
                OrderDate = KBar['date'][i+1]
                OrderPrice = KBar['open'][i+1]
                OrderQty = int(InitCapital/(Close)/1000)
                # 停損價、停利價
                StopLoss = OrderPrice *0.8
                TakeProfit = OrderPrice *1.6
                #print( '順勢 買進時間:', OrderDate.strftime('%Y/%m/%d') , '買進價格:',OrderPrice , '買進數量:' ,OrderQty )
                status = ' 順勢 '
                data['買進時間'].append(OrderDate.strftime('%Y/%m/%d')) #字典的append（新增)鍵值
                data['買進原因'].append(status)
                data['買進價格'].append(OrderPrice)
                data['數量'].append(OrderQty)
            # 高點賣出
            elif OrderQty != 0 and LastClose > LastBU and Close <= BU and c3 == 1:
                # 出場時間、價格
                CoverDate = KBar['date'][i+1]
                CoverPrice = KBar['open'][i+1]
                # 績效紀錄
                Profit = (CoverPrice-OrderPrice)*OrderQty*1000
                TotalProfit += [Profit]
                TotalTreadeNum += 1
                # InitCapital += Profit
                # 下單數量歸零，重新進場
                OrderQty = 0
                #print( '高點 售出時間:', CoverDate.strftime('%Y/%m/%d') , '售出價格:' , CoverPrice ,'獲利:',Profit  )
                status = ' 高點 '
                data['售出時間'].append(CoverDate.strftime('%Y/%m/%d'))
                data['售出原因'].append(status)
                data['售出價格'].append(CoverPrice)
                data['獲利'].append(Profit)
                data['累積獲利'].append(sum(data['獲利']))
            # 停損判斷
            elif OrderQty != 0 and Close < StopLoss and c2 == 1:
                # 出場時間、價格
                CoverDate = KBar['date'][i+1]
                CoverPrice = KBar['open'][i+1]
                # 績效紀錄
                Profit = (CoverPrice-OrderPrice)*OrderQty*1000
                TotalProfit += [Profit]
                TotalTreadeNum += 1
                # InitCapital += Profit
                # 下單數量歸零，重新進場
                OrderQty = 0
                #print( '停損 售出時間:', CoverDate.strftime('%Y/%m/%d') , '售出價格:' , CoverPrice ,'虧損:',Profit  )
                status = ' 停利 '
                data['售出時間'].append(CoverDate.strftime('%Y/%m/%d'))
                data['售出原因'].append(status)
                data['售出價格'].append(CoverPrice)
                data['獲利'].append(Profit)
                data['累積獲利'].append(sum(data['獲利']))
            # 停利判斷
            elif OrderQty != 0 and Close > TakeProfit and c1 == 1:
                # 出場時間、價格
                CoverDate = KBar['date'][i+1]
                CoverPrice = KBar['open'][i+1]
                # 績效紀錄
                Profit = (CoverPrice-OrderPrice)*OrderQty*1000
                TotalProfit += [Profit]
                TotalTreadeNum += 1
                # InitCapital += Profit
                # 下單數量歸零，重新進場
                OrderQty = 0
                #print( '停利 售出時間:', CoverDate.strftime('%Y/%m/%d') , '售出價格:' , CoverPrice ,'獲利:',Profit  )
                status = ' 停利 '
                data['售出時間'].append(CoverDate.strftime('%Y/%m/%d'))
                data['售出原因'].append(status)
                data['售出價格'].append(CoverPrice)
                data['獲利'].append(Profit)
                data['累積獲利'].append(sum(data['獲利']))
            # 回測時間結束，則出場
            elif OrderQty != 0 and i == len(KBar['date'])-1:
                # 出場時間、價格
                CoverDate = Date
                CoverPrice = Close
                # 績效紀錄
                Profit = (CoverPrice-OrderPrice)*OrderQty*1000
                TotalProfit += [Profit]
                TotalTreadeNum += 1
                # InitCapital += Profit
                # 下單數量歸零，重新進場
                OrderQty = 0
                #print( '結束 售出時間:', CoverDate.strftime('%Y/%m/%d') , '售出價格:' , CoverPrice ,'盈虧:',Profit  )
                status = ' 結束 '
                data['售出時間'].append(CoverDate.strftime('%Y/%m/%d'))
                data['售出原因'].append(status)
                data['售出價格'].append(CoverPrice)
                data['獲利'].append(Profit)
                data['累積獲利'].append(sum(data['獲利']))

        #print( '交易次數:' , TotalTreadeNum , '總盈虧:', sum(TotalProfit) )
        KPI_dict = {'交易次數' : [TotalTreadeNum],
                    '總盈虧' : [sum(TotalProfit)],
                    'data' :data
                    }
        return KPI_dict

#import matplotlib.pyplot as plt # 匯出績效圖表
#ax = plt.subplot(111)           # 新增繪圖圖片
#ax.plot( np.cumsum(TotalProfit), 'k-' )      # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
#plt.show()                      # 顯示圖案