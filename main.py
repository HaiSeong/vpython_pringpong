#Web VPython 3.2
from vpython import *

# 충돌 함수
def check_collision(ball, object):
    # ball의 중심에서 object의 표면까지의 거리를 계산
    dist = ball.pos - object.pos

    # 만약 이 거리가 ball의 반지름 + object의 반의 크기보다 작다면 충돌
    if (abs(dist.x) <= (ball.radius + object.size.x / 2) and
        abs(dist.y) <= (ball.radius + object.size.y / 2) and
        abs(dist.z) <= (ball.radius + object.size.z / 2)):
        return True  # 충돌 발생

    return False  # 충돌 안함


def handle_collision_table(ball, table):
    ball.v.y *= -1
    ball.pos.y = table.size.y / 2 + ball.radius


def handle_collision_net(ball, net):
    # 네트에 충돌했을 때 공을 적절한 위치로 이동
    if ball.v.x > 0:
        ball.pos.x = net.pos.x - net.size.x / 2 - ball.radius
    else:
        ball.pos.x = net.pos.x + net.size.x / 2 + ball.radius

    # 공의 속도를 역방향으로 설정
    ball.v.x *= -1



# 게임 세팅 초기화
# 예) 공, 라켓, 테이블, 스코어 등
g = 9.8 / 4

# 공 객체 생성
ball_radius = 0.05  # 공의 반지름
ball = sphere(pos=vector(-0.2, 0.5, 0), radius=ball_radius, color=color.orange)# 공의 질량 설정
ball.mass = 0.0027
ball.v = vector(0, 0, 0)
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
racket.pos = vec(table_length/2, 0.2, 0)


dt = 0.01

# 메인 루프
while True:
    # 공, 라켓 위치 등 초기화
    while True:
        rate(1/dt)
        # 사용자 입력 처리

        # 게임 로직 업데이트

        if check_collision(ball, net):
            handle_collision_net(ball, net)
        if check_collision(ball, table):
            handle_collision_table(ball, table)

        # 그래픽 업데이트
        ball.f = ball.mass * vector(0, -g, 0)
        ball.a = ball.f / ball.mass
        ball.v = ball.v + ball.a * dt
        ball.pos = ball.pos + ball.v * dt


    # 스코어 처리
