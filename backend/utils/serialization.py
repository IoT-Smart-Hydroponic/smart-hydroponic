from models.plant_data import SensorData
from models.environment_data import EnvironmentData
from models.actuator_data import ActuatorData
from models.user import User


def sensor_to_dict(obj: SensorData):
    return {
        "deviceid": obj.deviceid,
        "moisture1": obj.moisture1,
        "moisture2": obj.moisture2,
        "moisture3": obj.moisture3,
        "moisture4": obj.moisture4,
        "moisture5": obj.moisture5,
        "moisture6": obj.moisture6,
        "moistureavg": obj.moistureavg,
        "flowrate": obj.flowrate,
        "total_litres": obj.total_litres,
        "distance_cm": obj.distance_cm,
        "ph": obj.ph,
        "tds": obj.tds,
        "timestamp": obj.timestamp,
    }


def environment_to_dict(obj: EnvironmentData):
    return {
        "deviceid": obj.deviceid,
        "temperature_atas": obj.temperature_atas,
        "temperature_bawah": obj.temperature_bawah,
        "avg_temperature": obj.avg_temperature,
        "humidity_atas": obj.humidity_atas,
        "humidity_bawah": obj.humidity_bawah,
        "avg_humidity": obj.avg_humidity,
        "light_intensity_atas": obj.light_intensity_atas,
        "light_intensity_bawah": obj.light_intensity_bawah,
        "avg_light_intensity": obj.avg_light_intensity,
        "timestamp": obj.timestamp,
    }


def actuator_to_dict(obj: ActuatorData):
    return {
        "deviceid": obj.deviceid,
        "pumpStatus": obj.pumpStatus,
        "lightStatus": obj.lightStatus,
        "automationStatus": obj.automationStatus,
        "timestamp": obj.timestamp,
    }


def user_safe_dict(obj: User):
    return {
        "userid": str(obj.userid),
        "username": obj.username,
        "created_at": obj.created_at,
    }
