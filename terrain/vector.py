class Vector:  # Create vectors and perform dot products on them
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, vector2):
        return self.x * vector2.get_x() + self.y * vector2.get_y()

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y
