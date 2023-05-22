import time as t
import pandas as pd #如何安装pandas

# 计算两个坐标之间的距离
def get_distance(addr1, addr2):
    x1, y1 = addr1
    x2, y2 = addr2
    distance = (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    #print(f"地址{addr1}和{addr2}之间的距离是{distance}吉米") 
    return distance

# 计算两个坐标之间的斜率和截距
def get_k_b(addr1,addr2):
    x1, y1 = addr1
    x2, y2 = addr2
 
    k = (y2 - y1) / (x2 - x1)   #斜率k = (y2 - y1)/(x2 - x1)
    b = y1 - k * x1             #斜率公式 y = kx + b, b = y - kx
    return k,b

          
def get_outpost_addr(begin_addr, target_addr,outpost_addr_x = 0,outpost_addr_y = 0):    #通过设置起点坐标、目标坐标和前哨的坐标X或者Y，获取前哨的坐标。     
    k,b = get_k_b(begin_addr,target_addr)                                             #获取曲率线的斜率和截距。
   
    while outpost_addr_x == 0 and outpost_addr_y == 0 :     #如果前哨坐标x和y都为0，则输入坐标x或y。
        print("请输入前哨的坐标x或y！")
        outpost_addr_x = int(input("请输入前哨的x坐标: "))
        if outpost_addr_x == 0:
            outpost_addr_y = int(input("请输入前哨的y坐标: "))
       
    if outpost_addr_x == 0 and outpost_addr_y != 0:                             #如果前哨坐标x为0，前哨坐标y不为0，则通过坐标y计算坐标x。
        outpost_addr_x = (outpost_addr_y - b)/k
    elif outpost_addr_x != 0 and outpost_addr_y == 0:                           #如果前哨坐标x不为0，前哨坐标y为0，则通过坐标x计算坐标y。
        outpost_addr_y = k * outpost_addr_x + b

    #print(f"前哨坐标为({int(outpost_addr_x)},{int(outpost_addr_y)})")    
    return int(outpost_addr_x),int(outpost_addr_y)
    # print(f"前哨坐标为({outpost_addr_x},{outpost_addr_y})")    
    # return outpost_addr_x,outpost_addr_y
        
# 拉格朗日的坐标为(X,Y),每一小格(基地、前哨所在单位)在坐标上再细分为10，如(3066, 4081)可以理解为(306.6, 408.1)。
# 拉格朗日的曲率落点选择：自动计算与坐标所在小格4个顶点的距离，最近的为曲率落点。
def get_placement(begin_addr, target_addr):                                 #通过设置起飞坐标和目标坐标，获取目标所在小格的左下角坐标和曲率落点所在的顶角。
    angle = [(target_addr[0]//10*10,(target_addr[1]//10*10) + 10),(target_addr[0]//10*10,target_addr[1]//10*10),(target_addr[0]//10*10+10,target_addr[1]//10*10+10),(target_addr[0]//10*10+10,target_addr[1]//10*10)] #定义4地址列表，用于存放目标点4个顶点的坐标

    #计算起飞点到目标点及目标点4个角的距离，以distance[0]为起飞点到目标点的距离，distance[1]为起飞点到目标点左上角的距离，distance[2]为起飞点到目标点左下角的距离，distance[3]为起飞点到目标点右上角的距离，distance[4]为起飞点到目标点右下角的距离。
    distance = [get_distance(begin_addr, target_addr),get_distance(begin_addr, angle[0]),get_distance(begin_addr, angle[1]),get_distance(begin_addr, angle[2]),get_distance(begin_addr, angle[3])] #定义5数值列表，用于存放起飞点到目标点和目标点4个角的距离
    
    #获取distance中最小值的索引，即为曲率落点。1为左上角，2为左下角，3为右上角，4为右下角。
    down_point_index = distance.index(min(distance[1:4]))   
    down_point_addr = angle[down_point_index-1]             #获取曲率落点的坐标
    print(f"地址{begin_addr}到{target_addr}的曲率落点坐标为{down_point_addr}，落点所在小格的左下角坐标为{angle[1]},落点角为{down_point_index}。(注：1为左上角，2为左下角，3为右上角，4为右下角)")
    return down_point_addr      #返回曲率落点角坐标。  

# 3. 判定点在直线上方、下方还是在直线上:
def point_position(begin_addr, outpost_addr, target_addr):
    k,b = get_k_b(begin_addr,outpost_addr)
    x,y = target_addr

    if y == k * x + b:
        y = k * x + b
        return f'空投位置为({x},{y})，攻击目标{target_addr}在曲率线上'
    elif y > k * x + b:
        y = k * x + b
        return f'空投降落位置为({x},{y})，攻击目标{target_addr}在曲率线上方。'
    else:
        y = k * x + b
        return f'空投降落位置为({x},{y})，攻击目标{target_addr}在曲率线下方。'
    
def get_begin_addr(target_addr,outpost_addr,begin_addr_x):    #通过设置前哨曲率坐标、目标坐标和起飞坐标X，获取直接拍面的起飞坐标：）
    k,b = get_k_b(target_addr,outpost_addr) 
    
    begin_addr_y = k * begin_addr_x + b
    print(f"起飞坐标修正为({begin_addr_x},{begin_addr_y})")
    return begin_addr_x,begin_addr_y
    
def get_need_time(distance,speed):  #通过设置距离和速度获取需要的时间，以分钟为单位
    return (distance * 10000)/speed



pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚

df = pd.read_csv(
    filepath_or_buffer = r'data/database.csv', 
    encoding='utf8', 
    sep=',',
    #index_col=['user_name']
)  # 从csv文件中读取数据

print(df)

i = 0
while i < df.shape[0] :
    print(df[['user_name']],df['outpost_addr'])
    # df['outpost_addr'][i] = (2000,2000)
    # print(df['outpost_addr'][i])
    # print(i)
    i += 1
#介绍一下Series，它是一种类似于一维数组的对象，由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成。
exit()


target_addr = (1125,3104) #目标坐标

begin_addr = [(1600, 3239),(1600, 3241)] #起飞坐标
base_addr = [(3035,4075),(3035,4095)]      #设置基地坐标

outpost_addr = []
distance = [0,0]
speed = [0,0]
need_time = [0,0]
add_distance = [0,0]
add_speed = [0,0]
add_need_time = [0,0]
end_time = t.strptime("2013-05-22 17:00:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。

for i in range(0,2):
    x = 0
    
    if i == 0:
        print('疯风')
        x = 610
    else:
        print('暴行')
        x = 615
        
    outpost_addr.append(get_placement(begin_addr[i],get_outpost_addr(begin_addr[i], target_addr,x,0))) #获取前哨坐标,然后获取前哨曲率坐标
    print(outpost_addr[i])
    
    print(point_position(begin_addr[i], outpost_addr[i], target_addr))
    begin_addr[i] = get_begin_addr(target_addr, outpost_addr[i], 1600) #更新起飞坐标

    distance[i] = get_distance(begin_addr[i],target_addr) #获取起飞点到目标点的距离
    speed[i] = 2500    #设置舰船曲率速度
    need_time[i] = get_need_time(distance[i],speed[i])   #获取舰船从起飞点到目标点需要的时间
    print(f"地址{begin_addr[i]}到{target_addr}的距离是{distance[i]}吉米，速度是{speed[i]}米/分钟，需要{need_time[i]}秒。即{int(need_time[i]/3600)}小时{int(need_time[i]/60%60)}分钟{int(need_time[i]%60)}秒。")
    start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time[i])) #计算出发时间。
    print(f"出发时间为：{start_time}") 
    
    end_time2 = t.strptime("2013-05-22 17:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
    add_distance[i] = get_distance(base_addr[i],target_addr) #获取起飞点到基地点的距离
    add_speed[i] = 2000*5    #设置舰船曲率速度
    add_need_time[i] = get_need_time(add_distance[i],add_speed[i])   #获取舰船从起飞点到基地点需要的时间
    print(f"地址{base_addr[i]}到{target_addr}的距离是{add_distance[i]}吉米，速度是{add_speed[i]}米/分钟，需要{add_need_time[i]}秒。即{int(add_need_time[i]/3600)}小时{int(add_need_time[i]/60%60)}分钟{int(add_need_time[i]%60)}秒。")
    start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time2) - add_need_time[i])) #计算出发时间。
    print(f"增援出发时间为：{start_time}") 
        

