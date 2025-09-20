#!/usr/bin/env python3
"""
Servicio de integración con API del clima
Utiliza OpenWeatherMap API para obtener datos meteorológicos
"""

import os
import requests
from typing import Dict
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class WeatherService:
    """Clase para manejar la integración con la API del clima"""

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"

        if not self.api_key:
            raise ValueError(
                "OPENWEATHER_API_KEY no encontrada en las variables de entorno"
            )

    def get_weather_by_city(self, city: str, country_code: str = None) -> Dict:
        """
        Obtiene el clima actual de una ciudad específica

        Args:
            city (str): Nombre de la ciudad
            country_code (str, optional): Código del país (ej: 'ES', 'US')

        Returns:
            Dict: Datos del clima o mensaje de error
        """
        try:
            # Construir parámetros de búsqueda
            if country_code:
                query = f"{city},{country_code}"
            else:
                query = city

            # Parámetros de la API
            params = {
                "q": query,
                "appid": self.api_key,
                "units": "metric",  # Temperatura en Celsius
                "lang": "es",  # Respuesta en español
            }

            # Realizar petición a la API
            response = requests.get(
                f"{self.base_url}/weather", params=params, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return self._format_weather_data(data)
            else:
                return {
                    "error": True,
                    "message": f"Error {response.status_code}: {response.text}",
                }

        except requests.exceptions.RequestException as e:
            return {"error": True, "message": f"Error de conexión: {str(e)}"}
        except Exception as e:
            return {"error": True, "message": f"Error inesperado: {str(e)}"}

    def get_weather_by_coordinates(self, lat: float, lon: float) -> Dict:
        """
        Obtiene el clima actual por coordenadas geográficas

        Args:
            lat (float): Latitud
            lon (float): Longitud

        Returns:
            Dict: Datos del clima o mensaje de error
        """
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es",
            }

            response = requests.get(
                f"{self.base_url}/weather", params=params, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return self._format_weather_data(data)
            else:
                return {
                    "error": True,
                    "message": f"Error {response.status_code}: {response.text}",
                }

        except requests.exceptions.RequestException as e:
            return {"error": True, "message": f"Error de conexión: {str(e)}"}
        except Exception as e:
            return {"error": True, "message": f"Error inesperado: {str(e)}"}

    def get_forecast(self, city: str, days: int = 5) -> Dict:
        """
        Obtiene el pronóstico del clima para varios días

        Args:
            city (str): Nombre de la ciudad
            days (int): Número de días (máximo 5)

        Returns:
            Dict: Pronóstico del clima o mensaje de error
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es",
                "cnt": days * 8,  # 8 mediciones por día (cada 3 horas)
            }

            response = requests.get(
                f"{self.base_url}/forecast", params=params, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return self._format_forecast_data(data, days)
            else:
                return {
                    "error": True,
                    "message": f"Error {response.status_code}: {response.text}",
                }

        except requests.exceptions.RequestException as e:
            return {"error": True, "message": f"Error de conexión: {str(e)}"}
        except Exception as e:
            return {"error": True, "message": f"Error inesperado: {str(e)}"}

    def _format_weather_data(self, data: Dict) -> Dict:
        """Formatea los datos del clima en un formato más legible"""
        return {
            "error": False,
            "ciudad": data["name"],
            "pais": data["sys"]["country"],
            "temperatura": f"{data['main']['temp']:.1f}°C",
            "sensacion_termica": f"{data['main']['feels_like']:.1f}°C",
            "humedad": f"{data['main']['humidity']}%",
            "presion": f"{data['main']['pressure']} hPa",
            "descripcion": data["weather"][0]["description"].title(),
            "velocidad_viento": f"{data['wind']['speed']} m/s",
            "visibilidad": f"{data.get('visibility', 'N/A')} m",
            "coordenadas": {"lat": data["coord"]["lat"], "lon": data["coord"]["lon"]},
        }

    def _format_forecast_data(self, data: Dict, days: int) -> Dict:
        """Formatea los datos del pronóstico"""
        forecast_list = []

        for item in data["list"][: days * 8 : 8]:  # Una medición por día
            forecast_list.append(
                {
                    "fecha": item["dt_txt"],
                    "temperatura": f"{item['main']['temp']:.1f}°C",
                    "descripcion": item["weather"][0]["description"].title(),
                    "humedad": f"{item['main']['humidity']}%",
                    "velocidad_viento": f"{item['wind']['speed']} m/s",
                }
            )

        return {
            "error": False,
            "ciudad": data["city"]["name"],
            "pais": data["city"]["country"],
            "pronostico": forecast_list,
        }


def main():
    """Función de prueba para el servicio del clima"""
    try:
        weather = WeatherService()

        # Ejemplo de uso
        print("=== Servicio del Clima ===")

        # Obtener clima por ciudad
        result = weather.get_weather_by_city("Madrid", "ES")

        if not result.get("error"):
            print(f"\n🌤️  Clima en {result['ciudad']}, {result['pais']}")
            print(f"🌡️  Temperatura: {result['temperatura']}")
            print(f"🤔 Sensación térmica: {result['sensacion_termica']}")
            print(f"💧 Humedad: {result['humedad']}")
            print(f"📊 Presión: {result['presion']}")
            print(f"🌬️  Viento: {result['velocidad_viento']}")
            print(f"👁️  Visibilidad: {result['visibilidad']}")
            print(f"📝 Descripción: {result['descripcion']}")
        else:
            print(f"❌ Error: {result['message']}")

    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
