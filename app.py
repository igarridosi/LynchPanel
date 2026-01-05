# =============================================================================
# INGENIERO BROKER - Analizador de Inversiones Estilo Peter Lynch
# =============================================================================
# Aplicación web que automatiza el análisis de inversiones basado en la
# metodología de Peter Lynch ("Un paso por delante de Wall Street").
# =============================================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from groq import Groq
import os

# =============================================================================
# SISTEMA DE TRADUCCIONES (ESPAÑOL / INGLÉS)
# =============================================================================
TRANSLATIONS = {
    "es": {
        # Títulos principales
        "app_title": "INGENIERO BROKER",
        "app_subtitle": "Análisis de Inversiones · Metodología Peter Lynch",
        "config": "⚙ CONFIGURACIÓN",
        "language": "🌐 IDIOMA",
        
        # Sidebar
        "api_key_title": "🔑 API de Groq (Gratis)",
        "api_key_placeholder": "Introduce tu API Key:",
        "api_key_help": "Obtén tu API Key en: https://console.groq.com/keys",
        "api_key_warning": "⚠ Necesitas una API Key",
        "api_key_howto": """**¿Cómo obtenerla? (GRATIS)**
1. Ve a [Groq Console](https://console.groq.com/keys)
2. Crea una cuenta gratuita
3. Genera una nueva API Key
4. Cópiala y pégala aquí

✅ **Límites gratuitos:** 30 req/min, 14,400 req/día""",
        "methodology": "📚 Metodología Lynch",
        "peg_cheap": "Barato",
        "peg_fair": "Justo",
        "peg_expensive": "Caro",
        "classifications": "Clasificaciones:",
        "developed_with": "Desarrollado con",
        "using": "usando",
        
        # Clasificaciones Lynch
        "fast_growth": "🚀 Crecimiento Rápido",
        "stable": "🏛️ Estable",
        "cyclical": "🔄 Cíclica",
        "turnaround": "📈 Recuperación",
        "hidden_asset": "💎 Activo Oculto",
        
        # Búsqueda
        "search_stock": "🔍 Buscar Acción",
        "ticker_placeholder": "AAPL, KO, MSFT, IBE.MC, TSLA...",
        "ticker_help": "Introduce el símbolo de la acción. Para mercados europeos añade el sufijo (ej: IBE.MC para Iberdrola)",
        "analyze": "ANALIZAR",
        "quick_examples": "Ejemplos rápidos:",
        
        # Métricas panel
        "main_metrics": "📊 MÉTRICAS PRINCIPALES",
        "current_price": "Precio Actual",
        "per_trailing": "PER (Trailing)",
        "peg_ratio": "PEG Ratio",
        "dividend_yield": "Rentabilidad/Dividendo",
        "price_book": "Price / Book",
        "market_cap": "Market Cap",
        "cash_debt": "Efectivo / Deuda",
        "beta": "Beta",
        "quarterly": "trimestral",
        
        # Badges métricas
        "undervalued": "● Infravalorado",
        "normal": "● Normal",
        "overvalued": "● Sobrevalorado",
        "cheap": "● Barato",
        "fair": "● Justo",
        "expensive": "● Caro",
        "very_solid": "● Muy Sólido",
        "solid": "● Sólido",
        "moderate": "● Moderado",
        "risk": "● Riesgo",
        "excellent": "● Excelente",
        "no_debt": "Sin Deuda",
        "low_volatility": "● Baja volatilidad",
        "high_volatility": "● Alta volatilidad",
        "market": "● Mercado",
        "mega_cap": "Mega Cap",
        "large_cap": "Large Cap",
        "mid_cap": "Mid Cap",
        "small_cap": "Small Cap",
        
        # Header Google Finance
        "high": "HIGH",
        "low": "LOW",
        "vol": "VOL",
        "div": "DIV",
        
        # Gráfico
        "price_chart": "📈 Gráfico de Precios",
        "period": "Período:",
        "1m": "1M",
        "3m": "3M",
        "6m": "6M",
        "ytd": "YTD",
        "1y": "1Y",
        "5y": "5Y",
        "price": "Precio",
        
        # Análisis AI
        "ai_analysis": "🤖 Análisis con IA",
        "analyzing": "Analizando",
        "with_lynch_methodology": "con metodología Peter Lynch...",
        "analysis_result": "📋 RESULTADO DEL ANÁLISIS",
        "api_error": "Error al conectar con Groq API",
        "enter_api_key": "⚠️ Introduce tu API Key de Groq en el sidebar para obtener el análisis",
        
        # Tabs
        "summary": "📊 Resumen",
        "valuation": "💰 Valoración",
        "balance": "🏦 Balance",
        "dividends": "💵 Dividendos",
        "news": "📰 Noticias",
        
        # Secciones análisis
        "valuation_ratios": "📈 Ratios de Valoración",
        "balance_debt": "🏦 Balance y Deuda",
        "profitability": "📊 Rentabilidad",
        "recent_news": "📰 Noticias Recientes",
        
        # Campos de datos
        "total_debt": "Deuda Total",
        "total_cash": "Efectivo + Inversiones C/P",
        "cash_debt_ratio": "Ratio Efectivo/Deuda",
        "debt_equity": "Deuda/Equity",
        "financial_situation": "Situación Financiera",
        "roe": "ROE",
        "profit_margin": "Margen de Beneficio",
        "earnings_growth": "Crecimiento Beneficios",
        "revenue_growth": "Crecimiento Ingresos",
        
        # Estados
        "no_news": "No hay noticias recientes disponibles",
        "loading_data": "Cargando datos de",
        "error_loading": "Error al cargar datos",
        "invalid_ticker": "No se encontraron datos para el ticker",
        "enter_ticker": "Introduce un ticker para comenzar el análisis",
        
        # Gráfico - Estadísticas y rango
        "position_in_range": "POSICIÓN EN RANGO",
        "trend": "TENDENCIA",
        "bullish": "ALCISTA",
        "bearish": "BAJISTA",
        "sideways": "LATERAL",
        "of_range": "del rango",
        "maximum": "MÁXIMO",
        "minimum": "MÍNIMO",
        "avg_volume": "VOL. PROM",
        "volatility": "VOLATILIDAD",
        "historical_performance": "RENDIMIENTO HISTÓRICO",
        "1w": "1S",
        
        # Clasificaciones de empresa
        "market_giant_dividends": "Gigante del mercado con dividendos - empresa blue chip consolidada",
        "fast_grower_desc": "Empresa de alto crecimiento - expandiendo rápidamente",
        "cyclical_desc": "Empresa cíclica - dependiente del ciclo económico",
        "turnaround_desc": "Empresa en recuperación - mejorando desde dificultades",
        "asset_play_desc": "Activo oculto - valor no reconocido por el mercado",
        "stalwart_desc": "Empresa estable - crecimiento constante y predecible",
        
        # Footer
        "footer_text": "Desarrollado con metodología Peter Lynch · Los datos provienen de Yahoo Finance · No es asesoramiento financiero",
        
        # Modal de idioma
        "select_language": "SELECCIONAR IDIOMA",
        "language_spanish": "Español",
        "language_english": "Inglés",
    },
    "en": {
        # Main titles
        "app_title": "ENGINEER BROKER",
        "app_subtitle": "Investment Analysis · Peter Lynch Methodology",
        "config": "⚙ SETTINGS",
        "language": "🌐 LANGUAGE",
        
        # Sidebar
        "api_key_title": "🔑 Groq API (Free)",
        "api_key_placeholder": "Enter your API Key:",
        "api_key_help": "Get your API Key at: https://console.groq.com/keys",
        "api_key_warning": "⚠ API Key required",
        "api_key_howto": """**How to get it? (FREE)**
1. Go to [Groq Console](https://console.groq.com/keys)
2. Create a free account
3. Generate a new API Key
4. Copy and paste it here

✅ **Free limits:** 30 req/min, 14,400 req/day""",
        "methodology": "📚 Lynch Methodology",
        "peg_cheap": "Cheap",
        "peg_fair": "Fair",
        "peg_expensive": "Expensive",
        "classifications": "Classifications:",
        "developed_with": "Developed with",
        "using": "using",
        
        # Lynch classifications
        "fast_growth": "🚀 Fast Growth",
        "stable": "🏛️ Stalwart",
        "cyclical": "🔄 Cyclical",
        "turnaround": "📈 Turnaround",
        "hidden_asset": "💎 Asset Play",
        
        # Search
        "search_stock": "🔍 Search Stock",
        "ticker_placeholder": "AAPL, KO, MSFT, IBE.MC, TSLA...",
        "ticker_help": "Enter the stock symbol. For European markets add the suffix (e.g., IBE.MC for Iberdrola)",
        "analyze": "ANALYZE",
        "quick_examples": "Quick examples:",
        
        # Metrics panel
        "main_metrics": "📊 KEY METRICS",
        "current_price": "Current Price",
        "per_trailing": "P/E (Trailing)",
        "peg_ratio": "PEG Ratio",
        "dividend_yield": "Dividend Yield",
        "price_book": "Price / Book",
        "market_cap": "Market Cap",
        "cash_debt": "Cash / Debt",
        "beta": "Beta",
        "quarterly": "quarterly",
        
        # Metric badges
        "undervalued": "● Undervalued",
        "normal": "● Normal",
        "overvalued": "● Overvalued",
        "cheap": "● Cheap",
        "fair": "● Fair",
        "expensive": "● Expensive",
        "very_solid": "● Very Solid",
        "solid": "● Solid",
        "moderate": "● Moderate",
        "risk": "● Risk",
        "excellent": "● Excellent",
        "no_debt": "No Debt",
        "low_volatility": "● Low volatility",
        "high_volatility": "● High volatility",
        "market": "● Market",
        "mega_cap": "Mega Cap",
        "large_cap": "Large Cap",
        "mid_cap": "Mid Cap",
        "small_cap": "Small Cap",
        
        # Google Finance header
        "high": "HIGH",
        "low": "LOW",
        "vol": "VOL",
        "div": "DIV",
        
        # Chart
        "price_chart": "📈 Price Chart",
        "period": "Period:",
        "1m": "1M",
        "3m": "3M",
        "6m": "6M",
        "ytd": "YTD",
        "1y": "1Y",
        "5y": "5Y",
        "price": "Price",
        
        # AI Analysis
        "ai_analysis": "🤖 AI Analysis",
        "analyzing": "Analyzing",
        "with_lynch_methodology": "with Peter Lynch methodology...",
        "analysis_result": "📋 ANALYSIS RESULT",
        "api_error": "Error connecting to Groq API",
        "enter_api_key": "⚠️ Enter your Groq API Key in the sidebar to get the analysis",
        
        # Tabs
        "summary": "📊 Summary",
        "valuation": "💰 Valuation",
        "balance": "🏦 Balance",
        "dividends": "💵 Dividends",
        "news": "📰 News",
        
        # Analysis sections
        "valuation_ratios": "📈 Valuation Ratios",
        "balance_debt": "🏦 Balance & Debt",
        "profitability": "📊 Profitability",
        "recent_news": "📰 Recent News",
        
        # Data fields
        "total_debt": "Total Debt",
        "total_cash": "Cash + Short-term Investments",
        "cash_debt_ratio": "Cash/Debt Ratio",
        "debt_equity": "Debt/Equity",
        "financial_situation": "Financial Position",
        "roe": "ROE",
        "profit_margin": "Profit Margin",
        "earnings_growth": "Earnings Growth",
        "revenue_growth": "Revenue Growth",
        
        # States
        "no_news": "No recent news available",
        "loading_data": "Loading data for",
        "error_loading": "Error loading data",
        "invalid_ticker": "No data found for ticker",
        "enter_ticker": "Enter a ticker to start the analysis",
        
        # Chart - Stats and range
        "position_in_range": "POSITION IN RANGE",
        "trend": "TREND",
        "bullish": "BULLISH",
        "bearish": "BEARISH",
        "sideways": "SIDEWAYS",
        "of_range": "of range",
        "maximum": "HIGH",
        "minimum": "LOW",
        "avg_volume": "AVG VOL",
        "volatility": "VOLATILITY",
        "historical_performance": "HISTORICAL PERFORMANCE",
        "1w": "1W",
        
        # Company classifications
        "market_giant_dividends": "Market giant with dividends - consolidated blue chip company",
        "fast_grower_desc": "High growth company - expanding rapidly",
        "cyclical_desc": "Cyclical company - dependent on economic cycle",
        "turnaround_desc": "Turnaround company - improving from difficulties",
        "asset_play_desc": "Asset play - value not recognized by market",
        "stalwart_desc": "Stalwart company - constant and predictable growth",
        
        # Footer
        "footer_text": "Developed with Peter Lynch methodology · Data from Yahoo Finance · Not financial advice",
        
        # Modal de idioma
        "select_language": "SELECT LANGUAGE",
        "language_spanish": "Spanish",
        "language_english": "English",
    }
}

def get_text(key):
    """Obtiene el texto traducido según el idioma seleccionado."""
    lang = st.session_state.get('language', 'es')
    return TRANSLATIONS.get(lang, TRANSLATIONS['es']).get(key, key)

