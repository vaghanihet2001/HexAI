from flask import Blueprint, jsonify, request
from utils import memory  # <-- our utility

memory_bp = Blueprint("memory", __name__)

# -------------------------------
# GET memory (all or by key)
# -------------------------------
@memory_bp.route("/get_memory", methods=["GET"])
def get_memory_route():
    key = request.args.get("key")
    data = memory.get_memory(key)
    return jsonify({"memory": data})


# -------------------------------
# ADD memory (append entry)
# -------------------------------
@memory_bp.route("/add_memory", methods=["POST"])
def add_memory_route():
    key = request.form.get("key")
    value = request.form.get("value")
    if not key or not value:
        return jsonify({"error": "Missing key or value"}), 400

    memory.add_memory(key, value)
    return jsonify({"status": f"✅ Added value to {key}", "memory": memory.get_memory()})


# -------------------------------
# UPDATE memory (overwrite key)
# -------------------------------
@memory_bp.route("/update_memory", methods=["POST"])
def update_memory_route():
    key = request.form.get("key")
    value = request.form.get("value")
    if not key or not value:
        return jsonify({"error": "Missing key or value"}), 400

    memory.update_memory(key, value)
    return jsonify({"status": f"✏️ Updated {key}", "memory": memory.get_memory()})


# -------------------------------
# DELETE memory (remove key)
# -------------------------------
@memory_bp.route("/delete_memory", methods=["POST"])
def delete_memory_route():
    key = request.form.get("key")
    if not key:
        return jsonify({"error": "Missing key"}), 400

    memory.delete_memory(key)
    return jsonify({"status": f"🗑️ Deleted {key}", "memory": memory.get_memory()})
