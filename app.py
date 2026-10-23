# app.py - Production Flask Web Server & Health Monitor
import os
import time
from flask import Flask, render_template, jsonify, make_response
from config import BOT_NAME, ADMIN_CONTACT, JOIN_LINK

app = Flask(__name__)
START_TIME = time.time()

@app.after_request
def add_security_headers(response):
    """Adds essential production security headers per launch checklist."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:;"
    )
    return response

@app.route("/")
def welcome():
    uptime_seconds = int(time.time() - START_TIME)
    return render_template(
        "welcome.html",
        bot_name=BOT_NAME,
        admin_contact=ADMIN_CONTACT,
        join_link=JOIN_LINK,
        uptime_seconds=uptime_seconds
    )

@app.route("/health")
@app.route("/ping")
def health():
    """Uptime monitoring probe endpoint."""
    return jsonify({
        "status": "healthy",
        "service": BOT_NAME,
        "uptime_seconds": int(time.time() - START_TIME),
        "engine": "Pyrogram + Telethon Dual-Core"
    }), 200

@app.route("/terms")
def terms():
    return render_template(
        "terms.html",
        bot_name=BOT_NAME,
        admin_contact=ADMIN_CONTACT
    )

@app.route("/privacy")
def privacy():
    return render_template(
        "privacy.html",
        bot_name=BOT_NAME,
        admin_contact=ADMIN_CONTACT
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", bot_name=BOT_NAME), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
