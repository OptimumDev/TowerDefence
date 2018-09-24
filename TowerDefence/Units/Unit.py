class Unit:

    def __init__(self, coordinates, image):
        self._coordinates = coordinates
        self._image = image

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def image(self):
        return self._image