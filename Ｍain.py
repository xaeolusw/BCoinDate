# 计算两个坐标之间的距离
def get_distance(addr1, addr2):
    x1, y1 = addr1
    x2, y2 = addr2
    return (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

# 定义地址坐标
BeginAddr = (3066, 4081)
TargetAddr = (2520, 3370)
#EndAddr = (2415, 3185)

# 测试两个地址之间的距离
distance = get_distance(BeginAddr, TargetAddr) 
print(f"地址{BeginAddr}和{TargetAddr}之间的距离是{distance}吉米") 


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