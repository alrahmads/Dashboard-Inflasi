import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import numpy as np
from datetime import datetime
from io import BytesIO

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Dashboard Inflasi Indonesia",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    /* Remove default container padding */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
    }
    
    /* Header Styling */
    .dashboard-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 2rem;
        margin: 0;
        border-bottom: 4px solid #e74c3c;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .dashboard-header h1 {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    .dashboard-subheader {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem 2rem;
        border-bottom: 2px solid #bdc3c7;
        font-size: 1rem;
        color: #2c3e50;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Filter Section */
    .filter-section {
        background: transparent !important;
        padding: 1.5rem;
        border: none !important;
        box-shadow: none !important;
        margin: 0;
    }
    
    /* Quick Stats Grid */
    .stats-grid {
        background: transparent;
        padding: 0;
        margin-top: 0;
        box-shadow: none;
        border-radius: 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e0e6ed;
        border-radius: 10px;
        padding: 1.5rem 1rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        border-color: #2a5298;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e3c72;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-period {
        font-size: 0.8rem;
        color: #95a5a6;
        margin: 0.2rem 0 0 0;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 0.6rem 1rem;
        margin: 0.4rem 0 0.05rem 0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .section-header h3 {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Content Sections */
    .content-section {
        padding: 0.8rem 1.1rem;
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        margin: 0;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #ecf0f1;
        padding: 0;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ecf0f1;
        border-radius: 0;
        color: #7f8c8d;
        font-weight: 500;
        padding: 1rem 1.5rem;
        border: none;
        margin: 0;
        border-bottom: 3px solid transparent;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1e3c72 !important;
        border-bottom: 3px solid #e74c3c !important;
    }
    
    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1e7f4 100%);
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 4px solid #1e3c72;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .insight-box h4 {
        color: #2c3e50;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .insight-box p {
        color: #34495e;
        margin: 0;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        height: 100%;
        border: 2px solid #e0e6ed;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    .kpi-card h3 {
        color: #7f8c8d;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-card h2 {
        color: #1e3c72;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .kpi-card p {
        color: #95a5a6;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1e3c72 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #7f8c8d !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 2px solid #e0e6ed;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 6px !important;
        border: 2px solid #e0e6ed !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #1e3c72 !important;
        box-shadow: 0 0 0 2px rgba(30, 60, 114, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD DATA ====================
@st.cache_data
def load_data():
    with open('Data_inflasi.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%b')
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    return df

# Load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠ File 'Data_inflasi.json' tidak ditemukan! Pastikan file berada di direktori yang sama.")
    st.stop()

# ==================== HEADER SECTION ====================
st.markdown("""
<div class="dashboard-header">
    <h1>DASHBOARD INFLASI INDONESIA</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-subheader">
    <strong>Visualisasi Interaktif Data Makroekonomi Indonesia 2010-2024</strong>
</div>
""", unsafe_allow_html=True)

# ==================== FILTER SECTION (Moved to Sidebar) ====================
with st.sidebar:
    st.markdown("### Filter Data Periode")
    st.markdown("---")

    # Pilih Tahun & Bulan
    start_year = st.selectbox(
        "Tahun Mulai",
        options=sorted(df['year'].unique()),
        index=0,
        key="start_year"
    )

    end_year = st.selectbox(
        "Tahun Akhir", 
        options=sorted(df['year'].unique()),
        index=len(df['year'].unique()) - 1,
        key="end_year"
    )

    start_month = st.selectbox(
        "Bulan Mulai",
        options=list(range(1, 13)),
        format_func=lambda x: datetime(2020, x, 1).strftime('%B'),
        index=0,
        key="start_month"
    )

    end_month = st.selectbox(
        "Bulan Akhir",
        options=list(range(1, 13)),
        format_func=lambda x: datetime(2020, x, 1).strftime('%B'),
        index=11,
        key="end_month"
    )

    st.markdown("---")

    # Quick Info
    st.markdown("### Informasi Data")
    st.info("""
    Sumber Data:
    - Bank Indonesia
    - Badan Pusat Statistik
    
    Periode Data: 2010-2024
    Update Terakhir: """ + df['date'].max().strftime('%d %B %Y'))

# Filter data berdasarkan tahun dan bulan
def filter_data_by_date_range(df, start_year, start_month, end_year, end_month):
    # Create date objects for start and end
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    
    # Filter the dataframe
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    return df[mask]

df_filtered = filter_data_by_date_range(df, start_year, start_month, end_year, end_month)

# Display filter info
st.markdown(f"""
<div class="insight-box">
    <h4>Periode yang Ditampilkan</h4>
    <p>Data ditampilkan dari <b>{datetime(start_year, start_month, 1).strftime('%B %Y')}</b> hingga <b>{datetime(end_year, end_month, 1).strftime('%B %Y')}</b> 
    ({len(df_filtered)} bulan data)</p>
</div>
""", unsafe_allow_html=True)

# ==================== QUICK STATS GRID ====================
st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

# Calculate latest values for quick stats
if not df_filtered.empty:
    latest_data = df_filtered.iloc[-1]

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">INFLASI TERKINI</div>
            <div class="stat-value">{latest_data['inflasi']:.2f}%</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">BI RATE</div>
            <div class="stat-value">{latest_data['bi_rate']:.2f}%</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">KURS USD/IDR</div>
            <div class="stat-value">{latest_data['kurs']:,.0f}</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">UANG BEREDAR</div>
            <div class="stat-value">{latest_data['uang_beredar']/1000:.1f}T</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">INVESTASI</div>
            <div class="stat-value">{latest_data['investasi']/1000:.1f}T</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">EKSPOR</div>
            <div class="stat-value">{latest_data['ekspor']/1000:.1f}B USD</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">IMPOR</div>
            <div class="stat-value">{latest_data['impor']/1000:.1f}B USD</div>
            <div class="stat-period">{latest_data['periode']}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Silakan pilih periode lain.")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN CONTENT TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "TREN UTAMA", 
    "ANALISIS KOMPARATIF", 
    "MODEL & PREDIKSI", 
    "DATA & UNDUH"
])

