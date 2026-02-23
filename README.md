# 👁️ Bio-Eye Care Navigator

> 🏥 Intelligent Ophthalmic Diagnosis & Visual Acuity Testing System
> 🎓 CS-109 – Computer Programming | NED University of Engineering & Technology
> 📅 Spring Semester 2026 | Batch 2025

---

## 🚀 Overview

**Bio-Eye Care Navigator** is a biomedical Streamlit-based web application designed to evaluate patient eye health using multi-parameter clinical logic.

It analyzes:

* 👤 Patient Age
* 👁️ Primary Symptom
* 🔍 Visual Acuity (Snellen)
* 📊 Intraocular Pressure (IOP)
* 🧬 Family History

The system then classifies the patient into:

* 🟢 Normal
* 🟡 Abnormal
* 🔴 Critical

And provides:

* 🩺 Condition diagnosis
* 👨‍⚕️ Specialist recommendation
* 💡 Clinical reasoning
* 📄 Downloadable reports (5 formats)

---

## ✨ Features

### 📝 1. Smart Patient Diagnosis

* Multi-parameter clinical decision tree
* Age-adjusted medical logic
* IOP threshold analysis
* Risk factor modification (family history)
* Severity classification engine

---

### 👓 2. Interactive Snellen Visual Acuity Test

* Built-in Snellen chart
* 20/20 to 20/200 grading
* Automated interpretation
* Personalized recommendations

---

### 📊 3. Patient History & Analytics Dashboard

* Session-based patient record storage
* Color-coded severity tracking
* Summary metrics
* Symptom distribution charts
* Age analysis histogram
* Severity breakdown pie chart
* Export all records to CSV

---

### 💾 4. Multi-Format Report Generation

Each diagnosis can be exported as:

* 📄 TXT Report
* 📊 CSV File
* 📑 PDF Document
* 🖼️ PNG Image
* 📸 JPG Image

Reports include:

* Timestamp
* Patient information
* Condition
* Severity
* Clinical reasons
* Recommendations

---

## 🧠 Clinical Logic Example

```python
if symptom == "Flash of Light":
    if age > 50 or eye_pressure > 21:
        condition = "Retinal Detachment with Glaucoma Risk"
        severity = "Critical"
```

The application mimics real-world ophthalmic triage logic using:

* ✔ Conditional statements (if / elif / else)
* ✔ Logical operators (and / or)
* ✔ Threshold-based classification
* ✔ Dictionary-based mapping
* ✔ Multi-factor decision branching

---

## 🛠️ Tech Stack

| Technology    | Purpose                 |
| ------------- | ----------------------- |
| 🐍 Python     | Core Programming        |
| 🎨 Streamlit  | Web Interface           |
| 📊 Pandas     | Data Handling           |
| 📈 Matplotlib | Visualizations          |
| 🖼️ PIL       | Image Report Generation |
| 📑 FPDF       | PDF Report Creation     |
| 🧮 NumPy      | Numerical Support       |

---

## 📂 Project Structure

```
Bio-Eye-Care-Navigator/
│
├── eye.py              # Main Application
├── README.md           # Project Documentation
└── requirements.txt    # Python Dependencies
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/bio-eye-care-navigator.git
cd bio-eye-care-navigator
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install streamlit pandas numpy matplotlib seaborn pillow fpdf
```

---

## ▶️ Run the Application

```bash
streamlit run eye.py
```

Then open your browser at:

```
http://localhost:8501
```

---

## 📊 Assignment Requirements Coverage

| Requirement            | Implementation                               |
| ---------------------- | -------------------------------------------- |
| Input Design           | Text input, slider, selectbox, radio buttons |
| Processing Logic       | Multi-parameter decision tree                |
| Conditional Statements | Nested if/elif logic                         |
| Operators              | Logical & comparison operators               |
| Data Structures        | Lists & Dictionaries                         |
| Modular Design         | 10+ user-defined functions                   |
| Output Design          | Styled UI + Reports + Charts                 |

---

## 📈 Analytics Capabilities

* Real-time patient tracking
* Severity metrics
* Symptom frequency analysis
* Age distribution insights
* CSV export of entire database

---

## 🔒 Disclaimer

This is a **computer-assisted clinical decision support system** developed for academic purposes.

It does NOT replace professional medical consultation.

Always consult a qualified ophthalmologist for diagnosis and treatment.

---

## 👨‍💻 Developed For

**Course:** CS-109 Computer Programming
**Domain:** Biomedical Application
**University:** NED University of Engineering & Technology
**Semester:** Spring 2026

---

## 🌟 Key Highlights

* 🔥 Clean UI with custom CSS styling
* 🧠 Realistic medical decision modeling
* 📊 Integrated analytics dashboard
* 📁 Professional report generation
* 🎯 Fully modular and scalable design

---

## 📌 Future Improvements

* Database integration (MongoDB / PostgreSQL)
* Authentication system
* Real patient record persistence
* AI-based predictive modeling
* Deployment on Streamlit Cloud / AWS

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub and share it with others!

---

# 👁️ Bio-Eye Care Navigator

### Intelligent Eye Health Evaluation System

Built with precision. Designed with logic. Powered by Python.
