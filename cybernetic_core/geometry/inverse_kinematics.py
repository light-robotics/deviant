import math

a = 8
b = 12.3

def leg_angles(Cx: float, Cy: float) -> [float, float]:
    dist = math.sqrt(Cx ** 2 + Cy ** 2)

    alpha1 = math.acos((a ** 2 + dist ** 2 - b ** 2) / (2 * a * dist))
    beta1 = math.acos((a ** 2 + b ** 2 - dist ** 2) / (2 * a * b))
    #beta = -1 * (math.pi - beta1)
    beta = math.pi - beta1

    alpha2 = math.atan2(Cy, Cx)
    alpha = alpha1 + alpha2

    return math.degrees(alpha), math.degrees(beta)

    Bx = a * math.cos(alpha)
    By = a * math.sin(alpha)

    Cx = Bx + b * math.cos(alpha + beta)
    Cy = By + b * math.sin(alpha + beta)

    print(f'alpha: {math.degrees(alpha)}')
    print(f'beta : {math.degrees(beta)}')
    print(f'B: {[Bx, By]}. C: {[Cx, Cy]}')