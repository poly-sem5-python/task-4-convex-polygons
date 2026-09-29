

class Point:
    
    def __init__(self, x, y):
       
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class NotConvexError(Exception):
    pass


class ConvexPolygon:


    def __init__(self, vertices):
        
        if len(vertices) < 3:
            raise ValueError("Многоугольнику нужно минимум 3 вершины")

        self.vertices = [
            v if isinstance(v, Point) else Point(v[0], v[1])
            for v in vertices
        ]

        self._check_convex()

    @staticmethod
    def _cross(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    def _check_convex(self):
    
        n = len(self.vertices)
        sign = None

        for i in range(n):
            o = self.vertices[i]
            a = self.vertices[(i + 1) % n]
            b = self.vertices[(i + 2) % n]
            cr = self._cross(o, a, b)

            if abs(cr) < 1e-9:
                continue  

            current_sign = cr > 0
            if sign is None:
                sign = current_sign
            elif current_sign != sign:
                raise NotConvexError(
                    f"Многоугольник не выпуклый: нарушение в вершинах "
                    f"{o}, {a}, {b}"
                )


if __name__ == "__main__":
    square = ConvexPolygon([(0, 0), (4, 0), (4, 4), (0, 4)])
    print(square.vertices)

    try:
        ConvexPolygon([(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)])
    except NotConvexError as e:
        print( e)