from services.database_service import get_connection


def get_all_employees(sort_by="id", min_seniority=None):
    allowed_sort_columns = {
        "id": "employees.id",
        "name": "employees.name",
        "department": "employees.department",
        "hire_date": "employees.hire_date",
        "salary": "employees.salary",
        "seniority": "seniority"
    }

    sort_column = allowed_sort_columns.get(sort_by, "employees.id")

    query = """
        SELECT
            employees.id,
            employees.name,
            employees.department,
            employees.hire_date,
            employees.salary,
            employees.office_id,
            offices.floor AS office_floor,
            offices.room_number AS office_room,
            CAST((julianday('now') - julianday(employees.hire_date)) / 365 AS INTEGER) AS seniority
        FROM employees
        LEFT JOIN offices ON employees.office_id = offices.id
    """

    params = []

    if min_seniority:
        query += """
            WHERE CAST((julianday('now') - julianday(employees.hire_date)) / 365 AS INTEGER) >= ?
        """
        params.append(min_seniority)

    query += f" ORDER BY {sort_column}"

    conn = get_connection()
    employees = conn.execute(query, params).fetchall()
    conn.close()

    return employees


def get_employee_by_id(employee_id):
    conn = get_connection()

    employee = conn.execute("""
        SELECT
            employees.id,
            employees.name,
            employees.department,
            employees.hire_date,
            employees.salary,
            employees.office_id,
            offices.floor AS office_floor,
            offices.room_number AS office_room,
            CAST((julianday('now') - julianday(employees.hire_date)) / 365 AS INTEGER) AS seniority
        FROM employees
        LEFT JOIN offices ON employees.office_id = offices.id
        WHERE employees.id = ?
    """, (employee_id,)).fetchone()

    conn.close()
    return employee


def create_employee(name, department, hire_date, salary, office_id):
    if office_id == "":
        office_id = None

    conn = get_connection()

    conn.execute("""
        INSERT INTO employees (name, department, hire_date, salary, office_id)
        VALUES (?, ?, ?, ?, ?)
    """, (name, department, hire_date, salary, office_id))

    conn.commit()
    conn.close()


def update_employee(employee_id, name, department, hire_date, salary, office_id):
    if office_id == "":
        office_id = None

    conn = get_connection()

    conn.execute("""
        UPDATE employees
        SET name = ?, department = ?, hire_date = ?, salary = ?, office_id = ?
        WHERE id = ?
    """, (name, department, hire_date, salary, office_id, employee_id))

    conn.commit()
    conn.close()


def delete_employee(employee_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))

    conn.commit()
    conn.close()