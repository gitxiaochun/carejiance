import os

current_path = os.getcwd()  # 获取当前工作目录
target_path = "C:\\Users\\86189\\Desktop\\基于flask的图像处理1\\基于flask的图像处理\\static\\huidu.jpg"  # 目标路径

relative_path = os.path.relpath(target_path, current_path)
print(relative_path)
