import math
import random

def random_from_interval(min_val, max_val):
    return random.random() * (max_val - min_val) + min_val

def cubic_bezier(p0, p1, p2, p3, t):
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return [x, y]

def get_egg_shape_points(a, b, k, segment_points):
    result = []
    for i in range(segment_points):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 1.1 / segment_points, math.pi / 1.1 / segment_points)
        y = math.sin(degree) * b
        x = math.sqrt(((1 - (y * y) / (b * b)) / (1 + k * y)) * a * a) + random_from_interval(-a / 200.0, a / 200.0)
        result.append([x, y])
    
    for i in range(segment_points, 0, -1):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 1.1 / segment_points, math.pi / 1.1 / segment_points)
        y = math.sin(degree) * b
        x = -math.sqrt(((1 - (y * y) / (b * b)) / (1 + k * y)) * a * a) + random_from_interval(-a / 200.0, a / 200.0)
        result.append([x, y])
    
    for i in range(segment_points):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 1.1 / segment_points, math.pi / 1.1 / segment_points)
        y = -math.sin(degree) * b
        x = -math.sqrt(((1 - (y * y) / (b * b)) / (1 + k * y)) * a * a) + random_from_interval(-a / 200.0, a / 200.0)
        result.append([x, y])
    
    for i in range(segment_points, 0, -1):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 1.1 / segment_points, math.pi / 1.1 / segment_points)
        y = -math.sin(degree) * b
        x = math.sqrt(((1 - (y * y) / (b * b)) / (1 + k * y)) * a * a) + random_from_interval(-a / 200.0, a / 200.0)
        result.append([x, y])
    
    return result

def generate_mouth_shape0(face_contour, face_height, face_width):
    face_contour_copy = face_contour[:-2]
    mouth_right_y = random_from_interval(face_height / 7, face_height / 3.5)
    mouth_left_y = random_from_interval(face_height / 7, face_height / 3.5)
    mouth_right_x = random_from_interval(face_width / 10, face_width / 2)
    mouth_left_x = -mouth_right_x + random_from_interval(-face_width / 20, face_width / 20)
    mouth_right = [mouth_right_x, mouth_right_y]
    mouth_left = [mouth_left_x, mouth_left_y]

    control_point0 = [random_from_interval(0, mouth_right_x), random_from_interval(mouth_left_y + 5, face_height / 1.5)]
    control_point1 = [random_from_interval(mouth_left_x, 0), random_from_interval(mouth_left_y + 5, face_height / 1.5)]

    mouth_points = []
    for i in range(0, 100):
        t = i / 100.0
        mouth_points.append(cubic_bezier(mouth_left, control_point1, control_point0, mouth_right, t))
    
    if random.random() > 0.5:
        for i in range(0, 100):
            t = i / 100.0
            mouth_points.append(cubic_bezier(mouth_right, control_point0, control_point1, mouth_left, t))
    else:
        y_offset_portion = random_from_interval(0, 0.8)
        for i in range(0, 100):
            t = i / 100.0
            x = mouth_points[99][0] * (1 - t) + mouth_points[0][0] * t
            y = (mouth_points[99][1] * (1 - t) + mouth_points[0][1] * t) * (1 - y_offset_portion) + mouth_points[99 - i][1] * y_offset_portion
            mouth_points.append([x, y])
    
    return mouth_points

def generate_mouth_shape1(face_contour, face_height, face_width):
    face_contour_copy = face_contour[:-2]
    mouth_right_y = random_from_interval(face_height / 7, face_height / 4)
    mouth_left_y = random_from_interval(face_height / 7, face_height / 4)
    mouth_right_x = random_from_interval(face_width / 10, face_width / 2)
    mouth_left_x = -mouth_right_x + random_from_interval(-face_width / 20, face_width / 20)
    mouth_right = [mouth_right_x, mouth_right_y]
    mouth_left = [mouth_left_x, mouth_left_y]

    control_point0 = [random_from_interval(0, mouth_right_x), random_from_interval(mouth_left_y + 5, face_height / 1.5)]
    control_point1 = [random_from_interval(mouth_left_x, 0), random_from_interval(mouth_left_y + 5, face_height / 1.5)]

    mouth_points = []
    for i in range(0, 100):
        t = i / 100.0
        mouth_points.append(cubic_bezier(mouth_left, control_point1, control_point0, mouth_right, t))
    
    center = [(mouth_right[0] + mouth_left[0]) / 2, (mouth_points[25][1] + mouth_points[75][1]) / 2]
    if random.random() > 0.5:
        for i in range(0, 100):
            t = i / 100.0
            mouth_points.append(cubic_bezier(mouth_right, control_point0, control_point1, mouth_left, t))
    else:
        y_offset_portion = random_from_interval(0, 0.8)
        for i in range(0, 100):
            x = mouth_points[99][0] * (1 - i / 100.0) + mouth_points[0][0] * i / 100.0
            y = (mouth_points[99][1] * (1 - i / 100.0) + mouth_points[0][1] * i / 100.0) * (1 - y_offset_portion) + mouth_points[99 - i][1] * y_offset_portion
            mouth_points.append([x, y])
    
    for i in range(len(mouth_points)):
        mouth_points[i][0] -= center[0]
        mouth_points[i][1] -= center[1]
        mouth_points[i][1] = -mouth_points[i][1]
        mouth_points[i][0] *= 0.6
        mouth_points[i][1] *= 0.6
        mouth_points[i][0] += center[0]
        mouth_points[i][1] += center[1] * 0.8
    
    return mouth_points

def generate_mouth_shape2(face_contour, face_height, face_width):
    center = [random_from_interval(-face_width / 8, face_width / 8), random_from_interval(face_height / 4, face_height / 2.5)]
    mouth_points = get_egg_shape_points(random_from_interval(face_width / 4, face_width / 10), random_from_interval(face_height / 10, face_height / 20), 0.001, 50)
    random_rotation_degree = random_from_interval(-math.pi / 9.5, math.pi / 9.5)
    
    for i in range(len(mouth_points)):
        x = mouth_points[i][0]
        y = mouth_points[i][1]
        mouth_points[i][0] = x * math.cos(random_rotation_degree) - y * math.sin(random_rotation_degree)
        mouth_points[i][1] = x * math.sin(random_rotation_degree) + y * math.cos(random_rotation_degree)
        mouth_points[i][0] += center[0]
        mouth_points[i][1] += center[1]
    
    return mouth_points
