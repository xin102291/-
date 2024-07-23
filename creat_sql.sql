CREATE DATABASE IF NOT EXISTS server;

USE server;

CREATE TABLE IF NOT EXISTS patients (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('男', '女') NOT NULL,
    contact VARCHAR(15) NOT NULL,
    address VARCHAR(255) NOT NULL,
    medical_history TEXT NOT NULL,
    pk CHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS hospitals (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    contact VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS  doctors (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('男', '女') NOT NULL,
    contact VARCHAR(15) NOT NULL,
    address VARCHAR(255) NOT NULL,
    hospital_id VARCHAR(10) NOT NULL,
    hospital_name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);

CREATE TABLE IF NOT EXISTS  medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    record_date DATE NOT NULL,
    record TEXT NOT NULL,
    doctor_id VARCHAR(10) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    hospital_id VARCHAR(10) NOT NULL,
    hospital_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);

CREATE TABLE IF NOT EXISTS  medications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS  tests_and_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    test_date DATE NOT NULL,
    test_type VARCHAR(100) NOT NULL,
    results TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS  appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    doctor VARCHAR(100) NOT NULL,
    clinic VARCHAR(100) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS  health_reminders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    reminder TEXT NOT NULL,
    reminder_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS  medical_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    document_name VARCHAR(100) NOT NULL,
    document_path VARCHAR(255) NOT NULL,
    upload_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

INSERT INTO patients (id,name, age, gender, contact, address, medical_history,pk) VALUES
('Q224390730','林玟欣', 21, '女', '0912345678', '台北市大安區', '健康狀況良好，無重大疾病史',"010100010011001000110010001101000011001100111001001100000011011100110011000000000000000110010010110000100000000000000001010100011110010100000000000000010100110100010100");

INSERT INTO medications (patient_id, medication_name, dosage, start_date, end_date) VALUES
('Q224390730', '阿司匹林', '100mg 每日一次', '2024-06-01', NULL),
('Q224390730', '布洛芬', '200mg 每日兩次', '2024-06-05', '2024-06-15');

INSERT INTO tests_and_results (patient_id, test_date, test_type, results) VALUES
('Q224390730', '2024-06-01', '年度體檢', '血壓: 120/80 mmHg, 心率: 72 bpm, 血糖: 5.6 mmol/L, BMI: 22.5, 肝功能(ALT): 30 U/L, 血紅蛋白: 14.2 g/dL, 血小板計數: 250 x 10^9/L, 整體評估: 正常'),

('Q224390730', '2024-12-15', '半年度檢查', '血壓: 118/78 mmHg, 心率: 70 bpm, 血糖: 5.4 mmol/L, BMI: 22.3, 肝功能(ALT): 28 U/L, 血紅蛋白: 14.5 g/dL, 血小板計數: 260 x 10^9/L, 整體評估: 正常'),

('Q224390730', '2025-06-01', '年度體檢', '血壓: 122/82 mmHg, 心率: 74 bpm, 血糖: 5.7 mmol/L, BMI: 22.7, 肝功能(ALT): 32 U/L, 血紅蛋白: 14.0 g/dL, 血小板計數: 245 x 10^9/L, 整體評估: 輕微肝功能異常'),

('Q224390730', '2025-12-15', '半年度檢查', '血壓: 121/80 mmHg, 心率: 71 bpm, 血糖: 5.5 mmol/L, BMI: 22.4, 肝功能(ALT): 29 U/L, 血紅蛋白: 14.3 g/dL, 血小板計數: 255 x 10^9/L, 整體評估: 正常'),

('Q224390730', '2024-09-01', '血壓和心率檢查', '血壓: 119/79 mmHg, 心率: 73 bpm, 評估: 正常範圍內'),

('Q224390730', '2024-10-15', '血糖檢查', '血糖: 5.8 mmol/L, 評估: 略高，建議注意飲食'),

('Q224390730', '2025-03-01', '肝功能檢查', '肝功能(ALT): 35 U/L, 評估: 輕度異常，建議複查'),

('Q224390730', '2025-09-15', '血液常規檢查', '血紅蛋白: 13.8 g/dL, 血小板計數: 240 x 10^9/L, 評估: 正常範圍內');

INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor, clinic) VALUES
('Q224390730', '2024-07-01', '10:00:00', '張醫生', '內科'),
('Q224390730', '2024-07-05', '11:00:00', '李醫生', '外科');

INSERT INTO health_reminders (patient_id, reminder, reminder_date) VALUES
('Q224390730', '每周運動三次', '2024-06-10'),
('Q224390730', '每天喝八杯水', '2024-06-12');

INSERT INTO medical_documents (patient_id, document_name, document_path, upload_date) VALUES
('Q224390730', '健康檢查報告', '/documents/checkup_report_20240601.pdf', '2024-06-01'),
('Q224390730', '健康檢查報告', '/documents/checkup_report_20240605.pdf', '2024-06-05');

-- 插入3筆醫院資料
INSERT INTO hospitals (id, name, address, contact) VALUES
('H001', '台北醫院', '台北市中正區仁愛路1段1號', '02-12345678'),
('H002', '台中醫院', '台中市西區中港路2段2號', '04-87654321'),
('H003', '高雄醫院', '高雄市前鎮區中華五路3段3號', '07-65432198');

-- 插入3筆醫生資料
INSERT INTO doctors (id, name, age, gender, contact, address, hospital_id, hospital_name, position, department) VALUES
('D001', '陳醫生', 45, '男', '0912345678', '台北市大安區信義路100號', 'H001', '台北醫院', '主治醫師', '內科'),
('D002', '林醫生', 38, '女', '0987654321', '台中市北屯區北平路200號', 'H002', '台中醫院', '主治醫師', '外科'),
('D003', '王醫生', 50, '男', '0978123456', '高雄市苓雅區四維路300號', 'H003', '高雄醫院', '主任醫師', '心臟科');

-- 插入4筆病歷紀錄資料
INSERT INTO medical_records (patient_id, record_date, record, doctor_id, doctor_name, hospital_id, hospital_name) VALUES
('Q224390730', '2023-06-01', '患者出現輕微頭痛症狀，開立止痛藥。', 'D001', '陳醫生', 'H001', '台北醫院'),
('Q224390730', '2023-07-15', '患者進行例行體檢，健康狀況良好。', 'D002', '林醫生', 'H002', '台中醫院'),
('Q224390730', '2023-08-20', '患者因胸痛前來就診，安排心臟檢查。', 'D003', '王醫生', 'H003', '高雄醫院'),
('Q224390730', '2023-09-10', '患者心臟檢查結果正常，無需進一步治療。', 'D003', '王醫生', 'H003', '高雄醫院');

