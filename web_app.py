from flask import Flask, render_template, request, jsonify
from modules.chat import chat_bp
from modules.memory import memory_bp
from modules.apps import apps_bp
from modules.reminders import reminders_bp


app = Flask(__name__)

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(memory_bp, url_prefix='/memory')
app.register_blueprint(apps_bp, url_prefix='/apps')
app.register_blueprint(reminders_bp, url_prefix='/reminders')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    
    app.run(debug=True, port=5002)
