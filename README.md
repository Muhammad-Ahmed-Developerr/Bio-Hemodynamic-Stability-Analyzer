# ❤️ Bio Hemodynamic Stability Analyzer

> 🏥 Intelligent Cardiovascular Monitoring & Risk Classification System

🔗 **Live App:** [https://bio-hemodynamic-stability-analyzer.streamlit.app/](https://bio-hemodynamic-stability-analyzer.streamlit.app/)

---

## 🚀 Overview

**Bio Hemodynamic Stability Analyzer** is a Streamlit-based biomedical application designed to evaluate cardiovascular stability using real-time clinical parameters.

The system analyzes:

* 👤 Patient Age
* ❤️ Heart Rate (BPM)
* 🩸 Systolic Blood Pressure
* 🩸 Diastolic Blood Pressure
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
* MAP auto-calculation
* Severity-based risk engine

---

### 📊 2. Real-Time Calculations

Mean Arterial Pressure is calculated using:

```python
MAP = DBP + (SBP - DBP) / 3

Shock Index = HR / SBP

Pulse Pressure = SBP - DBP

RPP = HR × SBP