import random

def random_from_interval(min_val, max_val):
    return random.uniform(min_val, max_val)

def cubic_bezier(P0, P1, P2, P3, t):
    x = (1 - t) ** 3 * P0[0] + 3 * (1 - t) ** 2 * t * P1[0] + 3 * (1 - t) * t ** 2 * P2[0] + t ** 3 * P3[0]
    y = (1 - t) ** 3 * P0[1] + 3 * (1 - t) ** 2 * t * P1[1] + 3 * (1 - t) * t ** 2 * P2[1] + t ** 3 * P3[1]
    return [x, y]

def generate_eye_parameters(width):
    height_upper = random.random() * width / 1.2
    height_lower = random.random() * width / 1.2
    P0_upper_randX = random.random() * 0.4 - 0.2
    P3_upper_randX = random.random() * 0.4 - 0.2
    P0_upper_randY = random.random() * 0.4 - 0.2
    P3_upper_randY = random.random() * 0.4 - 0.2
    offset_upper_left_randY = random.random()
    offset_upper_right_randY = random.random()
    P0_upper = [-width / 2 + P0_upper_randX * width / 16, P0_upper_randY * height_upper / 16]
    P3_upper = [width / 2 + P3_upper_randX * width / 16, P3_upper_randY * height_upper / 16]
    P0_lower = P0_upper
    P3_lower = P3_upper
    eye_true_width = P3_upper[0] - P0_upper[0]

    offset_upper_left_x = random_from_interval(-eye_true_width / 10.0, eye_true_width / 2.3)
    offset_upper_right_x = random_from_interval(-eye_true_width / 10.0, eye_true_width / 2.3)
    offset_upper_left_y = offset_upper_left_randY * height_upper
    offset_upper_right_y = offset_upper_right_randY * height_upper
    offset_lower_left_x = random_from_interval(offset_upper_left_x, eye_true_width / 2.1)
    offset_lower_right_x = random_from_interval(offset_upper_right_x, eye_true_width / 2.1)
    offset_lower_left_y = random_from_interval(-offset_upper_left_y + 5, height_lower)
    offset_lower_right_y = random_from_interval(-offset_upper_right_y + 5, height_lower)

    left_converge0 = random.random()
    right_converge0 = random.random()
    left_converge1 = random.random()
    right_converge1 = random.random()

    return {
        'height_upper': height_upper,
        'height_lower': height_lower,
        'P0_upper_randX': P0_upper_randX,
        'P3_upper_randX': P3_upper_randX,
        'P0_upper_randY': P0_upper_randY,
        'P3_upper_randY': P3_upper_randY,
        'offset_upper_left_randY': offset_upper_left_randY,
        'offset_upper_right_randY': offset_upper_right_randY,
        'eye_true_width': eye_true_width,
        'offset_upper_left_x': offset_upper_left_x,
        'offset_upper_right_x': offset_upper_right_x,
        'offset_upper_left_y': offset_upper_left_y,
        'offset_upper_right_y': offset_upper_right_y,
        'offset_lower_left_x': offset_lower_left_x,
        'offset_lower_right_x': offset_lower_right_x,
        'offset_lower_left_y': offset_lower_left_y,
        'offset_lower_right_y': offset_lower_right_y,
        'left_converge0': left_converge0,
        'right_converge0': right_converge0,
        'left_converge1': left_converge1,
        'right_converge1': right_converge1
    }

