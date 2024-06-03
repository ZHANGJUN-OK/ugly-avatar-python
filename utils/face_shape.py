import math
import random

def random_from_interval(min_val, max_val):
    return random.uniform(min_val, max_val)

def random_from_interval(min_val, max_val):
    return random.uniform(min_val, max_val)

def random_from_interval(min_val, max_val):
    return random.uniform(min_val, max_val)

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

def find_intersection_points(radian, a, b):
    if radian < 0:
        radian = 0
    if radian > math.pi / 2:
        radian = math.pi / 2
    
    m = math.tan(radian)
    
    if math.isclose(radian, math.pi / 2, abs_tol=0.0001):
        return {'x': 0, 'y': b}
    
    y = m * a
    
    if y < b:
        return {'x': a, 'y': y}
    else:
        x = b / m
        return {'x': x, 'y': b}

def generate_rectangular_face_contour_points(a, b, segment_points):
    result = []
    for i in range(segment_points):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 11 / segment_points, math.pi / 11 / segment_points)
        intersection = find_intersection_points(degree, a, b)
        result.append([intersection['x'], intersection['y']])
    
    for i in range(segment_points, 0, -1):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 11 / segment_points, math.pi / 11 / segment_points)
        intersection = find_intersection_points(degree, a, b)
        result.append([-intersection['x'], intersection['y']])
    
    for i in range(segment_points):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 11 / segment_points, math.pi / 11 / segment_points)
        intersection = find_intersection_points(degree, a, b)
        result.append([-intersection['x'], -intersection['y']])
    
    for i in range(segment_points, 0, -1):
        degree = (math.pi / 2 / segment_points) * i + random_from_interval(-math.pi / 11 / segment_points, math.pi / 11 / segment_points)
        intersection = find_intersection_points(degree, a, b)
        result.append([intersection['x'], -intersection['y']])
    
    return result

def generate_face_contour_points(num_points=100):
    face_size_x0 = random_from_interval(50, 100)
    face_size_y0 = random_from_interval(70, 100)
    face_size_y1 = random_from_interval(50, 80)
    face_size_x1 = random_from_interval(70, 100)
    face_k0 = random_from_interval(0.001, 0.005) * (1 if random.random() > 0.5 else -1)
    face_k1 = random_from_interval(0.001, 0.005) * (1 if random.random() > 0.5 else -1)
    face0_translate_x = random_from_interval(-5, 5)
    face0_translate_y = random_from_interval(-15, 15)
    face1_translate_y = random_from_interval(-5, 5)
    face1_translate_x = random_from_interval(-5, 25)
    egg_or_rect0 = random.random() > 0.1
    egg_or_rect1 = random.random() > 0.3
    
    results0 = get_egg_shape_points(face_size_x0, face_size_y0, face_k0, num_points) if egg_or_rect0 else generate_rectangular_face_contour_points(face_size_x0, face_size_y0, num_points)
    results1 = get_egg_shape_points(face_size_x1, face_size_y1, face_k1, num_points) if egg_or_rect1 else generate_rectangular_face_contour_points(face_size_x1, face_size_y1, num_points)
    
    for i in range(len(results0)):
        results0[i][0] += face0_translate_x
        results0[i][1] += face0_translate_y
        results1[i][0] += face1_translate_x
        results1[i][1] += face1_translate_y
    
    results = []
    center = [0, 0]
    
    for i in range(len(results0)):
        results.append([
            results0[i][0] * 0.7 + results1[(i + int(len(results0) / 4)) % len(results0)][1] * 0.3,
            results0[i][1] * 0.7 - results1[(i + int(len(results0) / 4)) % len(results0)][0] * 0.3
        ])
        center[0] += results[i][0]
        center[1] += results[i][1]
    
    center[0] /= len(results)
    center[1] /= len(results)
    
    for i in range(len(results)):
        results[i][0] -= center[0]
        results[i][1] -= center[1]
    
    width = results[0][0] - results[int(len(results) / 2)][0]
    height = results[int(len(results) / 4)][1] - results[int(len(results) * 3 / 4)][1]
    
    results.append(results[0])
    results.append(results[1])
    
    return {'face': results, 'width': width, 'height': height, 'center': [0, 0]}
