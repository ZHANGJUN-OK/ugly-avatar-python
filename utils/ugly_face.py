import random
import svgwrite
import cairosvg
from utils.generate_init import FaceGenerator

def draw_point_nose(dwg, center_x, center_y, nose_id):
    nose_group = dwg.g(id=nose_id)
    for _ in range(10):
        r = random.uniform(1.0, 3.0)
        cx = center_x + random.uniform(-2, 2)
        cy = center_y + random.uniform(-2, 2)
        stroke_width = 1.0 + random.uniform(0.0, 0.5)
        nose_group.add(dwg.circle(center=(cx, cy), r=r, stroke='black', fill='none', stroke_width=stroke_width))
    return nose_group

def draw_line_nose(dwg, left_x, left_y, right_x, right_y, eye_height_offset):
    path_d = (
        f"M {left_x} {left_y} "
        f"Q {right_x} {right_y * 1.5} {(left_x + right_x) / 2} {-eye_height_offset * 0.2}"
    )
    stroke_width = 2.5 + random.uniform(0.0, 1.0)
    return dwg.path(d=path_d, fill='none', stroke='black', stroke_width=stroke_width, stroke_linejoin='round')

def generate_face_svg(output_file='face.svg', face_generator=None, save_png=False):
    if face_generator is None:
        face_generator = FaceGenerator()
        face_generator.generateFace()

    dwg = svgwrite.Drawing(output_file, profile='full', size=('500px', '500px'))
    dwg.viewbox(-100, -100, 200, 200)

    # Create filter
    fuzzy_filter = dwg.defs.add(dwg.filter(id='fuzzy'))
    fuzzy_filter.feTurbulence(baseFrequency="0.05", numOctaves=3, type="fractalNoise", result="noise")
    fuzzy_filter.feDisplacementMap(in_="SourceGraphic", in2="noise", scale=2)

    # Add background
    dwg.add(dwg.rect(insert=(-100, -100), size=("100%", "100%"), fill=random.choice(face_generator.backgroundColors)))

    # Add face contour
    dwg.add(dwg.polygon(points=face_generator.computedFacePoints, fill='#ffc9a9', stroke='black',
                        stroke_width=3.0 / face_generator.faceScale, stroke_linejoin="round", filter='url(#fuzzy)'))

    # Add left eye
    transform_left_eye = (
        'translate(' +
        str(-(face_generator.center[0] + face_generator.distanceBetweenEyes + face_generator.leftEyeOffsetX)) +
        ' ' +
        str(-(-face_generator.center[1] + face_generator.eyeHeightOffset + face_generator.leftEyeOffsetY)) +
        ')'
    )
    g_left_eye = dwg.add(dwg.g(transform=transform_left_eye))
    g_left_eye.add(dwg.polyline(points=face_generator.eyeLeftCountour, fill='white', stroke='white',
                                stroke_width=0.0 / face_generator.faceScale, stroke_linejoin="round", filter='url(#fuzzy)'))
    g_left_eye.add(dwg.polyline(points=face_generator.eyeLeftUpper, fill='none', stroke='black',
                                stroke_width=(5.0 if face_generator.haventSleptForDays else 3.0) / face_generator.faceScale,
                                stroke_linejoin="round", stroke_linecap="round", filter='url(#fuzzy)'))
    g_left_eye.add(dwg.polyline(points=face_generator.eyeLeftLower, fill='none', stroke='black',
                                stroke_width=(5.0 if face_generator.haventSleptForDays else 3.0) / face_generator.faceScale,
                                stroke_linejoin="round", stroke_linecap="round", filter='url(#fuzzy)'))
    for _ in range(10):
        clip_path_id = 'leftEyeClipPath'
        clip_path = dwg.defs.add(dwg.clipPath(id=clip_path_id))
        clip_path.add(dwg.polyline(points=face_generator.eyeLeftCountour))
        g_left_eye.add(dwg.circle(center=(face_generator.leftPupilShiftX + random.random() * 5 - 2.5,
                                          face_generator.leftPupilShiftY + random.random() * 5 - 2.5),
                                  r=random.random() * 2 + 3.0, fill='none', stroke='black',
                                  stroke_width=1.0 + random.random() * 0.5, stroke_linejoin="round",
                                  filter='url(#fuzzy)'))

    # Add right eye
    transform_right_eye = (
        'translate(' +
        str(face_generator.center[0] + face_generator.distanceBetweenEyes + face_generator.rightEyeOffsetX) +
        ' ' +
        str(-(-face_generator.center[1] + face_generator.eyeHeightOffset + face_generator.rightEyeOffsetY)) +
        ')'
    )
    g_right_eye = dwg.add(dwg.g(transform=transform_right_eye))
    g_right_eye.add(dwg.polyline(points=face_generator.eyeRightCountour, fill='white', stroke='white',
                                 stroke_width=0.0 / face_generator.faceScale, stroke_linejoin="round", filter='url(#fuzzy)'))
    g_right_eye.add(dwg.polyline(points=face_generator.eyeRightUpper, fill='none', stroke='black',
                                 stroke_width=(5.0 if face_generator.haventSleptForDays else 3.0) / face_generator.faceScale,
                                 stroke_linejoin="round", stroke_linecap="round", filter='url(#fuzzy)'))
    g_right_eye.add(dwg.polyline(points=face_generator.eyeRightLower, fill='none', stroke='black',
                                 stroke_width=(5.0 if face_generator.haventSleptForDays else 3.0) / face_generator.faceScale,
                                 stroke_linejoin="round", stroke_linecap="round", filter='url(#fuzzy)'))
    for _ in range(10):
        clip_path_id = 'rightEyeClipPath'
        clip_path = dwg.defs.add(dwg.clipPath(id=clip_path_id))
        clip_path.add(dwg.polyline(points=face_generator.eyeRightCountour))
        g_right_eye.add(dwg.circle(center=(face_generator.rightPupilShiftX + random.random() * 5 - 2.5,
                                           face_generator.rightPupilShiftY + random.random() * 5 - 2.5),
                                   r=random.random() * 2 + 3.0, fill='none', stroke='black',
                                   stroke_width=1.0 + random.random() * 0.5, stroke_linejoin="round",
                                   filter='url(#fuzzy)'))

    # Add hair
    hairColor = random.choice(face_generator.hairColors)
    for hair_line in face_generator.hairs:
        dwg.add(dwg.polyline(points=hair_line, fill='none', stroke=hairColor,
                             stroke_width=0.5 + random.random() * 2.5, stroke_linejoin='round', filter='url(#fuzzy)'))

    # Add nose
    if random.random() > 0.5:
        nose = draw_point_nose(dwg, face_generator.rightNoseCenterX, face_generator.rightNoseCenterY, 'rightNose')
        dwg.add(nose)
        nose = draw_point_nose(dwg, face_generator.leftNoseCenterX, face_generator.leftNoseCenterY, 'leftNose')
        dwg.add(nose)
    else:
        line_nose = draw_line_nose(dwg, face_generator.leftNoseCenterX, face_generator.leftNoseCenterY,
                                   face_generator.rightNoseCenterX, face_generator.rightNoseCenterY,
                                   face_generator.eyeHeightOffset)
        dwg.add(line_nose)

    # Add mouth
    dwg.add(dwg.polyline(points=face_generator.mouthPoints, fill="rgb(215,127,140)", stroke="black",
                         stroke_width=2.7 + random.random() * 0.5, stroke_linejoin="round", filter="url(#fuzzy)"))

    # Save image
    dwg.save()

    # Save as PNG if requested
    if save_png:
        cairosvg.svg2png(url=output_file, write_to=output_file.replace('.svg', '.png'))
