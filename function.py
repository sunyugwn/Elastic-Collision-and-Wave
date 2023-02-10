'''
particle = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름, 질량]
wall = [[x1, y1], [x2, y2], [x좌표 이동량, y좌표 이동량], [충격 흡수율]]
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
walls = [[[x1, y1], [x2, y2], [x좌표 이동량, y좌표 이동량], [충격 흡수율]], ...]
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
        x = random.uniform(r, space[0][0]-r)     #랜덤 좌표 부여
        y = random.uniform(r, space[0][1]-r)
        TF = True

        for cw in space[2]:    #벽과 겹치는지 검사
            if cw[0][0]-r<x<cw[1][0]+r and cw[1][1]-r<y<cw[0][1]+r:     #입자가 벽과 겹칠 가능성이 있는 범위에 있는가
                if cw[0][0]<x<cw[1][0] or cw[1][1]<y<cw[0][1]:          #입자가 벽의 모서리와 겹치는가
                    TF = False
                    break

                #입자가 벽의 꼭지점과 겹치는지 검사
                if cw[1][0]<x:     #x좌표가 벽의 오른쪽보다 큰가
                    cx = cw[1][0]   #검사할 꼭지점의 x좌표를 벽의 오른쪽으로 설정
                else:
                    cx = cw[0][0]   #검사할 꼭지점의 x좌표를 벽의 왼쪽으로 설정
                
                if cw[0][1]<y:     #y좌표가 벽의 위쪽보다 큰가
                    cy = cw[0][1]   #검사할 꼭지점의 y좌표를 벽의 위쪽으로 설정
                else:
                    cy = cw[1][1]   #검사할 꼭지점을 y좌표를 벽의 아래쪽으로 설정
                
                if calculate_line((x, y), (cx, cy)) < r:   #꼭지점과 겹치는지 검사
                    TF = False
                    break

        if TF == True:
            for cp in space[1]:     #다른 입자들과 닿아있는지 검사
                if calculate_line((x, y), cp[0]) < (r+cp[2]):
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
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5   #피타고라스 정리 이용


###두 점의 좌표가 주어졌을때 두 점 사이의 거리의 제곱 계산
'''
p = [x좌표, y좌표]
'''
def calculate_line_square(p1, p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2   #피타고라스 정리 이용


###두 점의 좌표가 주어졌을때 첫번째 점에서 두번째 점을 바라본 뱡향 계산
'''
p = [x좌표, y좌표]
'''
def calculate_direction(p1, p2):
    if p2[0]-p1[0] == 0:     #탄젠트 90, 270일때 에러 안나도록 예외
        return 180*(0>p2[1]-p1[1])
    
    return 90-math.degrees(math.atan((p2[1]-p1[1])/(p2[0]-p1[0])))+(p2[0]-p1[0]<0)*180   #탄젠트 값을 구하고 역탄젠트를 이용하여 방향 구하기


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
    #p1이 (0, 0)에 있고, p2의 이동량이 (0, 0)이라고 가정했을때 그려지는 직선과 p2가 중심인 반지름이 r1+r2인 원의 교점과 (0, 0)사이의 거리를 이용해서 구한다
    np2_pos = (p2[0][0]-p1[0][0], p2[0][1]-p1[0][1])   #p1이 (0, 0)에 있다고 가정할때, p2의 좌표 구하기
    p3_pos = minus_vector(p1[1], p2[1])               #p3 = p1이 (0, 0)에 있고, p2의 이동량이 (0, 0)이라고 가정할때, p1이 이동했을때의 좌표
    aq = calculate_line_square((0, 0), np2_pos)       #p1과 p2사이의 거리의 제곱
    bq = calculate_line_square(p3_pos, np2_pos)       #p2와 p3사이의 거리의 제곱
    c = calculate_line((0, 0), p3_pos)                #p1과 p3사이의 거리
    x = (aq-bq+c**2)/(2*c)     #p2에서 선분p1-p3에 내린 수선의 발과 p1사이의 거리(x+y=c, aq-x**2=bq-y**2으로 방정식 풀면 나오는 결과)
    hq = aq-x**2               #수선의 길이의 제곱
    rq = (p1[2]+p2[2])**2      #p1과 p2의 반지름의 합의 제곱
    if hq >= rq:               #충돌하는가
        return False
    
    q = (rq-hq)**0.5    #원의 교점과 수선의 발 사이의 거리
    result = (x-q)/c    #걸린 시간
    if result > 1:
        return False
    
    return (True, result)


###입자와 화면 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름]
size = [x크기, y크기]
'''
def check_crash_space(p, size):
    nx, ny = move_particle(p)      #충돌 없을때 이동 후 좌표
    r = p[2]
    x_check = r<=nx<=size[0]-r     #좌우 벽과 충돌하지 않았나
    y_check = r<=ny<=size[1]-r     #상하 벽과 충돌하지 않았나
    if x_check and y_check:        #아무 벽과 충돌하지 않았나
        return False
    
    if y_check:    #좌우 벽과 충돌 처리
        return (((p[1][0]>0)*size[0]-p[0][0]+((p[1][0]<0)*2-1)*p[2])/p[1][0], 'rl')    #시간 = 벽과의 거리/이동거리
    
    if x_check:    #상하 벽과 충돌 처리
        return (((p[1][1]>0)*size[1]-p[0][1]+((p[1][1]<0)*2-1)*p[2])/p[1][1], 'ud')    #시간 = 벽과의 거리/이동거리
    
    a = ((p[1][0]>0)*size[0]-p[0][0]+((p[1][0]<0)*2-1)*p[2])/p[1][0]    #좌우 벽과 충돌
    b = ((p[1][1]>0)*size[1]-p[0][1]+((p[1][1]<0)*2-1)*p[2])/p[1][1]    #상하 벽과 충돌
    if a < b:
        return (a, 'rl')
    
    return (b, 'ud')


