import psycopg2
from faker import Faker
import random
from datetime import timedelta


fake = Faker()

try:
    conn = psycopg2.connect(
        dbname="HOSPITAL",
        user="postgres",
        password="nalasri", 
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    print("Connected to database successfully!")

    depts = ['Cardiology', 'Oncology', 'Orthopedics', 'Pediatrics', 'Emergency']
    dept_map = {}
    for dept in depts:
        cursor.execute("INSERT INTO departments (dept_name) VALUES (%s) ON CONFLICT (dept_name) DO UPDATE SET dept_name = EXCLUDED.dept_name RETURNING dept_id", (dept,))
        dept_map[dept] = cursor.fetchone()[0]


    patient_ids = []
    for _ in range(200):
        cursor.execute(
            "INSERT INTO patients (age, gender, insurance_type) VALUES (%s, %s, %s) RETURNING patient_id",
            (random.randint(1, 90), random.choice(['Male', 'Female']), random.choice(['Private', 'Public', 'None']))
        )
        patient_ids.append(cursor.fetchone()[0])

    
    for dept_name in depts:
        for _ in range(3): 
            cursor.execute(
                "INSERT INTO Staffing (dept, UtilizationRate, ShiftHours) VALUES (%s, %s, %s)",
                (dept_name, round(random.uniform(60.0, 95.0), 2), random.choice([8, 12]))
            )

    for dept_name in depts:
        for r_type in ['Bed', 'Ventilator']:
            for _ in range(5): 
                cursor.execute(
                    "INSERT INTO resources (resource_type, status, department) VALUES (%s, %s, %s)",
                    (r_type, random.choice(['Occupied', 'Available']), dept_name)
                )

    for _ in range(650):
        admit = fake.date_between(start_date='-1y', end_date='today')
        discharge = admit + timedelta(days=random.randint(1, 14))
        cursor.execute(
            """INSERT INTO admissions (patient_id, dept_id, admit_date, discharge_date, total_cost) 
               VALUES (%s, %s, %s, %s, %s)""",
            (random.choice(patient_ids), random.choice(list(dept_map.values())), admit, discharge, round(random.uniform(1000, 25000), 2))
        )

    conn.commit()
    print("Successfully generated 650+ records across 5 tables!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()
