import time as t
import pandas as pd #如何安装pandas

# 计算两个坐标之间的距离
def get_distance(addr1, addr2):
    x1, y1 = addr1
    x2, y2 = addr2
    distance = (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    #print(f"地址{addr1}和{addr2}之间的距离是{distance}吉米") 
    return distance

# 拉格朗日的坐标为(X,Y),每一小格(基地、前哨所在单位)在坐标上再细分为10，如(3066, 4081)可以理解为(306.6, 408.1)。
# 拉格朗日的曲率落点选择：自动计算与坐标所在小格4个顶点的距离，最近的为曲率落点。

def get_placement(begin_addr, target_addr): #通过设置起飞坐标和目标坐标，获取目标所在小格的左下角坐标和曲率落点所在的顶角。
    angle = [(target_addr[0]//10*10,(target_addr[1]//10*10) + 10),(target_addr[0]//10*10,target_addr[1]//10*10),(target_addr[0]//10*10+10,target_addr[1]//10*10+10),(target_addr[0]//10*10+10,target_addr[1]//10*10)] #定义4地址列表，用于存放目标点4个顶点的坐标

    distance = [get_distance(begin_addr, target_addr),get_distance(begin_addr, angle[0]),get_distance(begin_addr, angle[1]),get_distance(begin_addr, angle[2]),get_distance(begin_addr, angle[3])] #定义5数值列表，用于存放起飞点到目标点和目标点4个角的距离
    
    #获取distance中最小值的索引，即为曲率落点。
    down_point_index = distance.index(min(distance[1:4]))   #获取目标所在小格曲率落点角的索引，1为左上角，2为左下角，3为右上角，4为右下角。
    down_point_addr = angle[down_point_index-1]             #获取曲率落点的坐标
    print(f"地址{begin_addr}到{target_addr}的曲率落点是{down_point_addr}")
    print(f"曲率落点所在小格的左下角坐标为{angle[1]},落点角为{down_point_index}。(注：1为左上角，2为左下角，3为右上角，4为右下角)")
    return down_point_addr      #返回曲率落点角坐标。  
        
def get_outpost_addr(begin_addr, target_addr,outpost_addr_x = 0,outpost_addr_y = 0):    #通过设置起点坐标、目标坐标和前哨的坐标X或者Y，获取前哨的坐标。
    x1, y1 = begin_addr
    x2, y2 = target_addr
       
    k = (y2 - y1) / (x2 - x1)   #斜率k = (y2 - y1)/(x2 - x1)
    b = y1 - k * x1             #斜率公式 y = kx + b, b = y - kx

    while outpost_addr_x == 0 and outpost_addr_y == 0 :
        outpost_addr_x = int(input("请输入前哨的X坐标: "))
        
        while outpost_addr_x != 0 and outpost_addr_y == 0 :
            outpost_addr_y = k * outpost_addr_x + b
            print(f"前哨坐标为({outpost_addr_x},{outpost_addr_y})")
            return outpost_addr_x,outpost_addr_y
        
        utpost_addr_xy = int(input("请输入前哨的Y坐标: "))
        while outpost_addr_x == 0 and outpost_addr_y != 0 :
            outpost_addr_x = (outpost_addr_y - b)/k
            print(f"前哨坐标为({outpost_addr_x},{outpost_addr_y})")
            return outpost_addr_x,outpost_addr_y
    else:
        if outpost_addr_x != 0 :
            outpost_addr_y = k * outpost_addr_x + b
            print(f"前哨坐标为({outpost_addr_x},{outpost_addr_y})")
            return outpost_addr_x,outpost_addr_y
        elif outpost_addr_y != 0:
            outpost_addr_x = (outpost_addr_y - b)/k
            print(f"前哨坐标为({outpost_addr_x},{outpost_addr_y})")
            return outpost_addr_x,outpost_addr_y
        

def get_begin_addr(outpost_addr, target_addr,begin_addr_x):    #通过设置前哨曲率坐标、目标坐标和起飞坐标X，获取直接拍面的起飞坐标：）
    x1, y1 = outpost_addr
    x2, y2 = target_addr
       
    k = (y2 - y1) / (x2 - x1)   #斜率k = (y2 - y1)/(x2 - x1)
    b = y1 - k * x1             #斜率公式 y = kx + b, b = y - kx

    begin_addr_y = k * begin_addr_x + b
    print(f"起飞坐标为({begin_addr_x},{int(begin_addr_y)})")
    return begin_addr_x,int(begin_addr_y)
    
def get_need_time(distance,speed):  #通过设置距离和速度获取需要的时间，以分钟为单位
    return (distance * 10000)/speed

# pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚

# df = pd.read_csv(
#     filepath_or_buffer = r'data\database.csv', 
#     encoding='utf8', 
#     sep=',',
#     #index_col=['user_name']
# )  # 从csv文件中读取数据

# print(df)

# i = 0
# while i < df.shape[0] :
#     print(df.loc('暴行'))
#     df['outpost_addr'][i] = (2000,2000)
#     print(df['outpost_addr'][i])
#     print(i)
#     i += 1
# #介绍一下Series，它是一种类似于一维数组的对象，由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成。
# exit()

target_addr = (1175,3154) #目标坐标

print('疯风')
begin_addr = (1600, 3246) #起飞坐标
base_addr = (3035,4075)           #设置疯风基地坐标

outpost_addr = get_outpost_addr(begin_addr, target_addr,505,0)
begin_addr = get_begin_addr(get_placement(begin_addr,outpost_addr), target_addr,1600) #获取起飞坐标

distance = get_distance(begin_addr,target_addr) #获取起飞点到目标点的距离
speed = 2500    #设置舰船曲率速度

need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
print(f"地址{begin_addr}到{target_addr}的距离是{distance}吉米，速度是{speed}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

#通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
end_time = t.strptime("2013-05-22 08:00:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
print(f"出发时间为：{start_time}")     

#增援舰队
distance = get_distance(base_addr,target_addr) #获取基地到目标点的距离
speed = 2000*5    #设置舰船曲率速度

need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
print(f"基地{base_addr}到{target_addr}的距离是{distance}吉米，速度是{speed*5}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

#通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
end_time = t.strptime("2013-05-22 08:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
print(f"增援出发时间为：{start_time}") 

print('暴行')
begin_addr = (1600, 3241) #起飞坐标
base_addr = (3035,4095)           #设置暴行基地坐标

outpost_addr = get_outpost_addr(begin_addr, target_addr,515,0)
get_begin_addr(get_placement(begin_addr,outpost_addr), target_addr,1600) #获取起飞坐标

distance = get_distance(begin_addr,target_addr) #获取起飞点到目标点的距离
speed = 2500    #设置舰船曲率速度

need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
print(f"地址{begin_addr}到{target_addr}的距离是{distance}吉米，速度是{speed}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

#通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
end_time = t.strptime("2013-05-22 08:00:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
print(f"出发时间为：{start_time}")     

#增援舰队
distance = get_distance(base_addr,target_addr) #获取基地到目标点的距离
speed = 2000*5    #设置舰船曲率速度

need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
print(f"基地{base_addr}到{target_addr}的距离是{distance}吉米，速度是{speed*5}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

#通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
end_time = t.strptime("2013-05-22 08:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
print(f"增援出发时间为：{start_time}") 

#增援舰队
distance = get_distance(base_addr,target_addr) #获取基地到目标点的距离
speed = 2250*5    #设置舰船曲率速度

need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
print(f"基地{base_addr}到{target_addr}的距离是{distance}吉米，速度是{speed*5}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

#通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
end_time = t.strptime("2013-05-22 08:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
print(f"增援出发时间为：{start_time}") 