#Web VPython 3.2
from vpython import *
import random

# 충돌 함수
def check_collision(ball, object):
    # ball의 중심에서 object의 표면까지의 거리를 계산
    dist = ball.pos - object.pos

    # 만약 이 거리가 ball의 반지름 + object의 반의 크기보다 작다면 충돌
    if (abs(dist.x) <= (ball.radius + object.size.x / 2) and abs(dist.y) <= (ball.radius + object.size.y / 2) and abs(dist.z) <= (ball.radius + object.size.z / 2)):
        return True  # 충돌 발생

    return False  # 충돌 안함


def handle_collision_table(ball, table):
    global before_table
    global user_win

    ball.v.y *= -1
    ball.pos.y = table.size.y / 2 + ball.radius

    if ball.pos.x >= 0:  # user쪽 테이블에 충돌
        if before_table == 1:
            user_win = False # user 패배
            return
        before_table = 1
        ball.color = color.green
    else:  # cpu쪽 테이블에 충돌
        ball.color = color.red
        if before_table == 2:
            user_win = True # user win
            return
        before_table = 2


def handle_collision_net(ball, net):
    # 비탄성 충돌 계수
    coefficient_of_restitution = 0.1

    # 네트에 충돌했을 때 공을 적절한 위치로 이동
    if ball.v.x > 0:
        ball.pos.x = net.pos.x - net.size.x / 2 - ball.radius
    else:
        ball.pos.x = net.pos.x + net.size.x / 2 + ball.radius

    # 공의 속도를 역방향으로 설정하고, 비탄성 충돌 계수를 곱해줌
    ball.v.x = -ball.v.x * coefficient_of_restitution


def handle_collision_racket(ball, racket):
    global before_hit
    global before_table
    global user_win
    global dir

    # 충돌했을 때 공을 적절한 위치로 이동
    if ball.v.x > 0: # cpu가 공을 칠때
        ball.pos.x = racket.pos.x - racket.size.x / 2 - ball.radius
        if before_table != 1: # 테이블에 바운드 되지 않고 바로 치는 경우 실점
            user_win = True
        before_hit = 2
        if dir is not None:
            ball.v.z += dir * 0.25
            dir = None
    else: # 유저가 공을 칠때
        ball.pos.x = racket.pos.x + racket.size.x / 2 + ball.radius
        if before_table != 2:
            user_win = False
        ball.v.z += (random.random() - 0.5) * 0.25
        before_hit = 1

    # 공의 속도를 역방향으로 설정
    ball.v.x *= -1
    ball.v.y = 1.2

    # # z 방향으로 약간의 랜덤 값 조정
    # ball.v.z += (random.random() - 0.5) * 0.025

def check_out_of_bounds(ball):
    global before_table
    global user_win
    # 볼이 테이블 영역 바깥에 있는지 확인
    if ball.pos.y >= -0.5:
        return

    if ball.pos.x >= 0: # user 쪽으로 떨어짐
        if before_table == 1:
            user_win = False # loose
            return
        else:
            user_win = True #win
            return
    else:
        if before_table == 2:
            user_win = True # user win
            return
        else:
            user_win = False #user loose
            return


def key_handle(evt):
    global move
    global dir

    speed = 0.02
    if evt.key == "w":
        move.y = speed
    if evt.key == "s":
        move.y = -speed
    if evt.key == "up":
        move.x = -speed
    if evt.key == "down":
        move.x = speed
    if evt.key == "left":
        move.z = speed
    if evt.key == "right":
        move.z = -speed

    if evt.key == "a":
        dir = 1
    elif evt.key == "d":
        dir = -1
    else:
        dir = None

# 게임 세팅 초기화
# 예) 공, 라켓, 테이블, 스코어 등
g = 9.8 / 4

# 공 객체 생성
ball_radius = 0.05  # 공의 반지름
ball = sphere(pos=vector(-0.2, 0.3, 0), radius=ball_radius, color=color.orange)# 공의 질량 설정
ball.mass = 0.0027
ball.v = vector(1.5, -0.1, 0)
ball.a = vector(0, -g, 0)
ball.f = vector(0, 0, 0)

# 탁구 테이블 객체 생성
table_length = 2.74
table_width = 1.525
table_height = 0.1
table = box(pos=vector(0, -table_height / 2, 0), size=vector(table_length, table_height, table_width), color=color.blue)

table_lines = [
    box(pos=vector(0, -table_height / 2, 0), size=vector(0.02, table_height+0.0001, table_width+0.0001), color=color.white),
    box(pos=vector(table_length/2 - 0.01, -table_height / 2, 0), size=vector(0.02+0.0001, table_height+0.0001, table_width+0.0001), color=color.white),
    box(pos=vector(-table_length/2 + 0.01, -table_height / 2, 0), size=vector(0.02+0.0001, table_height+0.0001, table_width+0.0001), color=color.white),
    box(pos=vector(0, -table_height / 2, table_width/2 - 0.01), size=vector(table_length, table_height+0.0001, 0.02+0.0001), color=color.white),
    box(pos=vector(0, -table_height / 2, -table_width/2 + 0.01), size=vector(table_length, table_height+0.0001, 0.02+0.0001), color=color.white),
]

