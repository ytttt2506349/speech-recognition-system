class Recognizer {
    constructor(apiUrl, resultEls) {
        this.apiUrl = apiUrl;
        this.chineseEl = resultEls.chinese;
        this.englishEl = resultEls.english;
        this.debounceDelay = 300;
        this.debounceTimer = null;
    }

    _debounce(fn) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(fn, this.debounceDelay);
    }

    recognize(blob) {
        this._debounce(async () => {
            try {
                this.chineseEl.textContent = "识别中...";
                this.englishEl.textContent = "识别中...";
                const formData = new FormData();
                formData.append("image", blob, "handwriting.png");
                const res = await fetch(this.apiUrl, {
                    method: "POST",
                    body: formData
                });
                const data = await res.json();
                this.chineseEl.textContent = data.chinese;
                this.englishEl.textContent = data.english;
            } catch (err) {
                this.chineseEl.textContent = "识别失败";
                this.englishEl.textContent = "识别失败";
                console.error(err);
            }
        });
    }

    reset() {
        this.chineseEl.textContent = "未识别";
        this.englishEl.textContent = "未识别";
        return this;
    }
}