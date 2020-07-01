


# 设计：沈阳航空航天大学 berry

# 博客：https://blog.csdn.net/qq_45037925/article/details/105901893

# 交流方式：私信我的博客即可



import time

from pyb import Servo
import sensor, image, time

from pyb import UART

#导入需要的模块


s1 = Servo(1) # P7

s2 = Servo(2) # P8

s3 = Servo(3) # P9 Only for OpenMV3 M7
#实例化3个舵机

uart = UART(3, 115200)#初始化串口

s2_now = -90
s3_now = 0


red_threshold  = (21, 100, 36, 127, -9, 34)#颜色阈值1   0001(14, 100, 8, 127, 9, 116)
blue_threshold  = ((20, 67, -52, -13, -36, -1))#颜色阈值2   0010
yellow_threshold  = (14, 100, 22, 127, 42, 113)#颜色阈值4    0100
green_threshold  = (20, 100, -128, -24, 17, 127)#颜色阈值8   1000





sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.


#以上部分是每个程序差不多都有的初始化设定



def move(s3_error,s2_error):#定义一个函数，作用是运动到目标物体位置
    kp=0.2
    global s2_now
    global s3_now #global关键字 用于全局变量

    s3_move = s3_error*kp+s3_now#pid计算

    if s3_move > 90:#这4句限制舵机运动角度，防止卡死
        s3_move = 90
    if s3_move < -90:
        s3_move = -90
    s3.angle(s3_move)#这一句是输出pwm控制舵机，采用openmv控制舵机时需要，采用arduino时不需要
    s3_now = s3_move#更新当前舵机角度存档

    if abs(s3_error)<10:
        s2_move = s2_error*kp+s2_now#pid计算
        if s2_move > -20:#这4句限制舵机运动角度，防止卡死
            s2_move = -20
        if s2_move < -90:
            s2_move = -90
            s2.angle(s2_move)#这一句是输出pwm控制舵机，采用openmv控制舵机时需要，采用arduino时不需要
            s2_now = s2_move
    #data.append((s2_now,s3_now))#这三句时串口输出舵机应转的角度，采用openmv控制舵机时不需要，采用arduino时需要
    #data_out = json.dumps(set(data))
    #uart.write(data_out +'\n')


def lay(shape,color):#定义一个函数，用于把抓取的物品放到指定位置
    global s2_now#global关键字 用于全局变量
    global s3_now
    angle = 0#这个值表示目的角度
    if color == 1:#根据颜色判断
        angle = 90
    else :
        angle = -90
    if shape > 0:#根据形状判断
        if angle >0:
            angle = angle - 30
        else:
            angle = angle + 30



#下面是机械臂把物品放到指定angle对应位置，并回到初始位置
    for i in range(s2_now,-20,-1):


        s2.angle(i)

        time.sleep(20)

    for i in range(s2_now,-20):


        s2.angle(i)

        time.sleep(20)

    for i in range(5,-19,-1):

        s1.angle(i)
        time.sleep(10)

    for i in range(-20,-90,-1):


        s2.angle(i)

        time.sleep(20)

    for i in range(s3_now,angle,-1):


        s3.angle(i)

        time.sleep(20)

    for i in range(s3_now,angle):


        s3.angle(i)

        time.sleep(20)



    for i in range(-90,-40):


        s2.angle(i)

        time.sleep(20)


    for i in range(-10,5):

        s1.angle(i)
        time.sleep(10)

    time.sleep(200)
    #data.append((s2_now,s3_now))
    #data_out = json.dumps(set(data))
    #uart.write(data_out +'\n')


    for i in range(-20,-90,-1):


        s2.angle(i)

        time.sleep(20)


    for i in range(angle,0,-1):


        s3.angle(i)

        time.sleep(20)

    for i in range(angle,0):


        s3.angle(i)

        time.sleep(20)
    time.sleep(2000)

    s2.angle(-90)
    s2_now = -90
    s3_now = angle
    #data.append((s2_now,s3_now))
    #data_out = json.dumps(set(data))
    #uart.write(data_out +'\n')



def find_max(blobs):#定义一个找最大色块的函数，输入一个色块对象列表，输出一个色块对象
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

def find_max_c(blobs):#定义一个找最大圆的函数，输入一个圆对象列表，输出一个圆对象
    max_size=0
    for blob in blobs:
        if blob[2] > max_size:
            max_blob=blob
            max_size = blob[2]
    return max_blob




s3.angle(s3_now)#初始化舵机
s2.angle(s2_now)
shape=0#记录形状和颜色
color=0
time.sleep(2000)
#下面是循环执行的部分
while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot().lens_corr(1.8)#拍摄一张照片，并畸变矫正
    claps = img.find_blobs([red_threshold])#寻找色块


    if claps:
        clap=find_max(claps)
        img.draw_cross(clap.x(), clap.y(), color = (0, 255, 0), size = 10, thickness = 2)#画一个十字

    #寻找色块
    blobs = img.find_blobs([yellow_threshold,green_threshold], roi=(0,0,160,80),pixels_threshold=100, area_threshold=100)# merge=True, margin=10
    if blobs:#如果找到了
        data=[]#初始化数据
        blob=find_max(blobs)#找最大
        color=blob.code()#记录颜色
        img.draw_rectangle(blob.x(),blob.y(),blob.w(),blob.h(), color = (255, 255, 255), thickness = 2, fill = False)
        #在色块周边一定范围内找圆
        circles= img.find_circles(threshold = 2600,r_min=10, x_margin = 10, y_margin = 10, r_margin = 10,
                    r_min = 2, r_max = 100, r_step = 2,roi=(blob.x(),blob.y(),blob.w(),blob.h()))
        #在色块周边一定范围内找方
        rects = img.find_rects(threshold = 10000,roi=(blob.x(),blob.y(),blob.w(),blob.h()))
        if circles:
            shape=shape+1
        if rects:
            shape=shape-1
        #上面两句会在一次抓取任务中对shape进行运算，shape表示该物品形状是圆还是方的概率，因此值理论上是-无穷到+无穷，实际不会太大，
        #正数表示更可能为圆，负数表示更可能为方，绝对值越大可能性越高，可以把中间值改成其他值以更好地提高准确率
        #由于openmv不能每一次都准确识别，因此采用这种方式显著提高了准确率。
        tx=blob.cx()
        ty=blob.cy()
        #s3_error = clap.cx()-tx#计算error
        #s2_error = clap.cy()-ty
        s3_error = 78-tx#计算error
        s2_error = 44-ty
        move(s3_error,s2_error)#使用前面定义的函数
        if abs(s3_error)<10:
            lay(shape,color)#使用前面定义的函数
            shape=0#清除标志
            color=0


S



        #s1.angle(5)打开#s1.angle(-10)闭合
        #s2.angle(-90)#前s2.angle(-20)后
        #s3.angle(-90)#左 s3.angle(0)#中s3.angle(90)#右






