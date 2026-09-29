
import math


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


    @property 
    def perimeter(self):
        n = len(self.vertices)
        total = 0.0
        for i in range(n):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % n]  # следующая вершина, с "зацикливанием"
            total += math.hypot(b.x - a.x, b.y - a.y)
        return total
    @property 
    def area(self):
        n = len(self.vertices)
        total = 0.0
        for i in range(n):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % n]
            total += a.x * b.y - b.x * a.y
        return abs(total) / 2.0

    def contains_point(self, point, include_boundary=True):
        if not isinstance(point, Point):
            point = Point(point[0], point[1])

        n = len(self.vertices)
        sign = None

        for i in range(n):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % n]
            cr = self._cross(a, b, point)

            if abs(cr) < 1e-9:
                if not include_boundary:
                    return False
                continue  

            current_sign = cr > 0
            if sign is None:
                sign = current_sign
            elif current_sign != sign:
                return False 

        return True

    def triangulate(self):
        
        n = len(self.vertices)
        triangles = []
        v0 = self.vertices[0]
        for i in range(1, n - 1):
            triangles.append((v0, self.vertices[i], self.vertices[i + 1]))
        return triangles


    @staticmethod
    def _segment_intersection(p1, p2, p3, p4):
        x1, y1, x2, y2 = p1.x, p1.y, p2.x, p2.y
        x3, y3, x4, y4 = p3.x, p3.y, p4.x, p4.y
 
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-12:
            return p2  
 
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return Point(x, y)
 
    def intersect(self, other):
        output = list(other.vertices)
 
        for i in range(len(self.vertices)):
            if not output:
                break
            a = self.vertices[i]
            b = self.vertices[(i + 1) % len(self.vertices)]
 
            input_list = output
            output = []
            n = len(input_list)
            for j in range(n):
                cur = input_list[j]
                prev = input_list[j - 1]  
 
                cur_inside = self._cross(a, b, cur) >= -1e-9
                prev_inside = self._cross(a, b, prev) >= -1e-9
 
                if cur_inside:
                    if not prev_inside:
                        output.append(
                            self._segment_intersection(prev, cur, a, b)
                        )
                    output.append(cur)
                elif prev_inside:
                    output.append(self._segment_intersection(prev, cur, a, b))
 
        cleaned = []
        for p in output:
            if not cleaned or cleaned[-1] != p:
                cleaned.append(p)
        if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
            cleaned.pop()
        output = cleaned
 
        if len(output) < 3:
            return None
 
        try:
            return ConvexPolygon(output)
        except (NotConvexError, ValueError):
            return None

if __name__ == "__main__":
    square = ConvexPolygon([(0, 0), (4, 0), (4, 4), (0, 4)])
    print(square.vertices)
    print(square.area)
    print(square.perimeter)
    print("(2,2) :", square.contains_point((2, 2)))  
    print("(5,5) :", square.contains_point((5, 5)))  
    print("(0,0) :", square.contains_point((0, 0)))  

    print(square.triangulate())
 
    triangle = ConvexPolygon([(2, -2), (6, 2), (2, 6)])
    inter = square.intersect(triangle)
    print( inter.vertices if inter else None)
    if inter:
        print(inter.area)


    try:
        ConvexPolygon([(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)])
    except NotConvexError as e:
        print( e)