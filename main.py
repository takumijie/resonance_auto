import cv2
from PIL import ImageGrab
import numpy as np
import time
import pyautogui

# 图片文件路径
image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg']

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
