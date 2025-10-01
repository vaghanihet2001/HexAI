from flask import Blueprint, jsonify, request
from utils import app_launcher

apps_bp = Blueprint('apps', __name__)

# Example apps
# installed_apps = [
#     {"name": "Notepad", "path": "/usr/bin/notepad"},
#     {"name": "Calculator", "path": "/usr/bin/calc"}
# ]

@apps_bp.route("/get_apps")
def get_apps():
    installed_apps = app_launcher.load_apps()
    apps = [{"name": app_name, "path": app_path["path"]} for app_name, app_path in installed_apps.items()]

    return jsonify({"apps":apps })

@apps_bp.route("/launch_app", methods=["POST"])
def launch_app():
    app_name = request.form.get("app_name")
    # app_path = request.form.get("app_path")
    app_launcher.open_app(app_name)
    # Here you can integrate actual OS-level launch if needed
    return jsonify({"status": f"Launch command sent for {app_name}"})

@apps_bp.route("/add_app", methods=["POST"])
def add_app():
    app_name = request.form.get("app_name")
    app_path = request.form.get("app_path")
    app_launcher.add_app(app_name, app_path)
    return jsonify({"status": f"App added: {app_name}"})
