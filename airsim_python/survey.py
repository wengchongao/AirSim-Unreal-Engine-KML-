import airsim
import math
import time

# 初始化客户端
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# 起飞并悬停
client.takeoffAsync().join()
time.sleep(5)
# client.hoverAsync().join()
client.moveByVelocityZAsync(10, 10, -300, 300).join()

# # 圆形路径参数
# radius = 10  # 米
# altitude = -5  # NED坐标系中，负值代表上方（相对原点上飞5米）
# center_x = 0
# center_y = 0
# num_points = 36  # 点越多，圆越平滑
# speed = 3  # m/s
#
# # 生成圆上的路径点
# path = []
# for i in range(num_points + 1):  # 多加一个点使圆闭合
#     angle = 2 * math.pi * i / num_points
#     x = center_x + radius * math.cos(angle)
#     y = center_y + radius * math.sin(angle)
#     z = altitude
#     path.append(airsim.Vector3r(x, y, z))
# print(path)
# # 飞行这个圆形路径
# client.moveOnPathAsync(path, speed, drivetrain=airsim.DrivetrainType.ForwardOnly,
#                        yaw_mode=airsim.YawMode(False, 0))
#
# # 悬停并降落
# client.hoverAsync().join()
client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)
