from typing import Union, List

class Rectangle:
    def __init__(self, width:Union[int,float], height:Union[int,float]):
        self.width = width
        self.height = height

    def __str__(self):
        s = f"Rectangle(width={self.width}, height={self.height})"
        return s

    def set_height(self,h:Union[int,float]):
        """Reset height of rectangle.

        Args:
            h (Union[int,float]): Height
        """
        self.height=h

    def set_width(self, w:Union[int,float]):
        """Reset width of rectangle.

        Args:
            w (Union[int,float]): Width
        """
        self.width = w

    def get_area(self) -> Union[int,float]:
        """Find area of the rectangle.

        Returns:
            Union[int,float]: Height * Width
        """
        return self.height*self.width

    def get_perimeter(self) -> Union[int,float]:
        """Find permieter of the rectangle.

        Returns:
            Union[int,float]: (2*Height) + (2*Width)
        """
        return (2*self.height)+(2*self.width)

    def get_diagonal(self) -> float:
        """Find diagonal of the rectangle.

        Returns:
            float: ((Width^2) + (Height^2))^0.5
        """
        return (self.width ** 2 + self.height ** 2) ** .5

    def get_picture(self) -> str:
        """Get a visual representation of the rectangle with asterisks.

        Returns:
            str: The rectangle.
        """
        if (self.width>50) | (self.height>50):
            return "Too big for picture."
        s = ""
        for i in range(self.height):
            s += "*"*self.width + "\n"
        return s

    def get_amount_inside(self, shape:Rectangle) -> int:
        """Find how many copies of another rectangle fit into this rectangle.

        Args:
            shape (Rectangle): The other rectangle.

        Returns:
            int: The exact number of complete times the other rectangle can fit.
        """
        return self.get_area()//shape.get_area()

class Square(Rectangle):
    def __init__(self, side_length:Union[int,float]):
        self.height=side_length
        self.width=side_length
        self.side_length = side_length

    def __str__(self):
        return f"Square(side={self.side_length})"

    def set_side(self, s:Union[int,float]):
        """Reset the side length of the rectangle.

        Args:
            s (Union[int,float]): [description]
        """
        self.height = s
        self.width = s

    def set_width(self, w:Union[int,float]):
        """Reset width of rectangle.

        Args:
            w (Union[int,float]): Width
        """
        return self.set_side(w)

    def set_height(self, h:Union[int,float]):
        """Reset height of rectangle.

        Args:
            h (Union[int,float]): Width
        """
        return self.set_side(h)

