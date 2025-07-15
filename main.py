from flask import Flask, request, redirect, render_template, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import pyotp
import os
import android as a

app = Flask(__name__, template_folder='pages')
app.secret_key = 'RANDOM_STRING'  # Required for session security

# Set up limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

PASSWORD = "PASSWORD"

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per 30 minutes")  # Limit login attempts
def login():
    error = ""
    if session.get('logged_in'):
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('main_menu'))
        else:
            time.sleep(2)  # Add delay to slow brute force
            error = "Incorrect password."
    return render_template('login.html', error=error)

@app.route('/main_menu')
@login_required
def main_menu():
    return render_template('main_menu.html')

@app.route('/totp')
@login_required
def totp():
    code1 = pyotp.TOTP("SECRET1").now()
    code2 = pyotp.TOTP("SECRET2").now()
    html = f"""
    <html>
    <head>
      <meta http-equiv="refresh" content="30">
      <title>TOTP codes</title>
    </head>
    <body>
      <h2>TOTP codes:</h2>
      <p>{code1} 1</p>
      <p>{code2} 2</p>
      <p><a href="{url_for('main_menu')}">Back to main menu</a></p>
    </body>
    </html>
    """
    return html

@app.route('/android')
@login_required
def android():
    import time

    tile_w = 10
    tile_h = 10
    image_width = 230
    image_height = 410
    cols = image_width // tile_w
    rows = image_height // tile_h

    row = request.args.get('row', type=int)
    col = request.args.get('col', type=int)
    
    if row is not None and col is not None:
        tile_id = row * cols + col
        if tile_id != 0:
            a.click(tile_id)
            print(f"Tile clicked: {tile_id}")
        time.sleep(1)
        a.update_screen()
        return redirect(url_for('android'))

    return render_template('android.html', rows=rows, cols=cols, tile_w=tile_w, tile_h=tile_h, selected_row=row)

if __name__ == '__main__':
    app.run(debug=True)