exit()
# #增援舰队
# distance = get_distance(base_addr,target_addr) #获取基地到目标点的距离
# speed = 2000*5    #设置舰船曲率速度

# need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
# print(f"基地{base_addr}到{target_addr}的距离是{distance}吉米，速度是{speed*5}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

# #通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
# end_time = t.strptime("2013-05-22 08:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
# start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
# print(f"增援出发时间为：{start_time}") 

# print('暴行')
# outpost_addr = get_outpost_addr(begin_addr, target_addr,515,0)
# get_begin_addr(get_placement(begin_addr,outpost_addr), target_addr,1600) #获取起飞坐标

# distance = get_distance(begin_addr,target_addr) #获取起飞点到目标点的距离
# speed = 2500    #设置舰船曲率速度

# need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
# print(f"地址{begin_addr}到{target_addr}的距离是{distance}吉米，速度是{speed}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

# #通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
# end_time = t.strptime("2013-05-22 08:00:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
# start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
# print(f"出发时间为：{start_time}")     

# #增援舰队
# distance = get_distance(base_addr,target_addr) #获取基地到目标点的距离
# speed = 2000*5    #设置舰船曲率速度

# need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
# print(f"基地{base_addr}到{target_addr}的距离是{distance}吉米，速度是{speed*5}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

# #通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
# end_time = t.strptime("2013-05-22 08:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
# start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
# print(f"增援出发时间为：{start_time}") 

# #增援舰队
# distance = get_distance(base_addr,target_addr) #获取基地到目标点的距离
# speed = 2250*5    #设置舰船曲率速度

# need_time = get_need_time(distance,speed)   #获取舰船从起飞点到目标点需要的时间
# print(f"基地{base_addr}到{target_addr}的距离是{distance}吉米，速度是{speed*5}米/分钟，需要{need_time}秒。即{int(need_time/3600)}小时{int(need_time/60%60)}分钟{int(need_time%60)}秒。")

# #通过设定“到达时间”，“需要时间"，从而计算"出发时间"。如设定到达时间为12:00，需要时间为2小时18分钟，则出发时间为9:42。
# end_time = t.strptime("2013-05-22 08:02:00","%Y-%m-%d %H:%M:%S")    #设置到达时间。
# start_time = t.strftime("%H:%M:%S", t.localtime(t.mktime(end_time) - need_time)) #计算出发时间。
# print(f"增援出发时间为：{start_time}") 









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