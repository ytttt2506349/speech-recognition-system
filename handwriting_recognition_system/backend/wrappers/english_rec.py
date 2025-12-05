import sys
from PIL import Image
from config.config import ENGLISH_REC_DIR
from backend.utils.file_utils import create_temp_image, remove_temp_file

def predict_english(image_file):
    """英文手写识别核心函数（适配处理后的en_writing_ocr）"""
    temp_path = None
    try:
        # 创建临时图片文件
        temp_path = create_temp_image(image_file)
        # 转为灰度图（英文项目通用要求）
        image = Image.open(temp_path).convert("L")
        image.save(temp_path)

        # 导入处理后的en_writing_ocr模型（示例，需根据实际模型调整）
        sys.path.append(ENGLISH_REC_DIR)
        from char_model import hex_to_char, create_model
        import tensorflow as tf

        # 加载英文识别模型
        model = create_model()
        model.load_weights(os.path.join(ENGLISH_REC_DIR, "char_model/saved_model"))

        # 图片预处理
        img = tf.io.read_file(temp_path)
        img = tf.image.decode_png(img, channels=1)
        img = tf.image.resize(img, (28, 28))
        img = img / 255.0
        img = tf.expand_dims(img, 0)

        # 模型预测
        pred = model.predict(img)
        pred_idx = tf.argmax(pred, axis=1).numpy()[0]
        result = hex_to_char[pred_idx]

        return result
    except Exception as e:
        return f"英文识别异常: {str(e)}"
    finally:
        # 确保临时文件被删除
        if temp_path:
            remove_temp_file(temp_path)