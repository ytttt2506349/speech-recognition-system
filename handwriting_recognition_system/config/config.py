import os
import torch

# 工程根目录（自动适配Windows/Linux/macOS）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 原项目路径配置
CHINESE_REC_DIR = os.path.join(ROOT_DIR, "Chinese_Character_Rec")
ENGLISH_REC_DIR = os.path.join(ROOT_DIR, "en_writing_ocr")

# 中文模型配置（与原项目保持一致）
CHINESE_MODEL_CONFIG = {
    "log_dir": os.path.join(CHINESE_REC_DIR, "log"),  # 预训练模型目录
    "char_dict_path": os.path.join(CHINESE_REC_DIR, "char_dict/char_dict.pkl"),  # 汉字字典
    "num_classes": 3755,  # 原项目3755类汉字
    "cpu": "cuda" if torch.cuda.is_available() else "cpu"  # 自动判断GPU/CPU
}

# 后端服务配置
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True
}

# 临时文件配置
TEMP_FILE_CONFIG = {
    "prefix": "handwriting_",
    "suffix": ".png",
    "dir": os.path.join(ROOT_DIR, "temp")
}

# 自动创建临时目录
os.makedirs(TEMP_FILE_CONFIG["dir"], exist_ok=True)