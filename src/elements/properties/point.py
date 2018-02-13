class Point():
    def __init__(self, new_x=0, new_y=0):
        self.x = new_x
        self.y = new_y

    def set_position(self, position):
        (self.x, self.y) = (position.x, position.y)
