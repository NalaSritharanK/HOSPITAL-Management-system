CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10),
    insurance_type VARCHAR(50)
);


CREATE TABLE admissions (
    admission_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    dept_id INT REFERENCES departments(dept_id),
    admit_date DATE NOT NULL,
    discharge_date DATE,
    total_cost DECIMAL(10, 2)
);
CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,
    resource_type VARCHAR(50), 
    status VARCHAR(20), 
    department VARCHAR(50)
);
CREATE TABLE staffing (
    doctorid INTEGER PRIMARY KEY,
    dept VARCHAR(50),
    utilizationrate NUMERIC(5,2), 
    shifthours INTEGER            
);

