# 🎯 Ingeniero Broker - Analizador de Inversiones Peter Lynch

Aplicación web que automatiza el análisis de inversiones basado en la metodología de **Peter Lynch** ("Un paso por delante de Wall Street"), utilizando IA (Google Gemini) para generar veredictos de inversión.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Características

- **📊 Datos en tiempo real**: Obtiene métricas financieras actualizadas via Yahoo Finance
- **📈 Gráficos interactivos**: Visualización del precio con media móvil de 50 días
- **🧠 Análisis con IA**: Veredicto automático usando Google Gemini con personalidad de "Ingeniero Broker"
- **📰 Scuttlebutt**: Muestra las últimas noticias de la empresa
- **🎯 Metodología Lynch**: Aplica las reglas del PEG ratio y clasificación de empresas

## 📋 Requisitos Previos

- Python 3.9 o superior
- Conexión a Internet
- API Key de Google Gemini (gratuita)

## 🔑 Obtener API Key de Google Gemini

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Create API Key"**
4. Copia la API Key generada
5. ¡Listo! Úsala en la aplicación

> **Nota**: La API de Gemini tiene un generoso tier gratuito que es suficiente para uso personal.

## ⚙️ Instalación

### 1. Clonar o descargar el proyecto

```bash
cd FinancialApp
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Cómo Usar

1. **Introduce tu API Key** de Gemini en la barra lateral izquierda
2. **Escribe un ticker** en el campo de búsqueda (ej: `AAPL`, `MSFT`, `KO`)
3. **Haz clic en "Analizar"** o usa los botones de ejemplo
4. **Revisa los resultados**:
   - Panel de métricas principales
   - Gráfico de evolución del precio
   - Últimas noticias
   - Análisis del Ingeniero Broker con veredicto

### Tickers de Ejemplo

| Ticker | Empresa | Mercado |
|--------|---------|---------|
| AAPL | Apple | NASDAQ |
| MSFT | Microsoft | NASDAQ |
| KO | Coca-Cola | NYSE |
| TSLA | Tesla | NASDAQ |
| IBE.MC | Iberdrola | Madrid |
| SAP.DE | SAP | Frankfurt |

## 📊 Métricas Analizadas

La aplicación obtiene y analiza:

- **Valoración**: PER (Trailing/Forward), PEG Ratio, Price/Book, Price/Sales
- **Dividendos**: Yield, Tasa, Payout Ratio
- **Balance**: Deuda total, Efectivo, Ratio Deuda/Equity
- **Rentabilidad**: ROE, ROA, Márgenes
- **Crecimiento**: Beneficios, Ingresos
- **Riesgo**: Beta

## 🎯 Metodología Peter Lynch

El "Ingeniero Broker" aplica las siguientes reglas:

### PEG Ratio (Price/Earnings to Growth)
- 🟢 **PEG < 1.0**: Empresa barata respecto a su crecimiento
- 🟡 **PEG 1.0 - 2.0**: Valoración justa
- 🔴 **PEG > 2.0**: Empresa cara

### Clasificación de Empresas
- 🚀 **Crecimiento Rápido**: Alto crecimiento, reinvierten beneficios
- 🏛️ **Estables**: Empresas grandes, crecimiento moderado, dividendos
- 🔄 **Cíclicas**: Dependen del ciclo económico
- 📈 **Recuperación**: En proceso de reestructuración
- 💎 **Activo Oculto**: Valor no reconocido en el balance

### Análisis de Deuda
- ✅ Más efectivo que deuda = Situación sólida
- ⚠️ Más deuda que efectivo = Precaución

## 🛠️ Stack Tecnológico

- **Frontend**: Streamlit
- **Datos Financieros**: yfinance (Yahoo Finance)
- **Gráficos**: Plotly
- **IA**: Google Gemini API (gemini-1.5-flash)
- **Procesamiento**: Pandas

## ⚠️ Disclaimer

**Este software es solo para fines educativos e informativos.**

- No constituye asesoramiento financiero, de inversión o fiscal
- Los resultados del análisis son generados por IA y pueden contener errores
- Siempre realiza tu propia investigación (DYOR)
- Consulta con un asesor financiero profesional antes de invertir
- El rendimiento pasado no garantiza resultados futuros

## 📄 Licencia

MIT License - Siéntete libre de usar, modificar y distribuir.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir cambios importantes.

---

**Desarrollado con ❤️ inspirado en la filosofía de inversión de Peter Lynch**

*"Invierte en lo que conoces"* - Peter Lynch
