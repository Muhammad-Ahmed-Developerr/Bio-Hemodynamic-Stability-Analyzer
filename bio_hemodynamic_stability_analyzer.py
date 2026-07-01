# bio_hemodynamic_stability_analyzer.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import base64
from fpdf import FPDF
import csv
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO


# Page configuration
st.set_page_config(
    page_title="Biomedical Hemodynamic Analyzer",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0;
        padding-bottom: 0;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-top: 0;
        padding-top: 0;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card-low {
        background: linear-gradient(135deg, #dc3545 0%, #ff6b6b 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(220,53,69,0.3);
        transition: transform 0.3s;
    }
    .metric-card-low:hover {
        transform: translateY(-5px);
    }
    .metric-card-high {
        background: linear-gradient(135deg, #28a745 0%, #34ce57 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(40,167,69,0.3);
        transition: transform 0.3s;
    }
    .metric-card-high:hover {
        transform: translateY(-5px);
    }
    .metric-card-normal {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(102,126,234,0.3);
        transition: transform 0.3s;
    }
    .metric-card-normal:hover {
        transform: translateY(-5px);
    }
    .critical-alert {
        background: linear-gradient(135deg, #FF4B4B 0%, #ff6b6b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.3rem;
        animation: pulse 2s infinite;
        box-shadow: 0 10px 20px rgba(255,75,75,0.3);
    }
    .normal-alert {
        background: linear-gradient(135deg, #28a745 0%, #34ce57 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.3rem;
        box-shadow: 0 10px 20px rgba(40,167,69,0.3);
    }
    .warning-alert {
        background: linear-gradient(135deg, #ffc107 0%, #ffdb58 100%);
        color: black;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.3rem;
        box-shadow: 0 10px 20px rgba(255,193,7,0.3);
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .stButton > button {
        width: 100%;
        margin-top: 1rem;
        background: linear-gradient(135deg, #FF4B4B 0%, #ff6b6b 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255,75,75,0.3);
    }
    .report-box {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        color: #00FF00;
        padding: 1.5rem;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        margin-top: 1rem;
        max-height: 500px;
        overflow-y: auto;
        border: 2px solid #FF4B4B;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .calculation-box {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1e9f5 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #FF4B4B;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .patient-info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px rgba(102,126,234,0.3);
    }
    .download-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 1.5rem;
        border: 1px solid #dee2e6;
    }
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #FF4B4B;
    }
    .reference-table {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .status-low {
        color: #dc3545 !important;
        font-weight: bold;
    }
    .status-high {
        color: #28a745 !important;
        font-weight: bold;
    }
    .status-normal {
        color: #667eea !important;
        font-weight: bold;
    }
    .delta-low {
        color: #dc3545 !important;
        font-weight: bold;
    }
    .delta-high {
        color: #28a745 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🫀 Biomedical Hemodynamic Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Patient Hemodynamic Monitoring & Risk Assessment System</p>', unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'patient_id_counter' not in st.session_state:
    st.session_state.patient_id_counter = 1
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = None

# ============================================================================
# HELPER FUNCTION FOR METRIC DISPLAY
# ============================================================================

def display_metric_with_status(label, value, unit, status, status_text=None):
    """
    Display a metric with color-coded status and appropriate arrow
    LOW → Red color with ↓ (down arrow)
    HIGH → Green color with ↑ (up arrow)
    NORMAL → Default color
    """
    if status == 'LOW':
        arrow = '↓'
        delta_color = 'red'
        css_class = 'metric-card-low'
    elif status == 'HIGH':
        arrow = '↑'
        delta_color = 'green'
        css_class = 'metric-card-high'
    else:
        arrow = '✓'
        delta_color = '#667eea'
        css_class = 'metric-card-normal'
    
    # Build the display text
    status_display = status_text if status_text else status
    
    # Use HTML for custom styling
    st.markdown(f"""
    <div class="{css_class}">
        <h3 style="margin: 0; font-size: 1.1rem;">{label}</h3>
        <h2 style="margin: 5px 0; font-size: 2rem;">{value} {unit}</h2>
        <p style="margin: 0; font-size: 1.2rem;">
            <span style="color: {'#dc3545' if status == 'LOW' else '#28a745' if status == 'HIGH' else '#667eea'}; font-weight: bold;">
                {arrow} {status_display}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CALCULATION FUNCTIONS (Modular Design)
# ============================================================================

def calculate_all_parameters(heart_rate, systolic_bp, diastolic_bp):
    """
    Calculate all hemodynamic parameters from patient vitals
    Using standard medical formulas
    """
    
    # 1. Mean Arterial Pressure (MAP)
    # Formula: DBP + 1/3(SBP - DBP)
    map_value = diastolic_bp + (systolic_bp - diastolic_bp) / 3
    
    # 2. Shock Index (SI)
    # Formula: HR / SBP
    shock_index = heart_rate / systolic_bp if systolic_bp > 0 else 0
    
    # 3. Pulse Pressure (PP)
    # Formula: SBP - DBP
    pulse_pressure = systolic_bp - diastolic_bp
    
    # 4. Rate Pressure Product (RPP)
    # Formula: HR × SBP
    rpp = heart_rate * systolic_bp
    
    return {
        'map': round(map_value, 2),
        'shock_index': round(shock_index, 2),
        'pulse_pressure': pulse_pressure,
        'rpp': rpp
    }

def classify_parameters(heart_rate, systolic_bp, diastolic_bp, calculated):
    """
    Classify each parameter as NORMAL, ABNORMAL, or CRITICAL
    Using logical conditions (if/else) as per assignment requirements
    """
    status = {}
    
    # Heart Rate Classification (Normal: 60-100 BPM)
    if heart_rate < 60:
        status['hr_status'] = 'LOW'
        status['hr_message'] = f'Bradycardia: Heart rate {heart_rate} BPM is below normal range (60-100 BPM)'
    elif 60 <= heart_rate <= 100:
        status['hr_status'] = 'NORMAL'
        status['hr_message'] = f'Normal heart rate: {heart_rate} BPM (within 60-100 BPM range)'
    else:
        status['hr_status'] = 'HIGH'
        status['hr_message'] = f'Tachycardia: Heart rate {heart_rate} BPM is above normal range (60-100 BPM)'
    
    # Blood Pressure Classification (Normal: SBP 90-140, DBP 60-90)
    if systolic_bp < 90 or diastolic_bp < 60:
        status['bp_status'] = 'LOW'
        status['bp_message'] = f'Hypotension: BP {systolic_bp}/{diastolic_bp} mmHg is below normal range'
    elif systolic_bp > 140 or diastolic_bp > 90:
        status['bp_status'] = 'HIGH'
        status['bp_message'] = f'Hypertension: BP {systolic_bp}/{diastolic_bp} mmHg is above normal range'
    else:
        status['bp_status'] = 'NORMAL'
        status['bp_message'] = f'Normal blood pressure: {systolic_bp}/{diastolic_bp} mmHg'
    
    # MAP Classification (Normal: 70-100 mmHg)
    if calculated['map'] < 70:
        status['map_status'] = 'LOW'
        status['map_message'] = f'Low MAP: {calculated["map"]} mmHg - Risk of inadequate organ perfusion'
    elif 70 <= calculated['map'] <= 100:
        status['map_status'] = 'NORMAL'
        status['map_message'] = f'Normal MAP: {calculated["map"]} mmHg - Adequate organ perfusion'
    else:
        status['map_status'] = 'HIGH'
        status['map_message'] = f'High MAP: {calculated["map"]} mmHg - Increased cardiac workload'
    
    # Shock Index Classification (Normal: 0.5-0.7)
    if calculated['shock_index'] < 0.5:
        status['si_status'] = 'LOW'
        status['si_message'] = f'Low shock index: {calculated["shock_index"]} - Hemodynamically stable'
    elif 0.5 <= calculated['shock_index'] <= 0.7:
        status['si_status'] = 'NORMAL'
        status['si_message'] = f'Normal shock index: {calculated["shock_index"]} - Within normal range'
    elif 0.7 < calculated['shock_index'] <= 1.0:
        status['si_status'] = 'ELEVATED'
        status['si_message'] = f'Elevated shock index: {calculated["shock_index"]} - Monitor closely'
    else:
        status['si_status'] = 'CRITICAL'
        status['si_message'] = f'CRITICAL: Shock index {calculated["shock_index"]} - Immediate intervention required'
    
    # Overall Patient Classification
    if (status['si_status'] == 'CRITICAL' or calculated['shock_index'] > 1.0):
        status['overall'] = 'CRITICAL'
        status['color'] = '#FF4B4B'
        status['alert'] = '⚠️ CRITICAL CONDITION - Immediate Medical Intervention Required!'
        status['priority'] = 1
    elif (status['si_status'] == 'ELEVATED' or
          status['map_status'] != 'NORMAL' or
          status['hr_status'] != 'NORMAL' or
          status['bp_status'] != 'NORMAL'):
        status['overall'] = 'ABNORMAL'
        status['color'] = '#ffc107'
        status['alert'] = '⚠️ Abnormal Parameters Detected - Medical Review Recommended'
        status['priority'] = 2
    else:
        status['overall'] = 'NORMAL'
        status['color'] = '#28a745'
        status['alert'] = '✅ Patient Stable - All Parameters Within Normal Range'
        status['priority'] = 3
    
    return status

def generate_clinical_report(patient_data):
    """
    Generate comprehensive clinical report as formatted string
    """
    report = []
    report.append("=" * 80)
    report.append("                    BIOMEDICAL HEMODYNAMIC ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"Report ID: {patient_data['patient_id']}")
    report.append(f"Patient Name: {patient_data['patient_name']}")
    report.append(f"Age: {patient_data['age']} years")
    report.append(f"Date & Time: {patient_data['timestamp']}")
    report.append("-" * 80)
    report.append("PATIENT VITAL SIGNS:")
    report.append(f"  • Heart Rate: {patient_data['heart_rate']} BPM ({patient_data['hr_status']})")
    report.append(f"  • Systolic Blood Pressure: {patient_data['systolic_bp']} mmHg")
    report.append(f"  • Diastolic Blood Pressure: {patient_data['diastolic_bp']} mmHg")
    report.append("-" * 80)
    report.append("CALCULATED HEMODYNAMIC PARAMETERS:")
    report.append(f"  • Mean Arterial Pressure (MAP): {patient_data['map']} mmHg ({patient_data['map_status']})")
    report.append(f"  • Shock Index (SI): {patient_data['shock_index']} ({patient_data['si_status']})")
    report.append(f"  • Pulse Pressure: {patient_data['pulse_pressure']} mmHg")
    report.append(f"  • Rate Pressure Product (RPP): {patient_data['rpp']}")
    report.append("-" * 80)
    report.append("CLINICAL INTERPRETATION:")
    report.append(f"  • Heart Rate: {patient_data['hr_message']}")
    report.append(f"  • Blood Pressure: {patient_data['bp_message']}")
    report.append(f"  • MAP Status: {patient_data['map_message']}")
    report.append(f"  • Shock Risk: {patient_data['si_message']}")
    report.append("-" * 80)
    report.append(f"OVERALL STATUS: {patient_data['overall']}")
    report.append(f"CLINICAL ALERT: {patient_data['alert']}")
    report.append("=" * 80)
    report.append("Generated by Biomedical Hemodynamic Analyzer")
    report.append("Advanced Patient Monitoring & Risk Assessment System")
    
    return "\n".join(report)

# ============================================================================
# FILE EXPORT FUNCTIONS
# ============================================================================

def save_report_as_txt(report_text, filename):
    """Save report as TXT file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        return filename
    except Exception as e:
        st.error(f"Error saving TXT: {e}")
        return None

def save_report_as_csv(patient_data, filename):
    """Save report as CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Parameter', 'Value', 'Status', 'Normal Range', 'Unit'])
            writer.writerow(['Patient ID', patient_data['patient_id'], '', '', ''])
            writer.writerow(['Patient Name', patient_data['patient_name'], '', '', ''])
            writer.writerow(['Timestamp', patient_data['timestamp'], '', '', ''])
            writer.writerow(['Age', patient_data['age'], '', '', 'years'])
            writer.writerow(['Heart Rate', patient_data['heart_rate'], patient_data['hr_status'], '60-100', 'BPM'])
            writer.writerow(['Systolic BP', patient_data['systolic_bp'], '', '90-140', 'mmHg'])
            writer.writerow(['Diastolic BP', patient_data['diastolic_bp'], '', '60-90', 'mmHg'])
            writer.writerow(['MAP', patient_data['map'], patient_data['map_status'], '70-100', 'mmHg'])
            writer.writerow(['Shock Index', patient_data['shock_index'], patient_data['si_status'], '0.5-0.7', ''])
            writer.writerow(['Pulse Pressure', patient_data['pulse_pressure'], '', '30-50', 'mmHg'])
            writer.writerow(['RPP', patient_data['rpp'], '', '<10000', ''])
            writer.writerow(['Overall Status', patient_data['overall'], '', '', ''])
        return filename
    except Exception as e:
        st.error(f"Error saving CSV: {e}")
        return None

def save_report_as_pdf(report_text, filename):
    """Save report as PDF file"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        for line in report_text.split('\n'):
            # Handle encoding issues
            line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(200, 5, txt=line, ln=True, align='L')
        
        pdf.output(filename)
        return filename
    except Exception as e:
        st.error(f"Error saving PDF: {e}")
        return None

def create_chart_image(patient_data, format_type='png'):
    """Create chart image using matplotlib (no kaleido required)"""
    try:
        # Create figure with matplotlib
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Bar chart for vitals
        categories = ['Heart Rate\n(BPM)', 'Systolic BP\n(mmHg)', 'Diastolic BP\n(mmHg)', 'MAP\n(mmHg)']
        values = [patient_data['heart_rate'], patient_data['systolic_bp'], 
                 patient_data['diastolic_bp'], patient_data['map']]
        
        # Color based on status
        colors = []
        if patient_data['hr_status'] == 'NORMAL':
            colors.append('#667eea')
        elif patient_data['hr_status'] == 'LOW':
            colors.append('#dc3545')
        else:
            colors.append('#28a745')
            
        colors.append('#6c757d')  # SBP
        colors.append('#6c757d')  # DBP
        
        if patient_data['map_status'] == 'NORMAL':
            colors.append('#667eea')
        elif patient_data['map_status'] == 'LOW':
            colors.append('#dc3545')
        else:
            colors.append('#28a745')
        
        bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
        ax1.set_title('Patient Vital Signs', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('Value', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar, v in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(v), ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Add reference lines
        ax1.axhline(y=60, color='gray', linestyle='--', alpha=0.5, label='Normal Lower Limit')
        ax1.axhline(y=100, color='gray', linestyle='--', alpha=0.5, label='Normal Upper Limit')
        ax1.legend(fontsize=9)
        
        # Gauge for overall status
        status_colors = {'NORMAL': '#667eea', 'ABNORMAL': '#ffc107', 'CRITICAL': '#dc3545'}
        status = patient_data['overall']
        color = status_colors.get(status, '#808080')
        
        # Create a donut chart for status
        wedges, texts = ax2.pie([1], colors=[color], radius=0.8, 
                                wedgeprops=dict(width=0.3, edgecolor='white'))
        ax2.text(0, 0, status, ha='center', va='center', fontsize=20, fontweight='bold')
        ax2.set_title('Overall Patient Status', fontsize=16, fontweight='bold', pad=20)
        
        # Add patient info
        plt.suptitle(f"Hemodynamic Analysis Report\nPatient: {patient_data['patient_name']} (ID: {patient_data['patient_id']})", 
                    fontsize=18, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        # Save to bytes
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format=format_type, dpi=150, bbox_inches='tight', 
                   facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        
        img_bytes.seek(0)
        return img_bytes
    except Exception as e:
        st.error(f"Error creating chart: {e}")
        return None

def save_chart_as_image(patient_data, filename, format_type='png'):
    """Save chart as image file"""
    try:
        img_bytes = create_chart_image(patient_data, format_type)
        if img_bytes:
            with open(filename, 'wb') as f:
                f.write(img_bytes.getvalue())
            return filename
    except Exception as e:
        st.error(f"Error saving {format_type.upper()}: {e}")
        return None

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_vitals_chart(patient_data):
    """Create interactive Plotly chart for display"""
    
    categories = ['Heart Rate (BPM)', 'Systolic BP (mmHg)', 'Diastolic BP (mmHg)', 'MAP (mmHg)']
    values = [patient_data['heart_rate'], patient_data['systolic_bp'], 
             patient_data['diastolic_bp'], patient_data['map']]
    
    # Color based on status
    colors = []
    for i, cat in enumerate(categories):
        if cat == 'Heart Rate (BPM)':
            if patient_data['hr_status'] == 'NORMAL':
                colors.append('#667eea')
            elif patient_data['hr_status'] == 'LOW':
                colors.append('#dc3545')
            else:
                colors.append('#28a745')
        elif cat == 'MAP (mmHg)':
            if patient_data['map_status'] == 'NORMAL':
                colors.append('#667eea')
            elif patient_data['map_status'] == 'LOW':
                colors.append('#dc3545')
            else:
                colors.append('#28a745')
        else:
            colors.append('#6c757d')
    
    fig = go.Figure(data=[
        go.Bar(name='Values', x=categories, y=values, marker_color=colors,
               text=values, textposition='auto',
               textfont=dict(size=14, color='white', family='Arial Black'))
    ])
    
    fig.update_layout(
        title={
            'text': 'Patient Vitals Visualization',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Arial Black')
        },
        xaxis_title='Parameter',
        yaxis_title='Value',
        template='plotly_white',
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add horizontal lines for normal ranges
    fig.add_hline(y=60, line_dash="dash", line_color="gray", 
                  annotation_text="Normal Lower Limit", annotation_position="bottom right")
    fig.add_hline(y=100, line_dash="dash", line_color="gray",
                  annotation_text="Normal Upper Limit", annotation_position="top right")
    
    return fig

# ============================================================================
# MAIN UI - TABS
# ============================================================================

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Patient Input", "📊 Analysis Results", "📈 Patient History", "ℹ️ About"])

# ============================================================================
# TAB 1: PATIENT INPUT
# ============================================================================

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 👤 Patient Information")
        st.markdown("Enter patient details for hemodynamic analysis")
        
        # Patient name input
        patient_name = st.text_input("**Patient Full Name**", value="Ahmed", 
                                     help="Enter patient's full name")
        
        # Patient age
        patient_age = st.number_input("**Age (years)**", min_value=0, max_value=120, value=19, step=1,
                                      help="Enter patient's age in years")
        
        # Vital signs inputs
        heart_rate = st.number_input("**Heart Rate (BPM)**", min_value=0, max_value=300, value=55, step=1,
                                     help="Normal range: 60-100 BPM")
        
        systolic_bp = st.number_input("**Systolic BP (mmHg)**", min_value=0, max_value=300, value=160, step=1,
                                      help="Normal range: 90-140 mmHg")
        
        diastolic_bp = st.number_input("**Diastolic BP (mmHg)**", min_value=0, max_value=200, value=92, step=1,
                                       help="Normal range: 60-90 mmHg")
        
        # Analyze button
        if st.button("🔬 Analyze Patient Data", use_container_width=True):
            with st.spinner("Calculating hemodynamic parameters..."):
                # Calculate parameters
                calculated = calculate_all_parameters(heart_rate, systolic_bp, diastolic_bp)
                status = classify_parameters(heart_rate, systolic_bp, diastolic_bp, calculated)
                
                # Create patient record
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                patient_id = f"PAT-{st.session_state.patient_id_counter:04d}"
                
                # Store in session state
                st.session_state.current_patient = {
                    'patient_id': patient_id,
                    'patient_name': patient_name,
                    'timestamp': timestamp,
                    'age': patient_age,
                    'heart_rate': heart_rate,
                    'systolic_bp': systolic_bp,
                    'diastolic_bp': diastolic_bp,
                    'map': calculated['map'],
                    'shock_index': calculated['shock_index'],
                    'pulse_pressure': calculated['pulse_pressure'],
                    'rpp': calculated['rpp'],
                    'hr_status': status['hr_status'],
                    'bp_status': status['bp_status'],
                    'map_status': status['map_status'],
                    'si_status': status['si_status'],
                    'hr_message': status['hr_message'],
                    'bp_message': status['bp_message'],
                    'map_message': status['map_message'],
                    'si_message': status['si_message'],
                    'overall': status['overall'],
                    'alert': status['alert'],
                    'color': status['color']
                }
                
                st.session_state.patient_id_counter += 1
                st.session_state.history.append(st.session_state.current_patient.copy())
                st.success("✅ Analysis Complete! Go to Analysis Results tab.")
    
    with col2:
        st.markdown("### 📋 Reference Ranges")
        
        # Reference ranges table
        ref_data = pd.DataFrame({
            'Parameter': ['Heart Rate', 'Systolic BP', 'Diastolic BP', 'MAP', 'Shock Index', 'Pulse Pressure', 'RPP'],
            'Normal Range': ['60-100 BPM', '90-140 mmHg', '60-90 mmHg', '70-100 mmHg', '0.5-0.7', '30-50 mmHg', '<10,000'],
            'Formula': ['Input', 'Input', 'Input', 'DBP + 1/3(SBP-DBP)', 'HR/SBP', 'SBP-DBP', 'HR × SBP'],
            'Clinical Significance': ['Cardiac rate', 'Vascular pressure', 'Vascular pressure', 'Organ perfusion', 'Shock risk', 'Cardiac output', 'Oxygen demand']
        })
        
        st.dataframe(ref_data, use_container_width=True, hide_index=True)
        
        # Live calculation preview
        st.markdown("### 🧪 Live Calculation Preview")
        
        preview_map = diastolic_bp + (systolic_bp - diastolic_bp) / 3
        preview_si = heart_rate / systolic_bp if systolic_bp > 0 else 0
        preview_pp = systolic_bp - diastolic_bp
        preview_rpp = heart_rate * systolic_bp
        
        st.markdown(f"""
        <div class="calculation-box">
            <h4>Based on current inputs:</h4>
            <p><b>MAP</b> = {diastolic_bp} + ({systolic_bp} - {diastolic_bp})/3 = <b>{preview_map:.2f} mmHg</b></p>
            <p><b>Shock Index</b> = {heart_rate} / {systolic_bp} = <b>{preview_si:.2f}</b></p>
            <p><b>Pulse Pressure</b> = {systolic_bp} - {diastolic_bp} = <b>{preview_pp} mmHg</b></p>
            <p><b>RPP</b> = {heart_rate} × {systolic_bp} = <b>{preview_rpp}</b></p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: ANALYSIS RESULTS
# ============================================================================

with tab2:
    if st.session_state.current_patient:
        p = st.session_state.current_patient
        
        # Alert based on overall status
        if p['overall'] == 'CRITICAL':
            st.markdown(f'<div class="critical-alert">{p["alert"]}</div>', unsafe_allow_html=True)
        elif p['overall'] == 'ABNORMAL':
            st.markdown(f'<div class="warning-alert">{p["alert"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="normal-alert">{p["alert"]}</div>', unsafe_allow_html=True)
        
        # Patient info card
        st.markdown(f"""
        <div class="patient-info-card">
            <h2>Patient: {p['patient_name']}</h2>
            <p style='font-size: 1.1rem;'>ID: {p['patient_id']} | Age: {p['age']} years | Time: {p['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Input vitals with color-coded status
        st.markdown("### 📊 Input Vital Signs")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            display_metric_with_status("Heart Rate", p['heart_rate'], "BPM", p['hr_status'])
        
        with col2:
            # For BP, we show both values but status is based on combined classification
            display_metric_with_status("Systolic BP", p['systolic_bp'], "mmHg", p['bp_status'])
        
        with col3:
            display_metric_with_status("Diastolic BP", p['diastolic_bp'], "mmHg", p['bp_status'])
        
        # Calculated parameters with color-coded status
        st.markdown("### 🧮 Calculated Hemodynamic Parameters")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_with_status("Mean Arterial Pressure", p['map'], "mmHg", p['map_status'])
            st.caption("DBP + 1/3(SBP-DBP)")
        
        with col2:
            display_metric_with_status("Shock Index", p['shock_index'], "", p['si_status'])
            st.caption("HR / SBP")
        
        with col3:
            # Pulse Pressure has no specific status, show normal
            display_metric_with_status("Pulse Pressure", p['pulse_pressure'], "mmHg", "NORMAL", "—")
            st.caption("SBP - DBP")
        
        with col4:
            # RPP has no specific status, show normal
            display_metric_with_status("Rate Pressure Product", p['rpp'], "", "NORMAL", "—")
            st.caption("HR × SBP")
        
        # Visualization
        st.markdown("### 📈 Vitals Visualization")
        fig = create_vitals_chart(p)
        st.plotly_chart(fig, use_container_width=True)
        
        # Clinical interpretation
        st.markdown("### 🔬 Clinical Interpretation")
        
        interpretation_df = pd.DataFrame({
            'Parameter': ['Heart Rate', 'Blood Pressure', 'MAP', 'Shock Index'],
            'Value': [f"{p['heart_rate']} BPM", f"{p['systolic_bp']}/{p['diastolic_bp']} mmHg", 
                     f"{p['map']} mmHg", f"{p['shock_index']}"],
            'Status': [p['hr_status'], p['bp_status'], p['map_status'], p['si_status']],
            'Clinical Interpretation': [p['hr_message'], p['bp_message'], p['map_message'], p['si_message']]
        })
        
        st.dataframe(interpretation_df, use_container_width=True, hide_index=True)
        
        # Clinical Report
        st.markdown("### 📄 Clinical Report")
        report_text = generate_clinical_report(p)
        
        st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
        
        # Download section
        st.markdown("### 💾 Download Reports")
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        
        # Create reports directory
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns(2)
        
        with col1:
            # TXT download
            txt_filename = f"reports/{p['patient_id']}_report_{timestamp_file}.txt"
            if save_report_as_txt(report_text, txt_filename):
                with open(txt_filename, 'rb') as f:
                    st.download_button(
                        label="📄 Download TXT Report",
                        data=f,
                        file_name=f"{p['patient_id']}_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
        
        with col2:
            # CSV download
            csv_filename = f"reports/{p['patient_id']}_report_{timestamp_file}.csv"
            if save_report_as_csv(p, csv_filename):
                with open(csv_filename, 'rb') as f:
                    st.download_button(
                        label="📊 Download CSV Report",
                        data=f,
                        file_name=f"{p['patient_id']}_report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        
        with col3:
            # PDF download
            pdf_filename = f"reports/{p['patient_id']}_report_{timestamp_file}.pdf"
            if save_report_as_pdf(report_text, pdf_filename):
                with open(pdf_filename, 'rb') as f:
                    st.download_button(
                        label="📑 Download PDF Report",
                        data=f,
                        file_name=f"{p['patient_id']}_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col4:
            # PNG download
            png_filename = f"reports/{p['patient_id']}_chart_{timestamp_file}.png"
            if save_chart_as_image(p, png_filename, 'png'):
                with open(png_filename, 'rb') as f:
                    st.download_button(
                        label="🖼️ Download PNG Chart",
                        data=f,
                        file_name=f"{p['patient_id']}_chart.png",
                        mime="image/png",
                        use_container_width=True
                    )
        
        with col5:
            # JPG download
            jpg_filename = f"reports/{p['patient_id']}_chart_{timestamp_file}.jpg"
            if save_chart_as_image(p, jpg_filename, 'jpg'):
                with open(jpg_filename, 'rb') as f:
                    st.download_button(
                        label="🖼️ Download JPG Chart",
                        data=f,
                        file_name=f"{p['patient_id']}_chart.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # New analysis button
        if st.button("🔄 New Patient Analysis", use_container_width=True):
            st.session_state.current_patient = None
            st.rerun()
    
    else:
        st.info("👈 Please enter patient details in the 'Patient Input' tab and click 'Analyze Patient Data'")
        
        # Sample preview
        st.markdown("### Sample Preview")
        sample_fig = create_vitals_chart({
            'heart_rate': 72,
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'map': 93.33,
            'hr_status': 'NORMAL',
            'map_status': 'NORMAL',
            'patient_name': 'Sample Patient',
            'patient_id': 'PAT-0000'
        })
        st.plotly_chart(sample_fig, use_container_width=True)

# ============================================================================
# TAB 3: PATIENT HISTORY
# ============================================================================

with tab3:
    st.markdown("### 📈 Patient History & Trends")
    
    if len(st.session_state.history) > 0:
        # Create DataFrame from history
        history_df = pd.DataFrame(st.session_state.history)
        
        # Select columns for display
        display_cols = ['timestamp', 'patient_id', 'patient_name', 'age', 'heart_rate', 
                       'systolic_bp', 'diastolic_bp', 'map', 'shock_index', 'overall']
        
        # Rename for better display
        display_df = history_df[display_cols].copy()
        display_df.columns = ['Date/Time', 'Patient ID', 'Name', 'Age', 'HR', 'SBP', 'DBP', 'MAP', 'SI', 'Status']
        
        # Display history table
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown("### 📊 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_hr = np.mean([p['heart_rate'] for p in st.session_state.history])
            st.metric("Average Heart Rate", f"{avg_hr:.1f} BPM")
        
        with col2:
            avg_map = np.mean([p['map'] for p in st.session_state.history])
            st.metric("Average MAP", f"{avg_map:.1f} mmHg")
        
        with col3:
            avg_si = np.mean([p['shock_index'] for p in st.session_state.history])
            st.metric("Average Shock Index", f"{avg_si:.2f}")
        
        with col4:
            critical_count = sum(1 for p in st.session_state.history if p['overall'] == 'CRITICAL')
            st.metric("Critical Cases", critical_count)
        
        # Export history button
        if st.button("📥 Export History to CSV", use_container_width=True):
            history_filename = f"reports/patient_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            history_df.to_csv(history_filename, index=False)
            
            with open(history_filename, 'rb') as f:
                st.download_button(
                    label="Download History CSV",
                    data=f,
                    file_name=os.path.basename(history_filename),
                    mime="text/csv"
                )
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    
    else:
        st.info("No patient history available. Analyze some patients first!")

# ============================================================================
# TAB 4: ABOUT
# ============================================================================

with tab4:
    st.markdown("### ℹ️ About Biomedical Hemodynamic Analyzer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h2>🏥 Biomedical Hemodynamic Analyzer</h2>
            <h3>Advanced Patient Monitoring & Risk Assessment System</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>📋 System Overview</h3>
            <p>This application implements a <b>Biomedical Hemodynamic Analyzer</b> that processes patient vital signs 
            (Heart Rate, Systolic BP, Diastolic BP) to calculate critical hemodynamic parameters and provides 
            clinical decision support through multi-parameter classification algorithms.</p>
            <p><b>Clinical Significance:</b> Hemodynamic monitoring is crucial in critical care, emergency medicine, 
            and perioperative settings. Early detection of hemodynamic instability can prevent shock, organ failure, 
            and death. This system demonstrates how computational analysis can assist in real-time clinical decision-making 
            by classifying patients into appropriate care pathways based on calculated parameters.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🧠 System Logic & Design</h3>
            <p><b>Core Logic:</b> The system uses a multi-parameter decision algorithm that:</p>
            <ol>
                <li><b>Calculates derived parameters</b> using standard medical formulas:
                    <ul>
                        <li>MAP = DBP + (SBP - DBP)/3 (Arithmetic operators: +, -, /)</li>
                        <li>Shock Index = HR / SBP (Arithmetic operator: /)</li>
                        <li>Pulse Pressure = SBP - DBP (Arithmetic operator: -)</li>
                        <li>RPP = HR × SBP (Arithmetic operator: ×)</li>
                    </ul>
                </li>
                <li><b>Applies threshold-based classification</b> using conditional statements:
                    <ul>
                        <li>If HR < 60 → BRADYCARDIA (LOW) → <span style="color:#dc3545;">↓ Red</span></li>
                        <li>If HR between 60-100 → NORMAL → <span style="color:#667eea;">✓ Blue</span></li>
                        <li>If HR > 100 → TACHYCARDIA (HIGH) → <span style="color:#28a745;">↑ Green</span></li>
                        <li>Similar logic for BP, MAP, and Shock Index</li>
                    </ul>
                </li>
                <li><b>Combines parameters</b> using logical operators (and/or) for overall classification:
                    <ul>
                        <li>If Shock Index > 1.0 → CRITICAL (emergency)</li>
                        <li>If any parameter abnormal → ABNORMAL (monitor)</li>
                        <li>If all parameters normal → NORMAL (stable)</li>
                    </ul>
                </li>
            </ol>
            <p><b>Status Indicators:</b></p>
            <ul>
                <li><span style="color:#dc3545; font-weight:bold;">↓ LOW</span> → Red background with down arrow</li>
                <li><span style="color:#28a745; font-weight:bold;">↑ HIGH</span> → Green background with up arrow</li>
                <li><span style="color:#667eea; font-weight:bold;">✓ NORMAL</span> → Blue background with checkmark</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🏆 Key Features</h3>
            <ul>
                <li>✓ 4 derived hemodynamic parameters calculated</li>
                <li>✓ 3-level severity classification</li>
                <li>✓ 5 export formats (TXT, CSV, PDF, PNG, JPG)</li>
                <li>✓ Interactive Plotly visualizations</li>
                <li>✓ Patient history with analytics</li>
                <li>✓ Real-time calculation preview</li>
                <li>✓ Professional clinical reports</li>
                <li>✓ Color-coded status indicators</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>👨‍⚕️ Clinical Parameters</h3>
            <ul>
                <li><b>MAP:</b> Organ perfusion pressure</li>
                <li><b>Shock Index:</b> Early shock detection</li>
                <li><b>Pulse Pressure:</b> Cardiac output indicator</li>
                <li><b>RPP:</b> Myocardial oxygen demand</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Technology Stack</h3>
            <ul>
                <li>🐍 Python</li>
                <li>🎨 Streamlit</li>
                <li>📊 Pandas</li>
                <li>📈 Matplotlib</li>
                <li>🧮 NumPy</li>
                <li>📑 FPDF</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    Biomedical Hemodynamic Analyzer | Advanced Patient Monitoring System
</div>
""", unsafe_allow_html=True)