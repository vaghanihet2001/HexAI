from flask import Blueprint, request, jsonify
from assistant_core import handle_command

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/send_command", methods=["POST"])
def send_command():
    command = request.form.get("command")
    response = handle_command(command)
    return jsonify({"response": response})
