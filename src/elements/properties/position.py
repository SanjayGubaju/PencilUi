from src.elements.properties.point import Point


class Position(Point):
    def __init__(self):
        Point.__init__(self)

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