def generate_eye_points(rands, width=50):
    P0_upper = [-width / 2 + rands['P0_upper_randX'] * width / 16, rands['P0_upper_randY'] * rands['height_upper'] / 16]
    P3_upper = [width / 2 + rands['P3_upper_randX'] * width / 16, rands['P3_upper_randY'] * rands['height_upper'] / 16]
    P0_lower = P0_upper
    P3_lower = P3_upper
    eye_true_width = P3_upper[0] - P0_upper[0]

    P1_upper = [P0_upper[0] + rands['offset_upper_left_x'], P0_upper[1] + rands['offset_upper_left_y']]
    P2_upper = [P3_upper[0] - rands['offset_upper_right_x'], P3_upper[1] + rands['offset_upper_right_y']]

    P1_lower = [P0_lower[0] + rands['offset_lower_left_x'], P0_lower[1] - rands['offset_lower_left_y']]
    P2_lower = [P3_lower[0] - rands['offset_lower_right_x'], P3_lower[1] - rands['offset_lower_right_y']]

    upper_eyelid_points = []
    upper_eyelid_points_left_control = []
    upper_eyelid_points_right_control = []
    upper_eyelid_left_control_point = [
        P0_upper[0] * (1 - rands['left_converge0']) + P1_lower[0] * rands['left_converge0'],
        P0_upper[1] * (1 - rands['left_converge0']) + P1_lower[1] * rands['left_converge0']
    ]
    upper_eyelid_right_control_point = [
        P3_upper[0] * (1 - rands['right_converge0']) + P2_lower[0] * rands['right_converge0'],
        P3_upper[1] * (1 - rands['right_converge0']) + P2_lower[1] * rands['right_converge0']
    ]
    for t in range(100):
        upper_eyelid_points.append(cubic_bezier(P0_upper, P1_upper, P2_upper, P3_upper, t / 100))
        upper_eyelid_points_left_control.append(cubic_bezier(upper_eyelid_left_control_point, P0_upper, P1_upper, P2_upper, t / 100))
        upper_eyelid_points_right_control.append(cubic_bezier(P1_upper, P2_upper, P3_upper, upper_eyelid_right_control_point, t / 100))

    for i in range(75):
        weight = ((75.0 - i) / 75.0) ** 2
        upper_eyelid_points[i] = [
            upper_eyelid_points[i][0] * (1 - weight) + upper_eyelid_points_left_control[i + 25][0] * weight,
            upper_eyelid_points[i][1] * (1 - weight) + upper_eyelid_points_left_control[i + 25][1] * weight
        ]
        upper_eyelid_points[i + 25] = [
            upper_eyelid_points[i + 25][0] * weight + upper_eyelid_points_right_control[i][0] * (1 - weight),
            upper_eyelid_points[i + 25][1] * weight + upper_eyelid_points_right_control[i][1] * (1 - weight)
        ]

    lower_eyelid_points = []
    lower_eyelid_points_left_control = []
    lower_eyelid_points_right_control = []
    lower_eyelid_left_control_point = [
        P0_lower[0] * (1 - rands['left_converge0']) + P1_upper[0] * rands['left_converge0'],
        P0_lower[1] * (1 - rands['left_converge0']) + P1_upper[1] * rands['left_converge0']
    ]
    lower_eyelid_right_control_point = [
        P3_lower[0] * (1 - rands['right_converge1']) + P2_upper[0] * rands['right_converge1'],
        P3_lower[1] * (1 - rands['right_converge1']) + P2_upper[1] * rands['right_converge1']
    ]
    for t in range(100):
        lower_eyelid_points.append(cubic_bezier(P0_lower, P1_lower, P2_lower, P3_lower, t / 100))
        lower_eyelid_points_left_control.append(cubic_bezier(lower_eyelid_left_control_point, P0_lower, P1_lower, P2_lower, t / 100))
        lower_eyelid_points_right_control.append(cubic_bezier(P1_lower, P2_lower, P3_lower, lower_eyelid_right_control_point, t / 100))

    for i in range(75):
        weight = ((75.0 - i) / 75.0) ** 2
        lower_eyelid_points[i] = [
            lower_eyelid_points[i][0] * (1 - weight) + lower_eyelid_points_left_control[i + 25][0] * weight,
            lower_eyelid_points[i][1] * (1 - weight) + lower_eyelid_points_left_control[i + 25][1] * weight
        ]
        lower_eyelid_points[i + 25] = [
            lower_eyelid_points[i + 25][0] * weight + lower_eyelid_points_right_control[i][0] * (1 - weight),
            lower_eyelid_points[i + 25][1] * weight + lower_eyelid_points_right_control[i][1] * (1 - weight)
        ]

    for i in range(100):
        lower_eyelid_points[i][1] = -lower_eyelid_points[i][1]
        upper_eyelid_points[i][1] = -upper_eyelid_points[i][1]

    eye_center = [
        (upper_eyelid_points[50][0] + lower_eyelid_points[50][0]) / 2.0,
        (upper_eyelid_points[50][1] + lower_eyelid_points[50][1]) / 2.0
    ]

    for i in range(100):
        lower_eyelid_points[i][0] -= eye_center[0]
        lower_eyelid_points[i][1] -= eye_center[1]
        upper_eyelid_points[i][0] -= eye_center[0]
        upper_eyelid_points[i][1] -= eye_center[1]

    eye_center = [0, 0]

    return {'upper': upper_eyelid_points, 'lower': lower_eyelid_points, 'center': eye_center}

def generate_both_eyes(width=50):
    rands_left = generate_eye_parameters(width)
    rands_right = rands_left.copy()

    for key in rands_right:
        if isinstance(rands_right[key], (int, float)):
            rands_right[key] += random_from_interval(-rands_right[key] / 2.0, rands_right[key] / 2.0)

    left_eye = generate_eye_points(rands_left, width)
    right_eye = generate_eye_points(rands_right, width)

    for key in left_eye:
        if isinstance(left_eye[key], list):
            for i in range(len(left_eye[key])):
                if isinstance(left_eye[key][i], list):
                    left_eye[key][i][0] = -left_eye[key][i][0]

    return {'left': left_eye, 'right': right_eye}
