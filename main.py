#Web VPython 3.2
from vpython import *

# 게임 세팅 초기화
# 예) 공, 라켓, 테이블, 스코어 등
g = 9.8

# 공 객체 생성
ball_radius = 0.05  # 공의 반지름
ball = sphere(pos=vector(0, 0.7, 0), radius=ball_radius, color=color.orange)# 공의 질량 설정
ball.mass = 0.0027
ball.v = vector(0, 0, 0)
ball.a = vector(0, -g, 0)
ball.f = vector(0, 0, 0)

# 탁구 테이블 객체 생성
table_length = 2.74
table_width = 1.525
table_height = 0.05
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

dt = 0.01

# 메인 루프
while True:
    # 공, 라켓 위치 등 초기화
    while True:
        rate(1/dt)
        # 사용자 입력 처리

        # 게임 로직 업데이트


        # 그래픽 업데이트
        ball.f = ball.mass * vector(0, -g, 0)
        ball.a = ball.f / ball.mass
        ball.v = ball.v + ball.a * dt
        ball.pos = ball.pos + ball.v * dt

    # 스코어 처리
