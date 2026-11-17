import random
from PIL import ImageOps


class SeaMonkey:
    """씨몽키 한 마리. 자기 위치와 속도를 알고, 스스로 움직이고 그린다"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = random.uniform(30, width - 30)
        self.y = random.uniform(60, height - 30)
        self.vx = 0.0
        self.vy = 0.0
        self.alive = True                 # 사신에게 닿으면 False가 된다

    def move(self, speed, flow_x, flow_y):
        if not self.alive:
            # 죽은 씨몽키는 헤엄치지 않고 바닥으로 천천히 가라앉는다
            self.y = min(self.height - 12, self.y + 0.5)
            return
        # 속도를 조금씩 무작위로 바꾼다 (-1 ~ 1 범위)
        self.vx = max(-1, min(1, self.vx + random.uniform(-0.3, 0.3)))
        self.vy = max(-1, min(1, self.vy + random.uniform(-0.3, 0.3)))
        # 위치 = 헤엄 + 물살, 화면 밖으로 못 나가게
        self.x = max(10, min(self.width - 10, self.x + self.vx * speed + flow_x))
        self.y = max(45, min(self.height - 10, self.y + self.vy * speed + flow_y))

    def draw(self, image, sprite):
        # 왼쪽으로 헤엄칠 땐 그림을 좌우로 뒤집는다 (원본 그림은 오른쪽을 봄)
        if self.vx < 0:
            sprite = ImageOps.mirror(sprite)
        half = sprite.width // 2
        # 세 번째 값(sprite)은 투명한 부분을 빼고 붙이라는 뜻
        image.paste(sprite, (int(self.x) - half, int(self.y) - half), sprite)
