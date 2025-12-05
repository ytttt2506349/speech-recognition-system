import torch
import pickle
import sys
from config.config import CHINESE_MODEL_CONFIG
from backend.utils.file_utils import check_path_exists

# 全局模型缓存（避免重复加载）
MODEL_CACHE = {
    "chinese_model": None,
    "idx2char": None
}

def load_chinese_model():
    """加载中文识别模型（100%复用原项目代码）"""
    global MODEL_CACHE
    if MODEL_CACHE["chinese_model"] and MODEL_CACHE["idx2char"]:
        return MODEL_CACHE["chinese_model"], MODEL_CACHE["idx2char"]
    
    # 添加上下文，导入原项目模块
    sys.path.append(CHINESE_MODEL_CONFIG["log_dir"].split("log")[0])
    from EfficientNetV2.model import EffNetV2
    from Utils import find_newest_log

    # 校验关键路径
    check_path_exists(CHINESE_MODEL_CONFIG["log_dir"], "中文预训练模型")
    check_path_exists(CHINESE_MODEL_CONFIG["char_dict_path"], "汉字字典")

    # 加载原项目预训练模型
    model_path = find_newest_log(CHINESE_MODEL_CONFIG["log_dir"])
    if not model_path:
        raise FileNotFoundError("请将预训练模型放入 Chinese_Character_Rec/log 目录（格式：logX.pth）")
    
    model = EffNetV2(num_classes=CHINESE_MODEL_CONFIG["num_classes"]).to(CHINESE_MODEL_CONFIG["device"])
    model.load_state_dict(torch.load(model_path, map_location=CHINESE_MODEL_CONFIG["device"]))
    model.eval()

    # 加载汉字字典并反转（索引->汉字）
    with open(CHINESE_MODEL_CONFIG["char_dict_path"], "rb") as f:
        char_dict = pickle.load(f)
    idx2char = {v: k for k, v in char_dict.items()}

    # 缓存模型和字典
    MODEL_CACHE["chinese_model"] = model
    MODEL_CACHE["idx2char"] = idx2char

    return model, idx2char