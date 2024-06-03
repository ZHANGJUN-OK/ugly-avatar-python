import math
import random
import utils.face_shape as faceShape
import utils.eye_shape as eyeShape
import utils.hair_lines as hairLines
import utils.mouth_shape as mouthShape


def randomFromInterval(min_val, max_val):
    return random.uniform(min_val, max_val)

class FaceGenerator:
    def __init__(self):
        self.faceScale = 1.8
        self.faceHeight = 0
        self.faceWidth = 0
        self.center = [0, 0]
        self.computedFacePoints = []
        self.eyeRightUpper = []
        self.eyeRightLower = []
        self.eyeRightCountour = []
        self.eyeLeftUpper = []
        self.eyeLeftLower = []
        self.eyeLeftCountour = []
        self.distanceBetweenEyes = 0
        self.leftEyeOffsetX = 0
        self.leftEyeOffsetY = 0
        self.rightEyeOffsetX = 0
        self.rightEyeOffsetY = 0
        self.eyeHeightOffset = 0
        self.leftEyeCenter = [0, 0]
        self.rightEyeCenter = [0, 0]
        self.rightPupilShiftX = 0
        self.rightPupilShiftY = 0
        self.leftPupilShiftX = 0
        self.leftPupilShiftY = 0
        self.rightNoseCenterX = 0
        self.rightNoseCenterY = 0
        self.leftNoseCenterX = 0
        self.leftNoseCenterY = 0
        self.hairs = []
        self.haventSleptForDays = False
        self.hairColors = [
        "rgb(0, 0, 0)", # Black
        "rgb(44, 34, 43)", # Dark Brown
        "rgb(80, 68, 68)", # Medium Brown
        "rgb(167, 133, 106)", # Light Brown
        "rgb(220, 208, 186)", # Blond
        "rgb(233, 236, 239)", # Platinum Blond
        "rgb(165, 42, 42)", # Red
        "rgb(145, 85, 61)", # Auburn
        "rgb(128, 128, 128)", # Grey
        "rgb(185, 55, 55)", # Fire
        "rgb(255, 192, 203)", # Pastel Pink
        "rgb(255, 105, 180)", # Bright Pink
        "rgb(230, 230, 250)", # Lavender
        "rgb(64, 224, 208)", # Turquoise
        "rgb(0, 191, 255)", # Bright Blue
        "rgb(148, 0, 211)", # Deep Purple
        "rgb(50, 205, 50)", # Lime Green
        "rgb(255, 165, 0)", # Vivid Orange
        "rgb(220, 20, 60)", # Crimson Red
        "rgb(192, 192, 192)", # Silver
        "rgb(255, 215, 0)", # Gold
        "rgb(255, 255, 255)", # White
        "rgb(124, 252, 0)", # Lawn Green
        "rgb(127, 255, 0)", # Chartreuse
        "rgb(0, 255, 127)", # Spring Green
        "rgb(72, 209, 204)", # Medium Turquoise
        "rgb(0, 255, 255)", # Cyan
        "rgb(0, 206, 209)", # Dark Turquoise
        "rgb(32, 178, 170)", # Light Sea Green
        "rgb(95, 158, 160)", # Cadet Blue
        "rgb(70, 130, 180)", # Steel Blue
        "rgb(176, 196, 222)", # Light Steel Blue
        "rgb(30, 144, 255)", # Dodger Blue
        "rgb(135, 206, 235)", # Sky Blue
        "rgb(0, 0, 139)", # Dark Blue
        "rgb(138, 43, 226)", # Blue Violet
        "rgb(75, 0, 130)", # Indigo
        "rgb(139, 0, 139)", # Dark Magenta
        "rgb(153, 50, 204)", # Dark Orchid
        "rgb(186, 85, 211)", # Medium Orchid
        "rgb(218, 112, 214)", # Orchid
        "rgb(221, 160, 221)", # Plum
        "rgb(238, 130, 238)", # Violet
        "rgb(255, 0, 255)", # Magenta
        "rgb(216, 191, 216)", # Thistle
        "rgb(255, 20, 147)", # Deep Pink
        "rgb(255, 69, 0)", # Orange Red
        "rgb(255, 140, 0)", # Dark Orange
        "rgb(255, 165, 0)", # Orange
        "rgb(250, 128, 114)", # Salmon
        "rgb(233, 150, 122)", # Dark Salmon
        "rgb(240, 128, 128)", # Light Coral
        "rgb(205, 92, 92)", # Indian Red
        "rgb(255, 99, 71)", # Tomato
        "rgb(255, 160, 122)", # Light Salmon
        "rgb(220, 20, 60)", # Crimson
        "rgb(139, 0, 0)", # Dark Red
        "rgb(178, 34, 34)", # Fire Brick
        "rgb(250, 235, 215)", # Antique White
        "rgb(255, 239, 213)", # Papaya Whip
        "rgb(255, 235, 205)", # Blanched Almond
        "rgb(255, 222, 173)", # Navajo White
        "rgb(245, 245, 220)", # Beige
        "rgb(255, 228, 196)", # Bisque
        "rgb(255, 218, 185)", # Peach Puff
        "rgb(244, 164, 96)", # Sandy Brown
        "rgb(210, 180, 140)", # Tan
        "rgb(222, 184, 135)", # Burly Wood
        "rgb(250, 250, 210)", # Light Goldenrod Yellow
        "rgb(255, 250, 205)", # Lemon Chiffon
        "rgb(255, 245, 238)", # Sea Shell
        "rgb(253, 245, 230)", # Old Lace
        "rgb(255, 228, 225)", # Misty Rose
        "rgb(255, 240, 245)", # Lavender Blush
        "rgb(250, 240, 230)", # Linen
        "rgb(255, 228, 181)", # Moccasin
        "rgb(255, 250, 250)", # Snow
        "rgb(240, 255, 255)", # Azure
        "rgb(240, 255, 240)", # Honeydew
        "rgb(245, 245, 245)", # White Smoke
        "rgb(245, 255, 250)", # Mint Cream
        "rgb(240, 248, 255)", # Alice Blue
        "rgb(240, 248, 255)", # Ghost White
        "rgb(248, 248, 255)", # Ghost White
        "rgb(255, 250, 240)", # Floral White
        "rgb(253, 245, 230)", # Old Lace
      ]
        self.hairColor = "black"
        self.dyeColorOffset = "50%"
        self.backgroundColors = [
        "rgb(245, 245, 220)", # Soft Beige
        "rgb(176, 224, 230)", # Pale Blue
        "rgb(211, 211, 211)", # Light Grey
        "rgb(152, 251, 152)", # Pastel Green
        "rgb(255, 253, 208)", # Cream
        "rgb(230, 230, 250)", # Muted Lavender
        "rgb(188, 143, 143)", # Dusty Rose
        "rgb(135, 206, 235)", # Sky Blue
        "rgb(245, 255, 250)", # Mint Cream
        "rgb(245, 222, 179)", # Wheat
        "rgb(47, 79, 79)", # Dark Slate Gray
        "rgb(72, 61, 139)", # Dark Slate Blue
        "rgb(60, 20, 20)", # Dark Brown
        "rgb(25, 25, 112)", # Midnight Blue
        "rgb(139, 0, 0)", # Dark Red
        "rgb(85, 107, 47)", # Olive Drab
        "rgb(128, 0, 128)", # Purple
        "rgb(0, 100, 0)", # Dark Green
        "rgb(0, 0, 139)", # Dark Blue
        "rgb(105, 105, 105)", # Dim Gray
        "rgb(240, 128, 128)", # Light Coral
        "rgb(255, 160, 122)", # Light Salmon
        "rgb(255, 218, 185)", # Peach Puff
        "rgb(255, 228, 196)", # Bisque
        "rgb(255, 222, 173)", # Navajo White
        "rgb(255, 250, 205)", # Lemon Chiffon
        "rgb(250, 250, 210)", # Light Goldenrod Yellow
        "rgb(255, 239, 213)", # Papaya Whip
        "rgb(255, 245, 238)", # Sea Shell
        "rgb(255, 248, 220)", # Cornsilk
        "rgb(255, 255, 240)", # Ivory
        "rgb(240, 255, 240)", # Honeydew
        "rgb(240, 255, 255)", # Azure
        "rgb(240, 248, 255)", # Alice Blue
        "rgb(248, 248, 255)", # Ghost White
        "rgb(255, 250, 250)", # Snow
        "rgb(255, 240, 245)", # Lavender Blush
        "rgb(255, 228, 225)", # Misty Rose
        "rgb(230, 230, 250)", # Lavender
        "rgb(216, 191, 216)", # Thistle
        "rgb(221, 160, 221)", # Plum
        "rgb(238, 130, 238)", # Violet
        "rgb(218, 112, 214)", # Orchid
        "rgb(186, 85, 211)", # Medium Orchid
        "rgb(147, 112, 219)", # Medium Purple
        "rgb(138, 43, 226)", # Blue Violet
        "rgb(148, 0, 211)", # Dark Violet
        "rgb(153, 50, 204)", # Dark Orchid
        "rgb(139, 69, 19)", # Saddle Brown
        "rgb(160, 82, 45)", # Sienna
        "rgb(210, 105, 30)", # Chocolate
        "rgb(205, 133, 63)", # Peru
        "rgb(244, 164, 96)", # Sandy Brown
        "rgb(222, 184, 135)", # Burly Wood
        "rgb(255, 250, 240)", # Floral White
        "rgb(253, 245, 230)", # Old Lace
        "rgb(250, 240, 230)", # Linen
      ]
        self.mouthPoints = []

    def generateFace(self):
        self.faceScale = 1.5 + random.random() * 0.6
        self.haventSleptForDays = random.random() > 0.8
        faceResults = faceShape.generate_face_contour_points()
        self.computedFacePoints = faceResults["face"]
        self.faceHeight = faceResults["height"]
        self.faceWidth = faceResults["width"]
        self.center = faceResults["center"]
        
        eyes = eyeShape.generate_both_eyes(self.faceWidth / 2)
        left = eyes["left"]
        right = eyes["right"]
        
        self.eyeRightUpper = right["upper"]
        self.eyeRightLower = right["lower"]
        self.eyeRightCountour = right["upper"][10:90] + right["lower"][10:90][::-1]
        self.eyeLeftUpper = left["upper"]
        self.eyeLeftLower = left["lower"]
        self.eyeLeftCountour = left["upper"][10:90] + left["lower"][10:90][::-1]
        
        self.distanceBetweenEyes = randomFromInterval(self.faceWidth / 4.5, self.faceWidth / 4)
        self.eyeHeightOffset = randomFromInterval(self.faceHeight / 8, self.faceHeight / 6)
        self.leftEyeOffsetX = randomFromInterval(-self.faceWidth / 20, self.faceWidth / 10)
        self.leftEyeOffsetY = randomFromInterval(-self.faceHeight / 50, self.faceHeight / 50)
        self.rightEyeOffsetX = randomFromInterval(-self.faceWidth / 20, self.faceWidth / 10)
        self.rightEyeOffsetY = randomFromInterval(-self.faceHeight / 50, self.faceHeight / 50)
        self.leftEyeCenter = left["center"]
        self.rightEyeCenter = right["center"]
        
        self.leftPupilShiftX = randomFromInterval(-self.faceWidth / 20, self.faceWidth / 20)
        
        leftInd0 = int(randomFromInterval(10, len(left["upper"]) - 10))
        rightInd0 = int(randomFromInterval(10, len(right["upper"]) - 10))
        leftInd1 = int(randomFromInterval(10, len(left["upper"]) - 10))
        rightInd1 = int(randomFromInterval(10, len(right["upper"]) - 10))
        
        leftLerp = randomFromInterval(0.2, 0.8)
        rightLerp = randomFromInterval(0.2, 0.8)
        
        self.leftPupilShiftY = left["upper"][leftInd0][1] * leftLerp + left["lower"][leftInd1][1] * (1 - leftLerp)
        self.rightPupilShiftY = right["upper"][rightInd0][1] * rightLerp + right["lower"][rightInd1][1] * (1 - rightLerp)
        self.leftPupilShiftX = left["upper"][leftInd0][0] * leftLerp + left["lower"][leftInd1][0] * (1 - leftLerp)
        self.rightPupilShiftX = right["upper"][rightInd0][0] * rightLerp + right["lower"][rightInd1][0] * (1 - rightLerp)
        
        numHairLines = [int(randomFromInterval(0, 50)) for _ in range(4)]
        self.hairs = []
        
        if random.random() > 0.3:
            self.hairs += hairLines.generate_hair_lines_0(self.computedFacePoints, math.floor(numHairLines[0] + 10))
        if random.random() > 0.3:
            self.hairs += hairLines.generate_hair_lines_1(self.computedFacePoints, math.floor(numHairLines[1] / 1.5 + 10))
        if random.random() > 0.5:
            self.hairs += hairLines.generate_hair_lines_2(self.computedFacePoints, math.floor(numHairLines[2] * 3 + 10))
        if random.random() > 0.5:
            self.hairs += hairLines.generate_hair_lines_3(self.computedFacePoints, math.floor(numHairLines[3] * 3 + 10))
        
        self.rightNoseCenterX = randomFromInterval(self.faceWidth / 18, self.faceWidth / 12)
        self.rightNoseCenterY = randomFromInterval(0, self.faceHeight / 5)
        self.leftNoseCenterX = randomFromInterval(-self.faceWidth / 18, -self.faceWidth / 12)
        self.leftNoseCenterY = self.rightNoseCenterY + randomFromInterval(-self.faceHeight / 30, self.faceHeight / 20)
        
        if random.random() > 0.8:
            self.mouthPoints = mouthShape.generate_mouth_shape2(self.computedFacePoints, self.faceHeight, self.faceWidth)
        elif random.random() > 0.4:
            self.mouthPoints = mouthShape.generate_mouth_shape1(self.computedFacePoints, self.faceHeight, self.faceWidth)
        else:
            self.mouthPoints = mouthShape.generate_mouth_shape0(self.computedFacePoints, self.faceHeight, self.faceWidth)
        
        self.hairColor = random.choice(self.hairColors)
        self.dyeColorOffset = f"{randomFromInterval(5, 95)}%"