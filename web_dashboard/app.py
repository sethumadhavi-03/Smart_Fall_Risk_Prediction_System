from flask import Flask, render_template, request, redirect, session, Response
from flask_socketio import SocketIO
import csv

app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- USER STORAGE ----------------
users = {}   # {username: password}

# ---------------- FALL DATA ----------------
fall_events = []

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    return render_template("register.html")

# ---------------- REGISTER ----------------

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    if username in users:
        return "User already exists ❌"

    users[username] = password
    return redirect("/login_page")

# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return redirect("/dashboard")

    return "Invalid Login ❌"

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login_page")

    return render_template("index.html", falls=fall_events, user=session["user"])

# ---------------- HISTORY ----------------

@app.route("/history")
def history():
    return render_template("history.html", falls=fall_events)

# ---------------- DOWNLOAD CSV ----------------

@app.route("/download")
def download():
    def generate():
        data = []

        # Header
        data.append(["Time", "Severity", "Torso Angle", "Shoulder Tilt", "Head-Hip Diff", "Cause"])

        for fall in fall_events:
            severity = "CRITICAL 🔴" if fall["risk"] == 3 else "HIGH 🟠" if fall["risk"] == 2 else "LOW 🟢"

            causes = []
            if fall["torso_angle"] > 45:
                causes.append("High torso tilt")
            if fall["shoulder_tilt"] > 0.1:
                causes.append("Shoulder imbalance")
            if fall["head_hip_diff"] < 0.15:
                causes.append("Body collapse")

            cause_text = ", ".join(causes)

            data.append([
                fall["time"],
                severity,
                fall["torso_angle"],
                fall["shoulder_tilt"],
                fall["head_hip_diff"],
                cause_text
            ])

        output = ""
        for row in data:
            output += ",".join(map(str, row)) + "\n"

        return output

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=fall_history.csv"}
    )

# ---------------- ANALYTICS ----------------

@app.route("/analytics")
def analytics():

    total = len(fall_events)
    high = len([f for f in fall_events if f["risk"] >= 2])

    backward = 0
    side = 0
    unstable = 0

    # -------- CORRECT CLASSIFICATION --------
    for f in fall_events:
        t = f.get("type")

        if t == "BACKWARD FALL":
            backward += 1

        elif t == "SIDE FALL":
            side += 1
     
        elif t == "UNSTABLE POSTURE":
            unstable += 1
        

    # -------- MOST COMMON CAUSE --------
    causes = {
        "High Torso Tilt": backward,
        "Shoulder Imbalance": side,
        "Unstable Posture": unstable
    }

    most_common = max(causes, key=causes.get) if total > 0 else "No Data"
    print("BACKEND COUNTS →", backward, side, unstable)

    return render_template("analytics.html",
        total=total,
        high=high,
        backward=backward,
        side=side,
        unstable=unstable,
        most_common=most_common
    )

# ---------------- SOCKET ----------------

@socketio.on('new_fall')
def handle_new_fall(data):
    print("RECEIVED DATA:", data) 
    fall_events.append(data)

    if len(fall_events) > 20:
        fall_events.pop(0)

    socketio.emit('new_fall', data)

# ---------------- RUN ----------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)