# ==================== TAB 1: TREN UTAMA ====================
with tab1:
    if not df_filtered.empty:
        col_overview1, col_overview2 = st.columns([2, 1])
        
        with col_overview1:
            st.markdown('<div class="section-header"><h3>TREN INFLASI INDONESIA</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            # Main Inflation Trend
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_filtered['date'],
                y=df_filtered['inflasi'],
                mode='lines',
                name='Inflasi',
                line=dict(color='#1e3c72', width=3.5),
                fill='tozeroy',
                fillcolor='rgba(30, 60, 114, 0.15)',
                hovertemplate='<b>%{x|%B %Y}</b><br>Inflasi: %{y:.2f}%<extra></extra>'
            ))
            
            # Add target range
            fig1.add_hrect(y0=2.5, y1=3.0, 
                          fillcolor="rgba(231, 76, 60, 0.1)", 
                          line_width=0,
                          annotation_text="Target BI: 2.5-3.0%", 
                          annotation_position="top left")
            
            fig1.update_layout(
                title={'text': "Tren Inflasi", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                xaxis_title="Periode",
                yaxis_title="Inflasi (%)",
                template="plotly_white",
                height=400,
                hovermode='x unified',
                showlegend=False,
                margin=dict(t=40, l=60, r=40, b=60),
                font=dict(size=12),
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(255,255,255,0.9)',
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_overview2:
            st.markdown('<div class="section-header"><h3>INDIKATOR KINERJA</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            # KPI Metrics
            avg_inflation = df_filtered['inflasi'].mean()
            max_inflation = df_filtered['inflasi'].max()
            min_inflation = df_filtered['inflasi'].min()
            volatility = df_filtered['inflasi'].std()
            
            col_kpi1, col_kpi2 = st.columns(2)
            
            with col_kpi1:
                st.markdown(f"""
                <div class="kpi-card">
                    <h3>Rata-rata Inflasi</h3>
                    <h2>{avg_inflation:.2f}%</h2>
                    <p>Periode {start_year}-{end_year}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="kpi-card" style="margin-top: 15px;">
                    <h3>Inflasi Terendah</h3>
                    <h2>{min_inflation:.2f}%</h2>
                    <p>{df_filtered.loc[df_filtered['inflasi'].idxmin(), 'periode']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_kpi2:
                st.markdown(f"""
                <div class="kpi-card">
                    <h3>Inflasi Tertinggi</h3>
                    <h2>{max_inflation:.2f}%</h2>
                    <p>{df_filtered.loc[df_filtered['inflasi'].idxmax(), 'periode']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="kpi-card" style="margin-top: 15px;">
                    <h3>Volatilitas</h3>
                    <h2>{volatility:.2f}%</h2>
                    <p>Standar Deviasi</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Insights and Additional Charts
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.markdown('<div class="section-header"><h3>ANALISIS TREN</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            trend = "naik" if df_filtered.iloc[-1]['inflasi'] > df_filtered.iloc[0]['inflasi'] else "turun"
            pct_change = ((df_filtered.iloc[-1]['inflasi'] - df_filtered.iloc[0]['inflasi']) / df_filtered.iloc[0]['inflasi'] * 100)
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Tren Perkembangan</h4>
                <p>Inflasi mengalami tren <b>{trend}</b> sebesar <b>{abs(pct_change):.1f}%</b> selama periode yang dipilih.</p>
            </div>
            """, unsafe_allow_html=True)
            
            corr_bi = df_filtered[['inflasi', 'bi_rate']].corr().iloc[0, 1]
            corr_status = "positif kuat" if corr_bi > 0.5 else "positif lemah" if corr_bi > 0 else "negatif"
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Korelasi dengan BI Rate</h4>
                <p>Korelasi <b>{corr_status}</b> ({corr_bi:.2f}) dengan BI Rate menunjukkan hubungan kebijakan moneter.</p>
            </div>
            """, unsafe_allow_html=True)
            
            current_inflation = df_filtered.iloc[-1]['inflasi']
            target_status = "di atas" if current_inflation > 3.0 else "di bawah" if current_inflation < 2.5 else "dalam"
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Pencapaian Target</h4>
                <p>Inflasi terkini <b>{current_inflation:.2f}%</b> berada <b>{target_status}</b> kisaran target BI 2.5-3.0%.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_insight2:
            st.markdown('<div class="section-header"><h3>POLA MUSIMAN</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            # Monthly Distribution
            monthly_avg = df_filtered.groupby('month_name')['inflasi'].mean().reindex(
                ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            )
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=monthly_avg.index,
                y=monthly_avg.values,
                marker_color='#1e3c72',
                hovertemplate='<b>Bulan:</b> %{x}<br><b>Rata-rata Inflasi:</b> %{y:.2f}%<extra></extra>'
            ))
            
            fig2.update_layout(
                title={'text':"Rata-rata Inflasi per Bulan (Pola Musiman)", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                xaxis_title="Bulan",
                yaxis_title="Rata-rata Inflasi (%)",
                template="plotly_white",
                height=300,
                showlegend=False,
                margin=dict(t=40, l=60, r=40, b=60),
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(255,255,255,0.9)',
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Seasonal insight
            if not monthly_avg.empty:
                highest_month = monthly_avg.idxmax()
                lowest_month = monthly_avg.idxmin()
                
                st.markdown(f"""
                <div class="insight-box">
                    <h4>Pola Musiman</h4>
                    <p>Inflasi cenderung tertinggi di bulan <b>{highest_month}</b> dan terendah di bulan <b>{lowest_month}</b>.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data untuk ditampilkan pada periode yang dipilih.")

# ==================== TAB 2: ANALISIS KOMPARATIF ====================
with tab2:
    if not df_filtered.empty:
        # Filter section for comparative analysis
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("### Filter Analisis Komparatif")
        
        # Variable selection for X-axis
        x_var = st.selectbox(
            "Pilih Variabel untuk Analisis Komparatif:",
            options=['bi_rate', 'kurs', 'uang_beredar', 'investasi', 'ekspor', 'impor'],
            format_func=lambda x: {
                'bi_rate': 'BI Rate (%)',
                'kurs': 'Kurs USD/IDR',
                'uang_beredar': 'Uang Beredar (Miliar)',
                'investasi': 'Investasi (Miliar)',
                'ekspor': 'Ekspor (Miliar USD)',
                'impor': 'Impor (Miliar USD)'
            }[x],
            key="x_var_comparative"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Line Chart - Comparative Analysis
        st.markdown('<div class="section-header"><h3>TREN BERBANDING: INFLASI vs ' + x_var.replace('_', ' ').upper() + '</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig3.add_trace(
            go.Scatter(
                x=df_filtered['date'],
                y=df_filtered['inflasi'],
                name="Inflasi",
                line=dict(color='#1e3c72', width=3.5),
            ),
            secondary_y=False
        )
        
        fig3.add_trace(
            go.Scatter(
                x=df_filtered['date'],
                y=df_filtered[x_var],
                name=x_var.replace('_', ' ').title(),
                line=dict(color='#e74c3c', width=2.5),
            ),
            secondary_y=True
        )
        
        fig3.update_xaxes(title_text="Periode")
        fig3.update_yaxes(title_text="Inflasi (%)", secondary_y=False)
        fig3.update_yaxes(title_text=x_var.replace('_', ' ').title(), secondary_y=True)
        
        fig3.update_layout(
            title={
                'text': f"Tren Inflasi vs {x_var.replace('_', ' ').title()}",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            template="plotly_white",
            height=450,
            hovermode='x unified',
            margin=dict(t=40, l=60, r=60, b=60),
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Scatter Plot - Correlation Analysis
        col_scatter1, col_scatter2 = st.columns([2, 1])
        
        with col_scatter1:
            st.markdown('<div class="section-header"><h3>ANALISIS HUBUNGAN: SCATTER PLOT</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            fig4 = px.scatter(
                df_filtered,
                x=x_var,
                y='inflasi',
                trendline='ols',
                color_discrete_sequence=['#1e3c72'],
                title=f"Hubungan antara Inflasi dan {x_var.replace('_', ' ').title()}",
                labels={
                    x_var: x_var.replace('_', ' ').title(),
                    'inflasi': 'Inflasi (%)'
                }
            )
            
            fig4.update_layout(
                title_x=0.35,
                template="plotly_white",
                height=400,
                margin=dict(t=40, l=60, r=40, b=60),
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(255,255,255,0.9)',
            )
            
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_scatter2:
            st.markdown('<div class="section-header"><h3>HUBUNGAN KORELASI</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            # Correlation analysis
            correlation = df_filtered[['inflasi', x_var]].corr().iloc[0,1]
            
            st.markdown(f"""
            <div style="
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                margin-bottom: 15px;
            ">
                <h4 style="margin-bottom: 8px; color: #1e3c72;">Koefisien Korelasi</h4>
                <h2 style="margin: 5px 0; color: #2c3e50;">{correlation:.3f}</h2>
                <p style="margin: 0; font-weight: bold; color: {'#27ae60' if correlation > 0 else '#c0392b'};">
                    {"Hubungan Positif" if correlation > 0 else "Hubungan Negatif"}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Interpretasi Korelasi</h4>
                <p><b>Nilai:</b> {correlation:.3f}</p>
                <p><b>Kekuatan:</b> {'Kuat' if abs(correlation) > 0.7 else 'Sedang' if abs(correlation) > 0.3 else 'Lemah'}</p>
                <p><b>Arah:</b> {'Positif' if correlation > 0 else 'Negatif'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional comparative insights
        st.markdown('<div class="section-header"><h3>ANALISIS LANJUTAN</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        
        col_insight1, col_insight2, col_insight3 = st.columns(3)
        
        with col_insight1:
            # Peak analysis
            max_inflasi_idx = df_filtered['inflasi'].idxmax()
            max_x_var_idx = df_filtered[x_var].idxmax()
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Puncak Data</h4>
                <p><b>Inflasi tertinggi:</b> {df_filtered.loc[max_inflasi_idx, 'inflasi']:.2f}% ({df_filtered.loc[max_inflasi_idx, 'periode']})</p>
                <p><b>{x_var.replace('_', ' ').title()} tertinggi:</b> {df_filtered.loc[max_x_var_idx, x_var]:.2f} ({df_filtered.loc[max_x_var_idx, 'periode']})</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_insight2:
            # Trend analysis
            inflasi_trend = "naik" if df_filtered.iloc[-1]['inflasi'] > df_filtered.iloc[0]['inflasi'] else "turun"
            x_var_trend = "naik" if df_filtered.iloc[-1][x_var] > df_filtered.iloc[0][x_var] else "turun"
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Tren Periode</h4>
                <p><b>Inflasi:</b> {inflasi_trend} ({df_filtered.iloc[0]['inflasi']:.2f}% → {df_filtered.iloc[-1]['inflasi']:.2f}%)</p>
                <p><b>{x_var.replace('_', ' ').title()}:</b> {x_var_trend} ({df_filtered.iloc[0][x_var]:.2f} → {df_filtered.iloc[-1][x_var]:.2f})</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_insight3:
            # Relationship insight
            if correlation > 0.5:
                insight = "Terdapat hubungan positif yang kuat antara kedua variabel"
            elif correlation > 0:
                insight = "Terdapat hubungan positif yang lemah antara kedua variabel"
            elif correlation > -0.5:
                insight = "Terdapat hubungan negatif yang lemah antara kedua variabel"
            else:
                insight = "Terdapat hubungan negatif yang kuat antara kedua variabel"
                
            st.markdown(f"""
            <div class="insight-box">
                <h4>Insight Hubungan</h4>
                <p>{insight}. Perubahan dalam satu variabel cenderung diikuti oleh perubahan dalam variabel lainnya.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data untuk ditampilkan pada periode yang dipilih.")

# ==================== TAB 3: MODEL & PREDIKSI ====================
with tab3:
    if not df_filtered.empty:
        # === CEK DATA TEST UNTUK VISUALISASI ===
        df_test = df_filtered[df_filtered['periode_data'] == 'test']

        if df_test.empty or df_test['inflasi_prediksi'].isna().all():
            st.warning("""
            Data prediksi tidak tersedia untuk periode yang dipilih. 
            Silakan pilih rentang tahun yang mencakup periode test (2022–2024).
            """)
        else:
            # ======== BAGIAN GRAFIK DAN EVALUASI ========
            col_pred1, col_pred2 = st.columns([2, 1])

            with col_pred1:
                st.markdown('<div class="section-header"><h3>PERBANDINGAN AKTUAL VS PREDIKSI</h3></div>', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)

                # Grafik Aktual vs Prediksi
                fig6 = go.Figure()
                fig6.add_trace(go.Scatter(
                    x=df_test['date'],
                    y=df_test['inflasi'],
                    name='Aktual',
                    line=dict(color='#1e3c72', width=3.5),
                    mode='lines+markers'
                ))
                fig6.add_trace(go.Scatter(
                    x=df_test['date'],
                    y=df_test['inflasi_prediksi'],
                    name='Prediksi',
                    line=dict(color='#e74c3c', width=3, dash='dash'),
                    mode='lines+markers'
                ))
                fig6.update_layout(
                    title={'text': "Aktual vs Prediksi Inflasi", 'x': 0.5},
                    xaxis_title="Periode",
                    yaxis_title="Inflasi (%)",
                    template="plotly_white",
                    height=450,
                    hovermode='x unified',
                    margin=dict(t=40, l=60, r=40, b=60),
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    paper_bgcolor='rgba(255,255,255,0.9)',
                )
                st.plotly_chart(fig6, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_pred2:
                st.markdown('<div class="section-header"><h3>EVALUASI MODEL</h3></div>', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)

                # Hitung metrik evaluasi
                mae = df_test['MAE'].iloc[0] if 'MAE' in df_test.columns else np.mean(np.abs(df_test['residual']))
                rmse = df_test['RMSE'].iloc[0] if 'RMSE' in df_test.columns else np.sqrt(np.mean(df_test['residual']**2))
                r2 = df_test['R2'].iloc[0] if 'R2' in df_test.columns else 1 - (
                    np.sum(df_test['residual'] ** 2) / np.sum((df_test['inflasi'] - df_test['inflasi'].mean()) ** 2)
                )

                st.metric("Mean Absolute Error (MAE)", f"{mae:.4f}")
                st.metric("Root Mean Square Error (RMSE)", f"{rmse:.4f}")
                st.metric("Koefisien Determinasi (R²)", f"{r2:.4f}")

                st.markdown(f"""
                <div class="insight-box">
                    <h4>Interpretasi Metrik</h4>
                    <p><b>MAE:</b> Rata-rata kesalahan absolut prediksi</p>
                    <p><b>RMSE:</b> Kesalahan dengan penalti untuk error besar</p>
                    <p><b>R²:</b> Proporsi variansi yang dijelaskan model</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ======== BAGIAN FORM PREDIKSI USER ========
            st.markdown("---")
            st.markdown('<div class="section-header"><h3>SIMULASI PREDIKSI INFLASI BERDASARKAN VARIABEL EKONOMI</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)

            st.write("""
            Masukkan nilai variabel ekonomi di bawah ini untuk mensimulasikan tingkat inflasi
            berdasarkan model **Ridge Regression** yang telah dilatih.
            """)

            import joblib
            import pandas as pd
            import numpy as np

            try:
                model = joblib.load("ridge_model.pkl")
            except:
                st.error("File 'ridge_model.pkl' tidak ditemukan. Pastikan file model berada di direktori yang sama dengan app Streamlit ini.")
                st.stop()

            col1, col2, col3 = st.columns(3)

            with col1:
                bi_rate = st.number_input("BI Rate (%)", min_value=0.0, max_value=20.0, step=0.1)
                kurs = st.number_input("Kurs (Rp/USD)", min_value=1000.0, max_value=20000.0, step=50.0)
            with col2:
                uang_beredar = st.number_input("Uang Beredar (M2, triliun Rp)", min_value=0.0, step=100.0)
                investasi = st.number_input("Investasi (triliun Rp)", min_value=0.0, step=10.0)
            with col3:
                ekspor = st.number_input("Ekspor (juta USD)", min_value=0.0, step=10.0)
                impor = st.number_input("Impor (juta USD)", min_value=0.0, step=10.0)

            # ==================== CUSTOM BUTTON STYLE ====================
            if "btn_clicked" not in st.session_state:
                st.session_state.btn_clicked = False
            
            button_color = "#1e3c72" if not st.session_state.btn_clicked else "#c0392b"  # biru → merah
            border_color = "#1e3c72" if not st.session_state.btn_clicked else "#c0392b"
            
            st.markdown(f"""
                <style>
                div.stButton > button:first-child {{
                    background-color: {button_color};
                    color: white !important;           
                    border: 2px solid {border_color};  /
                    padding: 0.6em 2em;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 16px;
                    display: block;
                    margin: 0 auto;
                    transition: all 0.3s ease;
                }}
                div.stButton > button:first-child:hover {{
                    background-color: {"#2a5298" if not st.session_state.btn_clicked else "#e74c3c"};
                    color: white !important;    
                    border-color: {"#2a5298" if not st.session_state.btn_clicked else "#e74c3c"};
                    transform: scale(1.05);
                }}
                </style>
            """, unsafe_allow_html=True)
            
            # ==================== BUTTON PREDIKSI ====================
            if st.button("Prediksi Inflasi"):
                st.session_state.btn_clicked = True  # ubah status jadi aktif
            
                user_input = pd.DataFrame([{
                    "tahun": 2025,
                    "bulan": 11,
                    "inflasi": np.nan,
                    "bi_rate": bi_rate,
                    "kurs": kurs,
                    "uang_beredar": uang_beredar,
                    "investasi": investasi,
                    "ekspor": ekspor,
                    "impor": impor
                }])

                # === FEATURE ENGINEERING ===
                user_input["bulan_num"] = user_input["bulan"]
                user_input["month"] = user_input["bulan_num"]
                user_input["year"] = user_input["tahun"]

                user_input["month_sin"] = np.sin(2 * np.pi * user_input["month"] / 12)
                user_input["month_cos"] = np.cos(2 * np.pi * user_input["month"] / 12)

                for col in ["uang_beredar", "investasi", "ekspor", "impor"]:
                    user_input[f"log_{col}"] = np.log1p(user_input[col])

                lag_features = [
                    "inflasi_lag_1", "inflasi_lag_3", "inflasi_lag_12",
                    "bi_rate_lag_1", "bi_rate_lag_3", "kurs_lag_1", "kurs_lag_3",
                    "uang_beredar_lag_1", "uang_beredar_lag_3",
                    "inflasi_roll_mean_3", "inflasi_roll_std_12"
                ]
                for col in lag_features:
                    user_input[col] = 0  # placeholder agar struktur sama

                try:
                    prediksi = model.predict(user_input)
                    st.success(f"Diprediksi akan terjadi inflasi sebesar: **{prediksi[0]:.2f}%**")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat prediksi: {e}")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Tidak ada data untuk ditampilkan pada periode yang dipilih.")



# ==================== TAB 4: DATA & UNDUH ====================
with tab4:
    if not df_filtered.empty:
        col_data1, col_data2 = st.columns([2, 1])
        
        with col_data1:
            st.markdown('<div class="section-header"><h3>DATA TIME SERIES</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            # Show data
            display_df = df_filtered[['periode', 'inflasi', 'bi_rate', 'kurs', 'uang_beredar', 'investasi']].copy()
            
            # Format the display
            display_df['uang_beredar'] = (display_df['uang_beredar'] / 1000).round(1).astype(str) + ' T'
            display_df['investasi'] = (display_df['investasi'] / 1000).round(1).astype(str) + ' T'
            display_df['kurs'] = display_df['kurs'].apply(lambda x: f"{x:,.0f}")
            display_df['inflasi'] = display_df['inflasi'].round(2).astype(str) + '%'
            display_df['bi_rate'] = display_df['bi_rate'].round(2).astype(str) + '%'
            
            st.dataframe(display_df, use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_data2:
            st.markdown('<div class="section-header"><h3>UNDUH DATA STATISTIK</h3></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Informasi Dataset</h4>
                <p><b>Periode:</b> {start_year}-{end_year}</p>
                <p><b>Jumlah Data:</b> {len(df_filtered)} observasi bulanan</p>
                <p><b>Update Terakhir:</b> {df_filtered['date'].max().strftime('%d %B %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download buttons
            csv_data = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="UNDUH DATA CSV",
                data=csv_data,
                file_name=f"data_inflasi_{start_year}_{end_year}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            json_data = df_filtered.to_json(orient='records', date_format='iso')
            st.download_button(
                label="UNDUH DATA JSON",
                data=json_data,
                file_name=f"data_inflasi_{start_year}_{end_year}.json",
                mime="application/json",
                use_container_width=True
            )

            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Data Inflasi')
            buffer.seek(0)

            st.download_button(
                label="UNDUH DATA EXCEL",
                data=buffer,
                file_name=f"data_inflasi_{start_year}_{end_year}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data untuk ditampilkan pada periode yang dipilih.")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d; font-size: 0.85rem; padding: 1.5rem;'>"
    "  Sumber Data: FRED & BPS | © 2025 Dashboard Inflasi Indonesia"
    "</div>",
    unsafe_allow_html=True
)
