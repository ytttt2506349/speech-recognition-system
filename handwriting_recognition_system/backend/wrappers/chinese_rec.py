# 1. 导入基础依赖库
import sys
import os
import torch
import torch.nn as nn
from PIL import Image

# 2. 配置Python搜索路径：确保能找到Chinese_Character_Rec目录下的Data模块
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHINESE_REC_DIR = os.path.join(PROJECT_ROOT, "Chinese_Character_Rec")
sys.path.append(CHINESE_REC_DIR)

# 3. 导入项目配置和自定义预处理模块
from config.config import CHINESE_MODEL_CONFIG
from Data import transform_test  # 从Data.py导入预处理流水线

# 4. 简易CNN模型（适配64x64输入的手写汉字识别，若有自定义模型可替换此类）
# 若你有VGG19/EfficientNetV2模型，删除此类并导入对应的模型类即可
class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        # 特征提取层：卷积+池化
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # 单通道输入（灰度图）
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 64→32
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 32→16
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(16, 16),  # 16→1
        )
        # 分类层：全连接
        self.classifier = nn.Sequential(
            nn.Linear(128 * 1 * 1, 512),
            nn.ReLU(),
            nn.Dropout(0.5),  # 防止过拟合
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        # 前向传播：特征提取→分类
        x = self.features(x)
        x = x.view(x.size(0), -1)  # 展平张量
        x = self.classifier(x)
        return x

# 5. 核心函数：加载中文手写识别模型（适配CPU环境）
def load_chinese_model():
    """加载预训练模型+生成索引→汉字的映射字典"""
    try:
        # 从配置文件读取参数
        num_classes = CHINESE_MODEL_CONFIG["num_classes"]
        device = CHINESE_MODEL_CONFIG["device"]
        model_path = os.path.join(CHINESE_MODEL_CONFIG["log_dir"], "log0.pth")

        # 初始化模型并加载权重
        model = SimpleCNN(num_classes=num_classes).to(device)
        if os.path.exists(model_path):
            # 加载权重：强制映射到CPU，适配无CUDA环境
            checkpoint = torch.load(model_path, map_location=device)
            # 兼容两种权重保存格式：直接state_dict / checkpoint字典
            if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                model.load_state_dict(checkpoint["model_state_dict"])
            else:
                model.load_state_dict(checkpoint)
            model.eval()  # 切换为推理模式（禁用Dropout/BatchNorm）
        else:
            raise FileNotFoundError(f"模型文件不存在：{model_path}")

        # 生成简易汉字映射字典（可替换为3755个常用字的完整字典）
        basic_chars = ["一", "二", "三", "十", "百", "千", "万", "人", "手", "口"]
        idx2char = {i: basic_chars[i] if i < len(basic_chars) else f"未知字{i}" for i in range(num_classes)}

        return model, idx2char
    except Exception as e:
        raise Exception(f"模型加载失败：{str(e)}")

# 6. 中文手写识别主函数：接收图像文件，返回识别结果
def predict_chinese(image_file):
    """
    中文手写识别核心接口
    :param image_file: 上传的图像文件路径/对象
    :return: 识别的汉字或异常信息
    """
    try:
        # 加载模型和汉字映射
        model, idx2char = load_chinese_model()

        # 图像预处理：和Data.py的transform_test保持一致
        image = Image.open(image_file).convert("RGB")
        image_tensor = transform_test(image).unsqueeze(0).to(CHINESE_MODEL_CONFIG["device"])  # 增加batch维度

        # 模型预测：关闭梯度计算提升速度
        with torch.no_grad():
            output = model(image_tensor)
            pred_idx = torch.argmax(output, dim=1).item()  # 获取预测的索引

        # 返回识别结果
        return idx2char.get(pred_idx, "未识别")
    except Exception as e:
        return f"中文识别异常: {str(e)}"