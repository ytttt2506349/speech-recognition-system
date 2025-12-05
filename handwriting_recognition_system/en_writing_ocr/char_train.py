import os
import tensorflow as tf
from char_model import create_model, class_names, num_classes
import shutil

# 数据集路径
TRAIN_PATH = os.path.join('datasets', 'char_train')
VALID_PATH = os.path.join('datasets', 'char_valid')
# 模型保存路径
MODEL_SAVE_PATH = 'char_model/saved_model'
TFLITE_SAVE_PATH = 'char_model/char_model.tflite'

# 图片参数
IMG_HEIGHT = 28
IMG_WIDTH = 28
BATCH_SIZE = 32

def filter_digit_folders(path):
    """过滤数据集文件夹中的数字类别（30-39），确保无数字数据"""
    digit_classes = [f"3{i}" for i in range(10)]  # 数字对应的十六进制文件夹名
    for cls in digit_classes:
        cls_path = os.path.join(path, cls)
        if os.path.exists(cls_path):
            print(f"删除数字类别文件夹：{cls_path}")
            shutil.rmtree(cls_path)

def load_dataset():
    """加载训练/验证数据集（仅字母）"""
    # 先过滤数字文件夹
    filter_digit_folders(TRAIN_PATH)
    filter_digit_folders(VALID_PATH)

    # 加载训练集
    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_PATH,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        color_mode='grayscale',
        label_mode='int'
    )

    # 加载验证集
    val_ds = tf.keras.utils.image_dataset_from_directory(
        VALID_PATH,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        color_mode='grayscale',
        label_mode='int'
    )

    # 数据预处理
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    return train_ds, val_ds

def train_model():
    """训练模型"""
    train_ds, val_ds = load_dataset()

    # 创建模型
    model = create_model()

    # 训练
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=10
    )

    # 保存原始模型
    if not os.path.exists(MODEL_SAVE_PATH):
        os.makedirs(MODEL_SAVE_PATH)
    model.save(MODEL_SAVE_PATH)

    # 转换为tflite模型
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with open(TFLITE_SAVE_PATH, 'wb') as f:
        f.write(tflite_model)

    print(f"模型训练完成！")
    print(f"原始模型保存至：{MODEL_SAVE_PATH}")
    print(f"TFLite模型保存至：{TFLITE_SAVE_PATH}")

if __name__ == '__main__':
    train_model()