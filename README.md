# 創建資料表
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(1000) NOT NULL
);

# 使用網站時請記得創建pqc使用者與server資料庫
dbConn = myconn.connect(
    host = 'localhost',   
    user = 'pqc',         
    password = '123456',  
    database = 'server'   #請在資料庫創建一個server的資料庫
)

### 1

# authentication資料夾 流程
先用check.py找檢查碼，生成編號
再用key_main.py輸入編號，生成公私鑰
接下來就可以使用asym_main.py進行身分驗證或是session_key.py產生會議金鑰

# 病患

CREATE TABLE patients (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('男', '女') NOT NULL,
    contact VARCHAR(15) NOT NULL,
    address VARCHAR(255) NOT NULL,
    medical_history TEXT NOT NULL
);

CREATE TABLE health_overview (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    overview TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    record_date DATE NOT NULL,
    record TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE medications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE tests_and_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    test_date DATE NOT NULL,
    test_type VARCHAR(100) NOT NULL,
    results TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    doctor VARCHAR(100) NOT NULL,
    clinic VARCHAR(100) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE health_reminders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    reminder TEXT NOT NULL,
    reminder_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE medical_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL,
    document_name VARCHAR(100) NOT NULL,
    document_path VARCHAR(255) NOT NULL,
    upload_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE health_education_resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resource_name VARCHAR(100) NOT NULL,
    resource_link VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
);

-- 插入範例數據
INSERT INTO patients (id,name, age, gender, contact, address, medical_history) VALUES
('d123456789','王小明', 30, '男', '0912345678', '台北市大安區', '無'),
('c123456789','李小美', 25, '女', '0987654321', '台中市西屯區', '無');

INSERT INTO health_overview (patient_id, overview) VALUES
('d123456789', '健康狀況良好，無重大疾病史'),
('c123456789', '健康狀況良好，無重大疾病史');

INSERT INTO medical_records (patient_id, record_date, record) VALUES
('d123456789', '2024-06-01', '一般健康檢查，結果正常'),
('c123456789', '2024-06-05', '一般健康檢查，結果正常');

INSERT INTO medications (patient_id, medication_name, dosage, start_date, end_date) VALUES
('d123456789', '阿司匹林', '100mg 每日一次', '2024-06-01', NULL),
('c123456789', '布洛芬', '200mg 每日兩次', '2024-06-05', '2024-06-15');

INSERT INTO tests_and_results (patient_id, test_date, test_type, results) VALUES
('d123456789', '2024-06-01', '血液檢查', '正常'),
('c123456789', '2024-06-05', '尿液檢查', '正常');

INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor, clinic) VALUES
('d123456789', '2024-07-01', '10:00:00', '張醫生', '內科'),
('c123456789', '2024-07-05', '11:00:00', '李醫生', '外科');

INSERT INTO health_reminders (patient_id, reminder, reminder_date) VALUES
('d123456789', '每周運動三次', '2024-06-10'),
('c123456789', '每天喝八杯水', '2024-06-12');

INSERT INTO medical_documents (patient_id, document_name, document_path, upload_date) VALUES
('d123456789', '健康檢查報告', '/documents/checkup_report_20240601.pdf', '2024-06-01'),
('c123456789', '健康檢查報告', '/documents/checkup_report_20240605.pdf', '2024-06-05');

INSERT INTO health_education_resources (resource_name, resource_link, description) VALUES
('健康飲食指南', 'https://example.com/healthy-eating', '提供健康飲食建議和食譜'),
('運動指南', 'https://example.com/exercise-guide', '提供不同類型的運動指南和計劃');
