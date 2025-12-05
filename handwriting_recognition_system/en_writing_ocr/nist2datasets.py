import os
import shutil
import cv2
import numpy as np
from scipy.io import loadmat

# NIST数据集路径（需自行下载后配置）
NIST_PATH = 'nist_dataset'
# 输出数据集路径
OUTPUT_TRAIN_PATH = os.path.join('datasets', 'char_train')
OUTPUT_VALID_PATH = os.path.join('datasets', 'char_valid')

# 数字类别过滤：30-39（十六进制）对应0-9，需跳过
DIGIT_CLASSES = [f"3{i}" for i in range(10)]
# 训练/验证分割比例
TRAIN_RATIO = 0.8

def create_folder(path):
    """创建文件夹（若不存在）"""
    if not os.path.exists(path):
        os.makedirs(path)

def process_nist_data():
    """处理NIST数据集，仅保留字母，过滤数字"""
    # 初始化输出文件夹
    create_folder(OUTPUT_TRAIN_PATH)
    create_folder(OUTPUT_VALID_PATH)

    # 遍历NIST数据集目录
    for root, dirs, files in os.walk(NIST_PATH):
        for file in files:
            if file.endswith('.mat'):
                # 加载mat文件
                mat_data = loadmat(os.path.join(root, file))
                # 获取字符类别（十六进制）
                char_hex = file.split('_')[0].lower()
                # 过滤数字类别
                if char_hex in DIGIT_CLASSES:
                    print(f"跳过数字类别：{char_hex}")
                    continue
                # 仅处理字母类别
                print(f"处理字母类别：{char_hex}")

                # 创建类别文件夹
                train_cls_path = os.path.join(OUTPUT_TRAIN_PATH, char_hex)
                valid_cls_path = os.path.join(OUTPUT_VALID_PATH, char_hex)
                create_folder(train_cls_path)
                create_folder(valid_cls_path)

                # 处理图片数据（示例逻辑，需根据NIST实际格式调整）
                images = mat_data['images']
                total_num = len(images)
                train_num = int(total_num * TRAIN_RATIO)

                for i, img in enumerate(images):
                    # 转换为28x28灰度图
                    img_28 = cv2.resize(img, (28, 28))
                    img_path = os.path.join(train_cls_path if i < train_num else valid_cls_path, f"{i}.png")
                    cv2.imwrite(img_path, img_28)

    print("数据集生成完成！。")

if __name__ == '__main__':
    process_nist_data()