from flask import Blueprint, render_template, request, redirect, jsonify

from services.employee_service import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)

from services.office_service import get_all_offices


employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/employees")
def employees_page():
    sort_by = request.args.get("sort_by", "id")
    min_seniority = request.args.get("min_seniority")

    employees = get_all_employees(
        sort_by=sort_by,
        min_seniority=min_seniority
    )

    return render_template(
        "employees.html",
        employees=employees,
        sort_by=sort_by,
        min_seniority=min_seniority
    )


@employee_bp.route("/employees/add", methods=["GET", "POST"])
def add_employee_page():
    offices = get_all_offices()

    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        hire_date = request.form["hire_date"]
        salary = request.form["salary"]
        office_id = request.form["office_id"]

        create_employee(name, department, hire_date, salary, office_id)

        return redirect("/employees")

    return render_template(
        "employee_form.html",
        employee=None,
        offices=offices
    )


@employee_bp.route("/employees/<int:employee_id>")
def employee_details_page(employee_id):
    employee = get_employee_by_id(employee_id)

    return render_template(
        "employee_details.html",
        employee=employee
    )


@employee_bp.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee_page(employee_id):
    employee = get_employee_by_id(employee_id)
    offices = get_all_offices()

    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        hire_date = request.form["hire_date"]
        salary = request.form["salary"]
        office_id = request.form["office_id"]

        update_employee(
            employee_id,
            name,
            department,
            hire_date,
            salary,
            office_id
        )

        return redirect("/employees")

    return render_template(
        "employee_form.html",
        employee=employee,
        offices=offices
    )


@employee_bp.route("/employees/<int:employee_id>/delete", methods=["POST"])
def delete_employee_page(employee_id):
    delete_employee(employee_id)
    return redirect("/employees")


@employee_bp.route("/api/employees", methods=["GET"])
def api_get_employees():
    sort_by = request.args.get("sort_by", "id")
    min_seniority = request.args.get("min_seniority")

    employees = get_all_employees(
        sort_by=sort_by,
        min_seniority=min_seniority
    )

    return jsonify([dict(employee) for employee in employees])


@employee_bp.route("/api/employees/<int:employee_id>", methods=["GET"])
def api_get_employee(employee_id):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(dict(employee))


@employee_bp.route("/api/employees", methods=["POST"])
def api_create_employee():
    data = request.get_json()

    create_employee(
        data["name"],
        data["department"],
        data["hire_date"],
        data["salary"],
        data.get("office_id")
    )

    return jsonify({"message": "Employee created successfully"}), 201


@employee_bp.route("/api/employees/<int:employee_id>", methods=["PUT"])
def api_update_employee(employee_id):
    data = request.get_json()

    update_employee(
        employee_id,
        data["name"],
        data["department"],
        data["hire_date"],
        data["salary"],
        data.get("office_id")
    )

    return jsonify({"message": "Employee updated successfully"})


@employee_bp.route("/api/employees/<int:employee_id>", methods=["DELETE"])
def api_delete_employee(employee_id):
    delete_employee(employee_id)

    return jsonify({"message": "Employee deleted successfully"})