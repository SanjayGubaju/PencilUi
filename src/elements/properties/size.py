class Size:
    def __init__(self, new_width=0, new_height=0):
        self.width = new_width
        self.height = new_height

    def set_size(self, size):
        (self.width, self.height) = (abs(size.width), abs(size.height))
