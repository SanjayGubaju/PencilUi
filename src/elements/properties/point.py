class Point:
    def __init__(self, new_x=0, new_y=0):
        self.x = new_x
        self.y = new_y

    def set_point(self, point):
        (self.x, self.y) = (point.x, point.y)
