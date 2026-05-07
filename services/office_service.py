from services.database_service import get_connection


def get_all_offices(sort_by="id", filter_by="all"):
    allowed_sort_columns = {
        "id": "offices.id",
        "floor": "offices.floor",
        "room_number": "offices.room_number",
        "capacity": "offices.capacity",
        "employees_count": "employees_count"
    }

    sort_column = allowed_sort_columns.get(sort_by, "offices.id")

    query = """
        SELECT
            offices.id,
            offices.floor,
            offices.room_number,
            offices.capacity,
            COUNT(employees.id) AS employees_count
        FROM offices
        LEFT JOIN employees ON offices.id = employees.office_id
        GROUP BY offices.id
    """

    if filter_by == "empty":
        query += " HAVING employees_count = 0"
    elif filter_by == "available":
        query += " HAVING employees_count < offices.capacity"
    elif filter_by == "overloaded":
        query += " HAVING employees_count > offices.capacity"

    query += f" ORDER BY {sort_column}"

    conn = get_connection()
    offices = conn.execute(query).fetchall()
    conn.close()

    return offices


def get_office_by_id(office_id):
    conn = get_connection()

    office = conn.execute("""
        SELECT
            offices.id,
            offices.floor,
            offices.room_number,
            offices.capacity,
            COUNT(employees.id) AS employees_count
        FROM offices
        LEFT JOIN employees ON offices.id = employees.office_id
        WHERE offices.id = ?
        GROUP BY offices.id
    """, (office_id,)).fetchone()

    conn.close()
    return office


def create_office(floor, room_number, capacity):
    conn = get_connection()

    conn.execute("""
        INSERT INTO offices (floor, room_number, capacity)
        VALUES (?, ?, ?)
    """, (floor, room_number, capacity))

    conn.commit()
    conn.close()


def update_office(office_id, floor, room_number, capacity):
    conn = get_connection()

    conn.execute("""
        UPDATE offices
        SET floor = ?, room_number = ?, capacity = ?
        WHERE id = ?
    """, (floor, room_number, capacity, office_id))

    conn.commit()
    conn.close()


def delete_office(office_id):
    conn = get_connection()

    conn.execute("""
        UPDATE employees
        SET office_id = NULL
        WHERE office_id = ?
    """, (office_id,))

    conn.execute("""
        DELETE FROM offices
        WHERE id = ?
    """, (office_id,))

    conn.commit()
    conn.close()


def get_employees_by_office(office_id):
    conn = get_connection()

    employees = conn.execute("""
        SELECT
            employees.id,
            employees.name,
            employees.department,
            employees.hire_date,
            employees.salary,
            employees.office_id,
            CAST((julianday('now') - julianday(employees.hire_date)) / 365 AS INTEGER) AS seniority
        FROM employees
        WHERE employees.office_id = ?
        ORDER BY employees.name
    """, (office_id,)).fetchall()

    conn.close()
    return employees


def assign_employees_to_office(office_id, employee_ids):
    conn = get_connection()

    for employee_id in employee_ids:
        conn.execute("""
            UPDATE employees
            SET office_id = ?
            WHERE id = ?
        """, (office_id, employee_id))

    conn.commit()
    conn.close()