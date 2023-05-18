# 计算两个坐标之间的距离
def get_distance(addr1, addr2):
    x1, y1 = addr1
    x2, y2 = addr2
    distance = (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    print(f"地址{addr1}和{addr2}之间的距离是{distance}吉米") 
    return distance

# 拉格朗日的坐标为(X,Y),每一小格(基地、前哨所在单位)在坐标上再细分为10，如(3066, 4081)可以理解为(306.6, 408.1)。
# 拉格朗日的曲率落点选择：自动计算与坐标所在小格4个顶点的距离，最近的为曲率落点。
# 获取起飞坐标曲率到目标坐标的曲率落点
def get_placement(begin_addr, target_addr):
    angle = [(target_addr[0]//10*10,(target_addr[1]//10*10) + 10),(target_addr[0]//10*10,target_addr[1]//10*10),(target_addr[0]//10*10+10,target_addr[1]//10*10+10),(target_addr[0]//10*10+10,target_addr[1]//10*10)] #定义4地址列表，用于存放目标点4个顶点的坐标

    distance = [get_distance(begin_addr, target_addr),get_distance(begin_addr, angle[0]),get_distance(begin_addr, angle[1]),get_distance(begin_addr, angle[2]),get_distance(begin_addr, angle[3])] #定义5数值列表，用于存放起飞点到目标点和目标点4个角的距离
    
    #获取distance中最小值的索引，即为曲率落点。
    return target_addr,distance.index(min(distance[1:4]))    #返回目标所在小格左下角坐标和曲率落点角的索引，1为左上角，2为左下角，3为右上角，4为右下角。  
        
begin_addr = (3094, 4063) #起飞坐标
target_addr = (1975,1455) #目标坐标

print(get_placement(begin_addr, target_addr))

exit()

#2. 根据斜率求直线方程:
def get_line_equation(Begin, Target, x = 0, y = 0):
    x1, y1 = Begin
    x2, y2 = Target
       
    k = (y2 - y1) / (x2 - x1) #斜率k = (y2 - y1)/(x2 - x1)
    b = y1 - k * x1 #斜率公式 y = kx + b, b = y - kx

    if x == 0 :
        if y != 0 :
            x = (y - b)/k
            return int(x),y
    elif y == 0 :
        y = k * x + b
        return x,y
    else :
        return x,y
        

# EndAddr = get_line_equation(BeginAddr,TargetAddr,int(input("请输入前哨的X坐标: ")),int(input("请输入前哨的Y坐标: ")))
EndAddr = get_line_equation(BeginAddr,TargetAddr,0,3182)
print(EndAddr)

print(2500/(719.98/(49)))
print(3250/(719.98/(38)))

print((462.79*172)/2500)
print((462.79*172)/3250)

exit()
# 3. 判定点在直线上方、下方还是在直线上:
def point_position(addr, k, b):
    x, y = addr
    if y == k * x + b:
        return '在直线上'
    elif y > k * x + b:
        return '在直线上方'
    else:
        return '在直线下方'
    
print(point_position(TigerAddr, k, b))  # 在直线上方


# 4. 求直线与坐标轴交点:
def intersect_point(k, b):
    if k == 0:
        x = 0
        y = b
    elif k == float('inf'):
        x = b 
        y = 0
    else:
        x = -b / k
        y = 0
    return x, y

x, y = intersect_point(2, 8)  # x = -4, y = 0

exit()
# 获取用户输入的两个地址坐标
addr1 = int(input("请输入第一个地址的x坐标: ")), int(input("请输入第一个地址的y坐标: "))
addr2 = int(input("请输入第二个地址的x坐标: ")), int(input("请输入第二个地址的y坐标: "))

# 计算用户输入地址之间的距离
distance = get_distance(addr1, addr2)
print(f"您输入的两个地址{addr1}和{addr2}之间的距离是{distance}吉米")#print("hello world")