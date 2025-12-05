class CanvasDrawer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext("2d");
        this.config = {
            lineWidth: 6,
            strokeStyle: "#000",
            lineCap: "round",
            isDrawing: false,
            lastX: 0,
            lastY: 0,
            pathHistory: [],
            currentPath: []
        };
        this._initCanvas();
    }

    _initCanvas() {
        this.ctx.lineWidth = this.config.lineWidth;
        this.ctx.strokeStyle = this.config.strokeStyle;
        this.ctx.lineCap = this.config.lineCap;
    }

    _getPos(e) {
        const rect = this.canvas.getBoundingClientRect();
        const clientX = e.type.includes("touch") ? e.touches[0].clientX : e.clientX;
        const clientY = e.type.includes("touch") ? e.touches[0].clientY : e.clientY;
        return {
            x: (clientX - rect.left) * (this.canvas.width / rect.width),
            y: (clientY - rect.top) * (this.canvas.height / rect.height)
        };
    }

    startDraw(e) {
        e.preventDefault();
        this.config.isDrawing = true;
        const pos = this._getPos(e);
        this.config.lastX = pos.x;
        this.config.lastY = pos.y;
        this.config.currentPath = [[pos.x, pos.y]];
    }

    drawing(e) {
        e.preventDefault();
        if (!this.config.isDrawing) return;
        const pos = this._getPos(e);
        this.ctx.beginPath();
        this.ctx.moveTo(this.config.lastX, this.config.lastY);
        this.ctx.lineTo(pos.x, pos.y);
        this.ctx.stroke();
        this.config.lastX = pos.x;
        this.config.lastY = pos.y;
        this.config.currentPath.push([pos.x, pos.y]);
    }

    endDraw(e) {
        e.preventDefault();
        if (!this.config.isDrawing) return;
        this.config.isDrawing = false;
        this.config.pathHistory.push(this.config.currentPath);
        this.config.currentPath = [];
    }

    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.config.pathHistory = [];
        this.config.currentPath = [];
        return this;
    }

    undo() {
        if (this.config.pathHistory.length === 0) return this;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.config.pathHistory.pop();
        this._redrawPaths();
        return this;
    }

    _redrawPaths() {
        this.config.pathHistory.forEach(path => {
            if (path.length < 2) return;
            this.ctx.beginPath();
            this.ctx.moveTo(path[0][0], path[0][1]);
            path.forEach(pos => this.ctx.lineTo(pos[0], pos[1]));
            this.ctx.stroke();
        });
    }

    getBlob(format = "image/png") {
        return new Promise(resolve => {
            this.canvas.toBlob(blob => resolve(blob), format);
        });
    }
}