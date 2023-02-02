'''
particle = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름, 질량]
wall = [[x1, y1], [x2, y2], [x좌표 이동량, y좌표 이동량]]
space = [[공간 가로길이, 공간 세로길이], [particle], [wall]]]
'''
#모듈 호출
import math
import random
#함수 정의
##만들기##
###공간 만들기
'''
size = [공간 가로길이, 공간 세로길이]
'''
def make_space(size):
    return [size, [], []]


###벽 만들기
'''
walls = [[[x1, y1], [x2, y2], [x좌표 이동량, y좌표 이동량]], ...]
'''
def make_walls(space, walls):
    space[2] += walls


###입자 만들기
'''
space = 공간
v = 속도
r = 반지름
m = 질량
l = 최대 입자 수
'''
def make_particles(space, v, r, m, l):
    for _ in range(l):
        x = random.uniform(r, space[0][0]-r)
        y = random.uniform(r, space[0][1]-r)
        TF = True
        if space[1] != []:
            for cp in space[1]:
                if calculate_line((x, y), cp[0]) < (r+cp[2]):
                    TF = False
                    break
        
        if TF == True:
            for cw in space[2]:
                if cw[0][0]-r<x<cw[1][0]+r and cw[1][1]-r<y<cw[0][1]+r:
                    if cw[0][0]<x<cw[1][0] or cw[1][1]<y<cw[0][1]:
                        TF = False
                        break

                    if cw[1][0]<x:
                        cx = cw[1][0]
                    else:
                        cx = cw[0][0]
                    
                    if cw[0][1]<y:
                        cy = cw[0][1]
                    else:
                        cy = cw[1][1]
                    
                    if calculate_line((x, y), (cx, cy)) < r:
                        TF = False
                        break
        
        if TF == True:
            pv = random.uniform(0, 2*v)
            pd = math.radians(random.uniform(0, 360))
            space[1].append([[x, y], [pv*math.sin(pd), pv*math.cos(pd)], r, m])


##측정##
###두 점의 좌표가 주어졌을때 두 점 사이의 거리 계산
'''
p = [x좌표, y좌표]
'''
def calculate_line(p1, p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5


###두 점의 좌표가 주어졌을때 두 점 사이의 거리의 제곱 계산
'''
p = [x좌표, y좌표]
'''
def calculate_line_square(p1, p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2


###두 점의 좌표가 주어졌을때 첫번째 점에서 두번째 점을 바라본 뱡향 계산
'''
p = [x좌표, y좌표]
'''
def calculate_direction(p1, p2):
    if p2[0]-p1[0] == 0:
        return 180*(0>p2[1]-p1[1])
    
    return 90-math.degrees(math.atan((p2[1]-p1[1])/(p2[0]-p1[0])))+(p2[0]-p1[0]<0)*180


##벡터##
###벡터 합
'''
v = [x좌표 이동량, y좌표 이동량]
'''
def plus_vector(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1]]


#벡터 차
'''
v = [x좌표 이동량, y좌표 이동량]
'''
def minus_vector(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1]]


##물리엔진##
###입자 이동시키기
'''
p = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량]]
'''
def move_particle(p):
    return [p[0][0]+p[1][0], p[0][1]+p[1][1]]


###입자끼리 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름]
'''
def check_crash_particle(p1, p2):
    np2_pos = (p2[0][0]-p1[0][0], p2[0][1]-p1[0][1])
    p3_pos = minus_vector(p1[1], p2[1])
    aq = calculate_line_square((0, 0), np2_pos)
    bq = calculate_line_square(p3_pos, np2_pos)
    c = calculate_line((0, 0), p3_pos)
    x = (aq-bq+c**2)/(2*c)
    hq = aq-x**2
    h = hq**0.5
    r = p1[2]+p2[2]
    if h >= r:
        return False
    
    w = (r**2-hq)**0.5
    return (True, (x-w)/c)


###입자와 화면 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름]
size = [x크기, y크기]
'''
def check_crash_space(p, size):
    nx, ny = move_particle(p)
    r = p[2]
    x_check = r<=nx<=size[0]-r
    y_check = r<=ny<=size[1]-r
    if x_check and y_check:
        return False
    
    if y_check:
        return (True, (size[0]/2-abs(p[0][0]-size[0]/2)-p[2])/abs(p[1][0]))
    
    if x_check:
        return (True, (size[1]/2-abs(p[0][1]-size[1]/2)-p[2])/abs(p[1][1]))
    
    return (True, min((size[0]/2-abs(p[0][0]-size[0]/2)-p[2])/abs(p[1][0]), (size[1]/2-abs(p[0][1]-size[1]/2)-p[2])/abs(p[1][1])))


###입자와 벽 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름]
w = [[x1, y1], [x2, y2], [x좌표 이동량, y좌표 이동량]]
'''
def check_crash_wall(p, w):
    pass
