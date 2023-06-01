#Web VPython 3.2
from vpython import *

# 게임 세팅 초기화
# 예) 공, 라켓, 테이블, 스코어 등


# 탁구 테이블 객체 생성
table_length = 2.74
table_width = 1.525
table_height = 0.05
table = box(pos=vector(0, -table_height / 2, 0), size=vector(table_length, table_height, table_width), color=color.blue)


dt = 0.01

# 메인 루프
while True:
    # 공, 라켓 위치 등 초기화
    while True:
        rate(1/dt)
        # 사용자 입력 처리

        # 게임 로직 업데이트

        # 그래픽 업데이트

    # 스코어 처리
