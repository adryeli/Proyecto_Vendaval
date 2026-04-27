
#Cada alerta es una clase, es decir, un objeto distinto con su mensaje, nombre. Ademas usan el mismo metodo, por lo que podemos usar polimorfismo 
#Reglas

##mirar coincidir nombres alertas con el diccionario de resultados que estableceremos 

class TempAlert:
    name = "temp_alert"
    message = "Alarma: Riesgo de temperatura"

    def check(self, record):
        return record.temperatura < -8 or record.temperatura > 40
    

class WindAlert:
    name = "wind_alert"
    message = "Alarma: Riesgo de viento alto"

    def check(self, record):
        return record.viento_velocidad >= 70
    

class HumidityAlert:
    name = "humidity_alert"
    message = "Alarma: Riesgo de humedad"

    def check(self, record):
        return (0 < record.humedad_nivel <= 20) or (70 < record.humedad_nivel <= 100)


class HeavyRain:
    name = "heavy_rain"
    message = "Alarma: Lluvia fuerte"

    def check(self, record):
        return 10 < record.precipitation <= 30


class HeavyRainRiskAlert:
    name = "heavy_rain_risk_alert"
    message = "Alarma: Riesgo de precipitaciones intensas"

    def check(self, record):
        return record.precipitation > 30

 #implementamos las alertas, con polimorfismo, no importa que tipo de alerta sea, todas tienen el metodo check   

class AlertSystem:
    def __init__(self):
        self.alerts = [TempAlert(), WindAlert(), HumidityAlert(), HeavyRain(), HeavyRainRiskAlert()]

    
    def check(self, record):
        messages = []
        results = {}

        for alert in self.alerts:
            active = alert.check(record)
            results[alert.name] = active
            if active:
                messages.append(alert.message)

        return {
            "mensajes": messages,
            "resultados": results
        }
