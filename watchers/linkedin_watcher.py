import os
import json
from datetime import datetime

LINKEDIN_ACTIVITY_FILE = "watchers/linkedin_activity.json"
LAST_PROCESSED_ACTIVITY_FILE = "last_processed_linkedin_activity.json"

def load_last_processed_activity():
    if os.path.exists(LAST_PROCESSED_ACTIVITY_FILE):
        with open(LAST_PROCESSED_ACTIVITY_FILE, "r") as f:
            return json.load(f)
    return {"last_id": -1}

def save_last_processed_activity(activity_id):
    with open(LAST_PROCESSED_ACTIVITY_FILE, "w") as f:
        json.dump({"last_id": activity_id}, f)

def check_linkedin_activity():
    """
    Monitors a local file for new LinkedIn activity entries.
    """
    if not os.path.exists(LINKEDIN_ACTIVITY_FILE):
        print(f"Warning: {LINKEDIN_ACTIVITY_FILE} not found. No LinkedIn activity to check.")
        return None

    try:
        with open(LINKEDIN_ACTIVITY_FILE, "r") as f:
            activities = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {LINKEDIN_ACTIVITY_FILE}.")
        return None

    if not activities:
        return None

    last_processed = load_last_processed_activity()
    current_last_id = last_processed["last_id"]

    new_activities = [activity for activity in activities if activity["id"] > current_last_id]

    if new_activities:
        # Sort by ID to ensure we process the oldest new activity first
        new_activities.sort(key=lambda x: x["id"])

        # Take the latest new activity for processing
        latest_activity = new_activities[-1]

        # Update last processed ID
        save_last_processed_activity(latest_activity["id"])

        return latest_activity["content"]

    return None

