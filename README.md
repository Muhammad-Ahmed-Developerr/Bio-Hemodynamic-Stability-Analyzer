# ❤️ Bio Hemodynamic Stability Analyzer

> 🏥 Intelligent Cardiovascular Monitoring & Risk Classification System
> 🎓 CS-109 – Computer Programming | Biomedical Application
> 📅 Spring Semester 2026

---

## 🚀 Overview

**Bio Hemodynamic Stability Analyzer** is a Streamlit-based biomedical application designed to evaluate cardiovascular stability using real-time clinical parameters.

The system analyzes:

* 👤 Patient Age
* ❤️ Heart Rate (BPM)
* 🩸 Systolic Blood Pressure
* 🩸 Diastolic Blood Pressure
* 🌡️ Oxygen Saturation (SpO₂)
* 📊 Mean Arterial Pressure (MAP)

Based on these inputs, it classifies the patient into:

* 🟢 Stable
* 🟡 At Risk
* 🔴 Critical

And provides:

* 🩺 Clinical condition assessment
* 🚑 Emergency recommendation level
* 📄 Downloadable diagnostic reports
* 📊 Analytical visualizations

---

## ✨ Features

### 🧠 1. Multi-Parameter Cardiovascular Analysis

* Heart rate abnormality detection (Bradycardia / Tachycardia)
* Blood pressure classification (Hypotension / Hypertension)
* Oxygen desaturation detection
* MAP auto-calculation
* Severity-based risk engine

---

### 📊 2. Real-Time Calculations

Mean Arterial Pressure is calculated using:

```python
MAP = (Systolic + 2 * Diastolic) / 3
```

System uses threshold-based clinical logic to detect instability.

---

### 📈 3. Interactive Dashboard

* Patient history tracking (session-based)
* Stability distribution charts
* Heart rate trend visualization
* Blood pressure comparison graph
* Oxygen saturation insights
* CSV export of all records

---

### 💾 4. Multi-Format Report Generation

Each patient assessment can be exported as:

* 📄 TXT File
* 📊 CSV File
* 📑 PDF Report
* 🖼️ PNG Image
* 📸 JPG Image

Reports include:

* Timestamp
* All vitals
* MAP value
* Clinical interpretation
* Stability classification
* Medical recommendation

---

## 🧠 Clinical Logic Example

```python
if heart_rate < 50 or spo2 < 90:
    stability = "Critical"
elif systolic < 90 or systolic > 180:
    stability = "At Risk"
else:
    stability = "Stable"
```

The decision engine uses:

* ✔ Nested conditional statements
* ✔ Logical operators (and / or)
* ✔ Comparison operators
* ✔ Mathematical formulas
* ✔ Multi-variable risk scoring

---

## 🛠️ Tech Stack

| Technology    | Purpose                 |
| ------------- | ----------------------- |
| 🐍 Python     | Core Logic              |
| 🎨 Streamlit  | Web Interface           |
| 📊 Pandas     | Data Management         |
| 📈 Matplotlib | Charts & Graphs         |
| 🧮 NumPy      | Calculations            |
| 📑 FPDF       | PDF Reports             |
| 🖼️ Pillow    | Image Report Generation |

---

## 📂 Project Structure

```
Hemodynamic-Stability-Analyzer/
│
├── hemodynamic.py      # Main Application File
├── README.md           # Project Documentation
└── requirements.txt    # Dependencies
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/hemodynamic-analyzer.git
cd hemodynamic-analyzer
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pandas numpy matplotlib pillow fpdf
```

---

## ▶️ Run Application

```bash
streamlit run hemodynamic.py
```

Open browser:

```
http://localhost:8501
```

---

## 📊 Assignment Coverage

| Requirement          | Implementation                       |
| -------------------- | ------------------------------------ |
| Input Design         | Sliders, number inputs, select boxes |
| Conditional Logic    | Multi-branch clinical decision tree  |
| Mathematical Formula | MAP Calculation                      |
| Data Structures      | Lists & Dictionaries                 |
| Modular Programming  | Multiple user-defined functions      |
| Data Visualization   | Charts & Graphs                      |
| File Handling        | Multi-format report export           |

---

## 📈 Analytical Capabilities

* Stability distribution metrics
* Heart rate abnormality detection
* Blood pressure trend monitoring
* Oxygen saturation alerts
* Exportable dataset

---

## 🔒 Disclaimer

This system is developed for academic and educational purposes.

It does NOT replace real-time medical supervision or professional healthcare diagnosis.

In emergency situations, contact medical services immediately.

---

## 👨‍💻 Academic Context

**Course:** CS-109 Computer Programming
**Domain:** Biomedical Systems
**Semester:** Spring 2026

---

## 🌟 Key Strengths

* 🔥 Clinical-style decision modeling
* 📊 Real-time calculation engine
* 💡 Clear severity classification
* 📁 Professional report generation
* ⚡ Modular and scalable architecture

---

## 📌 Future Enhancements

* Database integration (MongoDB / PostgreSQL)
* Real-time IoT sensor integration
* AI-based cardiovascular risk prediction
* Cloud deployment
* Multi-user authentication system

---

# ❤️ Bio Hemodynamic Stability Analyzer

### Intelligent Cardiovascular Monitoring System

Built with logic. Designed for precision. Powered by Python.
