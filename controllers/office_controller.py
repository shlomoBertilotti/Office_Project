from flask import Blueprint, render_template, request, redirect, jsonify

from services.office_service import (
    get_all_offices,
    get_office_by_id,
    create_office,
    update_office,
    delete_office,
    get_employees_by_office,
    assign_employees_to_office
)

from services.employee_service import get_all_employees


office_bp = Blueprint("office", __name__)


# =========================
# HTML PAGES
# =========================

@office_bp.route("/offices")
def offices_page():
    sort_by = request.args.get("sort_by", "id")
    filter_by = request.args.get("filter_by", "all")

    offices = get_all_offices(sort_by=sort_by, filter_by=filter_by)

    return render_template(
        "offices.html",
        offices=offices,
        sort_by=sort_by,
        filter_by=filter_by
    )


@office_bp.route("/offices/add", methods=["GET", "POST"])
def add_office_page():
    if request.method == "POST":
        floor = request.form["floor"]
        room_number = request.form["room_number"]
        capacity = request.form["capacity"]

        create_office(floor, room_number, capacity)

        return redirect("/offices")

    return render_template("office_form.html", office=None)


@office_bp.route("/offices/<int:office_id>")
def office_details_page(office_id):
    office = get_office_by_id(office_id)
    employees = get_employees_by_office(office_id)

    return render_template(
        "office_details.html",
        office=office,
        employees=employees
    )


@office_bp.route("/offices/<int:office_id>/edit", methods=["GET", "POST"])
def edit_office_page(office_id):
    office = get_office_by_id(office_id)

    if request.method == "POST":
        floor = request.form["floor"]
        room_number = request.form["room_number"]
        capacity = request.form["capacity"]

        update_office(office_id, floor, room_number, capacity)

        return redirect("/offices")

    return render_template("office_form.html", office=office)


@office_bp.route("/offices/<int:office_id>/delete", methods=["POST"])
def delete_office_page(office_id):
    delete_office(office_id)
    return redirect("/offices")


@office_bp.route("/offices/<int:office_id>/assign", methods=["GET", "POST"])
def assign_employees_page(office_id):
    office = get_office_by_id(office_id)
    employees = get_all_employees()

    if request.method == "POST":
        employee_ids = request.form.getlist("employee_ids")
        assign_employees_to_office(office_id, employee_ids)

        return redirect(f"/offices/{office_id}")

    return render_template(
        "assign_employees.html",
        office=office,
        employees=employees
    )


# =========================
# REST API
# =========================

@office_bp.route("/api/offices", methods=["GET"])
def api_get_offices():
    sort_by = request.args.get("sort_by", "id")
    filter_by = request.args.get("filter_by", "all")

    offices = get_all_offices(sort_by=sort_by, filter_by=filter_by)

    return jsonify([dict(office) for office in offices])


@office_bp.route("/api/offices/<int:office_id>", methods=["GET"])
def api_get_office(office_id):
    office = get_office_by_id(office_id)

    if office is None:
        return jsonify({"error": "Office not found"}), 404

    return jsonify(dict(office))


@office_bp.route("/api/offices", methods=["POST"])
def api_create_office():
    data = request.get_json()

    create_office(
        data["floor"],
        data["room_number"],
        data["capacity"]
    )

    return jsonify({"message": "Office created successfully"}), 201


@office_bp.route("/api/offices/<int:office_id>", methods=["PUT"])
def api_update_office(office_id):
    data = request.get_json()

    update_office(
        office_id,
        data["floor"],
        data["room_number"],
        data["capacity"]
    )

    return jsonify({"message": "Office updated successfully"})


@office_bp.route("/api/offices/<int:office_id>", methods=["DELETE"])
def api_delete_office(office_id):
    delete_office(office_id)

    return jsonify({"message": "Office deleted successfully"})


@office_bp.route("/api/offices/<int:office_id>/employees", methods=["GET"])
def api_get_employees_by_office(office_id):
    employees = get_employees_by_office(office_id)

    return jsonify([dict(employee) for employee in employees])


@office_bp.route("/api/offices/<int:office_id>/assign", methods=["PUT"])
def api_assign_employees_to_office(office_id):
    data = request.get_json()
    employee_ids = data["employee_ids"]

    assign_employees_to_office(office_id, employee_ids)

    return jsonify({"message": "Employees assigned to office successfully"})