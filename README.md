# 🎯 Ingeniero Broker - Analizador de Inversiones Peter Lynch

Aplicación web que automatiza el análisis de inversiones basado en la metodología de **Peter Lynch** ("Un paso por delante de Wall Street"), utilizando IA (**Groq - Llama 3.3**) para generar veredictos de inversión con análisis inteligente.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Características

- **📊 Datos en tiempo real**: Obtiene métricas financieras actualizadas via Yahoo Finance
- **📈 Gráficos interactivos**: Visualización del precio con media móvil de 50 días
- **🧠 Análisis con IA**: Veredicto automático usando **Groq (Llama 3.3 70B)** con personalidad de "Ingeniero Broker"
- **⚡ Ultra rápido**: Groq ofrece las respuestas de IA más rápidas del mercado
- **📰 Scuttlebutt**: Muestra las últimas noticias de la empresa
- **🎯 Metodología Lynch**: Aplica las reglas del PEG ratio y clasificación de empresas
- **🔄 Clasificación automática**: Detecta si la empresa es de Crecimiento Rápido, Estable, Cíclica, Recuperación o Activo Oculto
- **💰 Cálculo preciso del PEG**: Usa el `trailingPegRatio` de Yahoo Finance con growth de 5 años

## 📋 Requisitos Previos

- Python 3.9 o superior
- Conexión a Internet
- API Key de Groq (**100% GRATUITA**)

## 🔑 Obtener API Key de Groq (GRATIS)

1. Ve a [Groq Console](https://console.groq.com/keys)
2. Crea una cuenta gratuita (puedes usar tu cuenta de Google)
3. Haz clic en **"Create API Key"**
4. Dale un nombre a tu key y cópiala
5. ¡Listo! Úsala en la aplicación

> **Límites generosos gratuitos:**
> - ✅ **30 requests/minuto**
> - ✅ **14,400 requests/día**
> - ✅ Sin tarjeta de crédito requerida
> - ✅ Acceso al modelo **Llama 3.3 70B** (uno de los mejores modelos open source)

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
python -m streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

> **Nota**: En Windows, usa `python -m streamlit run app.py` en lugar de solo `streamlit run app.py` para evitar problemas con el PATH.

## 📖 Cómo Usar

1. **Introduce tu API Key** de Groq en la barra lateral izquierda
2. **Escribe un ticker** en el campo de búsqueda (ej: `AAPL`, `MSFT`, `KO`, `V`)
3. **Haz clic en "Analizar"** o usa los botones de ejemplo
4. **Revisa los resultados**:
   - Badge de clasificación Lynch (Crecimiento Rápido, Estable, Cíclica, etc.)
   - PEG Ratio calculado con growth de 5 años
   - Panel de métricas principales (precio, PER, PEG, dividendo)
   - Gráfico de evolución del precio
   - Últimas noticias
   - Análisis completo del Ingeniero Broker con veredicto COMPRAR/VENDER/MANTENER

### Tickers de Ejemplo

| Ticker | Empresa | Mercado |
|--------|---------|---------|
| AAPL | Apple | NASDAQ |
| MSFT | Microsoft | NASDAQ |
| KO | Coca-Cola | NYSE |
| TSLA | Tesla | NASDAQ |
| V | Visa | NYSE |
| PG | Procter & Gamble | NYSE |
| DUOL | Duolingo | NASDAQ |
| IBE.MC | Iberdrola | Madrid |
| SAP.DE | SAP | Frankfurt |

## 📊 Métricas Analizadas

La aplicación obtiene y analiza más de 40 métricas financieras:

- **Valoración**: PER (Trailing/Forward), **PEG Ratio** (calculado con growth 5Y), Price/Book, Price/Sales
- **Dividendos**: Yield, Tasa Anual, Payout Ratio, Promedio 5 años
- **Balance**: Deuda total, Efectivo, Ratio Deuda/Equity, Deuda/Efectivo
- **Rentabilidad**: ROE, ROA, Márgenes (beneficio, operativo)
- **Crecimiento**: Beneficios, Ingresos, EPS Forward, Crecimiento trimestral
- **Riesgo**: Beta, Volatilidad

### 🎯 PEG Ratio Mejorado

El PEG se calcula usando:
1. **`trailingPegRatio`** de Yahoo Finance (usa growth estimates de 5 años de analistas)
2. **Cálculo manual** con Forward EPS Growth si no está disponible
3. Muestra el **cálculo detallado** al pasar el cursor sobre el símbolo de ayuda (?)

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

- **Frontend**: Streamlit 1.28+
- **Datos Financieros**: yfinance (Yahoo Finance API)
- **Gráficos**: Plotly (interactivos con zoom y hover)
- **IA**: Groq API con **Llama 3.3 70B Versatile**
- **Procesamiento**: Pandas
- **Lenguaje**: Python 3.9+

### ¿Por qué Groq?

| Característica | Groq | Google Gemini |
|---------------|------|---------------|
| **Velocidad** | ⚡ Ultra rápido (< 1s) | Normal (2-5s) |
| **Límites gratuitos** | 14,400 req/día | ~60 req/día |
| **Calidad** | Llama 3.3 70B | Gemini Flash |
| **Sin restricciones** | ✅ | ❌ Muchas |

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

## 🐛 Problemas Conocidos y Soluciones

### Error: "streamlit no se reconoce como comando"
**Solución**: Usa `python -m streamlit run app.py` en lugar de `streamlit run app.py`

### PEG Ratio muestra N/A
El PEG requiere que Yahoo Finance tenga datos de crecimiento. Algunas empresas pequeñas o nuevas pueden no tener esta información disponible.

### Dividend Yield muestra N/A
Empresas que no pagan dividendos (como muchas tech de crecimiento) mostrarán N/A. Esto es normal.

---

**Desarrollado con ❤️ inspirado en la filosofía de inversión de Peter Lynch**

*"Invierte en lo que conoces"* - Peter Lynch

## 📸 Screenshots

### Análisis de Visa (V)
- PEG Ratio: 1.93 (Justo)
- Clasificación: Estable 🏛️
- Dividend Yield: 0.76%

### Análisis de Duolingo (DUOL)  
- PEG Ratio: Variable
- Clasificación: Crecimiento Rápido 🚀
- Sin dividendos (empresa de crecimiento)
