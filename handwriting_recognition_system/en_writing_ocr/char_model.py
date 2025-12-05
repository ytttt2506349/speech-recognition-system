import tensorflow as tf
from tensorflow.keras import layers, models

# 仅保留字母分类（A-Z + a-z，共52类），删除0-9数字分类
class_names = [
    # 大写字母 A-J
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a',
    # 大写字母 K-T
    '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54',
    # 大写字母 U-Z
    '55', '56', '57', '58', '59', '5a',
    # 小写字母 a-j
    '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a',
    # 小写字母 k-t
    '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74',
    # 小写字母 u-z
    '75', '76', '77', '78', '79', '7a'
]

# 字符映射：十六进制→实际字符
hex_to_char = [chr(int(h, 16)) for h in class_names]
num_classes = len(class_names)

def create_model(input_shape=(28, 28, 1)):
    """创建手写字母识别模型（删除数字后适配52类）"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        # 输出层适配52类
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])
    return model

if __name__ == '__main__':
    model = create_model()
    model.summary()
    print(f"模型分类数：{num_classes}（仅字母，无数字）")
    print(f"分类列表：{hex_to_char}")