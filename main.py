from flask import Flask, render_template
from services.database_service import create_tables
from controllers.office_controller import office_bp
from controllers.employee_controller import employee_bp

app = Flask(__name__)

app.register_blueprint(office_bp)
app.register_blueprint(employee_bp)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=5001)