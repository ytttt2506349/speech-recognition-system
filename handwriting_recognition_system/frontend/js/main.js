document.addEventListener("DOMContentLoaded", () => {
    // 初始化画布绘制类
    const drawer = new CanvasDrawer("drawCanvas");
    // 初始化识别请求类
    const recognizer = new Recognizer("http://127.0.0.1:5000/recognize", {
        chinese: document.getElementById("chineseResult"),
        english: document.getElementById("englishResult")
    });

    // 绑定画布鼠标事件
    const canvas = document.getElementById("drawCanvas");
    canvas.addEventListener("mousedown", e => drawer.startDraw(e));
    canvas.addEventListener("mousemove", e => drawer.drawing(e));
    canvas.addEventListener("mouseup", e => {
        drawer.endDraw(e);
        drawer.getBlob().then(blob => recognizer.recognize(blob));
    });
    canvas.addEventListener("mouseout", e => drawer.endDraw(e));

    // 绑定画布触屏事件（适配手机）
    canvas.addEventListener("touchstart", e => drawer.startDraw(e));
    canvas.addEventListener("touchmove", e => drawer.drawing(e));
    canvas.addEventListener("touchend", e => {
        drawer.endDraw(e);
        drawer.getBlob().then(blob => recognizer.recognize(blob));
    });

    // 绑定清除和撤销按钮事件
    document.getElementById("clearBtn").addEventListener("click", () => {
        drawer.clear();
        recognizer.reset();
    });
    document.getElementById("undoBtn").addEventListener("click", () => {
        drawer.undo();
        drawer.getBlob().then(blob => recognizer.recognize(blob));
    });
});