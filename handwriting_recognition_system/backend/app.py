import sys
import os
# 将项目根目录（handwriting_recognition_system）加入Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 原有导入代码
from flask import Flask, request, jsonify
from config.config import SERVER_CONFIG  # 现在能找到config模块了
# 其他代码...
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.config import SERVER_CONFIG
from backend.wrappers.chinese_rec import predict_chinese
from backend.wrappers.english_rec import predict_english

# 初始化Flask应用
app = Flask(__name__)
# 解决跨域问题
CORS(app)

# 统一识别接口
@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        # 校验是否上传图片
        if "image" not in request.files:
            return jsonify({"chinese": "未上传图片", "english": "未上传图片"})
        
        image_file = request.files["image"]
        # 调用中文识别
        chinese_res = predict_chinese(image_file)
        # 重新读取文件流（避免流被耗尽）
        image_file.seek(0)
        # 调用英文识别
        english_res = predict_english(image_file)

        # 返回识别结果
        return jsonify({
            "chinese": chinese_res,
            "english": english_res
        })
    except Exception as e:
        # 异常捕获
        return jsonify({"chinese": f"系统异常: {str(e)}", "english": f"系统异常: {str(e)}"})

if __name__ == "__main__":
    # 启动后端服务
    app.run(**SERVER_CONFIG)