# app.py
from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_data = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to BytesIO and encode as base64
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            qr_code_data = f"data:image/png;base64,{img_str}"
    
    return render_template('index.html', qr_code_data=qr_code_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
