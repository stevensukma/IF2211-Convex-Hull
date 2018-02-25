import matplotlib.pyplot
import random
from time import time
from math import sqrt, fabs, acos

def is_smaller(tup1, tup2):
    if tup1[0] < tup2[0]:
        return True
    elif tup1[0] == tup2[0]:
        return tup1[1] < tup2[1]
    else:
        return False

def is_greater(tup1, tup2):
    if tup1[0] > tup2[0]:
        return True
    elif tup1[0] == tup2[0]:
        return tup1[1] > tup2[1]
    else:
        return False

def swap(points, left_idx, right_idx):
    temp = points[left_idx]
    points[left_idx] = points[right_idx]
    points[right_idx] = temp

    return points

def quick_sort(points):
    if len(points) == 0 :
        return []
    elif len(points) == 1 :
        return [points[0]]
    else:
        pivot = points[0]
        left_pointer = 1
        right_pointer = len(points) - 1
        while left_pointer <= right_pointer:
            if is_smaller(pivot, points[left_pointer]):
                if is_greater(pivot, points[right_pointer]):
                    swap(points, left_pointer, right_pointer)
                    left_pointer += 1
                else:
                    right_pointer -= 1
            else:
                left_pointer += 1
        if is_greater(pivot, points[right_pointer]):
            # Because pivot is on index 0
            swap(points, 0, right_pointer)
        return quick_sort(points[:right_pointer]) + [points[right_pointer]] + quick_sort(points[right_pointer+1:])

def split(points, point1, point2):
    # | x1  y1  1 |
    # | x2  y2  1 | = x1 y2 + x3 y1 + x2 y3 - x3 y2 - x2 y1 - x1 y3
    # | x3  y3  1 |
    S1 = []
    S2 = []

    for point3 in points:
        det = point1[0]*point2[1] + point3[0]*point1[1] + point2[0]*point3[1] - point3[0]*point2[1] - point2[0]*point1[1] - point1[0]*point3[1]
        if det>0:
            S1.append(point3)
        elif det<0:
            S2.append(point3)
    return S1, S2


def triangle_split(points, point1, point2, point3):
    left_points, _ = split(points, point1, point3)
    _, right_points = split(points, point2, point3)

    return left_points, right_points

def triangle_split_lower(points, point1, point2, point3):
    _, left_points = split(points, point1, point3)
    right_points, _ = split(points, point2, point3)

    return left_points, right_points

def find_dots_distance(point1, point2):
    return sqrt(pow(point2[0] - point1[0],2) + pow(point2[1] - point1[1], 2))

def find_angle(point1, point2, point3):
    # Find angle on point1 
    line1 = find_dots_distance(point2, point3)
    line2 = find_dots_distance(point1, point3)
    line3 = find_dots_distance(point1, point2)

    return acos((pow(line1,2) - pow(line2,2) - pow(line3,2))/(2*line2*line3))

def find_furthest_point(points, point1, point2):
    furthest_point, distance, angle = point1, 0.0, 0.0

    for point in points:
        a = point1[1] - point2[1]
        b = point2[0] - point1[0]
        c = point1[0]*point2[1] - point2[0]*point1[1]
        temp_distance = fabs((a*point[0] + b*point[1] + c) / sqrt(pow(a, 2) + pow(b, 2)))

        if temp_distance > distance:
            angle = find_angle(point, point1, point2)
            distance = temp_distance
            furthest_point = point
        elif temp_distance == distance:
            temp_angle = find_angle(point, point1, point2)
            if temp_angle > angle:
                angle = temp_angle
                furthest_point = point
            
    return furthest_point

def find_convex(points, point1, point2, lower):
    if len(points) == 0:
        return [(point1, point2)]
    else:
        furthest_point = find_furthest_point(points, point1, point2)
        if(lower):
            left_points, right_points = triangle_split_lower(points, point1, point2, furthest_point)
        else:
            left_points, right_points = triangle_split(points, point1, point2, furthest_point)
        return find_convex(left_points, point1, furthest_point, lower) + find_convex(right_points, furthest_point, point2, lower)

def convex_hull(points, point1, point2):
    S1, S2 = split(points, point1, point2)
    line_list = []
    # if lower hull then lower = True
    line_list += find_convex(S1, point1, point2, False)
    line_list += find_convex(S2, point1, point2, True)
    return line_list

if __name__ == '__main__':
    n = int(input("Number of dots = "))
    points = [ ( random.randint(0, 100), random.randint(0, 100) ) for k in range(n) ]
    # points = [(68, 54), (76, 36), (68, 44), (72, 1), (42, 28), (46, 89), (5, 51), (25, 94), (21, 9), (13, 85)]
    start = time()
    points = quick_sort(points)
    hull = convex_hull(points, points[0], points[-1])
    end = time()

    fig = matplotlib.pyplot.figure(1)
    fig.canvas.set_window_title('Convex Hull')
    canvas = fig.add_subplot(1,1,1)
    fig.canvas.draw()

    canvas.scatter([point[0] for point in points], [point[1] for point in points], color="#188087")

    print("Outer line = ")
    for line in hull:
        print(line)
        list_x = [line[0][0], line[1][0]]
        list_y = [line[0][1], line[1][1]]
        canvas.plot(list_x, list_y, color="#188087")

    print("Execution time = ", end-start, "seconds")
    matplotlib.pyplot.show()