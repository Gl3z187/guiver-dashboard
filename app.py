from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from database import init_db, get_all_trades, add_trade, delete_trade
from metrics import calculate_summary
from functools import wraps
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "guiver_clave_secreta_123")
init_db()

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_reports(folder_name):
    folder_path = os.path.join(app.config["UPLOAD_FOLDER"], folder_name)
    os.makedirs(folder_path, exist_ok=True)
    files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            files.append(file)
    files.sort(reverse=True)
    return files


def save_report(file, folder_name):
    if file and allowed_file(file.filename):
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], folder_name)
        os.makedirs(folder_path, exist_ok=True)
        filename = secure_filename(file.filename)
        file.save(os.path.join(folder_path, filename))
        return True
    return False


def send_contact_email(nombre, telefono, email, asunto, mensaje):
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        raise RuntimeError("Faltan MAIL_USERNAME o MAIL_PASSWORD en el archivo .env")

    body = f"""
Nuevo mensaje desde la web de Guiver Asset Management

Nombre: {nombre}
Teléfono: {telefono}
Email: {email}
Asunto: {asunto}

Mensaje:
{mensaje}
"""

    msg = EmailMessage()
    msg["Subject"] = f"Nuevo contacto web - {asunto}"
    msg["From"] = MAIL_USERNAME
    msg["To"] = MAIL_USERNAME
    msg["Reply-To"] = email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
        smtp.send_message(msg)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/resumen")
def index():
    trades = get_all_trades()
    summary = calculate_summary(trades)
    return render_template("index.html", trades=trades, summary=summary)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form["password"]
        if password == "Guiver2026":
            session["authenticated"] = True
            return redirect(url_for("trades"))
        else:
            error = "Contraseña incorrecta"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/trades", methods=["GET", "POST"])
@login_required
def trades():
    if request.method == "POST":
        open_date = request.form["open_date"]
        close_date = request.form["close_date"]
        pair = request.form["pair"]
        direction = request.form["direction"]
        narrative = request.form["narrative"]
        setup_type = request.form["setup_type"]
        result_r = float(request.form["result_r"])
        notes = request.form["notes"]
        reflection = request.form["reflection"]

        add_trade(
            open_date,
            close_date,
            pair,
            direction,
            narrative,
            setup_type,
            result_r,
            notes,
            reflection
        )
        return redirect(url_for("trades"))

    all_trades = get_all_trades()
    return render_template("trades.html", trades=all_trades)


@app.route("/delete/<int:trade_id>")
@login_required
def delete(trade_id):
    delete_trade(trade_id)
    return redirect(url_for("trades"))


@app.route("/contacto", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()
        asunto = request.form.get("asunto", "").strip()
        mensaje = request.form.get("mensaje", "").strip()
        privacidad = request.form.get("privacidad")

        if not nombre or not email or not asunto or not mensaje:
            flash("Completa los campos obligatorios.", "error")
            return redirect(url_for("contact"))

        if not privacidad:
            flash("Debes aceptar la política de privacidad.", "error")
            return redirect(url_for("contact"))

        try:
            send_contact_email(nombre, telefono, email, asunto, mensaje)
            flash("Mensaje enviado correctamente.", "success")
        except Exception as e:
            print(f"Error enviando email: {e}")
            flash("No se pudo enviar el mensaje. Revisa la configuración del correo.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/geopolitico", methods=["GET", "POST"])
def geopolitico():
    if request.method == "POST" and session.get("authenticated"):
        file = request.files.get("pdf_file")
        if file and save_report(file, "geopolitico"):
            flash("Reporte subido correctamente.", "success")
        else:
            flash("No se pudo subir el PDF.", "error")
        return redirect(url_for("geopolitico"))

    reports = get_reports("geopolitico")
    return render_template("reports.html", title="Análisis geopolítico", folder="geopolitico", reports=reports)


@app.route("/macroeconomico", methods=["GET", "POST"])
def macroeconomico():
    if request.method == "POST" and session.get("authenticated"):
        file = request.files.get("pdf_file")
        if file and save_report(file, "macroeconomico"):
            flash("Reporte subido correctamente.", "success")
        else:
            flash("No se pudo subir el PDF.", "error")
        return redirect(url_for("macroeconomico"))

    reports = get_reports("macroeconomico")
    return render_template("reports.html", title="Análisis macroeconómico", folder="macroeconomico", reports=reports)


@app.route("/liquidez", methods=["GET", "POST"])
def liquidez():
    if request.method == "POST" and session.get("authenticated"):
        file = request.files.get("pdf_file")
        if file and save_report(file, "liquidez"):
            flash("Reporte subido correctamente.", "success")
        else:
            flash("No se pudo subir el PDF.", "error")
        return redirect(url_for("liquidez"))

    reports = get_reports("liquidez")
    return render_template("reports.html", title="Análisis de liquidez bancaria", folder="liquidez", reports=reports)


@app.route("/uploads/<folder>/<filename>")
def uploaded_file(folder, filename):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], folder), filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)