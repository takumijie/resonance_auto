import cv2
from PIL import ImageGrab
import numpy as np
import time
import pyautogui
import configparser
import sys
import os

print("欢迎使用雷索纳斯_auto Ciallo～(∠·ω< )⌒☆ -!")
# 获取脚本运行路径
script_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(script_path)

def select_image_files(section_number):
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, 'config.ini'))
    # 构建部分名称
    section_name = f'IMAGES_{section_number}'

    # 检查部分是否存在
    if section_name not in config:
        print(f"部分 {section_name} 不存在于配置文件中")
        return "检查脚本运行"

    # 获取部分中的图像文件路径
    image_files_list = []
    for i in range(1, 4):
        image_key = f'image{i}'
        if image_key in config[section_name]:
            image_files_list.append(config[section_name][image_key])

    return image_files_list


section_number = int(input("请选择要刷的关卡（1,铁安局  2,形态污染  3,红茶战争（关卡2） 4,红茶战争（关卡3））："))
image_files = select_image_files(section_number)
print(image_files)

# 设置阈值
threshold = 0.8  # 可以根据需要调整阈值


def find_current_step():
    """
    确定当前应该从哪一步开始执行的索引。
    """
    while True:
        # 获取屏幕截图并转换为 NumPy 数组
        screenshot = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))

        # 循环遍历每张图片，尝试匹配
        for i, image_file in enumerate(image_files):
            # 读取要识别的图片
            image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print("无法加载图片:", image_file)
                continue

            # 预处理截图
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            screenshot_blur = cv2.GaussianBlur(screenshot_gray, (5, 5), 0).astype(np.uint8)

            # 在预处理后的截图中搜索图片
            result = cv2.matchTemplate(screenshot_blur, image, cv2.TM_CCOEFF_NORMED)

            # 处理匹配结果
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                print("找到图片:", image_file)
                return i  # 返回当前匹配到的图片索引

        # 如果未找到任何图片，则打印提示信息，继续循环
        print("未找到任何图片，继续搜索...")


# 获取用户输入的循环时间（分钟）
loop_duration = float(input("请输入循环的时长（分钟）："))
loop_duration_seconds = loop_duration * 60

# 初始化当前图片索引
current_index = find_current_step()

# 记录循环开始时间
start_time = time.time()

# 开始循环
while True:
    # 如果已经超过设定的循环时间，则退出循环
    elapsed_time = time.time() - start_time
    if elapsed_time >= loop_duration_seconds:
        break

    # 获取当前应该匹配的图片文件名
    current_image_file = image_files[current_index]

    # 读取要识别的图片
    image = cv2.imread(current_image_file, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("无法加载图片:", current_image_file)
        continue

    # 获取屏幕截图并转换为 NumPy 数组
    screenshot = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))

    # 预处理截图
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    screenshot_blur = cv2.GaussianBlur(screenshot_gray, (5, 5), 0).astype(np.uint8)

    # 在预处理后的截图中搜索图片
    result = cv2.matchTemplate(screenshot_blur, image, cv2.TM_CCOEFF_NORMED)

    # 处理匹配结果
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > threshold:
        # 计算图片中心点的位置
        center_x = max_loc[0] + image.shape[1] // 2
        center_y = max_loc[1] + image.shape[0] // 2
        # 移动鼠标并点击
        pyautogui.moveTo(center_x, center_y)
        time.sleep(1)
        pyautogui.click()
        print("找到并点击图片:", current_image_file)

        # 将当前索引递增，准备匹配下一张图片
        current_index += 1
        if current_index >= len(image_files):
            # 如果已经匹配完所有图片，则重置索引，重新开始匹配
            current_index = 0
    else:
        print("未找到图片:", current_image_file)

    # 休眠1秒，模拟每次循环间隔
    time.sleep(1)

print("循环结束。")
