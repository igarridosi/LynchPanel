# =============================================================================
# INGENIERO BROKER - Analizador de Inversiones Estilo Peter Lynch
# =============================================================================
# Aplicación web que automatiza el análisis de inversiones basado en la
# metodología de Peter Lynch ("Un paso por delante de Wall Street").
# =============================================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from groq import Groq
import os

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
    .stTextInput input {
        background: rgba(15, 15, 25, 0.8) !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
        border-radius: 8px !important;
        color: #00FF9F !important;
        font-family: monospace !important;
    }
    
    .stTextInput input:focus {
        border-color: #00FF9F !important;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.3) !important;
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
# SYSTEM INSTRUCTION PARA GEMINI (PERSONALIDAD DEL INGENIERO BROKER)
# =============================================================================
SYSTEM_INSTRUCTION = """Actúa como mi Ingeniero Broker Senior (estilo Peter Lynch). Tu trabajo es analizar los datos que te paso y ejecutar 'La rutina de los dos minutos'.
REGLAS:

1. Si el PEG ratio es < 1.0, considéralo barato. Si es > 2.0, caro.

2. Compara el PER con el crecimiento esperado.

3. Clasifica la empresa (Cíclica, Recuperación, Activo Oculto, Crecimiento Rápido, Estable).

4. Busca problemas de deuda (¿Hay más deuda que efectivo?).

5. Tu veredicto debe ser directo: COMPRAR, VENDER o MANTENER, explicado con sentido común y analogías sencillas."""

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
            "Recuperación",
            "📈",
            "badge-recuperacion",
            "Empresa con pérdidas - en proceso de recuperación o reestructuración"
        )
    
    # 2. ESTABLE: Empresas grandes (>50B) con dividendos en sectores defensivos
    is_defensive = any(s in sector for s in sectores_defensivos)
    has_good_dividend = dividend_yield > 0.015  # >1.5% dividendo
    is_large_cap = market_cap > 50e9  # >50B
    is_mega_cap = market_cap > 200e9  # >200B
    
    if is_mega_cap and has_good_dividend:
        return (
            "Estable",
            "🏛️",
            "badge-estable",
            "Gigante del mercado con dividendos - empresa blue chip consolidada"
        )
    
    if is_large_cap and has_good_dividend and is_defensive:
        return (
            "Estable",
            "🏛️",
            "badge-estable",
            "Gran empresa defensiva con dividendos - crecimiento moderado y estable"
        )
    
    # 3. CÍCLICA: Sectores que dependen del ciclo económico
    is_cyclical = any(s in sector for s in sectores_ciclicos)
    is_auto = 'auto' in industria or 'vehicle' in industria
    is_airline = 'airline' in industria
    is_hotel = 'hotel' in industria or 'leisure' in industria
    
    if is_cyclical or is_auto or is_airline or is_hotel:
        return (
            "Cíclica",
            "🔄",
            "badge-ciclica",
            "Sector cíclico - rendimiento ligado al ciclo económico"
        )
    
    # 4. ACTIVO OCULTO: Bajo Price/Book y buena posición de caja
    if price_to_book < 1.2 and efectivo > deuda:
        return (
            "Activo Oculto",
            "💎",
            "badge-activo-oculto",
            "Valor oculto - cotiza por debajo de su valor en libros con caja neta positiva"
        )
    
    # 5. CRECIMIENTO RÁPIDO: Alto crecimiento de beneficios o ingresos
    has_high_growth = crecimiento > 0.20 or crecimiento_ingresos > 0.20
    has_good_peg = (peg is not None) and (isinstance(peg, (int, float))) and (peg < 1.5) and (peg > 0)
    is_tech = 'technology' in sector or 'software' in industria
    
    if has_high_growth:
        return (
            "Crecimiento Rápido",
            "🚀",
            "badge-crecimiento",
            "Alto crecimiento de beneficios (>20%) - potencial 'ten-bagger'"
        )
    
    if is_tech and market_cap < 100e9 and (crecimiento > 0.10 or crecimiento_ingresos > 0.15):
        return (
            "Crecimiento Rápido",
            "🚀",
            "badge-crecimiento",
            "Empresa tecnológica en fase de crecimiento"
        )
    
    # 6. ESTABLE por defecto para empresas grandes
    if is_large_cap:
        return (
            "Estable",
            "🏛️",
            "badge-estable",
            "Gran capitalización - empresa consolidada en su sector"
        )
    
    # 7. Por defecto para empresas medianas/pequeñas
    if market_cap > 10e9:  # Mid cap
        return (
            "Estable",
            "🏛️",
            "badge-estable",
            "Empresa de mediana capitalización consolidada"
        )
    else:
        return (
            "Crecimiento Rápido",
            "🚀",
            "badge-crecimiento",
            "Empresa de menor tamaño con potencial de crecimiento"
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


def build_analysis_prompt(data, ticker):
    """
    Construye el prompt dinámico para enviar a Gemini con todos los datos financieros.
    
    Args:
        data: Diccionario con datos financieros
        ticker: Símbolo del ticker
        
    Returns:
        String con el prompt completo
    """
    
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
            situacion_deuda = f"Más efectivo que deuda ✅ (puede pagar {ratio_efectivo_deuda:.1f}x su deuda)"
        else:
            situacion_deuda = f"Más deuda que efectivo ⚠️ (cubre {ratio_efectivo_deuda*100:.0f}% de la deuda)"
        ratio_str = f"{ratio_efectivo_deuda:.2f}x"
    elif efectivo and (not deuda or float(deuda) == 0):
        ratio_str = "Sin deuda"
        situacion_deuda = "Sin deuda - Excelente posición ✅"
        ratio_efectivo_deuda = float('inf')
    else:
        ratio_str = "N/A"
        ratio_efectivo_deuda = None
        situacion_deuda = "No se puede determinar"
    
    # Construir sección de noticias
    noticias_text = ""
    if data.get('noticias'):
        noticias_text = "\n📰 ÚLTIMAS NOTICIAS (Scuttlebutt):\n"
        for i, noticia in enumerate(data['noticias'][:3], 1):
            titulo = noticia.get('title', 'Sin título')
            noticias_text += f"   {i}. {titulo}\n"
    else:
        noticias_text = "\n📰 NOTICIAS: No hay noticias recientes disponibles.\n"
    
    # Construir el prompt completo
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
                    "content": SYSTEM_INSTRUCTION
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
            st.markdown(metric_card_modern("Precio Actual", f"${precio:.2f}", "#00FF9F"), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("Precio Actual", "—", "#555"), unsafe_allow_html=True)
    
    with col2:
        if per != 'N/A':
            if per > 25:
                color, badge_text = "#FF006E", "● Caro"
            elif per < 15:
                color, badge_text = "#00FF9F", "● Barato"
            else:
                color, badge_text = "#FFB74D", "● Normal"
            st.markdown(metric_card_modern("PER (Trailing)", f"{per:.2f}", color, badge_text), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("PER (Trailing)", "—", "#555"), unsafe_allow_html=True)
    
    with col3:
        if peg is not None and peg != 'N/A':
            try:
                peg_val = float(peg)
                if peg_val < 1:
                    color, badge_text = "#00FF9F", "● Barato"
                elif peg_val > 2:
                    color, badge_text = "#FF006E", "● Caro"
                else:
                    color, badge_text = "#FFB74D", "● Justo"
                st.markdown(metric_card_modern("PEG Ratio", f"{peg_val:.2f}", color, badge_text), unsafe_allow_html=True)
            except:
                st.markdown(metric_card_modern("PEG Ratio", "—", "#555"), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("PEG Ratio", "—", "#555"), unsafe_allow_html=True)
    
    with col4:
        # Dividendos mejorados con yield y monto
        if div_info['yield_pct'] is not None:
            yield_pct = div_info['yield_pct']
            quarterly = div_info.get('quarterly_amount')
            freq = div_info.get('frequency', 'trimestral')
            
            if quarterly:
                subtitle = f"${quarterly:.2f} USD / {freq}"
            else:
                subtitle = None
                
            color = "#00FF9F" if yield_pct >= 2 else "#6464FF"
            st.markdown(metric_card_modern("Rentabilidad/Dividendo", f"{yield_pct:.2f}%", color, None, subtitle), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("Dividendo", "—", "#555", "Sin dividendos"), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
    
    # Segunda fila de métricas
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        pb = data.get('price_to_book', 'N/A')
        if pb != 'N/A':
            if pb < 1.5:
                color, badge_text = "#00FF9F", "● Infravalorado"
            elif pb > 4:
                color, badge_text = "#FF006E", "● Sobrevalorado"
            else:
                color, badge_text = "#6464FF", None
            st.markdown(metric_card_modern("Price / Book", f"{pb:.2f}x", color, badge_text), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("Price / Book", "—", "#555"), unsafe_allow_html=True)
    
    with col6:
        mcap = data.get('market_cap', 'N/A')
        badge_text = None
        if mcap != 'N/A':
            try:
                mcap_val = float(mcap)
                if mcap_val >= 200e9:
                    badge_text = "Mega Cap"
                elif mcap_val >= 10e9:
                    badge_text = "Large Cap"
                elif mcap_val >= 2e9:
                    badge_text = "Mid Cap"
                else:
                    badge_text = "Small Cap"
            except:
                badge_text = None
        st.markdown(metric_card_modern("Market Cap", format_large_number(mcap), "#6464FF", badge_text), unsafe_allow_html=True)
    
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
                # Muy sólido: puede pagar su deuda 1.5x o más con efectivo
                color, badge_text = "#00FF9F", "● Muy Sólido"
            elif ratio_efectivo_deuda >= 1.0:
                # Sólido: más efectivo que deuda (posición neta positiva)
                color, badge_text = "#00FF9F", "● Sólido"
            elif ratio_efectivo_deuda >= 0.5:
                # Moderado: tiene al menos la mitad de su deuda en efectivo
                color, badge_text = "#FFB74D", "● Moderado"
            else:
                # Riesgo: poco efectivo respecto a deuda
                color, badge_text = "#FF006E", "● Riesgo"
            
            st.markdown(metric_card_modern("Efectivo / Deuda", f"{ratio_efectivo_deuda:.2f}x", color, badge_text), unsafe_allow_html=True)
        elif efectivo and (not deuda or float(deuda) == 0):
            # Sin deuda - caso excelente
            st.markdown(metric_card_modern("Efectivo / Deuda", "Sin Deuda", "#00FF9F", "● Excelente"), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("Efectivo / Deuda", "—", "#555"), unsafe_allow_html=True)
    
    with col8:
        beta = data.get('beta', 'N/A')
        if beta != 'N/A':
            if beta < 0.8:
                color, badge_text = "#00FF9F", "● Baja volatilidad"
            elif beta > 1.3:
                color, badge_text = "#FF006E", "● Alta volatilidad"
            else:
                color, badge_text = "#6464FF", "● Mercado"
            st.markdown(metric_card_modern("Beta", f"{beta:.2f}", color, badge_text), unsafe_allow_html=True)
        else:
            st.markdown(metric_card_modern("Beta", "—", "#555"), unsafe_allow_html=True)


# =============================================================================
# INTERFAZ PRINCIPAL DE LA APLICACIÓN
# =============================================================================

def main():
    """Función principal que ejecuta la aplicación Streamlit."""
    
    # Header principal retrofuturista
    st.markdown("""
    <div style='text-align: center; padding: 30px 0 20px 0;'>
        <h1 style='font-family: "JetBrains Mono", monospace; font-weight: 200; font-size: 3rem; 
                   color: #00FF9F; text-shadow: 0 0 40px rgba(0, 255, 159, 0.5); letter-spacing: 8px;
                   margin: 0;'>INGENIERO BROKER</h1>
        <p style='font-family: monospace; color: #FF006E; font-size: 0.9rem; letter-spacing: 3px;
                  text-transform: uppercase; margin-top: 10px;'>Analizador de Inversiones • Peter Lynch</p>
        <p style='font-family: monospace; color: rgba(255,255,255,0.4); font-size: 0.75rem; font-style: italic;
                  margin-top: 5px;'>"Compra lo que conoces"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 0 0 20px 0; opacity: 0.3;'>", unsafe_allow_html=True)
    
    # Sidebar para configuración
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 10px 0; margin-bottom: 20px;'>
            <span style='font-family: monospace; color: #00FF9F; font-size: 0.8rem; letter-spacing: 2px;
                        text-transform: uppercase;'>⚙ CONFIGURACIÓN</span>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key de Groq
        st.markdown("""
        <div style='font-family: monospace; color: #FF006E; font-size: 0.75rem; letter-spacing: 1px;
                    text-transform: uppercase; margin-bottom: 10px;'>🔑 API de Groq (Gratis)</div>
        """, unsafe_allow_html=True)
        api_key = st.text_input(
            "Introduce tu API Key:",
            type="password",
            help="Obtén tu API Key en: https://console.groq.com/keys",
            label_visibility="collapsed"
        )
        
        if not api_key:
            st.markdown("""
            <div style='background: rgba(255, 0, 110, 0.1); border: 1px solid rgba(255, 0, 110, 0.3);
                        border-radius: 8px; padding: 12px; margin: 10px 0; font-family: monospace;'>
                <span style='color: #FF006E; font-size: 0.75rem;'>⚠ Necesitas una API Key</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **¿Cómo obtenerla? (GRATIS)**
            1. Ve a [Groq Console](https://console.groq.com/keys)
            2. Crea una cuenta gratuita
            3. Genera una nueva API Key
            4. Cópiala y pégala aquí
            
            ✅ **Límites gratuitos:** 30 req/min, 14,400 req/día
            """)
        
        st.markdown("<hr style='opacity: 0.2; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Info sobre la metodología
        st.markdown("""
        <div style='font-family: monospace; color: #FF006E; font-size: 0.75rem; letter-spacing: 1px;
                    text-transform: uppercase; margin-bottom: 15px;'>📚 Metodología Lynch</div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='font-family: monospace; font-size: 0.75rem; line-height: 1.8;'>
            <div style='color: #00FF9F;'>● PEG < 1.0 → <span style='opacity: 0.7;'>Barato</span></div>
            <div style='color: #FFB74D;'>● PEG 1.0-2.0 → <span style='opacity: 0.7;'>Justo</span></div>
            <div style='color: #FF006E;'>● PEG > 2.0 → <span style='opacity: 0.7;'>Caro</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        # Clasificaciones - se actualizará dinámicamente
        st.markdown("""
        <div style='font-family: monospace; color: rgba(255,255,255,0.5); font-size: 0.7rem;
                    text-transform: uppercase; margin-bottom: 10px;'>Clasificaciones:</div>
        """, unsafe_allow_html=True)
        
        # Guardar placeholder para actualizar después
        classification_placeholder = st.empty()
        
        st.markdown("<hr style='opacity: 0.2; margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; font-family: monospace; font-size: 0.65rem; color: rgba(255,255,255,0.3);'>
            Desarrollado con <span style='color: #FF006E;'>♥</span> usando<br>
            Streamlit • yfinance • Groq AI
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar clasificaciones por defecto si no hay análisis activo
    if 'current_classification' not in st.session_state:
        with classification_placeholder.container():
            st.markdown("""
            <div class="sidebar-item">🚀 Crecimiento Rápido</div>
            <div class="sidebar-item">🏛️ Estable</div>
            <div class="sidebar-item">🔄 Cíclica</div>
            <div class="sidebar-item">📈 Recuperación</div>
            <div class="sidebar-item">💎 Activo Oculto</div>
            """, unsafe_allow_html=True)
    
    # Input del ticker con estilo retrofuturista
    st.markdown("""
    <div style='font-family: monospace; color: #00FF9F; font-size: 0.8rem; letter-spacing: 1px;
                text-transform: uppercase; margin-bottom: 10px;'>🔍 Buscar Acción</div>
    """, unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([3, 1])
    
    with col_input1:
        ticker_input = st.text_input(
            "Ticker:",
            placeholder="AAPL, KO, MSFT, IBE.MC, TSLA...",
            help="Introduce el símbolo de la acción. Para mercados europeos añade el sufijo (ej: IBE.MC para Iberdrola)",
            label_visibility="collapsed"
        )
    
    with col_input2:
        analyze_button = st.button("ANALIZAR", type="primary", use_container_width=True)
    
    # Ejemplos rápidos
    st.markdown("""
    <div style='font-family: monospace; color: rgba(255,255,255,0.4); font-size: 0.7rem; 
                margin: 10px 0 5px 0;'>Ejemplos rápidos:</div>
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
        
        with st.spinner(f"🔄 Descargando datos de {ticker}..."):
            data = get_stock_data(ticker)
        
        if data is None:
            st.error(f"""
            ❌ **No se encontró el ticker '{ticker}'**
            
            Por favor verifica que:
            - El símbolo esté escrito correctamente
            - Para mercados europeos, añade el sufijo correcto (ej: .MC para Madrid, .L para Londres)
            - La acción esté listada en una bolsa soportada por Yahoo Finance
            """)
            # Limpiar datos guardados si hay error
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
        st.markdown("""
        <div style='margin: 25px 0 15px 0;'>
            <span style='font-family: monospace; color: #FF006E; font-size: 1rem; letter-spacing: 2px; 
                        text-transform: uppercase; text-shadow: 0 0 15px rgba(255, 0, 110, 0.3);'>
                📊 MÉTRICAS PRINCIPALES
            </span>
        </div>
        """, unsafe_allow_html=True)
        display_metrics_panel(data)
        
        st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
        
        # =================================================================
        # GRÁFICO ESTILO GOOGLE FINANCE
        # =================================================================
        if not data.get('historico', pd.DataFrame()).empty:
            st.markdown("""
            <div style='margin: 20px 0 15px 0;'>
                <span style='font-family: monospace; color: #00FF9F; font-size: 1rem; letter-spacing: 2px; 
                            text-transform: uppercase; text-shadow: 0 0 15px rgba(0, 255, 159, 0.3);'>
                    📈 EVOLUCIÓN DEL PRECIO
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
                tendencia = "ALCISTA" if sma_corto > sma_largo else "BAJISTA" if sma_corto < sma_largo else "LATERAL"
                tendencia_color = "#00FF9F" if tendencia == "ALCISTA" else "#FF006E" if tendencia == "BAJISTA" else "#888"
                
                st.markdown("")
                
                # Widget de posición en rango - estilo retrofuturista
                st.markdown(f"""
                <div style='background: rgba(15, 15, 25, 0.9); border: 1px solid rgba(255,255,255,0.1); 
                            border-radius: 8px; padding: 20px; margin: 10px 0; font-family: monospace;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <div>
                            <span style='color: #555; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px;'>
                                POSICIÓN EN RANGO {periodo_seleccionado}
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
                            ◈ TENDENCIA: {tendencia}
                        </div>
                        <div style='color: #888; font-size: 0.8rem;'>
                            {posicion_rango:.0f}% del rango
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Métricas en grid compacto
                st.markdown(f"""
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 15px 0; font-family: monospace;'>
                    <div style='background: rgba(0, 255, 159, 0.05); border: 1px solid rgba(0, 255, 159, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>MÁXIMO</div>
                        <div style='color: #00FF9F; font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>${precio_max_periodo:,.2f}</div>
                    </div>
                    <div style='background: rgba(255, 0, 110, 0.05); border: 1px solid rgba(255, 0, 110, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>MÍNIMO</div>
                        <div style='color: #FF006E; font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>${precio_min_periodo:,.2f}</div>
                    </div>
                    <div style='background: rgba(100, 100, 255, 0.05); border: 1px solid rgba(100, 100, 255, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>VOL. PROM</div>
                        <div style='color: #6464FF; font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>{volumen_promedio/1e6:.1f}M</div>
                    </div>
                    <div style='background: rgba(255, 183, 77, 0.05); border: 1px solid rgba(255, 183, 77, 0.2); 
                                border-radius: 6px; padding: 12px; text-align: center;'>
                        <div style='color: #555; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;'>VOLATILIDAD</div>
                        <div style='color: {"#00FF9F" if volatilidad_pct < 3 else "#FFB74D" if volatilidad_pct < 5 else "#FF006E"}; 
                                    font-size: 1.2rem; font-weight: 400; margin-top: 4px;'>{volatilidad_pct:.1f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Calcular rendimientos
                hist_completo = data['historico'].copy()
                hist_completo = hist_completo.sort_index()
                precio_actual_rend = hist_completo['Close'].iloc[-1]
                
                periodos_calc = [("1S", 5), ("1M", 22), ("3M", 66), ("6M", 132), ("1A", 252), ("YTD", "ytd")]
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
                    <div style='color: #555; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;'>RENDIMIENTO HISTÓRICO</div>
                    <div style='display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px;'>{rend_divs}</div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.warning("⚠️ No hay suficientes datos para el período seleccionado")
        else:
            st.warning("⚠️ No hay datos históricos disponibles para mostrar el gráfico")
        
        st.markdown("---")
        
        # Análisis con IA - Estilo retrofuturista
        st.markdown("""
        <div style='margin: 30px 0 20px 0;'>
            <span style='font-family: "JetBrains Mono", monospace; color: #FF006E; font-size: 1.2rem; 
                        letter-spacing: 3px; text-transform: uppercase; text-shadow: 0 0 20px rgba(255, 0, 110, 0.4);'>
                🤖 ANÁLISIS INGENIERO BROKER
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if api_key:
            # Usar caché para el análisis de IA
            cache_key = f"ai_analysis_{ticker}"
            if cache_key not in st.session_state:
                with st.spinner("🧠 El Ingeniero Broker está analizando los datos..."):
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
            if st.button("🔄 Regenerar Análisis", key="regenerate_ai"):
                if cache_key in st.session_state:
                    del st.session_state[cache_key]
                st.rerun()
            
            # Disclaimer retrofuturista
            st.markdown("""
            <div style='background: rgba(255, 183, 77, 0.1); border: 1px solid rgba(255, 183, 77, 0.3); 
                        border-radius: 8px; padding: 15px; margin-top: 20px; font-family: monospace;'>
                <span style='color: #FFB74D; font-size: 0.75rem;'>⚠ DISCLAIMER:</span>
                <span style='color: rgba(255,255,255,0.6); font-size: 0.75rem;'> 
                    Este análisis es generado por IA con fines educativos. No constituye asesoramiento financiero. 
                    Siempre haz tu propia investigación antes de invertir.
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: rgba(255, 0, 110, 0.1); border: 1px solid rgba(255, 0, 110, 0.3);
                        border-radius: 8px; padding: 20px; font-family: monospace;'>
                <div style='color: #FF006E; font-size: 0.85rem; margin-bottom: 10px;'>⚠ API Key no configurada</div>
                <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>
                    Para obtener el análisis del Ingeniero Broker, introduce tu API Key de Groq en la barra lateral.<br>
                    Los datos financieros ya están disponibles arriba.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar los datos crudos como alternativa
            with st.expander("📋 Ver datos crudos para análisis manual"):
                prompt = build_analysis_prompt(data, ticker)
                st.code(prompt, language="text")
    
    # Mensaje si se presiona analizar sin ticker
    elif analyze_button and not ticker_input:
        st.markdown("""
        <div style='background: rgba(255, 183, 77, 0.1); border: 1px solid rgba(255, 183, 77, 0.3);
                    border-radius: 8px; padding: 15px; font-family: monospace; text-align: center;'>
            <span style='color: #FFB74D;'>⚠ Por favor, introduce un ticker para analizar</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer retrofuturista
    st.markdown("""
    <div style='margin-top: 50px; padding: 30px 0; border-top: 1px solid rgba(0, 255, 159, 0.1);'>
        <div style='text-align: center; font-family: monospace;'>
            <div style='color: rgba(255,255,255,0.4); font-size: 0.7rem; letter-spacing: 2px; margin-bottom: 10px;'>
                Basado en la metodología de <span style='color: #00FF9F;'>PETER LYNCH</span>
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
