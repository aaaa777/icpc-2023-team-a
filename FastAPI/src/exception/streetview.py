
class StreetViewPointNotFound(Exception):
    def __init__(self, message="StreetViewPoint not found"):
        self.message = message
        super().__init__(self.message)

class StreetViewLatitudeOutOfRange(Exception):
    def __init__(self, lat, message="StreetViewLatitude out of range: {lat}"):
        self.message = message
        self.lat = lat
        super().__init__(self.message.format(lat=self.lat))

class StreetViewLongitudeOutOfRange(Exception):
    def __init__(self, lon, message="StreetViewLongitude out of range: {lon}"):
        self.message = message
        self.lon = lon
        super().__init__(self.message.format(lon=self.lon))

class StreetViewZeroResults(Exception):
    def __init__(self, message="StreetViewZeroResults"):
        self.message = message
        super().__init__(self.message)

class StreetViewUnknownError(Exception):
    def __init__(self, message="StreetViewUnknownError: [{status}] {error_message}", status="", error_message=""):
        self.message = message
        super().__init__(self.message.format(status=status, error_message=error_message))