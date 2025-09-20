# Guía de Integración con API del Clima

## Descripción

Este proyecto incluye una integración completa con la API de OpenWeatherMap para obtener datos meteorológicos en tiempo real y pronósticos del clima.

## Características

- ✅ Clima actual por ciudad
- ✅ Clima actual por coordenadas geográficas
- ✅ Pronóstico de 5 días
- ✅ Integración con OpenAI para respuestas contextuales
- ✅ Manejo de errores robusto
- ✅ Respuestas en español

## Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Obtener API Key de OpenWeatherMap

1. Ve a [OpenWeatherMap](https://openweathermap.org/api)
2. Regístrate para obtener una cuenta gratuita
3. Obtén tu API key gratuita (1000 llamadas/día)

### 3. Configurar variables de entorno

Copia el archivo `env.example` a `.env` y configura tus claves:

```bash
cp env.example .env
```

Edita el archivo `.env`:

```env
# Configuración de OpenAI
OPENAI_API_KEY=tu_clave_de_openai_aqui

# Configuración de OpenWeatherMap
OPENWEATHER_API_KEY=tu_clave_de_openweather_aqui
```

## Uso

### Ejecutar el demo completo

```bash
python src/main.py
```

### Uso programático

```python
from weather_service import WeatherService

# Inicializar el servicio
weather = WeatherService()

# Obtener clima actual
clima = weather.get_weather_by_city("Madrid", "ES")
print(clima)

# Obtener pronóstico
pronostico = weather.get_forecast("Barcelona", 3)
print(pronostico)
```

### Funciones disponibles en main.py

```python
# Obtener información del clima
weather_info = get_weather_info("Madrid", "ES")

# Obtener pronóstico
forecast = get_weather_forecast("Barcelona", 3)

# Chat con IA incluyendo contexto del clima
weather_context = get_weather_info("Valencia", "ES")
# Usar weather_context en tus mensajes de OpenAI
```

## Estructura de datos

### Clima actual

```python
{
    'error': False,
    'ciudad': 'Madrid',
    'pais': 'ES',
    'temperatura': '22.5°C',
    'sensacion_termica': '24.1°C',
    'humedad': '65%',
    'presion': '1013 hPa',
    'descripcion': 'Cielos Despejados',
    'velocidad_viento': '3.2 m/s',
    'visibilidad': '10000 m',
    'coordenadas': {
        'lat': 40.4168,
        'lon': -3.7038
    }
}
```

### Pronóstico

```python
{
    'error': False,
    'ciudad': 'Barcelona',
    'pais': 'ES',
    'pronostico': [
        {
            'fecha': '2024-01-15 12:00:00',
            'temperatura': '18.5°C',
            'descripcion': 'Parcialmente Nublado',
            'humedad': '70%',
            'velocidad_viento': '2.1 m/s'
        },
        # ... más días
    ]
}
```

## Manejo de errores

El servicio incluye manejo robusto de errores:

- Errores de conexión
- Errores de API (ciudad no encontrada, límites excedidos)
- Errores de configuración (API key faltante)
- Timeouts de red

Todos los errores se devuelven en formato:

```python
{
    'error': True,
    'message': 'Descripción del error'
}
```

## Límites de la API gratuita

- **OpenWeatherMap Free**: 1000 llamadas/día
- **OpenAI**: Según tu plan

## Personalización

### Cambiar idioma

Modifica el parámetro `lang` en `weather_service.py`:

```python
params = {
    'lang': 'es'  # Cambiar a 'en', 'fr', etc.
}
```

### Cambiar unidades

Modifica el parámetro `units` en `weather_service.py`:

```python
params = {
    'units': 'metric'  # 'metric', 'imperial', 'kelvin'
}
```

## Troubleshooting

### Error: "OPENWEATHER_API_KEY no encontrada"

- Verifica que el archivo `.env` existe
- Verifica que la variable `OPENWEATHER_API_KEY` está configurada
- Reinicia tu aplicación después de cambiar `.env`

### Error: "Error 401: Unauthorized"

- Verifica que tu API key de OpenWeatherMap es correcta
- Asegúrate de que tu cuenta esté activa

### Error: "Error 404: Not Found"

- Verifica que el nombre de la ciudad es correcto
- Usa el código del país para mayor precisión: "Madrid,ES"

### Error de conexión

- Verifica tu conexión a internet
- Verifica que no hay firewall bloqueando las peticiones
