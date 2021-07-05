from math import pi, pow, sin, cos, atan2, asin, sqrt

class Location(dict):
    def __init__(self, name: str, lng: float, lat: float) -> None:
        self["name"] = name
        self["lng"] = lng
        self["lat"] = lat
    
    def haversine(self, other) -> float:
        pi1 = float(self["lat"]) * pi / 180
        pi2 = float(other["lat"]) * pi / 180

        deltaPi = (float(self["lat"]) - float(other["lat"])) * pi / 360
        deltaLambda = (float(self["lng"]) - float(other["lng"])) * pi / 360
        
        a = pow(sin(deltaPi), 2) + (cos(pi1) * cos(pi2) * pow(sin(deltaLambda), 2))

        # c = 2 * atan2(sqrt(a), sqrt(1 - a))
        c = 2 * asin(sqrt(a))
        return c

    @staticmethod
    def convert_from_string(string: str):
        temp = string.split(" ")
        
        return Location(temp[0], temp[1], temp[2])

    @staticmethod
    def convert_to_list_from_string(string: str):
        arrays = string.split("\r\n")

        result = []

        for row in arrays:
            result.append(Location.convert_from_string(row))
    
        return result

    @staticmethod
    def from_dict(dict: dict):
        return Location(dict["name"], dict["coordinates"]["lng"], dict["coordinates"]["lat"])

    def to_dict(self) -> dict:
        return {
            "name": self["name"],
            "coordinates": {
                "lng": self["lng"],
                "lat": self["lat"]
            }
        }

    def __str__(self) -> str:
        return super().__str__()