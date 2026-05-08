-- ==========================================
-- 10/10 Hospital-Grade Lab Reference Engine
-- SQLite Schema for:
-- Normal / Low / High / Critical
-- LOINC Mapped
-- Demographic Based
-- AI Ready
-- ==========================================

PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. MASTER TEST TABLE
-- ==========================================
CREATE TABLE tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_code TEXT UNIQUE NOT NULL,
    loinc_code TEXT UNIQUE,
    test_name TEXT NOT NULL,
    category TEXT,
    specimen TEXT,
    default_unit TEXT NOT NULL,
    method TEXT,
    active INTEGER DEFAULT 1
);

-- ==========================================
-- 2. DEMOGRAPHICS
-- ==========================================
CREATE TABLE demographics (
    demographic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT CHECK(gender IN ('Male','Female','Any')),
    min_age_days INTEGER NOT NULL,
    max_age_days INTEGER NOT NULL,
    notes TEXT
);

-- ==========================================
-- 3. REFERENCE RANGES
-- ==========================================
CREATE TABLE reference_ranges (
    range_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    demographic_id INTEGER NOT NULL,

    low_value REAL,
    high_value REAL,

    critical_low REAL,
    critical_high REAL,

    unit TEXT NOT NULL,

    panic_low_message TEXT,
    panic_high_message TEXT,

    FOREIGN KEY(test_id) REFERENCES tests(test_id),
    FOREIGN KEY(demographic_id) REFERENCES demographics(demographic_id)
);

-- ==========================================
-- 4. PATIENTS
-- ==========================================
CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mrn TEXT UNIQUE,
    full_name TEXT,
    gender TEXT,
    dob DATE
);

-- ==========================================
-- 5. LAB RESULTS
-- ==========================================
CREATE TABLE lab_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,

    result_value REAL NOT NULL,
    result_unit TEXT NOT NULL,

    result_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    status TEXT,
    interpretation TEXT,

    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY(test_id) REFERENCES tests(test_id)
);

-- ==========================================
-- SAMPLE TEST DATA
-- ==========================================
INSERT INTO tests
(test_code, loinc_code, test_name, category, specimen, default_unit)
VALUES
('HB', '718-7', 'Hemoglobin', 'CBC', 'Blood', 'g/dL'),
('GLU', '2345-7', 'Fasting Glucose', 'Diabetes', 'Blood', 'mg/dL'),
('TSH', '3016-3', 'TSH', 'Hormone', 'Serum', 'mIU/L'),
('CR', '2160-0', 'Creatinine', 'Kidney', 'Serum', 'mg/dL');

-- ==========================================
-- DEMOGRAPHICS
-- ==========================================
INSERT INTO demographics
(gender, min_age_days, max_age_days, notes)
VALUES
('Male', 6570, 21900, 'Adult Male'),
('Female', 6570, 21900, 'Adult Female'),
('Any', 0, 28, 'Neonate'),
('Any', 29, 6569, 'Child');

-- ==========================================
-- REFERENCE RANGES
-- ==========================================
INSERT INTO reference_ranges
(test_id, demographic_id, low_value, high_value,
 critical_low, critical_high, unit,
 panic_low_message, panic_high_message)
VALUES

-- Hemoglobin Male
(1,1,13.5,17.5,7.0,22.0,'g/dL',
 'Severe anemia',
 'Polycythemia emergency'),

-- Hemoglobin Female
(1,2,12.0,15.5,7.0,20.0,'g/dL',
 'Severe anemia',
 'Very high Hb'),

-- Glucose Adult
(2,1,70,99,40,500,'mg/dL',
 'Hypoglycemia emergency',
 'Hyperglycemic crisis'),

(2,2,70,99,40,500,'mg/dL',
 'Hypoglycemia emergency',
 'Hyperglycemic crisis'),

-- TSH
(3,1,0.4,4.0,0.1,20,'mIU/L',
 'Severe hyperthyroid risk',
 'Severe hypothyroid risk'),

(3,2,0.4,4.5,0.1,20,'mIU/L',
 'Severe hyperthyroid risk',
 'Severe hypothyroid risk');

-- ==========================================
-- SAMPLE PATIENT
-- ==========================================
INSERT INTO patients
(mrn, full_name, gender, dob)
VALUES
('MRN001','Ali Khan','Male','1998-05-10');

-- ==========================================
-- SAMPLE RESULT
-- ==========================================
INSERT INTO lab_results
(patient_id, test_id, result_value, result_unit)
VALUES
(1,1,6.8,'g/dL');

-- ==========================================
-- 10/10 CLASSIFICATION QUERY
-- ==========================================
SELECT
    p.full_name,
    t.test_name,
    t.loinc_code,
    lr.result_value,
    rr.unit,

    CASE
        WHEN lr.result_value <= rr.critical_low
            THEN 'Critical Low'

        WHEN lr.result_value < rr.low_value
            THEN 'Low'

        WHEN lr.result_value >= rr.critical_high
            THEN 'Critical High'

        WHEN lr.result_value > rr.high_value
            THEN 'High'

        ELSE 'Normal'
    END AS status,

    CASE
        WHEN lr.result_value <= rr.critical_low
            THEN rr.panic_low_message

        WHEN lr.result_value >= rr.critical_high
            THEN rr.panic_high_message

        ELSE 'No panic'
    END AS interpretation

FROM lab_results lr
JOIN patients p ON p.patient_id = lr.patient_id
JOIN tests t ON t.test_id = lr.test_id
JOIN demographics d
    ON d.gender IN (p.gender,'Any')
JOIN reference_ranges rr
    ON rr.test_id = t.test_id
   AND rr.demographic_id = d.demographic_id;

-- ==========================================
-- OUTPUT EXAMPLE
-- Ali Khan | Hemoglobin | 718-7 | 6.8 | g/dL
-- Critical Low | Severe anemia
-- ==========================================