# 네트의 속성 설정
net_height = 0.15  # 네트의 높이
net_thickness = 0.005-0.00001  # 네트의 두께

# 네트 객체 생성
net = box(pos=vector(0, net_height / 2, 0), size=vector(net_thickness, net_height, table_width), color=vector(0.6, 0.6, 0.6), opacity = 0.6) # 실제 충돌을 받을 객체는 안보이게함
net_lines = [
    box(pos=vector(0, net_height / 2 + 0.0001, table_width / 60 * i), size=vector(0.005, net_height, 0.005), color=color.white) for i in range(-30, 31)
] + [
    box(pos=vector(0, net_height / 6 * i, 0), size=vector(0.005, 0.005, table_width), color=color.white) for i in range(7) # 모양을 위한 객체
]

# 라켓 헤드 정의
racket_head_radius = 0.15  # 반지름
racket_head_length = 0.04  # 두께
racket_handle_width = 0.04  # 폭
racket_handle_length = 0.1  # 길이
racket_head = cylinder(pos=vector(-racket_handle_width/2, 0, 0),
                       radius=racket_head_radius,
                       length=racket_head_length,
                       color=color.red)
# 라켓 핸들 정의
racket_handle = box(pos=vector(0, -racket_head_radius - racket_handle_length / 2, 0),
                    size=vector(racket_handle_width, racket_handle_length, racket_head_length),
                    color=color.white)


# 라켓 정의
racket = compound([racket_head, racket_handle])
racket.pos = vec(table_length / 2 - 0.3, 0.2, 0)
racket2 = compound([racket_head, racket_handle])
racket2.pos = vec(-table_length/2 + 0.3, 0.2, 0)

# 이벤트 리스너를 등록
scene.bind("keydown", key_handle)

# 카메라의 위치를 설정
scene.camera.pos = vec(table_length -0.2, 1.5, 0)

# 카메라가 바라보는 방향을 설정
scene.camera.axis = vec(0,0,0) - scene.camera.pos

move = vec(0,0,0)
dir = None
before_hit = None # 이전에 친 라켓을 저장 1 or 2
before_table = None
user_win = None

score_user = 0
score_cpu = 0
serve = 1

dt = 0.01

# 메인 루프
while True:
    # 공, 라켓 위치 등 초기화
    while True:
        rate(1/dt)
        # 사용자 입력 처리

        # 게임 로직 업데이트
        if user_win is not None:
            if user_win:
                score_user += 1
                serve = 1 # 이긴사람이 서브를 가져감
            else:
                score_cpu += 1
                serve = -1
            score_label = label(pos=vector(0, 0, 0), text=f"user {score_user} : {score_cpu} cpu" , height=20, color=color.green)
            sleep(1.5)
            user_win = None
            before_table = None
            before_hit = None
            score_label.visible = False
            ball.v = vector(1.5 * serve, -0.1, 0) # 서브 받기
            ball.pos=vector(-0.2, 0.3, 0)
            racket.pos = vec(table_length / 2 - 0.3, 0.2, 0)
            racket2.pos = vec(-table_length / 2 + 0.3, 0.2, 0)

            break

        check_out_of_bounds(ball)
        if check_collision(ball, net):
            handle_collision_net(ball, net)
        elif check_collision(ball, table):
            handle_collision_table(ball, table)
        elif check_collision(ball, racket):
            handle_collision_racket(ball, racket)
        elif check_collision(ball, racket2):
            handle_collision_racket(ball, racket2)

        # 그래픽 업데이트
        ball.f = ball.mass * vector(0, -g, 0)
        ball.a = ball.f / ball.mass
        ball.v = ball.v + ball.a * dt
        ball.pos = ball.pos + ball.v * dt
        ball.opacity = 1.0 - ball.pos.y * 0.8 # 공이 높으면 투명하게 보이게 (높이 구별 위해)
        # 유저 라켓 이동
        racket.pos += move
        move *= 0.8

        if mag(ball.pos - racket.pos) < 0.25:
            racket.pos.y += (-racket.pos.y + ball.pos.y) * 0.2
        # cpu 라켓 이동
        if mag(ball.pos - racket2.pos) < 0.5:
            racket2.pos.y += (-racket2.pos.y + ball.pos.y) * 0.2
            racket2.pos.z += (-racket2.pos.z + ball.pos.z) * 0.95
        if mag(ball.pos - racket2.pos) < 2:
            racket2.pos.y += (-racket2.pos.y + ball.pos.y) * 0.02
            racket2.pos.z += (-racket2.pos.z + ball.pos.z) * 0.095


    # 스코어 처리