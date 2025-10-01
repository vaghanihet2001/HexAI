from flask import Blueprint, request, jsonify
import utils.reminder as reminders

reminders_bp = Blueprint("reminders", __name__)
reminders.start_reminder_service()


@reminders_bp.route("/get_reminders", methods=["GET"])
def get_reminders():
    return jsonify({"reminders": reminders.load_reminders()})


@reminders_bp.route("/add_reminder", methods=["POST"])
def add_reminder():
    text = request.form.get("text")
    time_str = request.form.get("time")
    if not text or not time_str:
        return jsonify({"status": "❌ Missing text or time"}), 400

    reminders.add_reminder(text, time_str)
    return jsonify({"status": f"✅ Reminder added: {time_str} - {text}"})


@reminders_bp.route("/delete_reminder", methods=["POST"])
def delete_reminder():
    text = request.form.get("text")
    time_str = request.form.get("time")
    reminders.delete_reminder(text, time_str)
    return jsonify({"status": f"🗑️ Reminder removed: {time_str} - {text}"})