###입자와 벽 충돌 체크 및 충돌 시간 반환
'''
p = [[x좌표, y좌표], [x좌표 이동량, y좌표 이동량], 반지름]
w = [[x1, y1], [x2, y2], [x좌표 이동량, y좌표 이동량]]
'''
def check_crash_wall(p, w):
    npv = minus_vector(p[1], w[2])
    
    x = (w[1][0]<p[0][0])-(w[0][0]>p[0][0])     #왼쪽:-1, 중간:0, 오른쪽:1
    
    y = (w[0][1]<p[0][0])-(w[1][1]>p[0][0])     #아래쪽:-1, 중간:0, 위쪽:1
    
    if (x, y) == (0, 0):
        return 'Error'
    
    #왼쪽 벽
    if x == -1:
        if npv[0] > 0 and p[0][0]+p[2] < w[0][0]:      #오른쪽으로 이동 중이고, 왼쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[0][0]-p[0][0]-p[2])/npv[0]          #걸린 시간
            if (0 <= t <= 1) and (w[1][1] <= p[0][1]+npv[1]*t <= w[0][1]):   #걸린 시간이 0과 1사이고, 충돌지점이 벽인가
                return (t, 'l')
    
    #오른쪽 벽
    elif x == 1:
        if npv[0] < 0 and p[0][0]-p[2] > w[0][0]:     #왼쪽으로 이동 중이고, 오른쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[1][0]-p[0][0]+p[2])/npv[0]         #걸린 시간
            if (0 <= t <= 1) and (w[1][1] <= p[0][1]+npv[1]*t <= w[0][1]):   #걸린 시간이 0과 1사이고, 충돌지점이 벽인가
                return (True, 'r')
    
    #아래쪽 벽
    if y == -1:
        if npv[1] > 0 and p[0][1]+p[2] < w[1][1]:     #위로 이동 중이고, 아래쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[1][1]-p[0][1]-p[2])/npv[0]         #걸린 시간
            if (0 <= 1 <= 1) and (w[0][0] <= p[0][0]+npv[0]*t <= w[1][0]):   #걸린 시간이 0과 1사이고, 충돌지점이 벽인가
                return (True, 'd')
    
    #위쪽 벽
    elif y == 1:
        if npv[1] < 0 and p[0][1]-p[2] > w[0][1]:     #아래로 이동 중이고, 위쪽 벽과 충돌 할 수 있는 위치에 있는가
            t = (w[0][1]-p[0][1]+p[2])/npv[0]         #걸린 시간
            if (0 <= 1 <= 1) and (w[0][0] <= p[0][0]+npv[0]*t <= w[1][0]):   #걸린 시간이 0과 1 사이고, 충돌지점이 벽인가
                return (True, 'u')
    
    #벽의 꼭지점
    f = lambda x:(x+1)//2    #-1 >>> 0, 1 >>> 1
    check = 10     #시간이 가장 적게 걸린 것을 고르기 위한 리스트(시간)
    
    if x == 0:   #(0, 1) 또는 (0, -1)에 있는 경우
        for i in [0, 1]:
            a = check_crash_particle(p, ([w[i][0], w[1-f(y)][1]], w[2], 0))     #충돌 검사
            if a != False and a[1] < check:     #충돌했고, 가장 적은 시간이 걸렸나
                check = a[1]                #충돌 시간과 충돌 대상 저장
                check_point = (i, 1-f(y))
    
    elif y == 0:   #(-1, 0) 또는 (1, 0)에 있는 경우
        for i in [0, 1]:
            a = check_crash_particle(p, ([w[f(x)][0], w[i][1]], w[2], 0))     #충돌 검사
            if a != False and a[1] < check:     #충돌했고, 가장 적은 시간이 걸렸나
                check = a[1]                #충돌 시간과 충돌 대상 저장
                check_point = (f(x), w[i])
    
    else:   #나머지 경우
        for i1 in [0, 1]:
            for i2 in [0, 1]:
                if (i1, i2) != (1-f(x), f(y)):   #충돌가능한 위치인가
                    a = check_crash_particle(p, ((w[i1][i2]), w[2], 0))   #충돌 검사
                    if a != False and a[1] < check:   #충돌했고, 가장 적은 시간이 걸렸나
                        check = a[1]        #충돌 시간과 충돌 대상 저장
                        check_point = (i1, i2)
    
    if check == 10:   #기본값이 안 바뀌었다면 충돌하지 않았다는 뜻
        return False
    
    return (check, check_point)
