import tempfile
import os
from config.config import TEMP_FILE_CONFIG

def create_temp_image(image_file):
    """创建临时图片文件（自动清理，避免残留）"""
    temp_fd, temp_path = tempfile.mkstemp(
        prefix=TEMP_FILE_CONFIG["prefix"],
        suffix=TEMP_FILE_CONFIG["suffix"],
        dir=TEMP_FILE_CONFIG["dir"]
    )
    # 将前端上传的图片写入临时文件
    with open(temp_path, "wb") as f:
        f.write(image_file.read())
    os.close(temp_fd)
    return temp_path

def remove_temp_file(file_path):
    """删除临时文件"""
    if os.path.exists(file_path):
        os.remove(file_path)

def check_path_exists(path, tip):
    """校验路径是否存在，不存在则抛异常"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{tip}路径不存在：{path}")