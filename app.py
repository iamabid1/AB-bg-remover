import os
import io
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image, ImageEnhance

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400

    bg_color = request.form.get("customColor", "#ffffff")
    mode = request.form.get("mode", "normal")

    input_image = Image.open(file.stream).convert("RGBA")

    output = remove(input_image).convert("RGBA")

    background = Image.new("RGBA", output.size, bg_color)

    final = Image.alpha_composite(background, output)

    if mode == "passport":
        final = final.resize((413, 531))

    final = ImageEnhance.Sharpness(final).enhance(1.3)
    final = ImageEnhance.Contrast(final).enhance(1.1)

    buffer = io.BytesIO()
    final.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="no-bg.png"
    )


@app.route('/ping')
def ping():
    return "working"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)