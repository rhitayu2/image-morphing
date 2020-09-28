from cv2 import cv2
import __main__ as im

# calculates the dot product of two vectors
def dot(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z

# calculates the cross product of two vectors
def cross(a, b):
    return Point( a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x )

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, b):
        return Point(self.x+b.x, self.y+b.y)
    def __sub__(self, b):
        return Point(self.x-b.x, self.y-b.y)
    def __mul__(self, b):
        return Point(b*self.x, b*self.y)
    __rmul__ = __mul__

    def IsInCircumcircleOf(self, T):
        a = T.v[0] - T.v[2]
        b = T.v[1] - T.v[2]
        z = cross(a,b)
        if dot(z,z) != 0:
            p0 = cross(dot(a,a)*b-dot(b,b)*a, z)*(0.5/dot(z,z)) + T.v[2]
            r2 = 0.25*dot(a, a)*dot(b,b)*dot(a-b, a-b)/dot(z, z)
            return dot(self-p0, self-p0) <= r2

class Triangle:
    def __init__(self, a, b, c):
        self.v = [None]*3
        self.v[0] = a
        self.v[1] = b
        self.v[2] = c
        self.neighbour = [None]*3    # Adjacent triangles
        
    def SetEdge(self, edge, T):
        temp_v = self.v + self.v[0:1]
        for i in range(3):
            if edge[0] == temp_v[i] and edge[1] == temp_v[i+1]:
                self.neighbour[(i+2)%3] = T
                return
     
class Delaunay_Triangulation:
    def __init__(self):
        a = Point(0, 0)
        b = Point(299, 0)
        c = Point(299, 399)
        d = Point(0, 399)

        # use the three points to represent a triangle
        T1 = Triangle(a, d, b)
        T2 = Triangle(c, b, d)

        T1.neighbour[0] = T2
        T2.neighbour[0] = T1
        self.triangles = [T1, T2]

    def AddPoint(self, p):
        bad_triangles = []
        for T in self.triangles:
            if p.IsInCircumcircleOf(T):
                bad_triangles.append(T)
        boundary = self.Boundary(bad_triangles)

        for T in bad_triangles:
            self.triangles.remove(T)

        new_triangles = []
        for edge in boundary:
            T = Triangle(p, edge[0], edge[1])

            T.neighbour[0] = edge[2]                   # To neighbour
            if T.neighbour[0]:
                T.neighbour[0].SetEdge(edge[1::-1], T)     # from neighbour

            new_triangles.append(T)

        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            T.neighbour[2] = new_triangles[(i-1) % N]   # back
            T.neighbour[1] = new_triangles[(i+1) % N]   # forward
   
        self.triangles.extend(new_triangles)

    def Boundary(self, bad_triangles):
        T = bad_triangles[0]
        edge = 0

        boundary = []

        while True:
            if len(boundary) > 1:
                if boundary[0] == boundary[-1]:
                    break
            if T.neighbour[edge] in bad_triangles:
                last = T
                T = T.neighbour[edge]
                edge = (T.neighbour.index(last) + 1) % 3 
            else:   
                boundary.append((T.v[(edge+1)%3], T.v[(edge+2)%3], T.neighbour[edge]))
                edge = (edge + 1) % 3
        return boundary[:-1]

    def export(self):
        ps = [p for t in self.triangles for p in t.v ]
        xs = [p.x for p in ps]
        ys = [p.y for p in ps]

        return xs, ys
# check if rectangle contains the given point
def rect_contains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

def triangulation(img, given_file, frame_control_pts,animate = False, generate_points=False):
    delaunay_color = (0,0,255)
    size = img.shape
    r = (0, 0, size[1], size[0])
    subdiv = Delaunay_Triangulation()
    # animate will allow to visualize the triangles drawn on the image
    if(animate):
        print("\n[Write]Saving current triangulated image")
        with open(given_file) as file :
            for line in file :
                x, y = line.split()
                if ((int(x),int(y)) not in im.corner_pts):
                    subdiv.AddPoint(Point(int(x),int(y)))
        x_triangle, y_triangle = subdiv.export()
        i = 0
        while(i < len(x_triangle)):
            pt1 = (int(x_triangle[i]), int(y_triangle[i]))
            pt2 = (int(x_triangle[i+1]), int(y_triangle[i+1]))
            pt3 = (int(x_triangle[i+2]), int(y_triangle[i+2]))
            i = i+3
            if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
                cv2.line(img, pt1, pt2, delaunay_color, 1)
                cv2.line(img, pt2, pt3, delaunay_color, 1)
                cv2.line(img, pt3, pt1, delaunay_color, 1)
        print("\n")
        cv2.imshow("Triangulated Image",img)
        cv2.waitKey(0)
        return img
    
    # generate_points only generates the triangle and returns a list of the triangles
    if(generate_points):
        for p in frame_control_pts:
            if ((int(p[0]),int(p[1])) not in im.corner_pts):
                subdiv.AddPoint(Point(int(p[0]), int(p[1])))
        x_triangle, y_triangle = subdiv.export()
        triangle_List = []
        i = 0
        while(i < len(x_triangle)):
            pt1 = (int(x_triangle[i]), int(y_triangle[i]))
            pt2 = (int(x_triangle[i+1]), int(y_triangle[i+1]))
            pt3 = (int(x_triangle[i+2]), int(y_triangle[i+2]))
            i = i+3
            if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
                try:
                    point1=frame_control_pts.index(pt1)
                    point2=frame_control_pts.index(pt2)
                    point3=frame_control_pts.index(pt3)
                    triangle_List.append((point1,point2,point3))
                except:
                    pass
        return triangle_List