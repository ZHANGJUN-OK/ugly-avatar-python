import math
import random

def random_from_interval(min_val, max_val):
    return random.uniform(min_val, max_val)

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def binomial_coefficient(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

def calculate_bezier_point(t, control_points):
    x, y = 0, 0
    n = len(control_points) - 1

    for i in range(n + 1):
        bin_coeff = binomial_coefficient(n, i)
        a = math.pow(1 - t, n - i)
        b = math.pow(t, i)
        x += bin_coeff * a * b * control_points[i]['x']
        y += bin_coeff * a * b * control_points[i]['y']

    return [x, y]

def compute_bezier_curve(control_points, number_of_points):
    curve = []
    for i in range(number_of_points + 1):
        t = i / number_of_points
        point = calculate_bezier_point(t, control_points)
        curve.append(point)
    return curve

def generate_hair_lines_0(face_countour, num_hair_lines=100):
    face_countour_copy = face_countour[:-2]
    results = []
    for i in range(num_hair_lines):
        num_hair_points = 20 + math.floor(random_from_interval(-5, 5))
        hair_line = []
        index_offset = math.floor(random_from_interval(30, 140))
        for j in range(num_hair_points):
            hair_line.append({
                'x': face_countour_copy[(len(face_countour_copy) - (j + index_offset)) % len(face_countour_copy)][0],
                'y': face_countour_copy[(len(face_countour_copy) - (j + index_offset)) % len(face_countour_copy)][1]
            })
        d0 = compute_bezier_curve(hair_line, num_hair_points)
        
        hair_line = []
        index_offset = math.floor(random_from_interval(30, 140))
        for j in range(num_hair_points):
            hair_line.append({
                'x': face_countour_copy[(len(face_countour_copy) - (-j + index_offset)) % len(face_countour_copy)][0],
                'y': face_countour_copy[(len(face_countour_copy) - (-j + index_offset)) % len(face_countour_copy)][1]
            })
        d1 = compute_bezier_curve(hair_line, num_hair_points)
        
        d = []
        for j in range(num_hair_points):
            d.append([
                d0[j][0] * (j * (1 / num_hair_points)) ** 2 + d1[j][0] * (1 - (j * (1 / num_hair_points)) ** 2),
                d0[j][1] * (j * (1 / num_hair_points)) ** 2 + d1[j][1] * (1 - (j * (1 / num_hair_points)) ** 2)
            ])
        
        results.append(d)
    
    return results

def generate_hair_lines_1(face_countour, num_hair_lines=100):
    face_countour_copy = face_countour[:-2]
    results = []
    for i in range(num_hair_lines):
        num_hair_points = 20 + math.floor(random_from_interval(-5, 5))
        hair_line = []
        index_start = math.floor(random_from_interval(20, 160))
        hair_line.append({
            'x': face_countour_copy[(len(face_countour_copy) - index_start) % len(face_countour_copy)][0],
            'y': face_countour_copy[(len(face_countour_copy) - index_start) % len(face_countour_copy)][1]
        })
        
        for j in range(1, num_hair_points + 1):
            index_start = math.floor(random_from_interval(20, 160))
            hair_line.append({
                'x': face_countour_copy[(len(face_countour_copy) - index_start) % len(face_countour_copy)][0],
                'y': face_countour_copy[(len(face_countour_copy) - index_start) % len(face_countour_copy)][1]
            })
        
        d = compute_bezier_curve(hair_line, num_hair_points)
        results.append(d)
    
    return results

def generate_hair_lines_2(face_countour, num_hair_lines=100):
    face_countour_copy = face_countour[:-2]
    results = []
    picked_indices = [math.floor(random_from_interval(10, 180)) for _ in range(num_hair_lines)]
    picked_indices.sort()
    
    for i in range(num_hair_lines):
        num_hair_points = 20 + math.floor(random_from_interval(-5, 5))
        hair_line = []
        index_offset = picked_indices[i]
        lower = random_from_interval(0.8, 1.4)
        reverse = 1 if random.random() > 0.5 else -1
        
        for j in range(num_hair_points):
            powerscale = random_from_interval(0.1, 3)
            portion = (1 - (j / num_hair_points) ** powerscale) * (1 - lower) + lower
            hair_line.append({
                'x': face_countour_copy[(len(face_countour_copy) - (reverse * j + index_offset)) % len(face_countour_copy)][0] * portion,
                'y': face_countour_copy[(len(face_countour_copy) - (reverse * j + index_offset)) % len(face_countour_copy)][1] * portion
            })
        
        d = compute_bezier_curve(hair_line, num_hair_points)
        if random.random() > 0.7:
            d.reverse()
        if len(results) == 0:
            results.append(d)
            continue
        
        last_hair_point = results[-1][-1]
        last_points_distance = math.sqrt((d[0][0] - last_hair_point[0]) ** 2 + (d[0][1] - last_hair_point[1]) ** 2)
        if random.random() > 0.5 and last_points_distance < 100:
            results[-1].extend(d)
        else:
            results.append(d)
    
    return results

def generate_hair_lines_3(face_countour, num_hair_lines=100):
    face_countour_copy = face_countour[:-2]
    results = []
    picked_indices = [math.floor(random_from_interval(10, 180)) for _ in range(num_hair_lines)]
    picked_indices.sort()
    split_point = math.floor(random_from_interval(0, 200))
    
    for i in range(num_hair_lines):
        num_hair_points = 30 + math.floor(random_from_interval(-8, 8))
        hair_line = []
        index_offset = picked_indices[i]
        lower = random_from_interval(1, 2.3)
        if random.random() > 0.9:
            lower = random_from_interval(0, 1.)
        reverse = 1 if index_offset > split_point else -1
        
        for j in range(num_hair_points):
            powerscale = random_from_interval(0.1, 3)
            portion = (1 - (j / num_hair_points) ** powerscale) * (1 - lower) + lower
            hair_line.append({
                'x': face_countour_copy[(len(face_countour_copy) - (reverse * j * 2 + index_offset)) % len(face_countour_copy)][0] * portion,
                'y': face_countour_copy[(len(face_countour_copy) - (reverse * j * 2 + index_offset)) % len(face_countour_copy)][1]
            })
        
        d = compute_bezier_curve(hair_line, num_hair_points)
        results.append(d)
    
    return results
