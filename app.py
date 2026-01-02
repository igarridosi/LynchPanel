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
# ESTILOS CSS PERSONALIZADOS
# =============================================================================
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #00D4AA;
    }
    .metric-title {
        color: #888;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #FFF;
        font-size: 24px;
        font-weight: bold;
    }
    .verdict-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid #00D4AA;
    }
    .stAlert {
        background-color: #2D2D2D;
    }
    .classification-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        margin: 5px 0;
    }
    .badge-crecimiento {
        background: linear-gradient(135deg, #00C853, #00E676);
        color: #000;
    }
    .badge-estable {
        background: linear-gradient(135deg, #1565C0, #42A5F5);
        color: #FFF;
    }
    .badge-ciclica {
        background: linear-gradient(135deg, #FF6F00, #FFB300);
        color: #000;
    }
    .badge-recuperacion {
        background: linear-gradient(135deg, #7B1FA2, #BA68C8);
        color: #FFF;
    }
    .badge-activo-oculto {
        background: linear-gradient(135deg, #FFD700, #FFF176);
        color: #000;
    }
    .peg-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        margin-left: 10px;
    }
    .peg-barato {
        background-color: #00C853;
        color: #000;
    }
    .peg-justo {
        background-color: #FFB300;
        color: #000;
    }
    .peg-caro {
        background-color: #FF5252;
        color: #FFF;
    }
    .sidebar-item-active {
        background-color: rgba(0, 212, 170, 0.2);
        border-radius: 8px;
        padding: 5px 10px;
        border-left: 3px solid #00D4AA;
    }
    .sidebar-item {
        padding: 5px 10px;
        opacity: 0.6;
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
            
            # Dividendos - múltiples fuentes
            "dividend_yield": safe_get(info, "dividendYield"),  # Puede venir como decimal 0.0076
            "trailing_annual_dividend_yield": safe_get(info, "trailingAnnualDividendYield"),  # Yield anual trailing
            "dividend_rate": safe_get(info, "dividendRate"),
            "five_year_avg_dividend_yield": safe_get(info, "fiveYearAvgDividendYield"),
            "payout_ratio": safe_get(info, "payoutRatio"),
            
            # Balance y deuda
            "deuda_total": safe_get(info, "totalDebt"),
            "efectivo_total": safe_get(info, "totalCash"),
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
        
        # Obtener historial de precios (1 año)
        try:
            hist = ticker.history(period="1y")
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
    
    # Calcular ratio deuda/efectivo
    deuda = data.get('deuda_total')
    efectivo = data.get('efectivo_total')
    if deuda != "N/A" and efectivo != "N/A" and efectivo and float(efectivo) > 0:
        ratio_deuda_efectivo = float(deuda) / float(efectivo)
        situacion_deuda = "MÁS DEUDA QUE EFECTIVO ⚠️" if ratio_deuda_efectivo > 1 else "Más efectivo que deuda ✅"
    else:
        ratio_deuda_efectivo = "N/A"
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

🏦 BALANCE Y DEUDA:
   • Deuda Total: {format_large_number(data.get('deuda_total'))}
   • Efectivo Total: {format_large_number(data.get('efectivo_total'))}
   • Ratio Deuda/Equity: {data.get('deuda_equity', 'N/A')}
   • ⚡ Situación: {situacion_deuda}

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


def create_price_chart(historico, ticker, nombre):
    """
    Crea un gráfico interactivo con la evolución del precio.
    
    Args:
        historico: DataFrame con el historial de precios
        ticker: Símbolo del ticker
        nombre: Nombre de la empresa
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    # Añadir línea de precio de cierre
    fig.add_trace(go.Scatter(
        x=historico.index,
        y=historico['Close'],
        mode='lines',
        name='Precio de Cierre',
        line=dict(color='#00D4AA', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 170, 0.1)'
    ))
    
    # Añadir media móvil de 50 días
    if len(historico) >= 50:
        ma50 = historico['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=historico.index,
            y=ma50,
            mode='lines',
            name='Media Móvil 50d',
            line=dict(color='#FFD700', width=1, dash='dash')
        ))
    
    # Configurar layout
    fig.update_layout(
        title=f"📈 Evolución del Precio - {nombre} ({ticker}) - Último Año",
        xaxis_title="Fecha",
        yaxis_title="Precio ($)",
        template="plotly_dark",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=400
    )
    
    return fig


def display_metrics_panel(data):
    """
    Muestra el panel de métricas principales en formato de tarjetas.
    
    Args:
        data: Diccionario con los datos financieros
    """
    # Primera fila de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        precio = data.get('precio_actual', 'N/A')
        if precio != 'N/A':
            st.metric(
                label="💰 Precio Actual",
                value=f"${precio:.2f}",
                delta=None
            )
        else:
            st.metric(label="💰 Precio Actual", value="N/A")
    
    with col2:
        per = data.get('per_trailing', 'N/A')
        if per != 'N/A':
            st.metric(
                label="📊 PER (Trailing)",
                value=f"{per:.2f}",
                delta="Alto" if per > 25 else "Normal" if per > 15 else "Bajo",
                delta_color="inverse" if per > 25 else "normal"
            )
        else:
            st.metric(label="📊 PER (Trailing)", value="N/A")
    
    with col3:
        peg = data.get('peg_ratio')
        peg_calculation = data.get('peg_calculation', 'Cálculo no disponible')
        if peg is not None and peg != 'N/A':
            try:
                peg_val = float(peg)
                if peg_val < 1:
                    delta_text = "¡Barato! 🟢"
                    delta_color = "normal"
                elif peg_val > 2:
                    delta_text = "Caro 🔴"
                    delta_color = "inverse"
                else:
                    delta_text = "Justo 🟡"
                    delta_color = "off"
                st.metric(
                    label=f"⭐ PEG Ratio",
                    value=f"{peg_val:.2f}",
                    delta=delta_text,
                    delta_color=delta_color,
                    help=f"📊 Cálculo: {peg_calculation}"
                )
            except (ValueError, TypeError):
                st.metric(label="⭐ PEG Ratio", value="N/A", help=f"ℹ️ {peg_calculation}")
        else:
            st.metric(label="⭐ PEG Ratio", value="N/A", help=f"ℹ️ {peg_calculation}")
    
    with col4:
        # Intentar obtener dividend yield de múltiples fuentes
        div = data.get('dividend_yield')
        div_trailing = data.get('trailing_annual_dividend_yield')
        
        # Priorizar trailing_annual_dividend_yield si está disponible
        div_value = None
        div_source = ""
        
        # Función helper para validar
        def is_valid_div(val):
            if val is None or val == 'N/A':
                return False
            try:
                v = float(val)
                return not pd.isna(v) and v > 0
            except:
                return False
        
        if is_valid_div(div_trailing):
            div_value = float(div_trailing)
            div_source = "Trailing Annual"
        elif is_valid_div(div):
            div_value = float(div)
            div_source = "Current"
        
        if div_value is not None:
            # Convertir a porcentaje si viene como decimal
            if div_value < 0.5:  # Probablemente viene como decimal (0.0076 = 0.76%)
                display_div = div_value * 100
            else:
                display_div = div_value
            
            # Validar que el dividendo sea razonable (entre 0 y 15%)
            if 0 < display_div < 15:
                st.metric(
                    label="💵 Dividend Yield",
                    value=f"{display_div:.2f}%",
                    help=f"Fuente: {div_source}"
                )
            else:
                st.metric(label="💵 Dividend Yield", value="N/A", help="Valor fuera de rango")
        else:
            st.metric(label="💵 Dividend Yield", value="N/A", help="No hay dividendos")
    
    # Segunda fila de métricas
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        pb = data.get('price_to_book', 'N/A')
        if pb != 'N/A':
            st.metric(label="📚 Price/Book", value=f"{pb:.2f}")
        else:
            st.metric(label="📚 Price/Book", value="N/A")
    
    with col6:
        mcap = data.get('market_cap', 'N/A')
        st.metric(label="🏛️ Market Cap", value=format_large_number(mcap))
    
    with col7:
        deuda = data.get('deuda_total', 'N/A')
        efectivo = data.get('efectivo_total', 'N/A')
        if deuda != 'N/A' and efectivo != 'N/A' and efectivo and float(efectivo) > 0:
            ratio = float(deuda) / float(efectivo)
            emoji = "⚠️" if ratio > 1 else "✅"
            st.metric(label=f"💳 Deuda/Efectivo {emoji}", value=f"{ratio:.2f}x")
        else:
            st.metric(label="💳 Deuda/Efectivo", value="N/A")
    
    with col8:
        beta = data.get('beta', 'N/A')
        if beta != 'N/A':
            st.metric(label="📉 Beta", value=f"{beta:.2f}")
        else:
            st.metric(label="📉 Beta", value="N/A")


# =============================================================================
# INTERFAZ PRINCIPAL DE LA APLICACIÓN
# =============================================================================

def main():
    """Función principal que ejecuta la aplicación Streamlit."""
    
    # Header principal
    st.title("🎯 Ingeniero Broker")
    st.markdown("### Analizador de Inversiones estilo Peter Lynch")
    st.markdown("*\"Compra lo que conoces\" - Peter Lynch*")
    st.markdown("---")
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # API Key de Groq
        st.markdown("#### 🔑 API de Groq (Gratis)")
        api_key = st.text_input(
            "Introduce tu API Key:",
            type="password",
            help="Obtén tu API Key en: https://console.groq.com/keys"
        )
        
        if not api_key:
            st.warning("⚠️ Necesitas una API Key de Groq para el análisis IA")
            st.markdown("""
            **¿Cómo obtenerla? (GRATIS)**
            1. Ve a [Groq Console](https://console.groq.com/keys)
            2. Crea una cuenta gratuita
            3. Genera una nueva API Key
            4. Cópiala y pégala aquí
            
            ✅ **Límites gratuitos:** 30 req/min, 14,400 req/día
            """)
        
        st.markdown("---")
        
        # Info sobre la metodología
        st.markdown("#### 📚 Metodología Peter Lynch")
        st.markdown("""
        **Reglas del Ingeniero Broker:**
        
        🟢 **PEG < 1.0**: Barato  
        🟡 **PEG 1.0-2.0**: Justo  
        🔴 **PEG > 2.0**: Caro  
        """)
        
        # Clasificaciones - se actualizará dinámicamente
        st.markdown("**Clasificaciones Lynch:**")
        
        # Guardar placeholder para actualizar después
        classification_placeholder = st.empty()
        
        st.markdown("---")
        st.markdown("*Desarrollado con ❤️ usando Streamlit, yfinance y Groq AI*")
    
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
    
    # Input del ticker
    col_input1, col_input2 = st.columns([3, 1])
    
    with col_input1:
        ticker_input = st.text_input(
            "🔍 Introduce el Ticker de la acción:",
            placeholder="Ej: AAPL, KO, MSFT, IBE.MC, TSLA...",
            help="Introduce el símbolo de la acción. Para mercados europeos añade el sufijo (ej: IBE.MC para Iberdrola)"
        )
    
    with col_input2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🚀 Analizar", type="primary", use_container_width=True)
    
    # Ejemplos rápidos
    st.markdown("**Ejemplos rápidos:** ", unsafe_allow_html=True)
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
        else:
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
            
            # Panel de métricas
            st.markdown("### 📊 Métricas Principales")
            display_metrics_panel(data)
            
            st.markdown("---")
            
            # Gráfico de precios
            if not data.get('historico', pd.DataFrame()).empty:
                st.markdown("### 📈 Evolución del Precio (1 año)")
                fig = create_price_chart(
                    data['historico'],
                    ticker,
                    data.get('nombre', ticker)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ No hay datos históricos disponibles para mostrar el gráfico")
            
            st.markdown("---")
            
            # Noticias recientes (Scuttlebutt)
            if data.get('noticias'):
                st.markdown("### 📰 Últimas Noticias (Scuttlebutt)")
                for noticia in data['noticias'][:3]:
                    titulo = noticia.get('title', 'Sin título')
                    link = noticia.get('link', '#')
                    publisher = noticia.get('publisher', 'Fuente desconocida')
                    st.markdown(f"- [{titulo}]({link}) - *{publisher}*")
                st.markdown("---")
            
            # Análisis con IA
            st.markdown("### 🤖 Análisis del Ingeniero Broker (IA)")
            
            if api_key:
                with st.spinner("🧠 El Ingeniero Broker está analizando los datos..."):
                    # Construir el prompt
                    prompt = build_analysis_prompt(data, ticker)
                    
                    # Obtener análisis de Groq (Llama 3.3 70B)
                    analysis = get_ai_analysis(prompt, api_key)
                
                # Mostrar el análisis
                st.markdown("""
                <div class="verdict-box">
                """, unsafe_allow_html=True)
                st.markdown(analysis)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Disclaimer
                st.markdown("""
                ---
                ⚠️ **Disclaimer:** Este análisis es generado por IA con fines educativos. 
                No constituye asesoramiento financiero. Siempre haz tu propia investigación 
                antes de invertir y consulta con un profesional financiero.
                """)
            else:
                st.warning("""
                ⚠️ **API Key no configurada**
                
                Para obtener el análisis del Ingeniero Broker, introduce tu API Key de Groq en la barra lateral.
                
                Los datos financieros ya están disponibles arriba. Solo falta el análisis de IA.
                """)
                
                # Mostrar los datos crudos como alternativa
                with st.expander("📋 Ver datos crudos para análisis manual"):
                    prompt = build_analysis_prompt(data, ticker)
                    st.code(prompt, language="text")

    elif analyze_button and not ticker_input:
        st.warning("⚠️ Por favor, introduce un ticker para analizar")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📚 Basado en la metodología de <b>Peter Lynch</b> - "Un paso por delante de Wall Street"</p>
        <p>🛠️ Desarrollado con Streamlit | 📊 Datos de Yahoo Finance | 🧠 IA por Groq (Llama 3.3)</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    main()
