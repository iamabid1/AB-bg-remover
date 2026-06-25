from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400

    # inputs
    bg_color = request.form.get("customColor", "#ffffff")
    mode = request.form.get("mode", "normal")

    # open image
    input_image = Image.open(file).convert("RGBA")

    # remove background
    output = remove(input_image).convert("RGBA")

    # background layer
    background = Image.new("RGBA", output.size, bg_color)

    # combine images
    final = Image.alpha_composite(background, output)

    # mode handling
    if mode == "passport":
        final = final.resize((413, 531))

    # enhancements
    final = ImageEnhance.Sharpness(final).enhance(1.3)
    final = ImageEnhance.Contrast(final).enhance(1.1)

    # save to memory
    buffer = io.BytesIO()
    final.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="no-bg.png"
    )


if __name__ == "__main__":
    app.run(debug=True)