@st.dialog(" ")
def language_modal():
    """Modal para selección de idioma con estilo retrofuturista."""
    # Título del modal con estilo
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <div style='font-family: monospace; color: #00FF9F; font-size: 1.2rem; letter-spacing: 3px;
                    text-transform: uppercase; margin-bottom: 10px;'>🌐</div>
        <div style='font-family: monospace; color: #00FF9F; font-size: 1rem; letter-spacing: 2px;
                    text-transform: uppercase;'>""" + get_text('select_language') + """</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón Español
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <style>
        div[data-testid="column"]:first-child button {
            background: """ + ('linear-gradient(135deg, #00FF9F 0%, #00CC7F 100%)' if st.session_state.get('language', 'es') == 'es' else 'rgba(0, 255, 159, 0.1)') + """ !important;
            border: 2px solid #00FF9F !important;
            color: """ + ('#0a0a0a' if st.session_state.get('language', 'es') == 'es' else '#00FF9F') + """ !important;
            font-family: monospace !important;
            font-weight: bold !important;
            padding: 20px !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Español", use_container_width=True, key="modal_es"):
            st.session_state.language = 'es'
            st.rerun()
    
    with col2:
        st.markdown("""
        <style>
        div[data-testid="column"]:last-child button {
            background: """ + ('linear-gradient(135deg, #6464FF 0%, #4444DD 100%)' if st.session_state.get('language', 'es') == 'en' else 'rgba(100, 100, 255, 0.1)') + """ !important;
            border: 2px solid #6464FF !important;
            color: """ + ('#ffffff' if st.session_state.get('language', 'es') == 'en' else '#6464FF') + """ !important;
            font-family: monospace !important;
            font-weight: bold !important;
            padding: 20px !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("English", use_container_width=True, key="modal_en"):
            st.session_state.language = 'en'
            st.rerun()
    
    # Indicador del idioma actual
    current_lang_text = "Español" if st.session_state.get('language', 'es') == 'es' else "English"
    current_flag = "🇪🇸" if st.session_state.get('language', 'es') == 'es' else "🇬🇧"
    st.markdown(f"""
    <div style='text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);'>
        <span style='font-family: monospace; color: rgba(255,255,255,0.5); font-size: 0.75rem;'>
            {'Idioma actual' if st.session_state.get('language', 'es') == 'es' else 'Current language'}: 
            <span style='color: #00FF9F;'>{current_lang_text}</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Ingeniero Broker - Análisis Peter Lynch",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ESTILOS CSS PERSONALIZADOS - RETROFUTURISTA
# =============================================================================
st.markdown("""
<style>
    /* ===== PALETA RETROFUTURISTA ===== */
    :root {
        --cyan-neon: #00FF9F;
        --magenta-neon: #FF006E;
        --yellow-neon: #FFB74D;
        --purple-neon: #6464FF;
        --dark-bg: #0A0A0F;
        --card-bg: rgba(15, 15, 25, 0.9);
    }
    
    /* ===== FONDO GENERAL ===== */
    .stApp {
        background: linear-gradient(180deg, #0A0A0F 0%, #0D0D15 50%, #0A0A0F 100%);
    }
    
    /* ===== SIDEBAR RETROFUTURISTA ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0A0F 0%, #12121A 100%) !important;
        border-right: 1px solid rgba(0, 255, 159, 0.1);
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #00FF9F !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 300;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        color: rgba(255, 255, 255, 0.7);
        font-family: monospace;
    }
    
    /* ===== TÍTULOS PRINCIPALES ===== */
    h1 {
        color: #00FF9F !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        text-shadow: 0 0 30px rgba(0, 255, 159, 0.5);
        font-weight: 200 !important;
        letter-spacing: 3px;
    }
    
    h2, h3 {
        color: #FF006E !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        text-shadow: 0 0 20px rgba(255, 0, 110, 0.3);
        font-weight: 300 !important;
    }
    
    /* ===== INPUT RETROFUTURISTA ===== */
    .stTextInput input,
    .stTextInput > div > div > input,
    .stTextInput [data-baseweb="input"] input,
    .stTextInput [data-baseweb="base-input"] input,
    input[type="text"],
    input[type="password"] {
        background: rgba(15, 15, 25, 0.8) !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
        border-radius: 8px !important;
        color: #00FF9F !important;
        font-family: monospace !important;
        outline: none !important;
        outline-color: transparent !important;
        box-shadow: none !important;
    }
    
    .stTextInput input:focus,
    .stTextInput input:active,
    .stTextInput input:focus-visible,
    .stTextInput input:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextInput > div > div > input:active,
    .stTextInput > div > div > input:focus-visible,
    .stTextInput [data-baseweb="input"]:focus-within,
    .stTextInput [data-baseweb="base-input"]:focus-within,
    input[type="text"]:focus,
    input[type="password"]:focus {
        border: 2px solid #00FF9F !important;
        outline: none !important;
        outline-color: transparent !important;
    }
    
    /* Eliminar el borde rojo de Streamlit/BaseWeb */
    .stTextInput [data-baseweb="input"],
    .stTextInput [data-baseweb="base-input"],
    .stTextInput > div,
    .stTextInput > div > div {
        border-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stTextInput [data-baseweb="input"]:focus-within,
    .stTextInput [data-baseweb="base-input"]:focus-within {
        border-color: transparent !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* ===== BOTONES RETROFUTURISTA ===== */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.1) 0%, rgba(255, 0, 110, 0.1) 100%) !important;
        border: 1px solid #00FF9F !important;
        color: #00FF9F !important;
        font-family: monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.3) 0%, rgba(255, 0, 110, 0.2) 100%) !important;
        box-shadow: 0 0 20px rgba(0, 255, 159, 0.4) !important;
        transform: translateY(-2px);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00FF9F 0%, #00CC7F 100%) !important;
        color: #0A0A0F !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 255, 159, 0.6) !important;
    }
    
    /* ===== TABS RETROFUTURISTA ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 15, 25, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: rgba(255, 255, 255, 0.6) !important;
        font-family: monospace !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.2) 0%, rgba(0, 255, 159, 0.05) 100%) !important;
        border: 1px solid #00FF9F !important;
        color: #00FF9F !important;
    }
    
    /* ===== EXPANDER RETROFUTURISTA ===== */
    .streamlit-expanderHeader {
        background: rgba(15, 15, 25, 0.8) !important;
        border: 1px solid rgba(255, 0, 110, 0.2) !important;
        border-radius: 8px !important;
        color: #FF006E !important;
        font-family: monospace !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 15, 25, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: none !important;
    }
    
    /* ===== SPINNER RETROFUTURISTA ===== */
    .stSpinner > div {
        border-color: #00FF9F !important;
    }
    
    /* ===== ALERTAS RETROFUTURISTA ===== */
    .stAlert {
        background: rgba(15, 15, 25, 0.9) !important;
    }
    
    /* ===== SELECTBOX Y RADIO ===== */
    .stSelectbox > div > div {
        background: rgba(15, 15, 25, 0.8) !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
    }
    
    .stRadio > div {
        gap: 5px;
    }
    
    .stRadio > div > label {
        background: rgba(15, 15, 25, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        color: rgba(255, 255, 255, 0.6) !important;
        font-family: monospace !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #00FF9F !important;
        color: #00FF9F !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.2) 0%, rgba(0, 255, 159, 0.05) 100%) !important;
        border-color: #00FF9F !important;
        color: #00FF9F !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(0, 255, 159, 0.3) 50%, transparent 100%);
    }
    
    /* ===== SCROLLBAR RETROFUTURISTA ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A0A0F;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00FF9F 0%, #FF006E 100%);
        border-radius: 4px;
    }
    
    /* ===== SIDEBAR ITEMS ===== */
    .sidebar-item-active {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.2) 0%, rgba(0, 255, 159, 0.05) 100%);
        border-radius: 8px;
        padding: 8px 12px;
        border-left: 3px solid #00FF9F;
        color: #00FF9F;
        font-family: monospace;
    }
    
    .sidebar-item {
        padding: 8px 12px;
        color: rgba(255, 255, 255, 0.4);
        font-family: monospace;
    }
    
    /* ===== CLASSIFICATION BADGES ===== */
    .classification-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        margin: 5px 0;
        font-family: monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-crecimiento {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.2) 0%, rgba(0, 255, 159, 0.05) 100%);
        border: 1px solid #00FF9F;
        color: #00FF9F;
        text-shadow: 0 0 10px rgba(0, 255, 159, 0.5);
    }
    
    .badge-estable {
        background: linear-gradient(135deg, rgba(100, 100, 255, 0.2) 0%, rgba(100, 100, 255, 0.05) 100%);
        border: 1px solid #6464FF;
        color: #6464FF;
        text-shadow: 0 0 10px rgba(100, 100, 255, 0.5);
    }
    
    .badge-ciclica {
        background: linear-gradient(135deg, rgba(255, 183, 77, 0.2) 0%, rgba(255, 183, 77, 0.05) 100%);
        border: 1px solid #FFB74D;
        color: #FFB74D;
        text-shadow: 0 0 10px rgba(255, 183, 77, 0.5);
    }
    
    .badge-recuperacion {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2) 0%, rgba(255, 0, 110, 0.05) 100%);
        border: 1px solid #FF006E;
        color: #FF006E;
        text-shadow: 0 0 10px rgba(255, 0, 110, 0.5);
    }
    
    .badge-activo-oculto {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 215, 0, 0.05) 100%);
        border: 1px solid #FFD700;
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    /* ===== PEG BADGES ===== */
    .peg-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        margin-left: 10px;
        font-family: monospace;
    }
    
    .peg-barato {
        background: rgba(0, 255, 159, 0.2);
        border: 1px solid #00FF9F;
        color: #00FF9F;
    }
    
    .peg-justo {
        background: rgba(255, 183, 77, 0.2);
        border: 1px solid #FFB74D;
        color: #FFB74D;
    }
    
    .peg-caro {
        background: rgba(255, 0, 110, 0.2);
        border: 1px solid #FF006E;
        color: #FF006E;
    }
    
    /* ===== DATAFRAME RETROFUTURISTA ===== */
    .stDataFrame {
        border: 1px solid rgba(0, 255, 159, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00FF9F 0%, #FF006E 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SYSTEM INSTRUCTIONS PARA GROQ (PERSONALIDAD DEL INGENIERO BROKER)
# =============================================================================
SYSTEM_INSTRUCTIONS = {
    'es': """Actúa como mi Ingeniero Broker Senior (estilo Peter Lynch). Tu trabajo es analizar los datos que te paso y ejecutar 'La rutina de los dos minutos'.
REGLAS:

1. Si el PEG ratio es < 1.0, considéralo barato. Si es > 2.0, caro.

2. Compara el PER con el crecimiento esperado.

3. Clasifica la empresa (Cíclica, Recuperación, Activo Oculto, Crecimiento Rápido, Estable).

4. Busca problemas de deuda (¿Hay más deuda que efectivo?).

5. Tu veredicto debe ser directo: COMPRAR, VENDER o MANTENER, explicado con sentido común y analogías sencillas.

IMPORTANTE: Responde SIEMPRE en español.""",

    'en': """Act as my Senior Broker Engineer (Peter Lynch style). Your job is to analyze the data I provide and execute 'The Two-Minute Drill'.
RULES:

1. If the PEG ratio is < 1.0, consider it cheap. If > 2.0, expensive.

2. Compare the P/E with expected growth.

3. Classify the company (Cyclical, Turnaround, Asset Play, Fast Grower, Stalwart).

4. Look for debt problems (Is there more debt than cash?).

5. Your verdict must be direct: BUY, SELL or HOLD, explained with common sense and simple analogies.

IMPORTANT: ALWAYS respond in English."""
}

def get_system_instruction():
    """Obtiene la instrucción del sistema según el idioma seleccionado."""
    lang = st.session_state.get('language', 'es')
    return SYSTEM_INSTRUCTIONS.get(lang, SYSTEM_INSTRUCTIONS['es'])

# =============================================================================
# CLASIFICACIÓN AUTOMÁTICA DE EMPRESAS (METODOLOGÍA PETER LYNCH)
# =============================================================================

def classify_company(data):
    """
    Clasifica automáticamente una empresa según la metodología de Peter Lynch.
    
    Categorías:
    - 🚀 Crecimiento Rápido: Alto crecimiento de beneficios (>20%), reinvierten
    - 🏛️ Estable: Empresas grandes, crecimiento moderado, pagan dividendos
    - 🔄 Cíclica: Sectores que dependen del ciclo económico
    - 📈 Recuperación: Empresas en reestructuración o recuperándose
    - 💎 Activo Oculto: Valor oculto en balance (bajo P/B, mucho efectivo)
    
    Args:
        data: Diccionario con datos financieros de la empresa
        
    Returns:
        Tupla (clasificación, emoji, css_class, explicación)
    """
    # Extraer métricas relevantes
    sector = (data.get('sector') or '').lower()
    industria = (data.get('industria') or '').lower()
    
    # Función helper para convertir valores seguros a float
    def safe_float(value, default=0):
        if value is None or value == 'N/A' or value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    market_cap = safe_float(data.get('market_cap'), 0)
    crecimiento = safe_float(data.get('crecimiento_beneficios'), 0)
    crecimiento_ingresos = safe_float(data.get('crecimiento_ingresos'), 0)
    
    # Normalizar dividend yield (puede venir como 0.029 o 2.9)
    dividend_yield_raw = safe_float(data.get('dividend_yield'), 0)
    if dividend_yield_raw > 1:  # Viene como porcentaje (2.9 en lugar de 0.029)
        dividend_yield = dividend_yield_raw / 100
    else:
        dividend_yield = dividend_yield_raw
    
    price_to_book = safe_float(data.get('price_to_book'), 999)
    per_trailing = safe_float(data.get('per_trailing'), 0)
    deuda = safe_float(data.get('deuda_total'), 0)
    efectivo = safe_float(data.get('efectivo_total'), 0)
    roe = safe_float(data.get('roe'), 0)
    peg = safe_float(data.get('peg_ratio'), None)
    
    # Sectores cíclicos típicos
    sectores_ciclicos = ['consumer cyclical', 'basic materials', 'energy', 'industrials']
    sectores_defensivos = ['consumer defensive', 'healthcare', 'utilities', 'consumer staples']
    
    # 1. RECUPERACIÓN: PER negativo indica pérdidas
    if per_trailing is not None and per_trailing < 0:
        return (
            "Recuperación" if st.session_state.get('language', 'es') == 'es' else "Turnaround",
            "📈",
            "badge-recuperacion",
            get_text('turnaround_desc')
        )
    
    # 2. ESTABLE: Empresas grandes (>50B) con dividendos en sectores defensivos
    is_defensive = any(s in sector for s in sectores_defensivos)
    has_good_dividend = dividend_yield > 0.015  # >1.5% dividendo
    is_large_cap = market_cap > 50e9  # >50B
    is_mega_cap = market_cap > 200e9  # >200B
    
    if is_mega_cap and has_good_dividend:
        return (
            "Estable" if st.session_state.get('language', 'es') == 'es' else "Stalwart",
            "🏛️",
            "badge-estable",
            get_text('market_giant_dividends')
        )
    
    if is_large_cap and has_good_dividend and is_defensive:
        return (
            "Estable" if st.session_state.get('language', 'es') == 'es' else "Stalwart",
            "🏛️",
            "badge-estable",
            get_text('stalwart_desc')
        )
    
    # 3. CÍCLICA: Sectores que dependen del ciclo económico
    is_cyclical = any(s in sector for s in sectores_ciclicos)
    is_auto = 'auto' in industria or 'vehicle' in industria
    is_airline = 'airline' in industria
    is_hotel = 'hotel' in industria or 'leisure' in industria
    
    if is_cyclical or is_auto or is_airline or is_hotel:
        return (
            "Cíclica" if st.session_state.get('language', 'es') == 'es' else "Cyclical",
            "🔄",
            "badge-ciclica",
            get_text('cyclical_desc')
        )
    
    # 4. ACTIVO OCULTO: Bajo Price/Book y buena posición de caja
    if price_to_book < 1.2 and efectivo > deuda:
        return (
            "Activo Oculto" if st.session_state.get('language', 'es') == 'es' else "Asset Play",
            "💎",
            "badge-activo-oculto",
            get_text('asset_play_desc')
        )
    
    # 5. CRECIMIENTO RÁPIDO: Alto crecimiento de beneficios o ingresos
    has_high_growth = crecimiento > 0.20 or crecimiento_ingresos > 0.20
    has_good_peg = (peg is not None) and (isinstance(peg, (int, float))) and (peg < 1.5) and (peg > 0)
    is_tech = 'technology' in sector or 'software' in industria
    
    if has_high_growth:
        return (
            "Crecimiento Rápido" if st.session_state.get('language', 'es') == 'es' else "Fast Grower",
            "🚀",
            "badge-crecimiento",
            get_text('fast_grower_desc')
        )
    
    if is_tech and market_cap < 100e9 and (crecimiento > 0.10 or crecimiento_ingresos > 0.15):
        return (
            "Crecimiento Rápido" if st.session_state.get('language', 'es') == 'es' else "Fast Grower",
            "🚀",
            "badge-crecimiento",
            "Empresa tecnológica en fase de crecimiento" if st.session_state.get('language', 'es') == 'es' else "Technology company in growth phase"
        )
    
    # 6. ESTABLE por defecto para empresas grandes
    if is_large_cap:
        return (
            "Estable" if st.session_state.get('language', 'es') == 'es' else "Stalwart",
            "🏛️",
            "badge-estable",
            "Gran capitalización - empresa consolidada en su sector" if st.session_state.get('language', 'es') == 'es' else "Large cap - established company in its sector"
        )
    
    # 7. Por defecto para empresas medianas/pequeñas
    if market_cap > 10e9:  # Mid cap
        return (
            "Estable" if st.session_state.get('language', 'es') == 'es' else "Stalwart",
            "🏛️",
            "badge-estable",
            "Empresa de mediana capitalización consolidada" if st.session_state.get('language', 'es') == 'es' else "Consolidated mid-cap company"
        )
    else:
        return (
            "Crecimiento Rápido" if st.session_state.get('language', 'es') == 'es' else "Fast Grower",
            "🚀",
            "badge-crecimiento",
            "Empresa de menor tamaño con potencial de crecimiento" if st.session_state.get('language', 'es') == 'es' else "Smaller company with growth potential"
        )

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def format_large_number(num):
    """
    Formatea números grandes a formato legible (B para billones, M para millones).
    
    Args:
        num: Número a formatear
        
    Returns:
        String formateado o 'N/A' si no es válido
    """
    if num is None or pd.isna(num):
        return "N/A"
    
    try:
        num = float(num)
        if abs(num) >= 1e12:
            return f"${num/1e12:.2f}T"
        elif abs(num) >= 1e9:
            return f"${num/1e9:.2f}B"
        elif abs(num) >= 1e6:
            return f"${num/1e6:.2f}M"
        else:
            return f"${num:,.2f}"
    except (ValueError, TypeError):
        return "N/A"


def safe_get(data_dict, key, default="N/A"):
    """
    Obtiene un valor de un diccionario de forma segura.
    
    Args:
        data_dict: Diccionario de datos
        key: Clave a buscar
        default: Valor por defecto si no existe
        
    Returns:
        Valor encontrado o default
    """
    try:
        value = data_dict.get(key)
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return default
        return value
    except (KeyError, TypeError, AttributeError):
        return default


def get_stock_data(ticker_symbol):
    """
    Obtiene todos los datos financieros de una acción usando yfinance.
    
    Args:
        ticker_symbol: Símbolo del ticker (ej: AAPL, KO, IBE.MC)
        
    Returns:
        Diccionario con todos los datos financieros o None si hay error
    """
    try:
        # Crear objeto ticker
        ticker = yf.Ticker(ticker_symbol)
        
        # Obtener información general
        info = ticker.info
        
        # Verificar que el ticker es válido
        if not info or 'regularMarketPrice' not in info and 'currentPrice' not in info:
            return None
        
        # Extraer métricas clave
        data = {
            # Información básica
            "nombre": safe_get(info, "longName", safe_get(info, "shortName", ticker_symbol)),
            "sector": safe_get(info, "sector"),
            "industria": safe_get(info, "industry"),
            "pais": safe_get(info, "country"),
            "moneda": safe_get(info, "currency", "USD"),
            
            # Precios
            "precio_actual": safe_get(info, "currentPrice", safe_get(info, "regularMarketPrice")),
            "precio_objetivo": safe_get(info, "targetMeanPrice"),
            "precio_52w_high": safe_get(info, "fiftyTwoWeekHigh"),
            "precio_52w_low": safe_get(info, "fiftyTwoWeekLow"),
            
            # Ratios de valoración (CRUCIALES para Lynch)
            "per_trailing": safe_get(info, "trailingPE"),
            "per_forward": safe_get(info, "forwardPE"),
            "trailing_peg_ratio": safe_get(info, "trailingPegRatio"),  # PEG calculado por Yahoo (más fiable)
            "price_to_book": safe_get(info, "priceToBook"),
            "price_to_sales": safe_get(info, "priceToSalesTrailing12Months"),
            
            # Dividendos - múltiples fuentes para mejor precisión
            "dividend_yield": safe_get(info, "dividendYield"),  # Yield actual (decimal)
            "trailing_annual_dividend_yield": safe_get(info, "trailingAnnualDividendYield"),  # Yield anual trailing
            "dividend_rate": safe_get(info, "dividendRate"),  # Dividendo anual por acción
            "last_dividend_value": safe_get(info, "lastDividendValue"),  # Último dividendo pagado
            "last_dividend_date": safe_get(info, "lastDividendDate"),  # Fecha del último dividendo
            "ex_dividend_date": safe_get(info, "exDividendDate"),  # Fecha ex-dividendo
            "five_year_avg_dividend_yield": safe_get(info, "fiveYearAvgDividendYield"),
            "payout_ratio": safe_get(info, "payoutRatio"),
            
            # Balance y deuda (datos básicos del info)
            "deuda_total_info": safe_get(info, "totalDebt"),
            "efectivo_total_info": safe_get(info, "totalCash"),
            "deuda_equity": safe_get(info, "debtToEquity"),
            
            # Rentabilidad
            "roe": safe_get(info, "returnOnEquity"),
            "roa": safe_get(info, "returnOnAssets"),
            "margen_beneficio": safe_get(info, "profitMargins"),
            "margen_operativo": safe_get(info, "operatingMargins"),
            
            # Crecimiento - múltiples fuentes para mejor precisión
            "crecimiento_beneficios": safe_get(info, "earningsGrowth"),
            "crecimiento_ingresos": safe_get(info, "revenueGrowth"),
            "crecimiento_beneficios_trimestral": safe_get(info, "earningsQuarterlyGrowth"),
            "eps_actual": safe_get(info, "trailingEps"),
            "eps_forward": safe_get(info, "forwardEps"),
            "eps_current_year": safe_get(info, "epsCurrentYear"),
            
            # Tamaño
            "market_cap": safe_get(info, "marketCap"),
            "enterprise_value": safe_get(info, "enterpriseValue"),
            "num_empleados": safe_get(info, "fullTimeEmployees"),
            
            # Beta (volatilidad)
            "beta": safe_get(info, "beta"),
        }
        
        # =====================================================================
        # CALCULAR PEG RATIO - MÉTODO MEJORADO
        # =====================================================================
        # Prioridad:
        # 1. trailingPegRatio de Yahoo Finance (ya calculado con 5Y growth)
        # 2. Calcular manualmente con EPS forward growth anualizado a 5 años
        
        peg_final = None
        peg_calculation = ""
        growth_rate_used = None
        per_used = None
        
        # Función helper para validar números
        def is_valid_number(val):
            if val is None or val == 'N/A':
                return False
            try:
                v = float(val)
                return not (pd.isna(v)) and v != 0
            except:
                return False
        
        # Obtener valores
        per_trailing = data.get("per_trailing")
        trailing_peg = data.get("trailing_peg_ratio")
        eps_trailing = data.get("eps_actual")
        eps_forward = data.get("eps_forward")
        
        # MÉTODO 1: Usar trailingPegRatio de Yahoo (el más fiable)
        if is_valid_number(trailing_peg):
            peg_val = float(trailing_peg)
            if 0.1 <= peg_val <= 10:  # Validar rango razonable
                peg_final = peg_val
                # Calcular el growth implícito: Growth = PE / PEG
                if is_valid_number(per_trailing):
                    implied_growth = float(per_trailing) / peg_val
                    peg_calculation = f"P/E: {float(per_trailing):.2f} ÷ Growth (5Y Est.): {implied_growth:.1f}% = PEG: {peg_val:.2f} (Yahoo Finance)"
                    growth_rate_used = implied_growth
                    per_used = float(per_trailing)
                else:
                    peg_calculation = f"PEG: {peg_val:.2f} (Yahoo Finance - trailingPegRatio)"
        
        # MÉTODO 2: Calcular con Forward EPS Growth si no hay trailingPegRatio
        if peg_final is None and is_valid_number(per_trailing) and is_valid_number(eps_trailing) and is_valid_number(eps_forward):
            pe = float(per_trailing)
            eps_t = float(eps_trailing)
            eps_f = float(eps_forward)
            
            if eps_t > 0 and eps_f > eps_t:
                # Growth de 1 año
                growth_1y = ((eps_f - eps_t) / eps_t) * 100
                # Estimar growth anualizado a 5 años (más conservador)
                # Asumimos que el growth disminuye gradualmente
                growth_5y_est = growth_1y * 0.6  # Factor de ajuste conservador
                
                if growth_5y_est > 0:
                    peg_final = pe / growth_5y_est
                    peg_calculation = f"P/E: {pe:.2f} ÷ Growth Est. (5Y): {growth_5y_est:.1f}% = PEG: {peg_final:.2f} (Calculado)"
                    growth_rate_used = growth_5y_est
                    per_used = pe
        
        # MÉTODO 3: Intentar obtener growth de analyst estimates
        if peg_final is None:
            try:
                growth_estimates = ticker.growth_estimates
                if growth_estimates is not None and not growth_estimates.empty:
                    # Buscar el crecimiento del próximo año (+1y) en stockTrend
                    if '+1y' in growth_estimates.index and 'stockTrend' in growth_estimates.columns:
                        growth_1y = growth_estimates.loc['+1y', 'stockTrend']
                        if pd.notna(growth_1y) and is_valid_number(per_trailing):
                            growth_pct = float(growth_1y) * 100
                            if growth_pct > 0:
                                pe = float(per_trailing)
                                peg_final = pe / growth_pct
                                peg_calculation = f"P/E: {pe:.2f} ÷ Growth Analyst (+1Y): {growth_pct:.1f}% = PEG: {peg_final:.2f}"
                                growth_rate_used = growth_pct
                                per_used = pe
            except:
                pass
        
        # Si aún no tenemos PEG, indicar por qué
        if peg_final is None:
            if is_valid_number(per_trailing):
                peg_calculation = f"P/E: {float(per_trailing):.2f} ÷ Growth Rate: N/A = No calculable"
                per_used = float(per_trailing)
            else:
                peg_calculation = "P/E y/o Growth Rate no disponibles"
        
        # Guardar resultados
        data["peg_ratio"] = peg_final
        data["peg_calculation"] = peg_calculation
        data["growth_rate_used"] = growth_rate_used
        data["per_used"] = per_used
        
        # Obtener historial de precios (5 años para tener datos completos)
        try:
            hist = ticker.history(period="5y")
            # Limpiar el índice para evitar "Unnamed" en el gráfico
            if not hist.empty:
                hist.index.name = None
                # Asegurar que el índice sea datetime
                hist.index = pd.to_datetime(hist.index)
            data["historico"] = hist
        except Exception:
            data["historico"] = pd.DataFrame()
        
        # Obtener noticias recientes (Scuttlebutt de Lynch)
        try:
            news = ticker.news
            if news and len(news) > 0:
                data["noticias"] = news[:5]  # Últimas 5 noticias
            else:
                data["noticias"] = []
        except Exception:
            data["noticias"] = []
        
        # =====================================================================
        # CALCULAR RATIO EFECTIVO/DEUDA - MÉTODO MEJORADO
        # =====================================================================
        # Usamos datos del balance sheet trimestral para mayor precisión
        # El ratio Efectivo/Deuda indica cuántas veces puede pagar su deuda
        # con el efectivo disponible. Un ratio > 1 significa posición neta positiva.
        
        try:
            balance_sheet = ticker.quarterly_balance_sheet
            if not balance_sheet.empty:
                latest_bs = balance_sheet.iloc[:, 0]  # Columna más reciente
                
                # Obtener deuda total del balance (más preciso)
                deuda_total_bs = None
                for field in ['Total Debt', 'TotalDebt']:
                    if field in latest_bs.index and pd.notna(latest_bs.get(field)):
                        deuda_total_bs = float(latest_bs[field])
                        break
                
                # Obtener efectivo + inversiones a corto plazo (liquidez total)
                efectivo_inversiones = None
                for field in ['Cash Cash Equivalents And Short Term Investments', 
                              'CashCashEquivalentsAndShortTermInvestments',
                              'Cash And Cash Equivalents',
                              'CashAndCashEquivalents']:
                    if field in latest_bs.index and pd.notna(latest_bs.get(field)):
                        efectivo_inversiones = float(latest_bs[field])
                        break
                
                # Obtener Net Debt (ya calculado por yfinance si está disponible)
                net_debt = None
                for field in ['Net Debt', 'NetDebt']:
                    if field in latest_bs.index and pd.notna(latest_bs.get(field)):
                        net_debt = float(latest_bs[field])
                        break
                
                # Guardar datos del balance
                data["deuda_total_balance"] = deuda_total_bs
                data["efectivo_inversiones_balance"] = efectivo_inversiones
                data["net_debt"] = net_debt
                data["balance_date"] = str(balance_sheet.columns[0].date()) if hasattr(balance_sheet.columns[0], 'date') else str(balance_sheet.columns[0])
            else:
                data["deuda_total_balance"] = None
                data["efectivo_inversiones_balance"] = None
                data["net_debt"] = None
                data["balance_date"] = None
        except Exception:
            data["deuda_total_balance"] = None
            data["efectivo_inversiones_balance"] = None
            data["net_debt"] = None
            data["balance_date"] = None
        
        # Determinar mejores valores para deuda y efectivo
        # Prioridad: Balance Sheet > Info
        data["deuda_total"] = data.get("deuda_total_balance") or data.get("deuda_total_info") or None
        data["efectivo_total"] = data.get("efectivo_inversiones_balance") or data.get("efectivo_total_info") or None
        
        return data
        
    except Exception as e:
        st.error(f"Error al obtener datos: {str(e)}")
        return None


def get_insider_data(ticker_symbol):
    """
    Obtiene datos de insiders e institucionales de una acción.
    
    Args:
        ticker_symbol: Símbolo del ticker (ej: AAPL, KO)
        
    Returns:
        Diccionario con datos de insiders, institucionales y transacciones
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        insider_data = {
            "major_holders": None,
            "institutional_holders": None,
            "insider_transactions": None,
            "ownership_info": None,  # Datos precisos del ticker.info
        }
        
        # Obtener datos precisos de propiedad desde ticker.info
        try:
            info = ticker.info
            ownership_info = {}
            
            # Shares Outstanding (total de acciones) - Dato base fiable
            shares_outstanding = None
            if 'sharesOutstanding' in info and info['sharesOutstanding'] is not None:
                shares_outstanding = info['sharesOutstanding']
                ownership_info['shares_outstanding'] = shares_outstanding
            
            # Float Shares (acciones disponibles para negociar)
            float_shares = None
            if 'floatShares' in info and info['floatShares'] is not None:
                float_shares = info['floatShares']
                ownership_info['float_shares'] = float_shares
            
            # MÉTODO MEJORADO: Calcular participación de insiders
            # Fórmula: (Shares Outstanding - Float Shares) / Shares Outstanding
            # Esto da las acciones NO disponibles para el público (restricted/insider shares)
            insiders_pct_calculated = None
            if shares_outstanding and float_shares and shares_outstanding > 0:
                restricted_shares = shares_outstanding - float_shares
                if restricted_shares >= 0:
                    insiders_pct_calculated = restricted_shares / shares_outstanding
                    ownership_info['insiders_percent_calculated'] = insiders_pct_calculated
            
            # Obtener también el valor de Yahoo para comparar
            if 'heldPercentInsiders' in info and info['heldPercentInsiders'] is not None:
                ownership_info['insiders_percent_yahoo'] = info['heldPercentInsiders']
            
            # Usar el valor calculado como principal (más fiable), con fallback a Yahoo
            if insiders_pct_calculated is not None:
                ownership_info['insiders_percent'] = insiders_pct_calculated
                ownership_info['insiders_method'] = 'calculated'
            elif 'insiders_percent_yahoo' in ownership_info:
                ownership_info['insiders_percent'] = ownership_info['insiders_percent_yahoo']
                ownership_info['insiders_method'] = 'yahoo'
            
            # Participación Institucional (%) - este dato suele ser más fiable
            if 'heldPercentInstitutions' in info and info['heldPercentInstitutions'] is not None:
                ownership_info['institutions_percent'] = info['heldPercentInstitutions']
            
            # Implied Shares Outstanding (puede ser diferente por dilución)
            if 'impliedSharesOutstanding' in info and info['impliedSharesOutstanding'] is not None:
                ownership_info['implied_shares'] = info['impliedSharesOutstanding']
            
            # Short Interest
            if 'sharesShort' in info and info['sharesShort'] is not None:
                ownership_info['shares_short'] = info['sharesShort']
            
            if 'shortRatio' in info and info['shortRatio'] is not None:
                ownership_info['short_ratio'] = info['shortRatio']
            
            if 'shortPercentOfFloat' in info and info['shortPercentOfFloat'] is not None:
                ownership_info['short_percent_float'] = info['shortPercentOfFloat']
            
            if 'sharesShortPriorMonth' in info and info['sharesShortPriorMonth'] is not None:
                ownership_info['shares_short_prior'] = info['sharesShortPriorMonth']
            
            if 'dateShortInterest' in info and info['dateShortInterest'] is not None:
                ownership_info['short_interest_date'] = info['dateShortInterest']
            
            if ownership_info:
                insider_data["ownership_info"] = ownership_info
                
        except:
            pass
        
        # Obtener Major Holders como respaldo
        try:
            major = ticker.major_holders
            if major is not None and not major.empty:
                insider_data["major_holders"] = major
        except:
            pass
        
        # Obtener Institutional Holders (fondos, ETFs, etc.)
        try:
            institutional = ticker.institutional_holders
            if institutional is not None and not institutional.empty:
                insider_data["institutional_holders"] = institutional
        except:
            pass
        
        # Obtener transacciones de insiders
        try:
            insider_trans = ticker.insider_transactions
            if insider_trans is not None and not insider_trans.empty:
                insider_data["insider_transactions"] = insider_trans
        except:
            pass
        
        return insider_data
        
    except Exception as e:
        return None


def get_peter_lynch_chart_data(ticker_symbol):
    """
    Genera los datos para el Gráfico de Valoración Dinámica de Peter Lynch.
    
    Características:
    - Interpolación lineal suave (sin efecto escalera)
    - Proyección a 1 año usando Forward EPS
    - Línea de Valor Conservador (PEG=1) como referencia de suelo
    - Técnicas vectorizadas (sin bucles for, sin sumar enteros a fechas)
    
    Args:
        ticker_symbol: Símbolo del ticker (ej: AAPL, MSFT)
        
    Returns:
        Diccionario con datos para el gráfico
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        result = {
            "price_history": None,
            "fair_value_line": None,
            "conservative_value_line": None,  # Nueva línea PEG=1
            "fair_multiplier": 15,
            "conservative_multiplier": 15,  # Basado en growth rate
            "growth_rate": None,
            "has_data": False,
            "method": None,
            "error": None,
            "has_projection": False,
            "forward_eps": None,
            "trailing_eps": None
        }
        
        # =====================================================================
        # PASO 1: Extraer historial de precios (5 años)
        # =====================================================================
        try:
            price_hist = ticker.history(period="5y")
            if price_hist.empty:
                result["error"] = "No price history available"
                return result
            
            # Limpiar índice de timezone
            price_hist.index = pd.to_datetime(price_hist.index)
            if price_hist.index.tz is not None:
                price_hist.index = price_hist.index.tz_localize(None)
            
            prices_df = price_hist[['Close']].copy().dropna()
            
            if len(prices_df) < 50:
                result["error"] = "Insufficient price data"
                return result
                
        except Exception as e:
            result["error"] = f"Error fetching prices: {str(e)}"
            return result
        
        # =====================================================================
        # PASO 2: Extraer datos de EPS históricos
        # =====================================================================
        eps_points = {}  # {fecha: eps_value}
        method_used = None
        
        # Intentar obtener EPS de múltiples fuentes
        for source_name, source_func in [
            ("financials", lambda: ticker.financials),
            ("income_stmt", lambda: ticker.income_stmt),
        ]:
            if eps_points:
                break
            try:
                data_source = source_func()
                if data_source is not None and not data_source.empty:
                    for field in ['Basic EPS', 'Diluted EPS', 'BasicEPS', 'DilutedEPS']:
                        if field in data_source.index:
                            eps_row = data_source.loc[field].dropna()
                            for date, value in eps_row.items():
                                if pd.notna(value) and value > 0:
                                    clean_date = pd.to_datetime(date)
                                    if hasattr(clean_date, 'tz') and clean_date.tz is not None:
                                        clean_date = clean_date.tz_localize(None)
                                    eps_points[clean_date] = float(value)
                            if eps_points:
                                method_used = source_name
                                break
            except:
                pass
        
        # Fallback: usar EPS actual
        if len(eps_points) < 2:
            try:
                info = ticker.info
                trailing_eps = info.get('trailingEps')
                if trailing_eps and trailing_eps > 0:
                    # Asignar a la fecha más reciente del historial
                    eps_points[prices_df.index[-1]] = float(trailing_eps)
                    # Y a una fecha anterior para tener al menos 2 puntos
                    eps_points[prices_df.index[0]] = float(trailing_eps)
                    method_used = "current_eps_only"
            except:
                pass
        
        if len(eps_points) < 2:
            result["error"] = "No EPS data available"
            return result
        
        # =====================================================================
        # PASO 3: Obtener Forward EPS y Trailing EPS para proyección y growth
        # =====================================================================
        forward_eps = None
        trailing_eps = None
        growth_rate = None
        
        try:
            info = ticker.info
            forward_eps = info.get('forwardEps')
            trailing_eps = info.get('trailingEps')
            
            if forward_eps and forward_eps > 0:
                result["forward_eps"] = forward_eps
            if trailing_eps and trailing_eps > 0:
                result["trailing_eps"] = trailing_eps
            
            # Calcular tasa de crecimiento esperada
            if forward_eps and trailing_eps and trailing_eps > 0:
                growth_rate = (forward_eps - trailing_eps) / trailing_eps
                result["growth_rate"] = growth_rate
        except:
            pass
        
        # =====================================================================
        # PASO 4: Crear rango de fechas extendido (histórico + 1 año futuro)
        # =====================================================================
        last_price_date = prices_df.index.max()
        first_price_date = prices_df.index.min()
        
        # IMPORTANTE: Usar pd.date_range para fechas futuras (NUNCA sumar enteros)
        future_dates = pd.date_range(
            start=last_price_date,
            periods=365,  # ~1 año (más realista)
            freq='D'
        )
        
        # Crear índice completo: histórico + futuro
        full_date_range = pd.date_range(
            start=first_price_date,
            end=future_dates[-1],
            freq='D'
        )
        
        # =====================================================================
        # PASO 5: Construir Serie de EPS con puntos conocidos + proyección
        # =====================================================================
        # Crear DataFrame vacío con todas las fechas
        eps_df = pd.DataFrame(index=full_date_range, columns=['EPS'])
        eps_df['EPS'] = np.nan
        
        # Asignar valores de EPS históricos a sus fechas
        for date, eps_value in eps_points.items():
            # Encontrar la fecha más cercana en el índice
            if date in eps_df.index:
                eps_df.loc[date, 'EPS'] = eps_value
            else:
                # Buscar fecha más cercana
                nearest_idx = eps_df.index.get_indexer([date], method='nearest')[0]
                eps_df.iloc[nearest_idx, 0] = eps_value
        
        # Añadir Forward EPS al final del período futuro (1 año)
        if forward_eps and forward_eps > 0:
            # Asignar forward EPS al final del período de proyección
            future_eps_date = future_dates[-1]  # Final del año de proyección
            eps_df.loc[future_eps_date, 'EPS'] = forward_eps
            result["has_projection"] = True
        
        # =====================================================================
        # PASO 6: INTERPOLACIÓN SUAVE (método 'time' para series temporales)
        # =====================================================================
        # Primero, interpolar linealmente entre puntos conocidos
        eps_df['EPS'] = eps_df['EPS'].interpolate(method='time')
        
        # Rellenar extremos si quedan NaN
        eps_df['EPS'] = eps_df['EPS'].ffill().bfill()
        
        # Filtrar solo valores positivos
        eps_df = eps_df[eps_df['EPS'] > 0]
        
        if eps_df.empty:
            result["error"] = "No valid EPS after interpolation"
            return result
        
        # =====================================================================
        # PASO 7: Calcular Fair PE Multiplier (mediana histórica)
        # =====================================================================
        # Solo usar el período histórico para calcular el multiplicador
        historical_mask = eps_df.index <= last_price_date
        
        # Combinar precios con EPS interpolado (solo histórico)
        historical_df = eps_df[historical_mask].copy()
        historical_df = historical_df.join(prices_df, how='inner')
        
        fair_multiplier = 15  # Default
        
        if len(historical_df) > 20:
            try:
                historical_df['PE'] = historical_df['Close'] / historical_df['EPS']
                valid_pe = historical_df['PE'].replace([np.inf, -np.inf], np.nan).dropna()
                valid_pe = valid_pe[(valid_pe > 0) & (valid_pe < 200)]
                
                if len(valid_pe) > 20:
                    fair_multiplier = valid_pe.median()
                    # Límites de seguridad
                    fair_multiplier = max(5, min(60, fair_multiplier))
            except:
                pass
        
        result["fair_multiplier"] = round(fair_multiplier, 1)
        
        # =====================================================================
        # PASO 8: Calcular Fair Value Line (suavizada)
        # =====================================================================
        eps_df['Fair_Value'] = eps_df['EPS'] * result["fair_multiplier"]
        
        # =====================================================================
        # PASO 9: Calcular Conservative Value Line (PEG=1)
        # =====================================================================
        # El multiplicador conservador se basa en la tasa de crecimiento
        # Si crece al 15% anual, PER justo sería 15 (PEG=1)
        conservative_multiplier = 15  # Default para empresas estables
        
        if growth_rate is not None and growth_rate > 0:
            # Convertir tasa de crecimiento a multiplicador (ej: 0.15 -> 15)
            conservative_multiplier = growth_rate * 100
        
        # Aplicar suelo y techo para evitar extremos
        conservative_multiplier = max(15, min(25, conservative_multiplier))
        result["conservative_multiplier"] = round(conservative_multiplier, 1)
        
        # Calcular línea de valor conservador
        eps_df['Conservative_Value'] = eps_df['EPS'] * conservative_multiplier
        
        # Separar histórico y proyección
        result["fair_value_line"] = eps_df[['Fair_Value']].copy()
        result["conservative_value_line"] = eps_df[['Conservative_Value']].copy()
        result["price_history"] = prices_df.copy()
        result["projection_start"] = last_price_date
        result["has_data"] = True
        result["method"] = method_used
        
        return result
        
    except Exception as e:
        return {
            "has_data": False,
            "error": f"Unexpected error: {str(e)}"
        }


def build_analysis_prompt(data, ticker):
    """
    Construye el prompt dinámico para enviar a Gemini con todos los datos financieros.
    
    Args:
        data: Diccionario con datos financieros
        ticker: Símbolo del ticker
        
    Returns:
        String con el prompt completo
    """
    
    lang = st.session_state.get('language', 'es')
    is_en = lang == 'en'
    
    # Formatear dividend yield
    div_yield = data.get('dividend_yield')
    if div_yield and div_yield != "N/A":
        div_yield_str = f"{float(div_yield) * 100:.2f}%"
    else:
        div_yield_str = "N/A"
    
    # Formatear márgenes y ROE
    roe = data.get('roe')
    if roe and roe != "N/A":
        roe_str = f"{float(roe) * 100:.2f}%"
    else:
        roe_str = "N/A"
    
    margen = data.get('margen_beneficio')
    if margen and margen != "N/A":
        margen_str = f"{float(margen) * 100:.2f}%"
    else:
        margen_str = "N/A"
    
    # Calcular ratio efectivo/deuda (capacidad de pago)
    deuda = data.get('deuda_total')
    efectivo = data.get('efectivo_total')
    net_debt = data.get('net_debt')
    
    if deuda and efectivo and float(deuda) > 0:
        ratio_efectivo_deuda = float(efectivo) / float(deuda)
        if ratio_efectivo_deuda >= 1:
            if is_en:
                situacion_deuda = f"More cash than debt ✅ (can pay {ratio_efectivo_deuda:.1f}x its debt)"
            else:
                situacion_deuda = f"Más efectivo que deuda ✅ (puede pagar {ratio_efectivo_deuda:.1f}x su deuda)"
        else:
            if is_en:
                situacion_deuda = f"More debt than cash ⚠️ (covers {ratio_efectivo_deuda*100:.0f}% of debt)"
            else:
                situacion_deuda = f"Más deuda que efectivo ⚠️ (cubre {ratio_efectivo_deuda*100:.0f}% de la deuda)"
        ratio_str = f"{ratio_efectivo_deuda:.2f}x"
    elif efectivo and (not deuda or float(deuda) == 0):
        ratio_str = "No debt" if is_en else "Sin deuda"
        situacion_deuda = "No debt - Excellent position ✅" if is_en else "Sin deuda - Excelente posición ✅"
        ratio_efectivo_deuda = float('inf')
    else:
        ratio_str = "N/A"
        ratio_efectivo_deuda = None
        situacion_deuda = "Cannot be determined" if is_en else "No se puede determinar"
    
    # Construir sección de noticias
    noticias_text = ""
    if data.get('noticias'):
        noticias_text = "\n📰 " + ("LATEST NEWS (Scuttlebutt):" if is_en else "ÚLTIMAS NOTICIAS (Scuttlebutt):") + "\n"
        for i, noticia in enumerate(data['noticias'][:3], 1):
            titulo = noticia.get('title', 'No title' if is_en else 'Sin título')
            noticias_text += f"   {i}. {titulo}\n"
    else:
        noticias_text = "\n📰 " + ("NEWS: No recent news available." if is_en else "NOTICIAS: No hay noticias recientes disponibles.") + "\n"
    
    # Textos según idioma
    if is_en:
        prompt = f"""
================================================================================
🎯 INVESTMENT ANALYSIS: {ticker} - {data.get('nombre', 'N/A')}
================================================================================

📊 GENERAL INFORMATION:
   • Sector: {data.get('sector', 'N/A')}
   • Industry: {data.get('industria', 'N/A')}
   • Country: {data.get('pais', 'N/A')}
   • Market Cap: {format_large_number(data.get('market_cap'))}
   • Number of Employees: {data.get('num_empleados', 'N/A')}

💰 PRICES:
   • Current Price: {data.get('moneda', '$')}{data.get('precio_actual', 'N/A')}
   • Analyst Target Price: {data.get('moneda', '$')}{data.get('precio_objetivo', 'N/A')}
   • 52-Week High: {data.get('moneda', '$')}{data.get('precio_52w_high', 'N/A')}
   • 52-Week Low: {data.get('moneda', '$')}{data.get('precio_52w_low', 'N/A')}

📈 VALUATION RATIOS (KEY FOR LYNCH):
   • Trailing P/E (last 12 months): {data.get('per_trailing', 'N/A')}
   • Forward P/E (estimated): {data.get('per_forward', 'N/A')}
   • ⭐ PEG Ratio (MOST IMPORTANT): {data.get('peg_ratio', 'N/A')}
   • Price/Book: {data.get('price_to_book', 'N/A')}
   • Price/Sales: {data.get('price_to_sales', 'N/A')}

💵 DIVIDENDS:
   • Dividend Yield: {div_yield_str}
   • Dividend per Share: {data.get('moneda', '$')}{data.get('dividend_rate', 'N/A')}
   • Payout Ratio: {data.get('payout_ratio', 'N/A')}

🏦 BALANCE SHEET & DEBT (Most recent Balance Sheet data):
   • Total Debt: {format_large_number(data.get('deuda_total'))}
   • Cash + Short-term Investments: {format_large_number(data.get('efectivo_total'))}
   • Cash/Debt Ratio: {ratio_str}
   • Debt/Equity Ratio: {data.get('deuda_equity', 'N/A')}
   • ⚡ Financial Position: {situacion_deuda}

📊 PROFITABILITY:
   • ROE (Return on Equity): {roe_str}
   • Profit Margin: {margen_str}
   • Earnings Growth: {data.get('crecimiento_beneficios', 'N/A')}
   • Revenue Growth: {data.get('crecimiento_ingresos', 'N/A')}

📉 VOLATILITY:
   • Beta: {data.get('beta', 'N/A')}

{noticias_text}

================================================================================
Please execute Peter Lynch's "Two-Minute Drill":
1. Classify this company (Cyclical, Turnaround, Asset Play, Fast Grower, Stalwart)
2. Analyze the PEG ratio and determine if it's cheap or expensive
3. Evaluate the debt situation
4. Give your VERDICT: BUY, SELL or HOLD
5. Explain with simple analogies that anyone can understand
================================================================================
"""
    else:
        prompt = f"""
================================================================================
🎯 ANÁLISIS DE INVERSIÓN: {ticker} - {data.get('nombre', 'N/A')}
================================================================================

📊 INFORMACIÓN GENERAL:
   • Sector: {data.get('sector', 'N/A')}
   • Industria: {data.get('industria', 'N/A')}
   • País: {data.get('pais', 'N/A')}
   • Capitalización de Mercado: {format_large_number(data.get('market_cap'))}
   • Número de Empleados: {data.get('num_empleados', 'N/A')}

💰 PRECIOS:
   • Precio Actual: {data.get('moneda', '$')}{data.get('precio_actual', 'N/A')}
   • Precio Objetivo Analistas: {data.get('moneda', '$')}{data.get('precio_objetivo', 'N/A')}
   • Máximo 52 semanas: {data.get('moneda', '$')}{data.get('precio_52w_high', 'N/A')}
   • Mínimo 52 semanas: {data.get('moneda', '$')}{data.get('precio_52w_low', 'N/A')}

📈 RATIOS DE VALORACIÓN (CLAVE PARA LYNCH):
   • PER Trailing (últimos 12 meses): {data.get('per_trailing', 'N/A')}
   • PER Forward (estimado): {data.get('per_forward', 'N/A')}
   • ⭐ PEG Ratio (EL MÁS IMPORTANTE): {data.get('peg_ratio', 'N/A')}
   • Price/Book: {data.get('price_to_book', 'N/A')}
   • Price/Sales: {data.get('price_to_sales', 'N/A')}

💵 DIVIDENDOS:
   • Dividend Yield: {div_yield_str}
   • Dividendo por acción: {data.get('moneda', '$')}{data.get('dividend_rate', 'N/A')}
   • Payout Ratio: {data.get('payout_ratio', 'N/A')}

🏦 BALANCE Y DEUDA (Datos del Balance Sheet más reciente):
   • Deuda Total: {format_large_number(data.get('deuda_total'))}
   • Efectivo + Inversiones C/P: {format_large_number(data.get('efectivo_total'))}
   • Ratio Efectivo/Deuda: {ratio_str}
   • Ratio Deuda/Equity: {data.get('deuda_equity', 'N/A')}
   • ⚡ Situación Financiera: {situacion_deuda}

📊 RENTABILIDAD:
   • ROE (Return on Equity): {roe_str}
   • Margen de Beneficio: {margen_str}
   • Crecimiento Beneficios: {data.get('crecimiento_beneficios', 'N/A')}
   • Crecimiento Ingresos: {data.get('crecimiento_ingresos', 'N/A')}

📉 VOLATILIDAD:
   • Beta: {data.get('beta', 'N/A')}

{noticias_text}

================================================================================
Por favor, ejecuta "La rutina de los dos minutos" de Peter Lynch:
1. Clasifica esta empresa (Cíclica, Recuperación, Activo Oculto, Crecimiento Rápido, Estable)
2. Analiza el PEG ratio y determina si está barata o cara
3. Evalúa la situación de deuda
4. Da tu VEREDICTO: COMPRAR, VENDER o MANTENER
5. Explica con analogías sencillas que cualquiera pueda entender
================================================================================
"""
    
    return prompt


def get_ai_analysis(prompt, api_key):
    """
    Envía el prompt a la API de Groq y obtiene el análisis.
    
    Args:
        prompt: Prompt con los datos financieros
        api_key: API Key de Groq
        
    Returns:
        String con el análisis generado o mensaje de error
    """
    try:
        # Crear cliente de Groq
        client = Groq(api_key=api_key)
        
        # Generar respuesta usando Llama 3.3 70B (gratuito y muy potente)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": get_system_instruction()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=2048,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error al conectar con Groq: {str(e)}"


def create_google_finance_chart(historico, ticker, nombre, periodo_label="1A"):
    """
    Crea un gráfico estilo retrofuturista con hover de línea vertical.
    """
    if historico.empty:
        return None
    
    df = historico.copy()
    
    # Limpiar índice
    df.index = pd.to_datetime(df.index)
    df.index.name = None
    df = df.reset_index(drop=False)
    new_cols = ['Fecha' if i == 0 else str(col) for i, col in enumerate(df.columns)]
    df.columns = new_cols
    
    # Calcular cambios
    precio_inicial = float(df['Close'].iloc[0])
    precio_actual = float(df['Close'].iloc[-1])
    cambio = precio_actual - precio_inicial
    
    # Calcular rango del eje Y con margen
    precio_min = float(df['Close'].min())
    precio_max = float(df['Close'].max())
    rango = precio_max - precio_min
    margen = rango * 0.15 if rango > 0 else precio_min * 0.05
    y_min = precio_min - margen
    y_max = precio_max + margen
    
    # Colores retrofuturistas
    if cambio >= 0:
        line_color = '#00FF9F'
        fill_color = 'rgba(0, 255, 159, 0.08)'
        glow_color = 'rgba(0, 255, 159, 0.4)'
    else:
        line_color = '#FF006E'
        fill_color = 'rgba(255, 0, 110, 0.08)'
        glow_color = 'rgba(255, 0, 110, 0.4)'
    
    # Crear figura
    fig = go.Figure()
    
    # Efecto glow detrás de la línea principal
    fig.add_trace(go.Scatter(
        x=df['Fecha'].tolist(),
        y=df['Close'].tolist(),
        mode='lines',
        line=dict(color=glow_color, width=8),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Línea principal
    fig.add_trace(go.Scatter(
        x=df['Fecha'].tolist(),
        y=df['Close'].tolist(),
        mode='lines',
        name=ticker,
        line=dict(color=line_color, width=2),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate='<b>%{x|%d %b %Y}</b><br>$%{y:,.2f}<extra></extra>'
    ))
    
    # Layout retrofuturista con spikelines para línea vertical
    fig.update_layout(
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(10, 10, 15, 0.8)',
        height=380,
        margin=dict(l=10, r=60, t=10, b=40),
        hovermode='x',
        
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            showline=False,
            zeroline=False,
            tickformat='%b %Y' if len(df) > 60 else '%d %b',
            tickfont=dict(size=10, color='#555', family='monospace'),
            showspikes=True,
            spikecolor=line_color,
            spikethickness=1,
            spikedash='solid',
            spikemode='across',
            spikesnap='cursor',
        ),
        
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.03)',
            showline=False,
            zeroline=False,
            side='right',
            tickformat='$,.0f',
            tickfont=dict(size=10, color='#555', family='monospace'),
            range=[y_min, y_max],
            fixedrange=True,
        ),
        
        hoverlabel=dict(
            bgcolor='rgba(15, 15, 25, 0.95)',
            bordercolor=line_color,
            font=dict(color='#fff', family='monospace', size=12)
        ),
    )
    
    # Línea de referencia del precio inicial
    fig.add_hline(
        y=precio_inicial,
        line_dash="dot",
        line_color="rgba(255, 255, 255, 0.15)",
        line_width=1,
    )
    
    return fig


def display_google_finance_header(data, historico, periodo_dias):
    """
    Muestra el header estilo Google Finance con precio y cambio destacado.
    
    Args:
        data: Datos de la empresa
        historico: DataFrame con el historial filtrado
        periodo_dias: Número de días del período
    """
    if historico.empty:
        return
    
    precio_actual = historico['Close'].iloc[-1]
    precio_inicial = historico['Close'].iloc[0]
    cambio = precio_actual - precio_inicial
    cambio_pct = (cambio / precio_inicial) * 100
    
    # Determinar período para el texto
    if periodo_dias == 1:
        periodo_text = "hoy"
    elif periodo_dias <= 5:
        periodo_text = "esta semana"
    elif periodo_dias <= 30:
        periodo_text = "este mes"
    elif periodo_dias <= 90:
        periodo_text = "últimos 3 meses"
    elif periodo_dias <= 180:
        periodo_text = "últimos 6 meses"
    elif periodo_dias <= 365:
        periodo_text = "último año"
    elif periodo_dias <= 1300:
        periodo_text = "últimos 5 años"
    else:
        periodo_text = "máx. histórico"
    
    # Color y símbolo - estilo retrofuturista
    if cambio >= 0:
        color = "#00FF9F"  # Cyan neón
        arrow = "▲"
        signo = "+"
        glow = "0 0 10px rgba(0, 255, 159, 0.5)"
    else:
        color = "#FF006E"  # Magenta neón
        arrow = "▼"
        signo = ""
        glow = "0 0 10px rgba(255, 0, 110, 0.5)"
    
    # Header con precio grande - estilo retrofuturista minimalista
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown(f'''
        <div style='padding: 10px 0;'>
            <div style='font-size: 2.8rem; font-weight: 300; color: #fff; line-height: 1; 
                        font-family: "SF Mono", "Monaco", monospace; letter-spacing: -1px;'>
                ${precio_actual:,.2f}
            </div>
            <div style='font-size: 1rem; color: {color}; margin-top: 8px; font-family: monospace;
                        text-shadow: {glow};'>
                {arrow} {signo}${abs(cambio):,.2f} ({signo}{cambio_pct:.2f}%) 
                <span style='color: #444; font-size: 0.8rem; margin-left: 5px;'>⏤ {periodo_text}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        # Mini estadísticas con estilo retrofuturista (sin bordes izquierdos)
        max_periodo = historico['High'].max()
        min_periodo = historico['Low'].min()
        vol_promedio = historico['Volume'].mean()
        
        # Obtener info de dividendos
        dividend_rate = data.get('dividend_rate')
        div_yield = data.get('dividend_yield')
        trailing_yield = data.get('trailing_annual_dividend_yield')
        precio_actual_val = data.get('precio_actual', precio_actual)
        
        # Calcular dividend yield si es posible
        div_yield_pct = None
        div_quarterly = None
        if dividend_rate and precio_actual_val:
            try:
                annual_div = float(dividend_rate)
                div_yield_pct = (annual_div / float(precio_actual_val)) * 100
                div_quarterly = annual_div / 4
            except:
                pass
        elif trailing_yield:
            try:
                yield_val = float(trailing_yield)
                div_yield_pct = yield_val * 100 if yield_val < 1 else yield_val
            except:
                pass
        elif div_yield:
            try:
                yield_val = float(div_yield)
                div_yield_pct = yield_val * 100 if yield_val < 1 else yield_val
            except:
                pass
        
        # Validar yield razonable
        if div_yield_pct and (div_yield_pct < 0 or div_yield_pct > 20):
            div_yield_pct = None
        
        # HTML para dividendos si existe - todo en una línea para evitar problemas de renderizado
        div_html = ""
        if div_yield_pct:
            div_html = f'<div style="text-align: center; padding: 8px 12px; background: rgba(0,0,0,0.2); border-radius: 8px;"><div style="color: #555; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 1px;">DIV. YIELD</div><div style="color: #00FF9F; font-size: 1rem; font-weight: 400;">{div_yield_pct:.2f}%</div></div>'
            if div_quarterly:
                div_html += f'<div style="text-align: center; padding: 8px 12px; background: rgba(0,0,0,0.2); border-radius: 8px;"><div style="color: #555; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 1px;">DIV/TRIM</div><div style="color: #888; font-size: 1rem; font-weight: 400;">${div_quarterly:.2f}</div></div>'
        
        stats_html = f'<div style="display: flex; gap: 15px; padding: 12px 0; font-family: monospace; flex-wrap: wrap; align-items: center;"><div style="text-align: center; padding: 8px 12px; background: rgba(0, 255, 159, 0.08); border-radius: 8px;"><div style="color: #555; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 1px;">HIGH</div><div style="color: #00FF9F; font-size: 1rem; font-weight: 400;">${max_periodo:,.2f}</div></div><div style="text-align: center; padding: 8px 12px; background: rgba(255, 0, 110, 0.08); border-radius: 8px;"><div style="color: #555; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 1px;">LOW</div><div style="color: #FF006E; font-size: 1rem; font-weight: 400;">${min_periodo:,.2f}</div></div><div style="text-align: center; padding: 8px 12px; background: rgba(0,0,0,0.2); border-radius: 8px;"><div style="color: #555; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 1px;">VOL AVG</div><div style="color: #888; font-size: 1rem; font-weight: 400;">{vol_promedio/1e6:.1f}M</div></div>{div_html}</div>'
        
        st.markdown(stats_html, unsafe_allow_html=True)


def create_price_chart(historico, ticker, nombre):
    """
    Función de compatibilidad - usa el nuevo estilo retrofuturista.
    """
    return create_google_finance_chart(historico, ticker, nombre)


def display_metrics_panel(data):
    """
    Muestra el panel de métricas principales con estilo retrofuturista mejorado.
    Diseño tipo Google Finance con tarjetas más visuales.
    """
    
    # Función helper para convertir hex a rgba
    def hex_to_rgba(hex_color, alpha):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        return f"rgba(85, 85, 85, {alpha})"
    
    # Función para crear tarjeta de métrica moderna
    def metric_card_modern(label, value, color="#00FF9F", badge_text=None, subtitle=None):
        color_60 = hex_to_rgba(color, 0.6)
        color_30 = hex_to_rgba(color, 0.3)
        color_12 = hex_to_rgba(color, 0.12)
        
        # Construir HTML del badge si existe
        badge_section = ""
        if badge_text:
            badge_section = f'<div style="display: inline-block; background: {color_12}; border: 1px solid {color}; border-radius: 12px; padding: 2px 12px 6px 12px; margin-top: 8px;"><span style="color: {color}; font-size: 0.65rem; font-weight: 500; text-transform: uppercase;">{badge_text}</span></div>'
        
        # Construir HTML del subtitle si existe
        subtitle_section = ""
        if subtitle:
            subtitle_section = f'<div style="color: #666; font-size: 0.6rem; margin-top: 6px;">{subtitle}</div>'
        
        html = f'<div style="background: linear-gradient(145deg, rgba(20, 20, 35, 0.9) 0%, rgba(15, 15, 25, 0.95) 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 18px 15px; text-align: center; font-family: monospace; position: relative; overflow: hidden;"><div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 40%; height: 2px; background: linear-gradient(90deg, transparent, {color_60}, transparent);"></div><div style="color: #666; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">{label}</div><div style="color: {color}; font-size: 1.5rem; font-weight: 400; text-shadow: 0 0 20px {color_30};">{value}</div>{badge_section}{subtitle_section}</div>'
        
        return html
    
    # Función para calcular dividend yield y frecuencia
    def get_dividend_info(data):
        """Obtiene información precisa de dividendos."""
        precio = data.get('precio_actual', 0)
        dividend_rate = data.get('dividend_rate')  # Dividendo anual por acción
        last_dividend = data.get('last_dividend_value')  # Último dividendo pagado
        div_yield = data.get('dividend_yield')
        trailing_yield = data.get('trailing_annual_dividend_yield')
        
        result = {
            'yield_pct': None,
            'annual_amount': None,
            'quarterly_amount': None,
            'frequency': None
        }
        
        # Intentar obtener el yield más preciso
        def is_valid(val):
            if val is None or val == 'N/A':
                return False
            try:
                v = float(val)
                return not pd.isna(v) and v > 0
            except:
                return False
        
        # Prioridad para yield: trailing_annual > dividend_yield calculado desde rate
        if is_valid(dividend_rate) and is_valid(precio) and float(precio) > 0:
            # Calcular yield desde dividend_rate (más preciso)
            annual_div = float(dividend_rate)
            result['yield_pct'] = (annual_div / float(precio)) * 100
            result['annual_amount'] = annual_div
            result['quarterly_amount'] = annual_div / 4  # Asumimos trimestral por defecto
            result['frequency'] = 'trimestral'
        elif is_valid(trailing_yield):
            yield_val = float(trailing_yield)
            result['yield_pct'] = yield_val * 100 if yield_val < 1 else yield_val
        elif is_valid(div_yield):
            yield_val = float(div_yield)
            result['yield_pct'] = yield_val * 100 if yield_val < 1 else yield_val
        
        # Validar que el yield sea razonable (0-20%)
        if result['yield_pct'] is not None and (result['yield_pct'] < 0 or result['yield_pct'] > 20):
            result['yield_pct'] = None
            
        return result
    
    # Obtener valores
    precio = data.get('precio_actual', 'N/A')
    per = data.get('per_trailing', 'N/A')
    peg = data.get('peg_ratio')
    div_info = get_dividend_info(data)
    
    # Primera fila de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if precio != 'N/A':
            st.markdown(metric_card_modern(get_text('current_price'), f"${precio:.2f}", "#00FF9F"), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern(get_text('current_price'), "—", "#555"), unsafe_allow_html=True)
    
    with col2:
        if per != 'N/A':
            if per > 25:
                color, badge_text = "#FF006E", get_text('expensive')
            elif per < 15:
                color, badge_text = "#00FF9F", get_text('cheap')
            else:
                color, badge_text = "#FFB74D", get_text('normal')
            st.markdown(metric_card_modern(get_text('per_trailing'), f"{per:.2f}", color, badge_text), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern(get_text('per_trailing'), "—", "#555"), unsafe_allow_html=True)
    
    with col3:
        if peg is not None and peg != 'N/A':
            try:
                peg_val = float(peg)
                if peg_val < 1:
                    color, badge_text = "#00FF9F", get_text('cheap')
                elif peg_val > 2:
                    color, badge_text = "#FF006E", get_text('expensive')
                else:
                    color, badge_text = "#FFB74D", get_text('fair')
                st.markdown(metric_card_modern(get_text('peg_ratio'), f"{peg_val:.2f}", color, badge_text), unsafe_allow_html=True)
            except:
                st.markdown(metric_card_modern(get_text('peg_ratio'), "—", "#555"), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern(get_text('peg_ratio'), "—", "#555"), unsafe_allow_html=True)
    
    with col4:
        # Dividendos mejorados con yield y monto
        if div_info['yield_pct'] is not None:
            yield_pct = div_info['yield_pct']
            quarterly = div_info.get('quarterly_amount')
            freq = get_text('quarterly')
            
            if quarterly:
                subtitle = f"${quarterly:.2f} USD / {freq}"
            else:
                subtitle = None
                
            color = "#00FF9F" if yield_pct >= 2 else "#6464FF"
            st.markdown(metric_card_modern(get_text('dividend_yield'), f"{yield_pct:.2f}%", color, None, subtitle), unsafe_allow_html=True)
        else:
            no_div = "Sin dividendos" if st.session_state.get('language', 'es') == 'es' else "No dividends"
            st.markdown(metric_card_modern(get_text('dividend_yield'), "—", "#555", no_div), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
    
    # Segunda fila de métricas
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        pb = data.get('price_to_book', 'N/A')
        if pb != 'N/A':
            if pb < 1.5:
                color, badge_text = "#00FF9F", get_text('undervalued')
            elif pb > 4:
                color, badge_text = "#FF006E", get_text('overvalued')
            else:
                color, badge_text = "#6464FF", None
            st.markdown(metric_card_modern(get_text('price_book'), f"{pb:.2f}x", color, badge_text), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern(get_text('price_book'), "—", "#555"), unsafe_allow_html=True)
    
    with col6:
        mcap = data.get('market_cap', 'N/A')
        badge_text = None
        if mcap != 'N/A':
            try:
                mcap_val = float(mcap)
                if mcap_val >= 200e9:
                    badge_text = get_text('mega_cap')
                elif mcap_val >= 10e9:
                    badge_text = get_text('large_cap')
                elif mcap_val >= 2e9:
                    badge_text = get_text('mid_cap')
                else:
                    badge_text = get_text('small_cap')
            except:
                badge_text = None
        st.markdown(metric_card_modern(get_text('market_cap'), format_large_number(mcap), "#6464FF", badge_text), unsafe_allow_html=True)
    
    with col7:
        # Ratio Efectivo/Deuda (como Google Finance) - indica capacidad de pago
        deuda = data.get('deuda_total')
        efectivo = data.get('efectivo_total')
        net_debt = data.get('net_debt')
        
        if deuda and efectivo and float(deuda) > 0:
            # Calcular ratio Efectivo/Deuda (cuántas veces puede pagar su deuda)
            ratio_efectivo_deuda = float(efectivo) / float(deuda)
            
            # Evaluar solidez financiera
            if ratio_efectivo_deuda >= 1.5:
                color, badge_text = "#00FF9F", get_text('very_solid')
            elif ratio_efectivo_deuda >= 1.0:
                color, badge_text = "#00FF9F", get_text('solid')
            elif ratio_efectivo_deuda >= 0.5:
                color, badge_text = "#FFB74D", get_text('moderate')
            else:
                color, badge_text = "#FF006E", get_text('risk')
            
            st.markdown(metric_card_modern(get_text('cash_debt'), f"{ratio_efectivo_deuda:.2f}x", color, badge_text), unsafe_allow_html=True)
        elif efectivo and (not deuda or float(deuda) == 0):
            st.markdown(metric_card_modern(get_text('cash_debt'), get_text('no_debt'), "#00FF9F", get_text('excellent')), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern(get_text('cash_debt'), "—", "#555"), unsafe_allow_html=True)
    
    with col8:
        beta = data.get('beta', 'N/A')
        if beta != 'N/A':
            if beta < 0.8:
                color, badge_text = "#00FF9F", get_text('low_volatility')
            elif beta > 1.3:
                color, badge_text = "#FF006E", get_text('high_volatility')
            else:
                color, badge_text = "#6464FF", get_text('market')
            st.markdown(metric_card_modern(get_text('beta'), f"{beta:.2f}", color, badge_text), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern(get_text('beta'), "—", "#555"), unsafe_allow_html=True)


# =============================================================================
# INTERFAZ PRINCIPAL DE LA APLICACIÓN
# =============================================================================

def main():
    """Función principal que ejecuta la aplicación Streamlit."""
    
    # Inicializar idioma en session_state si no existe
    if 'language' not in st.session_state:
        st.session_state.language = 'es'
    
    # Header principal retrofuturista (dinámico según idioma)
    st.markdown(f"""
    <div style='text-align: center; padding: 30px 0 20px 0;'>
        <h1 style='font-family: "JetBrains Mono", monospace; font-weight: 200; font-size: 3rem; 
                   color: #00FF9F; text-shadow: 0 0 40px rgba(0, 255, 159, 0.5); letter-spacing: 8px;
                   margin: 0;'>{get_text('app_title')}</h1>
        <p style='font-family: monospace; color: #FF006E; font-size: 0.9rem; letter-spacing: 3px;
                  text-transform: uppercase; margin-top: 10px;'>{get_text('app_subtitle')}</p>
        <p style='font-family: monospace; color: rgba(255,255,255,0.4); font-size: 0.75rem; font-style: italic;
                  margin-top: 5px;'>"{'Compra lo que conoces' if st.session_state.language == 'es' else 'Buy what you know'}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 0 0 20px 0; opacity: 0.3;'>", unsafe_allow_html=True)
    
    # Sidebar para configuración
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px 0; margin-bottom: 20px;'>
            <span style='font-family: monospace; color: #00FF9F; font-size: 0.8rem; letter-spacing: 2px;
                        text-transform: uppercase;'>{get_text('config')}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== SELECTOR DE IDIOMA (BOTÓN QUE ABRE MODAL) ==========
        current_flag = "🇪🇸" if st.session_state.language == 'es' else "🇬🇧"
        current_lang = "ES" if st.session_state.language == 'es' else "EN"
        
        if st.button(f"🌐 {current_lang}", use_container_width=True, key="open_language_modal"):
            language_modal()
        
        st.markdown("<hr style='opacity: 0.2; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # API Key de Groq
        st.markdown(f"""
        <div style='font-family: monospace; color: #FF006E; font-size: 0.75rem; letter-spacing: 1px;
                    text-transform: uppercase; margin-bottom: 10px;'>{get_text('api_key_title')}</div>
        """, unsafe_allow_html=True)
        api_key = st.text_input(
            get_text('api_key_placeholder'),
            type="password",
            help=get_text('api_key_help'),
            label_visibility="collapsed"
        )
        
        if not api_key:
            st.markdown(f"""
            <div style='background: rgba(255, 0, 110, 0.1); border: 1px solid rgba(255, 0, 110, 0.3);
                        border-radius: 8px; padding: 12px; margin: 10px 0; font-family: monospace;'>
                <span style='color: #FF006E; font-size: 0.75rem;'>{get_text('api_key_warning')}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(get_text('api_key_howto'))
        
        st.markdown("<hr style='opacity: 0.2; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Info sobre la metodología
        st.markdown(f"""
        <div style='font-family: monospace; color: #FF006E; font-size: 0.75rem; letter-spacing: 1px;
                    text-transform: uppercase; margin-bottom: 15px;'>{get_text('methodology')}</div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='font-family: monospace; font-size: 0.75rem; line-height: 1.8;'>
            <div style='color: #00FF9F;'>● PEG < 1.0 → <span style='opacity: 0.7;'>{get_text('peg_cheap')}</span></div>
            <div style='color: #FFB74D;'>● PEG 1.0-2.0 → <span style='opacity: 0.7;'>{get_text('peg_fair')}</span></div>
            <div style='color: #FF006E;'>● PEG > 2.0 → <span style='opacity: 0.7;'>{get_text('peg_expensive')}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        # Clasificaciones - se actualizará dinámicamente
        st.markdown(f"""
        <div style='font-family: monospace; color: rgba(255,255,255,0.5); font-size: 0.7rem;
                    text-transform: uppercase; margin-bottom: 10px;'>{get_text('classifications')}</div>
        """, unsafe_allow_html=True)
        
        # Guardar placeholder para actualizar después
        classification_placeholder = st.empty()
        
        st.markdown("<hr style='opacity: 0.2; margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align: center; font-family: monospace; font-size: 0.65rem; color: rgba(255,255,255,0.3);'>
            {get_text('developed_with')} <span style='color: #FF006E;'>♥</span> {get_text('using')}<br>
            Streamlit • yfinance • Groq AI
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar clasificaciones por defecto si no hay análisis activo
    if 'current_classification' not in st.session_state:
        with classification_placeholder.container():
            st.markdown(f"""
            <div class="sidebar-item">{get_text('fast_growth')}</div>
            <div class="sidebar-item">{get_text('stable')}</div>
            <div class="sidebar-item">{get_text('cyclical')}</div>
            <div class="sidebar-item">{get_text('turnaround')}</div>
            <div class="sidebar-item">{get_text('hidden_asset')}</div>
            """, unsafe_allow_html=True)
    
    # Input del ticker con estilo retrofuturista
    st.markdown(f"""
    <div style='font-family: monospace; color: #00FF9F; font-size: 0.8rem; letter-spacing: 1px;
                text-transform: uppercase; margin-bottom: 10px;'>{get_text('search_stock')}</div>
    """, unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([3, 1])
    
    with col_input1:
        ticker_input = st.text_input(
            "Ticker:",
            placeholder=get_text('ticker_placeholder'),
            help=get_text('ticker_help'),
            label_visibility="collapsed"
        )
    
    with col_input2:
        analyze_button = st.button(get_text('analyze'), type="primary", use_container_width=True)
    
    # Ejemplos rápidos
    st.markdown(f"""
    <div style='font-family: monospace; color: rgba(255,255,255,0.4); font-size: 0.7rem; 
                margin: 10px 0 5px 0;'>{get_text('quick_examples')}</div>
    """, unsafe_allow_html=True)
    col_ex1, col_ex2, col_ex3, col_ex4, col_ex5 = st.columns(5)
    
    with col_ex1:
        if st.button("AAPL", use_container_width=True):
            ticker_input = "AAPL"
            analyze_button = True
    with col_ex2:
        if st.button("MSFT", use_container_width=True):
            ticker_input = "MSFT"
            analyze_button = True
    with col_ex3:
        if st.button("KO", use_container_width=True):
            ticker_input = "KO"
            analyze_button = True
    with col_ex4:
        if st.button("TSLA", use_container_width=True):
            ticker_input = "TSLA"
            analyze_button = True
    with col_ex5:
        if st.button("GOOGL", use_container_width=True):
            ticker_input = "GOOGL"
            analyze_button = True
    
    st.markdown("---")
    
    # Proceso de análisis
    if analyze_button and ticker_input:
        ticker = ticker_input.upper().strip()
        
        loading_msg = f"🔄 {get_text('loading_data')} {ticker}..."
        with st.spinner(loading_msg):
            data = get_stock_data(ticker)
        
        if data is None:
            error_msg = f"""
            ❌ **{get_text('invalid_ticker')} '{ticker}'**
            
            {'Por favor verifica que:' if st.session_state.get('language', 'es') == 'es' else 'Please verify that:'}
            - {'El símbolo esté escrito correctamente' if st.session_state.get('language', 'es') == 'es' else 'The symbol is spelled correctly'}
            - {'Para mercados europeos, añade el sufijo correcto (ej: .MC para Madrid, .L para Londres)' if st.session_state.get('language', 'es') == 'es' else 'For European markets, add the correct suffix (e.g., .MC for Madrid, .L for London)'}
            - {'La acción esté listada en una bolsa soportada por Yahoo Finance' if st.session_state.get('language', 'es') == 'es' else 'The stock is listed on an exchange supported by Yahoo Finance'}
            """
            st.error(error_msg)
            if 'stock_data' in st.session_state:
                del st.session_state['stock_data']
            if 'current_ticker' in st.session_state:
                del st.session_state['current_ticker']
        else:
            # Guardar datos en session_state para persistencia
            st.session_state['stock_data'] = data
            st.session_state['current_ticker'] = ticker
    
    # Mostrar análisis si hay datos (ya sea recién cargados o en session_state)
    if 'stock_data' in st.session_state and st.session_state['stock_data'] is not None:
        data = st.session_state['stock_data']
        ticker = st.session_state.get('current_ticker', 'N/A')
        
        # Clasificar la empresa automáticamente
        clasificacion, emoji_class, css_class, explicacion_class = classify_company(data)
        
        # Guardar clasificación en session_state para la sidebar
        st.session_state['current_classification'] = clasificacion
        
        # Actualizar sidebar con la clasificación activa
        with classification_placeholder.container():
            # Clasificaciones traducidas según el idioma
            if st.session_state.get('language', 'es') == 'en':
                classifications = [
                    ("🚀 Fast Grower", "Fast Grower"),
                    ("🏛️ Stalwart", "Stalwart"),
                    ("🔄 Cyclical", "Cyclical"),
                    ("📈 Turnaround", "Turnaround"),
                    ("💎 Asset Play", "Asset Play"),
                ]
            else:
                classifications = [
                    ("🚀 Crecimiento Rápido", "Crecimiento Rápido"),
                    ("🏛️ Estable", "Estable"),
                    ("🔄 Cíclica", "Cíclica"),
                    ("📈 Recuperación", "Recuperación"),
                    ("💎 Activo Oculto", "Activo Oculto"),
                ]
            for label, name in classifications:
                if name == clasificacion:
                    st.markdown(f'<div class="sidebar-item-active">✓ {label}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="sidebar-item">{label}</div>', unsafe_allow_html=True)
        
        # Obtener PEG ya calculado y validado
        peg = data.get('peg_ratio')
        peg_calculation = data.get('peg_calculation', '')
        
        # Crear la barra de información usando componentes nativos de Streamlit
        # Header con nombre y sector
        col_info1, col_info2 = st.columns([3, 1])
        
        with col_info1:
            # Nombre y sector
            empresa_nombre = data.get('nombre', ticker)
            empresa_sector = data.get('sector', 'N/A')
            empresa_industria = data.get('industria', 'N/A')
            
            # Construir texto del PEG
            if peg is not None and peg != 'N/A':
                try:
                    peg_val = float(peg)
                    if peg_val < 1:
                        peg_text = f" | 🟢 PEG: {peg_val:.2f} (Barato)"
                    elif peg_val > 2:
                        peg_text = f" | 🔴 PEG: {peg_val:.2f} (Caro)"
                    else:
                        peg_text = f" | 🟡 PEG: {peg_val:.2f} (Justo)"
                except:
                    peg_text = ""
            else:
                peg_text = ""
            
            st.success(f"✅ **{empresa_nombre}** - {empresa_sector} | {empresa_industria}{peg_text}")
        
        with col_info2:
            # Badge de clasificación
            if css_class == "badge-crecimiento":
                st.info(f"{emoji_class} {clasificacion}")
            elif css_class == "badge-estable":
                st.success(f"{emoji_class} {clasificacion}")
            elif css_class == "badge-ciclica":
                st.warning(f"{emoji_class} {clasificacion}")
            elif css_class == "badge-recuperacion":
                st.error(f"{emoji_class} {clasificacion}")
            else:  # activo oculto
                st.warning(f"{emoji_class} {clasificacion}")
        
        # Explicación de la clasificación
        st.caption(f"💡 {explicacion_class}")
        
        # Panel de métricas con título retrofuturista
        st.markdown(f"""
        <div style='margin: 25px 0 15px 0;'>
            <span style='font-family: monospace; color: #FF006E; font-size: 1rem; letter-spacing: 2px; 
                        text-transform: uppercase; text-shadow: 0 0 15px rgba(255, 0, 110, 0.3);'>
                {get_text('main_metrics')}
            </span>
        </div>
        """, unsafe_allow_html=True)
        display_metrics_panel(data)
        
        st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
        
        # =================================================================
        # GRÁFICO ESTILO GOOGLE FINANCE
        # =================================================================
        if not data.get('historico', pd.DataFrame()).empty:
            st.markdown(f"""
            <div style='margin: 20px 0 15px 0;'>
                <span style='font-family: monospace; color: #00FF9F; font-size: 1rem; letter-spacing: 2px; 
                            text-transform: uppercase; text-shadow: 0 0 15px rgba(0, 255, 159, 0.3);'>
                    {get_text('price_chart')}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Selector de período con estilo retrofuturista
            periodos = {
                "1S": 5,
                "1M": 22,
                "3M": 66,
                "6M": 132,
                "1A": 252,
                "5A": 1260
            }
            
            # Radio buttons horizontales para período
            periodo_seleccionado = st.radio(
                "Período:",
                options=list(periodos.keys()),
                index=4,  # Default: 1A
                horizontal=True,
                key="periodo_chart",
                label_visibility="collapsed"
            )
            
            # Obtener el historial completo
            historico_completo = data['historico']
            dias_periodo = periodos[periodo_seleccionado]
            
            # Filtrar según período
            if dias_periodo == -1:  # MAX
                historico_filtrado = historico_completo
                dias_reales = len(historico_completo)
            else:
                historico_filtrado = historico_completo.tail(dias_periodo)
                dias_reales = min(dias_periodo, len(historico_completo))
            
            # Verificar que hay datos
            if not historico_filtrado.empty and len(historico_filtrado) > 1:
                # Mostrar header con precio y cambio
                display_google_finance_header(data, historico_filtrado, dias_reales)
                
                # Crear el gráfico
                result = create_google_finance_chart(
                    historico_filtrado,
                    ticker,
                    data.get('nombre', ticker),
                    periodo_seleccionado
                )
                
                if result is not None:
                    fig = result
                    
                    # Mostrar gráfico simple con hover
                    st.plotly_chart(
                        fig, 
                        use_container_width=True, 
                        config={
                            'displayModeBar': False,
                            'displaylogo': False
                        }
                    )
                
                # =========================================================
                # PANEL RETROFUTURISTA - MÉTRICAS Y ANÁLISIS
                # =========================================================
                
                # Calcular estadísticas del período
                precio_actual = historico_filtrado['Close'].iloc[-1]
                precio_apertura_periodo = historico_filtrado['Open'].iloc[0]
                precio_max_periodo = historico_filtrado['High'].max()
                precio_min_periodo = historico_filtrado['Low'].min()
                volumen_total = historico_filtrado['Volume'].sum()
                volumen_promedio = historico_filtrado['Volume'].mean()
                
                # Volatilidad (desviación estándar)
                volatilidad = historico_filtrado['Close'].std()
                volatilidad_pct = (volatilidad / precio_actual) * 100
                
                # Calcular posición en el rango (0-100%)
                rango_total = precio_max_periodo - precio_min_periodo
                posicion_rango = ((precio_actual - precio_min_periodo) / rango_total * 100) if rango_total > 0 else 50
                
                # Determinar tendencia
                sma_corto = historico_filtrado['Close'].tail(10).mean()
                sma_largo = historico_filtrado['Close'].tail(30).mean() if len(historico_filtrado) >= 30 else sma_corto
                
                # Traducciones de tendencia
                if sma_corto > sma_largo:
                    tendencia = get_text('bullish')
                    tendencia_color = "#00FF9F"
                elif sma_corto < sma_largo:
                    tendencia = get_text('bearish')
                    tendencia_color = "#FF006E"
                else:
                    tendencia = get_text('sideways')
                    tendencia_color = "#888"
                
                st.markdown("")
                
                # Widget de posición en rango - estilo retrofuturista
                st.markdown(f"""
                <div style='background: rgba(15, 15, 25, 0.9); border: 1px solid rgba(255,255,255,0.1); 
                            border-radius: 8px; padding: 20px; margin: 10px 0; font-family: monospace;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <div>
                            <span style='color: #555; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px;'>
                                {get_text('position_in_range')} {periodo_seleccionado}
                            </span>
                        </div>
                        <div style='display: flex; align-items: center; gap: 15px;'>
                            <span style='color: #FF006E; font-size: 0.75rem;'>LOW ${precio_min_periodo:,.2f}</span>
                            <span style='color: #00FF9F; font-size: 0.75rem;'>HIGH ${precio_max_periodo:,.2f}</span>
                        </div>
                    </div>
                    <div style='position: relative; height: 8px; background: linear-gradient(90deg, #FF006E 0%, #444 50%, #00FF9F 100%); 
                                border-radius: 4px; margin-bottom: 10px;'>
                        <div style='position: absolute; top: -4px; left: {posicion_rango}%; transform: translateX(-50%);
                                    width: 16px; height: 16px; background: #fff; border-radius: 50%; 
                                    box-shadow: 0 0 10px rgba(255,255,255,0.5);'></div>
                    </div>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='color: {tendencia_color}; font-size: 0.8rem;'>
                            ◈ {get_text('trend')}: {tendencia}
                        </div>
                        <div style='color: #888; font-size: 0.8rem;'>
                            {posicion_rango:.0f}% {get_text('of_range')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Métricas en grid compacto
                st.markdown(f"""
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 15px 0; font-family: monospace;'>
                    <div style='background: rgba(0, 255, 159, 0.05); border: 1px solid rgba(0, 255, 159, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>{get_text('maximum')}</div>
                        <div style='color: #00FF9F; font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>${precio_max_periodo:,.2f}</div>
                    </div>
                    <div style='background: rgba(255, 0, 110, 0.05); border: 1px solid rgba(255, 0, 110, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>{get_text('minimum')}</div>
                        <div style='color: #FF006E; font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>${precio_min_periodo:,.2f}</div>
                    </div>
                    <div style='background: rgba(100, 100, 255, 0.05); border: 1px solid rgba(100, 100, 255, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>{get_text('avg_volume')}</div>
                        <div style='color: #6464FF; font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>{volumen_promedio/1e6:.1f}M</div>
                    </div>
                    <div style='background: rgba(255, 183, 77, 0.05); border: 1px solid rgba(255, 183, 77, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>{get_text('volatility')}</div>
                        <div style='color: {"#00FF9F" if volatilidad_pct < 3 else "#FFB74D" if volatilidad_pct < 5 else "#FF006E"}; 
                                    font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>{volatilidad_pct:.1f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Calcular rendimientos
                hist_completo = data['historico'].copy()
                hist_completo = hist_completo.sort_index()
                precio_actual_rend = hist_completo['Close'].iloc[-1]
                
                # Nombres de períodos según idioma
                period_1w = get_text('1w')
                periodos_calc = [(period_1w, 5), ("1M", 22), ("3M", 66), ("6M", 132), ("1A" if st.session_state.get('language', 'es') == 'es' else "1Y", 252), ("YTD", "ytd")]
                rendimientos_items = []
                
                for nombre_p, dias_p in periodos_calc:
                    try:
                        if dias_p == "ytd":
                            inicio_anio = pd.Timestamp(f"{pd.Timestamp.now().year}-01-01")
                            if hist_completo.index.tz:
                                inicio_anio = inicio_anio.tz_localize(hist_completo.index.tz)
                            datos_ytd = hist_completo[hist_completo.index >= inicio_anio]
                            if len(datos_ytd) > 1:
                                precio_inicio = datos_ytd['Close'].iloc[0]
                                valor = ((precio_actual_rend - precio_inicio) / precio_inicio) * 100
                            else:
                                valor = None
                        else:
                            if len(hist_completo) > dias_p:
                                precio_inicio = hist_completo['Close'].iloc[-(dias_p + 1)]
                                valor = ((precio_actual_rend - precio_inicio) / precio_inicio) * 100
                            else:
                                valor = None
                    except:
                        valor = None
                    
                    rendimientos_items.append((nombre_p, valor))
                
                # Renderizar rendimientos históricos en un solo bloque HTML
                rend_divs = ""
                for nombre_p, valor in rendimientos_items:
                    if valor is not None:
                        color = "#00FF9F" if valor >= 0 else "#FF006E"
                        signo = "+" if valor >= 0 else ""
                        rend_divs += f"<div style='text-align: center;'><div style='color: #444; font-size: 0.65rem;'>{nombre_p}</div><div style='color: {color}; font-size: 0.95rem; font-weight: 400;'>{signo}{valor:.1f}%</div></div>"
                    else:
                        rend_divs += f"<div style='text-align: center;'><div style='color: #444; font-size: 0.65rem;'>{nombre_p}</div><div style='color: #333; font-size: 0.95rem;'>—</div></div>"
                
                st.markdown(f"""
                <div style='background: rgba(15, 15, 25, 0.6); border: 1px solid rgba(255,255,255,0.05); 
                            border-radius: 6px; padding: 15px; font-family: monospace;'>
                    <div style='color: #555; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;'>{get_text('historical_performance')}</div>
                    <div style='display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px;'>{rend_divs}</div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.warning("⚠️ No hay suficientes datos para el período seleccionado")
        else:
            st.warning("⚠️ No hay datos históricos disponibles para mostrar el gráfico")
        
        st.markdown("---")
        
        # Análisis con IA - Estilo retrofuturista
        ai_title = "🤖 AI ENGINEER BROKER ANALYSIS" if st.session_state.get('language', 'es') == 'en' else "🤖 ANÁLISIS INGENIERO BROKER"
        st.markdown(f"""
        <div style='margin: 30px 0 20px 0;'>
            <span style='font-family: "JetBrains Mono", monospace; color: #FF006E; font-size: 1.2rem; 
                        letter-spacing: 3px; text-transform: uppercase; text-shadow: 0 0 20px rgba(255, 0, 110, 0.4);'>
                {ai_title}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if api_key:
            # Usar caché para el análisis de IA
            cache_key = f"ai_analysis_{ticker}"
            if cache_key not in st.session_state:
                spinner_msg = "🧠 The Engineer Broker is analyzing the data..." if st.session_state.get('language', 'es') == 'en' else "🧠 El Ingeniero Broker está analizando los datos..."
                with st.spinner(spinner_msg):
                    # Construir el prompt
                    prompt = build_analysis_prompt(data, ticker)
                    
                    # Obtener análisis de Groq (Llama 3.3 70B)
                    analysis = get_ai_analysis(prompt, api_key)
                    st.session_state[cache_key] = analysis
            else:
                analysis = st.session_state[cache_key]
            
            # Mostrar el análisis con estilo retrofuturista
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(15, 15, 25, 0.95) 0%, rgba(20, 20, 35, 0.95) 100%); 
                        border: 1px solid rgba(255, 0, 110, 0.3); border-radius: 12px; padding: 25px; margin: 15px 0;
                        box-shadow: 0 0 30px rgba(255, 0, 110, 0.1);'>
                <div style='font-family: monospace; color: rgba(255,255,255,0.85); line-height: 1.8; font-size: 0.9rem;'>
                    {analysis}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón para regenerar análisis
            regen_text = "🔄 Regenerate Analysis" if st.session_state.get('language', 'es') == 'en' else "🔄 Regenerar Análisis"
            if st.button(regen_text, key="regenerate_ai"):
                if cache_key in st.session_state:
                    del st.session_state[cache_key]
                st.rerun()
            
            # Disclaimer retrofuturista (bilingüe)
            disclaimer_text = "This analysis is generated by AI for educational purposes. It does not constitute financial advice. Always do your own research before investing." if st.session_state.get('language', 'es') == 'en' else "Este análisis es generado por IA con fines educativos. No constituye asesoramiento financiero. Siempre haz tu propia investigación antes de invertir."
            st.markdown(f"""
            <div style='background: rgba(255, 183, 77, 0.1); border: 1px solid rgba(255, 183, 77, 0.3); 
                        border-radius: 8px; padding: 15px; margin-top: 20px; font-family: monospace;'>
                <span style='color: #FFB74D; font-size: 0.75rem;'>⚠ DISCLAIMER:</span>
                <span style='color: rgba(255,255,255,0.6); font-size: 0.75rem;'> 
                    {disclaimer_text}
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: rgba(255, 0, 110, 0.1); border: 1px solid rgba(255, 0, 110, 0.3);
                        border-radius: 8px; padding: 20px; font-family: monospace;'>
                <div style='color: #FF006E; font-size: 0.85rem; margin-bottom: 10px;'>{'⚠ API Key not configured' if st.session_state.get('language', 'es') == 'en' else '⚠ API Key no configurada'}</div>
                <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>
                    {'To get the Engineer Broker analysis, enter your Groq API Key in the sidebar.' if st.session_state.get('language', 'es') == 'en' else 'Para obtener el análisis del Ingeniero Broker, introduce tu API Key de Groq en la barra lateral.'}<br>
                    {'Financial data is already available above.' if st.session_state.get('language', 'es') == 'en' else 'Los datos financieros ya están disponibles arriba.'}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar los datos crudos como alternativa
            raw_data_label = "📋 View raw data for manual analysis" if st.session_state.get('language', 'es') == 'en' else "📋 Ver datos crudos para análisis manual"
            with st.expander(raw_data_label):
                prompt = build_analysis_prompt(data, ticker)
                st.code(prompt, language="text")
        
        # =====================================================================
        # GRÁFICO DE PETER LYNCH - Precio vs Línea de Beneficios
        # =====================================================================
        st.markdown("---")
        
        is_en = st.session_state.get('language', 'es') == 'en'
        lynch_chart_title = "📊 PETER LYNCH CHART - Price vs Earnings" if is_en else "📊 GRÁFICO DE PETER LYNCH - Precio vs Beneficios"
        st.markdown(f"""
        <div style='margin: 30px 0 20px 0;'>
            <span style='font-family: "JetBrains Mono", monospace; color: #FFB74D; font-size: 1.2rem; 
                        letter-spacing: 3px; text-transform: uppercase; text-shadow: 0 0 20px rgba(255, 183, 77, 0.4);'>
                {lynch_chart_title}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Explicación del gráfico
        lynch_explanation = """
        <div style='background: rgba(255, 183, 77, 0.1); border: 1px solid rgba(255, 183, 77, 0.3); 
                    border-radius: 8px; padding: 15px; margin-bottom: 20px; font-family: monospace;'>
            <div style='color: #FFB74D; font-size: 0.8rem; margin-bottom: 8px;'>💡 {}</div>
            <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; line-height: 1.6;'>
                {}
            </div>
        </div>
        """
        if is_en:
            lynch_title = "What does this chart show?"
            lynch_desc = "Peter Lynch recommended comparing the stock price with its 'fair value line' (EPS × Fair P/E). The <span style='color:#FFB74D;'>fair P/E multiplier</span> is calculated as the <b>historical median</b> of the stock's P/E ratio. When the <span style='color:#00FF9F;'>price line</span> is ABOVE the <span style='color:#FFB74D;'>fair value line</span>, the stock may be overvalued. When it's BELOW, it may be undervalued."
        else:
            lynch_title = "¿Qué muestra este gráfico?"
            lynch_desc = "Peter Lynch recomendaba comparar el precio de la acción con su 'línea de valor justo' (EPS × P/E Justo). El <span style='color:#FFB74D;'>multiplicador P/E justo</span> se calcula como la <b>mediana histórica</b> del P/E de la acción. Cuando la <span style='color:#00FF9F;'>línea de precio</span> está POR ENCIMA de la <span style='color:#FFB74D;'>línea de valor justo</span>, la acción puede estar sobrevalorada. Cuando está POR DEBAJO, puede estar infravalorada."
        
        st.markdown(lynch_explanation.format(lynch_title, lynch_desc), unsafe_allow_html=True)
        
        # Obtener datos para el gráfico de Lynch
        lynch_data = get_peter_lynch_chart_data(ticker)
        
        if lynch_data and lynch_data.get("has_data"):
            try:
                import plotly.graph_objects as go
                
                price_df = lynch_data["price_history"]
                fair_value_df = lynch_data["fair_value_line"]
                conservative_value_df = lynch_data.get("conservative_value_line")
                fair_multiplier = lynch_data.get("fair_multiplier", 15)
                conservative_multiplier = lynch_data.get("conservative_multiplier", 15)
                growth_rate = lynch_data.get("growth_rate")
                method_used = lynch_data.get("method", "unknown")
                has_projection = lynch_data.get("has_projection", False)
                projection_start = lynch_data.get("projection_start")
                forward_eps = lynch_data.get("forward_eps")
                
                # Crear figura
                fig = go.Figure()
                
                # Si hay proyección, separar datos históricos de proyectados
                if has_projection and projection_start is not None:
                    # Datos históricos (hasta projection_start)
                    hist_fair = fair_value_df[fair_value_df.index < projection_start]
                    proj_fair = fair_value_df[fair_value_df.index >= projection_start]
                    
                    # Conservador histórico y proyectado
                    if conservative_value_df is not None:
                        hist_conservative = conservative_value_df[conservative_value_df.index < projection_start]
                        proj_conservative = conservative_value_df[conservative_value_df.index >= projection_start]
                    else:
                        hist_conservative = None
                        proj_conservative = None
                    
                    # Añadir área sombreada para la zona de proyección
                    if len(proj_fair) > 0:
                        fig.add_vrect(
                            x0=projection_start,
                            x1=proj_fair.index[-1],
                            fillcolor="rgba(255, 183, 77, 0.08)",
                            layer="below",
                            line_width=0
                        )
                        # Línea vertical indicando inicio de proyección
                        fig.add_vline(
                            x=projection_start,
                            line=dict(color='rgba(255,183,77,0.4)', width=1, dash='dot'),
                        )
                else:
                    hist_fair = fair_value_df
                    proj_fair = None
                    hist_conservative = conservative_value_df if conservative_value_df is not None else None
                    proj_conservative = None
                
                # =====================================================================
                # ORDEN DE TRAZADO PARA BANDA DE VALOR:
                # 1. Línea Conservadora (abajo) - sin fill
                # 2. Línea Fair Value (arriba) - con fill='tonexty' para crear la banda
                # 3. Línea de Precio (encima de todo)
                # =====================================================================
                
                # 1. Línea de valor conservador histórica (PRIMERO - línea inferior de la banda)
                if hist_conservative is not None and len(hist_conservative) > 0:
                    growth_pct = f" ({growth_rate*100:.0f}% growth)" if growth_rate and growth_rate > 0 else ""
                    growth_pct_es = f" ({growth_rate*100:.0f}% crecim.)" if growth_rate and growth_rate > 0 else ""
                    conservative_legend = f"Conservative PEG=1 (EPS×{conservative_multiplier}){growth_pct}" if is_en else f"Conservador PEG=1 (EPS×{conservative_multiplier}){growth_pct_es}"
                    fig.add_trace(go.Scatter(
                        x=hist_conservative.index,
                        y=hist_conservative['Conservative_Value'],
                        name=conservative_legend,
                        line=dict(color='#8B9DC3', width=1.5),
                        opacity=0.8,
                        hovertemplate='%{x|%Y-%m-%d}<br>Conservative Value: $%{y:.2f}<extra></extra>' if is_en else '%{x|%Y-%m-%d}<br>Valor Conservador: $%{y:.2f}<extra></extra>'
                    ))
                
                # 2. Línea de valor justo histórica (SEGUNDO - con fill='tonexty' para banda)
                legend_name = f"Fair Value (EPS×{fair_multiplier})" if is_en else f"Valor Justo (EPS×{fair_multiplier})"
                band_legend = f"Fair Value Band" if is_en else f"Banda de Valor Justo"
                fig.add_trace(go.Scatter(
                    x=hist_fair.index,
                    y=hist_fair['Fair_Value'],
                    name=band_legend,
                    line=dict(color='#FFB74D', width=2, dash='dash'),
                    fill='tonexty' if hist_conservative is not None and len(hist_conservative) > 0 else None,
                    fillcolor='rgba(255, 183, 77, 0.12)',  # Naranja suave semitransparente
                    hovertemplate='%{x|%Y-%m-%d}<br>Fair Value: $%{y:.2f}<extra></extra>' if is_en else '%{x|%Y-%m-%d}<br>Valor Justo: $%{y:.2f}<extra></extra>'
                ))
                
                # 3. Línea de precio (TERCERO - siempre encima, Z-index superior)
                fig.add_trace(go.Scatter(
                    x=price_df.index,
                    y=price_df['Close'],
                    name='Price' if is_en else 'Precio',
                    line=dict(color='#00FF9F', width=2.5),
                    hovertemplate='%{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>' if is_en else '%{x|%Y-%m-%d}<br>Precio: $%{y:.2f}<extra></extra>'
                ))
                
                # Líneas de proyección (si existen)
                if proj_fair is not None and len(proj_fair) > 0:
                    # Proyección Conservadora primero (para fill='tonexty')
                    if proj_conservative is not None and len(proj_conservative) > 0:
                        fig.add_trace(go.Scatter(
                            x=proj_conservative.index,
                            y=proj_conservative['Conservative_Value'],
                            name=f"Proj. Conservative" if is_en else f"Proy. Conservador",
                            line=dict(color='#8B9DC3', width=1.5, dash='dot'),
                            opacity=0.6,
                            showlegend=False,
                            hovertemplate='%{x|%Y-%m-%d}<br>Projected Conservative: $%{y:.2f}<extra></extra>' if is_en else '%{x|%Y-%m-%d}<br>Conservador Proyectado: $%{y:.2f}<extra></extra>'
                        ))
                    
                    # Proyección Fair Value con banda
                    proj_legend = f"Projection" if is_en else f"Proyección"
                    fig.add_trace(go.Scatter(
                        x=proj_fair.index,
                        y=proj_fair['Fair_Value'],
                        name=proj_legend,
                        line=dict(color='#FFB74D', width=2, dash='dot'),
                        fill='tonexty' if proj_conservative is not None and len(proj_conservative) > 0 else None,
                        fillcolor='rgba(255, 183, 77, 0.08)',
                        opacity=0.7,
                        hovertemplate='%{x|%Y-%m-%d}<br>Projected Fair Value: $%{y:.2f}<extra></extra>' if is_en else '%{x|%Y-%m-%d}<br>Valor Justo Proyectado: $%{y:.2f}<extra></extra>'
                    ))
                    
                    # Añadir anotación de "Projection"
                    annotation_text = "PROJECTION" if is_en else "PROYECCIÓN"
                    mid_proj_idx = len(proj_fair) // 2
                    fig.add_annotation(
                        x=proj_fair.index[mid_proj_idx],
                        y=proj_fair['Fair_Value'].max() * 1.05,
                        text=annotation_text,
                        showarrow=False,
                        font=dict(size=10, color='rgba(255,183,77,0.6)'),
                        bgcolor='rgba(0,0,0,0.4)',
                        borderpad=4
                    )
                
                # Calcular valores actuales para mostrar (usar histórico, no proyección)
                current_price = price_df['Close'].iloc[-1] if len(price_df) > 0 else None
                current_fair = hist_fair['Fair_Value'].iloc[-1] if len(hist_fair) > 0 else None
                current_conservative = hist_conservative['Conservative_Value'].iloc[-1] if hist_conservative is not None and len(hist_conservative) > 0 else None
                
                # Configurar layout
                fig.update_layout(
                    paper_bgcolor='rgba(10, 10, 15, 0.95)',
                    plot_bgcolor='rgba(15, 15, 25, 0.8)',
                    font=dict(family='JetBrains Mono, monospace', color='rgba(255,255,255,0.8)'),
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.05)',
                        linecolor='rgba(255,255,255,0.1)',
                        tickfont=dict(size=10),
                        title=None
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.05)',
                        linecolor='rgba(255,255,255,0.1)',
                        tickfont=dict(size=10),
                        tickprefix='$',
                        title=None
                    ),
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=1.02,
                        xanchor='center',
                        x=0.5,
                        bgcolor='rgba(0,0,0,0.3)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    ),
                    margin=dict(l=50, r=30, t=60, b=40),
                    height=450,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar análisis de la valuación actual
                if current_price and current_fair and current_fair > 0:
                    premium_discount = ((current_price - current_fair) / current_fair) * 100
                    
                    # =====================================================================
                    # LÓGICA DE VEREDICTO CON JERARQUÍA DE PRIORIDADES
                    # =====================================================================
                    # PRIORIDAD 1: Deep Value (precio < valor conservador) - MÁXIMA PRIORIDAD
                    # PRIORIDAD 2: Overvalued (precio muy por encima del fair value)
                    # PRIORIDAD 3: High PE Warning (PER > 35 pero precio > conservador)
                    # PRIORIDAD 4: Standard (Fair Value / Undervalued normal)
                    # =====================================================================
                    
                    high_pe_threshold = 35
                    is_high_pe = fair_multiplier > high_pe_threshold
                    is_deep_value = current_conservative and current_conservative > 0 and current_price < current_conservative
                    
                    # Calcular descuento vs conservador si aplica
                    if current_conservative and current_conservative > 0:
                        discount_vs_conservative = ((current_price - current_conservative) / current_conservative) * 100
                    else:
                        discount_vs_conservative = 0
                    
                    # PRIORIDAD 1: Deep Value - Precio por debajo de la línea conservadora
                    if is_deep_value:
                        status_color = "#00FFFF"  # Cian brillante
                        status_icon = "💎"
                        status_text = "DEEP VALUE" if is_en else "OPORTUNIDAD PROFUNDA"
                        status_desc = f"Price is {abs(discount_vs_conservative):.1f}% below conservative value. Market is extremely pessimistic." if is_en else f"El precio está {abs(discount_vs_conservative):.1f}% por debajo del valor conservador. El mercado es muy pesimista."
                    
                    # PRIORIDAD 2: Claramente sobrevalorado (> 20% sobre fair value)
                    elif premium_discount > 20:
                        status_color = "#FF006E"
                        status_icon = "🔴"
                        status_text = "OVERVALUED" if is_en else "SOBREVALORADO"
                        status_desc = f"Price is {premium_discount:.1f}% above fair value" if is_en else f"El precio está {premium_discount:.1f}% por encima del valor justo"
                    
                    # PRIORIDAD 3: Ligeramente sobrevalorado (0-20% sobre fair value)
                    elif premium_discount > 0:
                        status_color = "#FFB74D"
                        status_icon = "🟡"
                        status_text = "SLIGHTLY OVERVALUED" if is_en else "LIGERAMENTE SOBREVALORADO"
                        status_desc = f"Price is {premium_discount:.1f}% above fair value" if is_en else f"El precio está {premium_discount:.1f}% por encima del valor justo"
                    
                    # PRIORIDAD 4: High PE Warning (PER > 35, pero precio aún sobre conservador)
                    elif is_high_pe:
                        status_color = "#FFB74D"
                        status_icon = "⚠️"
                        status_text = "PRICED FOR PERFECTION" if is_en else "PRECIO DE PERFECCIÓN"
                        status_desc = f"High P/E ({fair_multiplier:.0f}x) requires sustained high growth" if is_en else f"PER alto ({fair_multiplier:.0f}x) requiere crecimiento alto sostenido"
                    
                    # PRIORIDAD 5: Fair Value (PER normal, precio cercano al fair value)
                    elif premium_discount > -20:
                        status_color = "#E2D1F3"
                        status_icon = "⚖️"
                        status_text = "FAIR VALUE" if is_en else "VALOR JUSTO"
                        status_desc = f"Price is {abs(premium_discount):.1f}% below fair value" if is_en else f"El precio está {abs(premium_discount):.1f}% por debajo del valor justo"
                    
                    # PRIORIDAD 6: Undervalued (PER normal, precio muy por debajo del fair value)
                    else:
                        status_color = "#00FF9F"
                        status_icon = "🟢"
                        status_text = "UNDERVALUED" if is_en else "INFRAVALORADO"
                        status_desc = f"Price is {abs(premium_discount):.1f}% below fair value" if is_en else f"El precio está {abs(premium_discount):.1f}% por debajo del valor justo"
                    
                    cols_status = st.columns([1, 2, 1])
                    with cols_status[1]:
                        # Mostrar status con 3 métricas
                        conservative_value_text = f"${current_conservative:.2f}" if current_conservative and current_conservative > 0 else "N/A"
                        conservative_label = 'Conservative (PEG=1)' if is_en else 'Conservador (PEG=1)'
                        
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(15, 15, 25, 0.9) 0%, rgba(20, 20, 35, 0.9) 100%); 
                                    border: 2px solid {status_color}; border-radius: 12px; padding: 20px; text-align: center;
                                    box-shadow: 0 0 20px {status_color}33;'>
                            <div style='font-size: 2rem; margin-bottom: 5px;'>{status_icon}</div>
                            <div style='font-size: 1.1rem; font-weight: bold; color: {status_color}; font-family: monospace; letter-spacing: 2px;'>
                                {status_text}
                            </div>
                            <div style='font-size: 0.75rem; color: rgba(255,255,255,0.6); margin-top: 8px; font-family: monospace;'>
                                {status_desc}
                            </div>
                            <div style='display: flex; justify-content: space-around; margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                                <div>
                                    <div style='font-size: 0.65rem; color: rgba(255,255,255,0.5);'>{'Current Price' if is_en else 'Precio Actual'}</div>
                                    <div style='font-size: 1rem; color: #00FF9F; font-weight: bold;'>${current_price:.2f}</div>
                                </div>
                                <div>
                                    <div style='font-size: 0.65rem; color: rgba(255,255,255,0.5);'>{'Fair Value' if is_en else 'Valor Justo'}</div>
                                    <div style='font-size: 1rem; color: #FFB74D; font-weight: bold;'>${current_fair:.2f}</div>
                                </div>
                                <div>
                                    <div style='font-size: 0.65rem; color: rgba(255,255,255,0.5);'>{conservative_label}</div>
                                    <div style='font-size: 1rem; color: #8B9DC3; font-weight: bold;'>{conservative_value_text}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Nota metodológica con multiplicador dinámico
                if is_en:
                    method_note = f"ℹ️ Fair value = EPS × {fair_multiplier} (historical median P/E). "
                    method_note += f"Conservative (PEG=1) = EPS × {conservative_multiplier} (based on growth rate, floor 15, cap 25). "
                    if method_used == "current_eps_only":
                        method_note += "Using current EPS only."
                    else:
                        method_note += "Projection: 1 year using Forward EPS."
                else:
                    method_note = f"ℹ️ Valor justo = EPS × {fair_multiplier} (mediana histórica del P/E). "
                    method_note += f"Conservador (PEG=1) = EPS × {conservative_multiplier} (basado en tasa de crecimiento, mín 15, máx 25). "
                    if method_used == "current_eps_only":
                        method_note += "Usando solo EPS actual."
                    else:
                        method_note += "Proyección: 1 año usando Forward EPS."
                
                st.markdown(f"""
                <div style='font-size: 0.65rem; color: rgba(255,183,77,0.6); font-family: monospace; margin-top: 15px; text-align: center;'>
                    {method_note}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.warning(f"{'Could not generate Peter Lynch chart' if is_en else 'No se pudo generar el gráfico de Peter Lynch'}: {str(e)}")
        else:
            # Mostrar mensaje de error específico si está disponible
            error_msg = lynch_data.get("error", "") if lynch_data else ""
            if error_msg:
                no_data_msg = f"{'Could not generate chart' if is_en else 'No se pudo generar el gráfico'}: {error_msg}"
            else:
                no_data_msg = "Not enough earnings data available to generate the Peter Lynch chart" if is_en else "No hay suficientes datos de beneficios disponibles para generar el gráfico de Peter Lynch"
            st.info(no_data_msg)
        
        # =====================================================================
        # SECCIÓN DE INSIDERS Y INSTITUCIONALES
        # =====================================================================
        st.markdown("---")
        
        is_en = st.session_state.get('language', 'es') == 'en'
        insiders_title = "👔 INSIDER & INSTITUTIONAL DATA" if is_en else "👔 DATOS DE INSIDERS E INSTITUCIONALES"
        st.markdown(f"""
        <div style='margin: 30px 0 20px 0;'>
            <span style='font-family: "JetBrains Mono", monospace; color: #6464FF; font-size: 1.2rem; 
                        letter-spacing: 3px; text-transform: uppercase; text-shadow: 0 0 20px rgba(100, 100, 255, 0.4);'>
                {insiders_title}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Obtener datos de insiders
        insider_data = get_insider_data(ticker)
        
        if insider_data:
            # ==================== RESUMEN DE PROPIEDAD ====================
            major_title = "📊 Ownership Summary" if is_en else "📊 Resumen de Propiedad"
            with st.expander(major_title, expanded=True):
                ownership_info = insider_data.get("ownership_info")
                
                if ownership_info:
                    # Usar datos precisos del ticker.info
                    cols = st.columns(2)
                    
                    # Tarjeta 1: Participación Institucional
                    with cols[0]:
                        inst_pct = ownership_info.get('institutions_percent')
                        if inst_pct is not None:
                            pct_value = f"{inst_pct * 100:.2f}%" if inst_pct < 1 else f"{inst_pct:.2f}%"
                        else:
                            pct_value = "N/A"
                        label = "Institutional Ownership" if is_en else "Participación Institucional"
                        st.markdown(f"""
                        <div style='background: rgba(15, 15, 25, 0.6); border-radius: 10px; padding: 15px; 
                                    border: 1px solid rgba(100, 100, 255, 0.3); margin-bottom: 10px;'>
                            <div style='font-size: 1.5rem; font-weight: bold; font-family: monospace; color: #6464FF;'>
                                {pct_value}
                            </div>
                            <div style='font-size: 0.75rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 5px;'>
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tarjeta 2: Float Shares
                    with cols[1]:
                        float_shares = ownership_info.get('float_shares')
                        if float_shares is not None:
                            if float_shares >= 1e9:
                                formatted_value = f"{float_shares/1e9:.2f}B"
                            elif float_shares >= 1e6:
                                formatted_value = f"{float_shares/1e6:.1f}M"
                            else:
                                formatted_value = f"{float_shares:,.0f}"
                        else:
                            formatted_value = "N/A"
                        label = "Float Shares" if is_en else "Acciones en Circulación (Float)"
                        st.markdown(f"""
                        <div style='background: rgba(15, 15, 25, 0.6); border-radius: 10px; padding: 15px; 
                                    border: 1px solid rgba(0, 255, 159, 0.3); margin-bottom: 10px;'>
                            <div style='font-size: 1.5rem; font-weight: bold; font-family: monospace; color: #00FF9F;'>
                                {formatted_value}
                            </div>
                            <div style='font-size: 0.75rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 5px;'>
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Nota informativa
                    note_text = "ℹ️ Data sourced from Yahoo Finance. Float shares are the shares available for public trading." if is_en else "ℹ️ Datos obtenidos de Yahoo Finance. Las acciones float son las disponibles para negociación pública."
                    st.markdown(f"""
                    <div style='font-size: 0.65rem; color: rgba(255,183,77,0.7); font-family: monospace; margin-top: 10px; margin-bottom: 10px; padding: 10px; 
                                background: rgba(255,183,77,0.1); border-radius: 6px; border-left: 3px solid rgba(255,183,77,0.5);'>
                        {note_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif insider_data.get("major_holders") is not None:
                    # Fallback: usar major_holders si no hay ownership_info
                    major_df = insider_data["major_holders"]
                    
                    label_translations = {
                        'insidersPercentHeld': ('Insiders Ownership' if is_en else 'Participación de Insiders', '#FF006E'),
                        'institutionsPercentHeld': ('Institutional Ownership' if is_en else 'Participación Institucional', '#6464FF'),
                        'institutionsFloatPercentHeld': ('Institutions % of Float' if is_en else '% Institucional del Float', '#6464FF'),
                        'institutionsCount': ('Number of Institutions' if is_en else 'Número de Instituciones', '#00FF9F'),
                    }
                    
                    cols = st.columns(2)
                    col_idx = 0
                    
                    for idx, row in major_df.iterrows():
                        raw_value = row.iloc[0] if len(row) > 0 else None
                        raw_label = row.iloc[1] if len(row) > 1 else str(idx)
                        
                        if raw_label in label_translations:
                            label, color = label_translations[raw_label]
                        else:
                            label = raw_label
                            color = '#00FF9F'
                        
                        if raw_value is not None:
                            try:
                                val = float(raw_value)
                                if val < 1:
                                    formatted_value = f"{val * 100:.2f}%"
                                elif val > 100:
                                    formatted_value = f"{int(val):,}"
                                else:
                                    formatted_value = f"{val:.2f}%"
                            except:
                                formatted_value = str(raw_value)
                        else:
                            formatted_value = "N/A"
                        
                        with cols[col_idx % 2]:
                            st.markdown(f"""
                            <div style='background: rgba(15, 15, 25, 0.6); border-radius: 10px; padding: 15px; 
                                        border: 1px solid rgba(100, 100, 255, 0.2); margin-bottom: 10px;'>
                                <div style='font-size: 1.5rem; font-weight: bold; font-family: monospace; color: {color};'>
                                    {formatted_value}
                                </div>
                                <div style='font-size: 0.75rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 5px;'>
                                    {label}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        col_idx += 1
                else:
                    no_data_msg = "No ownership data available" if is_en else "No hay datos de propiedad disponibles"
                    st.info(no_data_msg)
            
            # ==================== TENEDORES INSTITUCIONALES ====================
            inst_title = "🏦 Top Institutional Holders" if is_en else "🏦 Principales Tenedores Institucionales"
            with st.expander(inst_title):
                if insider_data.get("institutional_holders") is not None:
                    inst_df = insider_data["institutional_holders"].head(10)
                    display_df = inst_df.copy()
                    
                    # Renombrar columnas
                    col_names = {
                        'Holder': 'Institution' if is_en else 'Institución', 
                        'Shares': 'Shares' if is_en else 'Acciones', 
                        'Date Reported': 'Date' if is_en else 'Fecha', 
                        'pctHeld': '% Held' if is_en else '% Posición', 
                        'Value': 'Value' if is_en else 'Valor'
                    }
                    
                    for old_col, new_col in col_names.items():
                        if old_col in display_df.columns:
                            display_df = display_df.rename(columns={old_col: new_col})
                    
                    # Formatear valores
                    for col in display_df.columns:
                        if 'Shares' in col or 'Acciones' in col:
                            display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
                        elif 'Value' in col or 'Valor' in col:
                            display_df[col] = display_df[col].apply(lambda x: f"${x/1e9:.2f}B" if pd.notna(x) and x >= 1e9 else (f"${x/1e6:.1f}M" if pd.notna(x) else "N/A"))
                        elif '%' in col:
                            display_df[col] = display_df[col].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
                        elif 'Date' in col or 'Fecha' in col:
                            display_df[col] = display_df[col].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d') if pd.notna(x) else "N/A")
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    no_data_msg = "No institutional holders data available" if is_en else "No hay datos de institucionales disponibles"
                    st.info(no_data_msg)
            
            # ==================== SHORT INTEREST (INTERÉS EN CORTO) ====================
            short_title = "📉 Short Interest" if is_en else "📉 Interés en Corto"
            with st.expander(short_title, expanded=False):
                ownership_info = insider_data.get("ownership_info")
                
                if ownership_info and any(key in ownership_info for key in ['shares_short', 'short_ratio', 'short_percent_float']):
                    cols = st.columns(3)
                    
                    # Tarjeta 1: Acciones en Corto
                    with cols[0]:
                        shares_short = ownership_info.get('shares_short')
                        if shares_short is not None:
                            if shares_short >= 1e9:
                                formatted_value = f"{shares_short/1e9:.2f}B"
                            elif shares_short >= 1e6:
                                formatted_value = f"{shares_short/1e6:.2f}M"
                            else:
                                formatted_value = f"{shares_short:,.0f}"
                        else:
                            formatted_value = "N/A"
                        label = "Shares Short" if is_en else "Acciones en Corto"
                        st.markdown(f"""
                        <div style='background: rgba(15, 15, 25, 0.6); border-radius: 10px; padding: 15px; 
                                    border: 1px solid rgba(255, 0, 110, 0.3); text-align: center;'>
                            <div style='font-size: 1.4rem; font-weight: bold; font-family: monospace; color: #FF006E;'>
                                {formatted_value}
                            </div>
                            <div style='font-size: 0.7rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 5px;'>
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tarjeta 2: Short Ratio (Days to Cover)
                    with cols[1]:
                        short_ratio = ownership_info.get('short_ratio')
                        if short_ratio is not None:
                            formatted_value = f"{short_ratio:.2f}"
                            # Color según el ratio
                            if short_ratio < 3:
                                ratio_color = "#00FF9F"  # Bajo
                            elif short_ratio < 7:
                                ratio_color = "#FFB74D"  # Moderado
                            else:
                                ratio_color = "#FF006E"  # Alto
                        else:
                            formatted_value = "N/A"
                            ratio_color = "#6464FF"
                        label = "Short Ratio (Days)" if is_en else "Ratio en Corto (Días)"
                        st.markdown(f"""
                        <div style='background: rgba(15, 15, 25, 0.6); border-radius: 10px; padding: 15px; 
                                    border: 1px solid rgba(100, 100, 255, 0.3); text-align: center;'>
                            <div style='font-size: 1.4rem; font-weight: bold; font-family: monospace; color: {ratio_color};'>
                                {formatted_value}
                            </div>
                            <div style='font-size: 0.7rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 5px;'>
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tarjeta 3: % del Float en Corto
                    with cols[2]:
                        short_pct = ownership_info.get('short_percent_float')
                        if short_pct is not None:
                            formatted_value = f"{short_pct * 100:.2f}%" if short_pct < 1 else f"{short_pct:.2f}%"
                            # Color según el porcentaje
                            pct_val = short_pct * 100 if short_pct < 1 else short_pct
                            if pct_val < 5:
                                pct_color = "#00FF9F"  # Bajo
                            elif pct_val < 15:
                                pct_color = "#FFB74D"  # Moderado
                            else:
                                pct_color = "#FF006E"  # Alto (potencial short squeeze)
                        else:
                            formatted_value = "N/A"
                            pct_color = "#6464FF"
                        label = "% Float Short" if is_en else "% Float en Corto"
                        st.markdown(f"""
                        <div style='background: rgba(15, 15, 25, 0.6); border-radius: 10px; padding: 15px; 
                                    border: 1px solid rgba(0, 255, 159, 0.3); text-align: center;'>
                            <div style='font-size: 1.4rem; font-weight: bold; font-family: monospace; color: {pct_color};'>
                                {formatted_value}
                            </div>
                            <div style='font-size: 0.7rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 5px;'>
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Comparativa mes anterior (si hay datos)
                    shares_short_prior = ownership_info.get('shares_short_prior')
                    shares_short = ownership_info.get('shares_short')
                    if shares_short_prior is not None and shares_short is not None and shares_short_prior > 0:
                        change_pct = ((shares_short - shares_short_prior) / shares_short_prior) * 100
                        change_color = "#FF006E" if change_pct > 0 else "#00FF9F"
                        change_icon = "📈" if change_pct > 0 else "📉"
                        change_text = f"{change_icon} {'Change vs Prior Month:' if is_en else 'Cambio vs Mes Anterior:'} <span style='color: {change_color};'>{'+' if change_pct > 0 else ''}{change_pct:.1f}%</span>"
                        st.markdown(f"""
                        <div style='font-size: 0.75rem; color: rgba(255,255,255,0.6); font-family: monospace; margin-top: 15px; text-align: center;'>
                            {change_text}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Nota explicativa
                    note_text = "ℹ️ Short Ratio indicates days to cover all short positions at average daily volume. High % Float Short (>15%) may indicate bearish sentiment or potential short squeeze." if is_en else "ℹ️ El Ratio en Corto indica días para cubrir todas las posiciones cortas al volumen diario promedio. Alto % Float en Corto (>15%) puede indicar sentimiento bajista o potencial short squeeze."
                    st.markdown(f"""
                    <div style='font-size: 0.65rem; color: rgba(255,183,77,0.7); font-family: monospace; margin-top: 15px; margin-bottom: 10px; padding: 10px; 
                                background: rgba(255,183,77,0.1); border-radius: 6px; border-left: 3px solid rgba(255,183,77,0.5);'>
                        {note_text}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    no_data_msg = "No short interest data available for this ticker" if is_en else "No hay datos de interés en corto disponibles para este ticker"
                    st.info(no_data_msg)
            
            # ==================== TRANSACCIONES DE INSIDERS ====================
            activity_title = "📈 Recent Insider Transactions" if is_en else "📈 Transacciones Recientes de Insiders"
            with st.expander(activity_title, expanded=False):
                
                has_transactions = insider_data.get("insider_transactions") is not None
                
                if has_transactions:
                    trans_df = insider_data["insider_transactions"]
                    display_df = trans_df.head(15).copy()
                    
                    # Identificar tipo de transacción
                    def get_transaction_type(text):
                        if pd.isna(text):
                            return "—"
                        text_lower = str(text).lower()
                        if 'sale' in text_lower or 'sold' in text_lower:
                            return "🔴 " + ("Sale" if is_en else "Venta")
                        elif 'purchase' in text_lower or 'bought' in text_lower or ('acquisition' in text_lower and 'non' not in text_lower):
                            return "🟢 " + ("Buy" if is_en else "Compra")
                        elif 'exercise' in text_lower or 'conversion' in text_lower:
                            return "🔵 " + ("Exercise" if is_en else "Ejercicio")
                        elif 'gift' in text_lower:
                            return "🟣 " + ("Gift" if is_en else "Regalo")
                        else:
                            return "⚪ " + ("Other" if is_en else "Otro")
                    
                    if 'Text' in display_df.columns:
                        display_df['Type'] = display_df['Text'].apply(get_transaction_type)
                    
                    # Seleccionar columnas relevantes
                    desired_cols = ['Insider', 'Position', 'Type', 'Shares', 'Value', 'Start Date']
                    existing_cols = [col for col in desired_cols if col in display_df.columns]
                    display_df = display_df[existing_cols]
                    
                    # Renombrar columnas
                    col_renames = {
                        'Insider': 'Insider',
                        'Position': 'Position' if is_en else 'Cargo',
                        'Type': 'Type' if is_en else 'Tipo',
                        'Shares': 'Shares' if is_en else 'Acciones',
                        'Value': 'Value' if is_en else 'Valor',
                        'Start Date': 'Date' if is_en else 'Fecha'
                    }
                    display_df = display_df.rename(columns=col_renames)
                    
                    # Formatear valores
                    for col in display_df.columns:
                        if col in ['Shares', 'Acciones']:
                            display_df[col] = display_df[col].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "—")
                        elif col in ['Value', 'Valor']:
                            display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "—")
                        elif col in ['Date', 'Fecha']:
                            display_df[col] = display_df[col].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d') if pd.notna(x) else "—")
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    no_data_msg = "No insider activity data available" if is_en else "No hay datos de actividad insider disponibles"
                    st.info(no_data_msg)
        else:
            no_insider_msg = "Could not retrieve insider data for this ticker" if is_en else "No se pudieron obtener datos de insiders para este ticker"
            st.warning(no_insider_msg)
    
    # Mensaje si se presiona analizar sin ticker
    elif analyze_button and not ticker_input:
        warning_msg = "⚠ Please enter a ticker to analyze" if st.session_state.get('language', 'es') == 'en' else "⚠ Por favor, introduce un ticker para analizar"
        st.markdown(f"""
        <div style='background: rgba(255, 183, 77, 0.1); border: 1px solid rgba(255, 183, 77, 0.3);
                    border-radius: 8px; padding: 15px; font-family: monospace; text-align: center;'>
            <span style='color: #FFB74D;'>{warning_msg}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer retrofuturista
    methodology_text = "Based on" if st.session_state.get('language', 'es') == 'en' else "Basado en la metodología de"
    st.markdown(f"""
    <div style='margin-top: 50px; padding: 30px 0; border-top: 1px solid rgba(0, 255, 159, 0.1);'>
        <div style='text-align: center; font-family: monospace;'>
            <div style='color: rgba(255,255,255,0.4); font-size: 0.7rem; letter-spacing: 2px; margin-bottom: 10px;'>
                {methodology_text} <span style='color: #00FF9F;'>PETER LYNCH</span> {'methodology' if st.session_state.get('language', 'es') == 'en' else ''}
            </div>
            <div style='color: rgba(255,255,255,0.3); font-size: 0.65rem;'>
                <span style='color: #FF006E;'>Streamlit</span> • 
                <span style='color: #6464FF;'>Yahoo Finance</span> • 
                <span style='color: #00FF9F;'>Groq AI (Llama 3.3)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    main()
