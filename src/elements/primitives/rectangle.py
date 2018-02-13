from src.elements.properties.position import Position
from src.elements.properties.size import Size


class Rectangle(Position, Size):
    def __init__(self):
        Position.__init__(self)
        Size.__init__(self)
