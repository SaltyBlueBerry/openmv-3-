# openmv-3-
物品以颜色和形状区分
硬件使用基础的4自由度机械臂加以改造，你可以在我的代码上稍作修改以适应你的机械结构。
大致思路是：判断物品的颜色 判断物品的形状是圆形或方形哪一个的可能性更高，然后把不同形状和颜色的物品区分放在4个区域（左上左下右上右下）
使用openmv3自带的舵机引脚控制舵机，如果你需要控制更多舵机或者你使用的是openmv2可以使用舵机扩展板（openmv2可以控制2个舵机）
