try:
    import cv2
    import numpy as np
    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
    from PIL import ImageGrab
except ImportError as e:
    print(f"ImportError: {e}")

def get_screenshot():
    # 获取屏幕截图
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    return screenshot

def match_template(screenshot, template_path):
    # 读取模板图像
    template = cv2.imread(template_path, 0)
    # 检查模板图像是否成功加载
    if template is None:
        print(f"错误: 无法加载模板图像 {template_path}")
        return
    w, h = template.shape[::-1]

    # 使用模板匹配
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        # 在匹配的位置绘制矩形
        cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    cv2.imshow('Detected', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_window_info():
    # 获取当前屏幕上所有窗口的信息
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

    # 使用字典去重，并拼接 PID
    unique_windows = {}
    for window in window_list:
        window_owner = window.get('kCGWindowOwnerName', 'Unknown')
        window_pid = str(window['kCGWindowOwnerPID'])

        if window_owner in unique_windows:
            unique_windows[window_owner].append(window_pid)
        else:
            unique_windows[window_owner] = [window_pid]

    # 打印去重后的窗口信息
    for owner, pids in unique_windows.items():
        print(f"Window Owner: {owner}, PIDs: {', '.join(pids)}")

    # unique_windows = set()
    # for window in window_list:
    #     window_title = window.get('kCGWindowOwnerName', 'Unknown')
    #     if window_title not in unique_windows:
    #         unique_windows.add(window_title)
    #         print(f"Name: {window_title}, PID: {window['kCGWindowOwnerPID']}")

def main():
    # 获取窗口信息
    get_window_info()

    # 获取屏幕截图
    screenshot = get_screenshot()
    template_path = 'path_to_template_image.png'  # 模板图像的路径
    match_template(screenshot, template_path)

if __name__ == "__main__":
    main()