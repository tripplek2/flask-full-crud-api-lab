from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Validate request
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate new ID
    new_id = max(event.id for event in events) + 1 if events else 1

    # Create event
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return "", 204

    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
