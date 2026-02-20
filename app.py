from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey123"

users = {
    "admin": "1234",
    "ralph": "mathlover"
}


attendance = {}  

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("attendance_page"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if username in users:
            error = "Username already exists"
        elif password != confirm:
            error = "Passwords do not match"
        else:
            users[username] = password
            success = "Registration successful! You can now log in"
    return render_template("register.html", error=error, success=success)

@app.route("/attendance", methods=["GET", "POST"])
def attendance_page():
    if "user" not in session:
        return redirect(url_for("login"))

    message = None

    if request.method == "POST":
        date = request.form["date"]
        student = request.form["student"]
        status = request.form["status"].capitalize()

        if date not in attendance:
            attendance[date] = {}

        attendance[date][student] = status
        message = f"Record for {student} on {date} set to {status}"

    search_query = request.args.get("search", "").strip().lower()

    filtered_attendance = {}

    if search_query:
        for date, records in attendance.items():
            for student, status in records.items():
                if search_query in student.lower():
                    if date not in filtered_attendance:
                        filtered_attendance[date] = {}
                    filtered_attendance[date][student] = status
    else:
        filtered_attendance = attendance

    student_stats = {}
    for date, records in filtered_attendance.items():
        for student, status in records.items():
            if student not in student_stats:
                student_stats[student] = {"Present": 0, "Absent": 0}
            if status in student_stats[student]:
                student_stats[student][status] += 1

    return render_template(
        "attendance.html",
        attendance=filtered_attendance,
        student_stats=student_stats,
        message=message,
        search_query=search_query
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
