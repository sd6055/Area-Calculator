class Square:
    
    def __init__(self, length, width):
        self.perimeter = length * 4
        self.area = length * width
    
    def get_perimeter(self):
        return f"Perimeter is {self.perimeter}"
    
    def get_area(self):
        return f"Area is {self.area}"
    
square = Square(4, 4)
print(square.get_perimeter())
print(square.get_area())