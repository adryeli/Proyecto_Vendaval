
#Cada alerta es una clase, es decir, un objeto distinto con su mensaje, nombre. Ademas usan el mismo metodo, por lo que podemos usar polimorfismo 
#Reglas

##mirar coincidir nombres alertas con el diccionario de resultados que estableceremos 

class TempAlert:
    name = "temp_alert"
    message = "Alarma: Riesgo de temperatura"

    def check(self, record):
        return record["temperature_c"] < -8 or record["temperature_c"] > 40
    

class WindAlert:
    name = "wind_alert"
    message = "Alarma: Riesgo de viento alto"

    def check(self, record):
        return record["wind_kph"] >= 70
    

class HumidityAlert:
    name = "humidity_alert"
    message = "Alarma: Riesgo de humedad"

    def check(self, record):
        return (0 < record["humidity_pct"] <= 20) or (70 < record["humidity_pct"] <= 100)


class HeavyRainAlert:
    name = "heavy_rain_alert"
    message = "Alarma: Lluvia fuerte"

    def check(self, record):
        return 10 < record["rain_mm"] <= 30


class HeavyRainRiskAlert:
    name = "heavy_rain_risk_alert"
    message = "Alarma: Riesgo de precipitaciones intensas"

    def check(self, record):
        return record["rain_mm"] > 30

 #implementamos las alertas, con polimorfismo, no importa que tipo de alerta sea, todas tienen el metodo check   

class AlertSystem:
    def __init__(self):
        self.alerts = [TempAlert(), WindAlert(), HumidityAlert(), HeavyRainAlert(), HeavyRainRiskAlert()]

    
    def check(self, record):
        messages = []
        results = {}

        for alert in self.alerts:
            active = alert.check(record)
            results[alert.name] = active
            if active:
                messages.append(alert.message)

        return {
            "messages": messages,
            "results": results
        }
