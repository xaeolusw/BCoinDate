import time as t
import pandas as pd

# 计算两个坐标之间的距离
def get_distance(addr1, addr2):
    x1, y1 = addr1
    x2, y2 = addr2
    distance = (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    #print(f"地址{addr1}和{addr2}之间的距离是{distance}吉米") 
    return distance

# 拉格朗日的坐标为(X,Y),每一小格(基地、前哨所在单位)在坐标上再细分为10，如(3066, 4081)可以理解为(306.6, 408.1)。
# 拉格朗日的曲率落点选择：自动计算与坐标所在小格4个顶点的距离，最近的为曲率落点。
# 获取起飞坐标曲率到目标坐标的曲率落点
def get_placement(begin_addr, target_addr):
    angle = [(target_addr[0]//10*10,(target_addr[1]//10*10) + 10),(target_addr[0]//10*10,target_addr[1]//10*10),(target_addr[0]//10*10+10,target_addr[1]//10*10+10),(target_addr[0]//10*10+10,target_addr[1]//10*10)] #定义4地址列表，用于存放目标点4个顶点的坐标

    distance = [get_distance(begin_addr, target_addr),get_distance(begin_addr, angle[0]),get_distance(begin_addr, angle[1]),get_distance(begin_addr, angle[2]),get_distance(begin_addr, angle[3])] #定义5数值列表，用于存放起飞点到目标点和目标点4个角的距离
    
    #获取distance中最小值的索引，即为曲率落点。
    down_point_index = distance.index(min(distance[1:4]))   #返回目标所在小格左下角坐标和曲率落点角的索引，1为左上角，2为左下角，3为右上角，4为右下角。
    down_point_addr = angle[down_point_index-1]             #获取曲率落点的坐标
    print(f"地址{begin_addr}到{target_addr}的曲率落点是{angle[distance.index(min(distance[1:4]))-1]}")
    print(f"曲率落点所在小格的左下角坐标为{angle[1]},落点角为{distance.index(min(distance[1:4]))}。(注：1为左上角，2为左下角，3为右上角，4为右下角)")
    #return angle[1],distance.index(min(distance[1:4]))      #返回目标所在小格左下角坐标和曲率落点角的索引，1为左上角，2为左下角，3为右上角，4为右下角。  
        
def get_outpost_addr(begin_addr, target_addr,outpost_addr_x = 0,outpost_addr_y = 0):    #通过设置前哨曲率坐标的X或者Y获取前哨曲率坐标
    x1, y1 = begin_addr
    x2, y2 = target_addr
       
    k = (y2 - y1) / (x2 - x1)   #斜率k = (y2 - y1)/(x2 - x1)
    b = y1 - k * x1             #斜率公式 y = kx + b, b = y - kx

    while outpost_addr_x == 0 and outpost_addr_y == 0 :
        outpost_addr_x = int(input("请输入前哨的X坐标: "))
        
        while outpost_addr_x != 0 and outpost_addr_y == 0 :
            outpost_addr_y = k * outpost_addr_x + b
            return outpost_addr_x,outpost_addr_y
        
        utpost_addr_xy = int(input("请输入前哨的Y坐标: "))
        while outpost_addr_x == 0 and outpost_addr_y != 0 :
            outpost_addr_x = (outpost_addr_y - b)/k
            return outpost_addr_x,outpost_addr_y    

def get_need_time(distance,speed):  #通过设置距离和速度获取需要的时间，以分钟为单位
    return (distance * 10000)/speed


pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚
df = pd.read_csv('/Users/aeolus/PythonProjects/BCoinDate/data/database.csv', encoding='utf8', parse_dates=['user_name'], low_memory=False)  # 从csv文件中读取数据

print(df)
exit()

begin_addr = (3094, 4063) #起飞坐标
target_addr = (1975,1455) #目标坐标
base_addr = (0,0)           #设置基地坐标

get_placement(begin_addr, get_outpost_addr(begin_addr, target_addr)) #打印前哨设置的信息。

distance = get_distance(begin_addr,target_addr)
speed = 2500

need_time = get_need_time(distance,speed)
print(f"地址{begin_addr}到{target_addr}的距离是{distance}吉米，速度是{speed}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

#通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
end_time = t.strptime("2013-05-19 12:00:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
print(f"出发时间为：{start_time}")     #
#strftime()函数的第一个参数是时间格式，第二个参数是时间戳。时间格式中的%H表示小时，%M表示分钟。localtime()函数的参数是时间戳，返回值是一个时间元组。time()函数的返回值是一个时间戳。
#strftime函数在那个库中：
#怎样将时间转换为时间戳：如12:00转换为720分钟，即12*60=720。编程语言中的时间函数为time()，时间格式化函数为strftime()。time()函数的返回值是一个时间戳。时间戳是从1970年1月1日0时0分0秒到现在的总秒数。
#怎样将2013-05-19 12:20:00转换为时间戳：如2013-05-19 12:20:00转换为时间戳，编程为time.mktime(time.strptime("2013-05-19 12:20:00","%Y-%m-%d %H:%M:%S"))。strptime()函数的第一个参数是时间字符串，第二个参数是时间格式。mktime()函数的参数是时间元组，返回值是一个时间戳。