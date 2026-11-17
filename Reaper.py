import time
import random
from PIL import ImageOps

WARN_SECONDS = 2.5    # 경고 불빛이 켜져 있는 시간 (초)
REAPER_SPEED = 3      # 사신이 한 장면에 움직이는 거리 (픽셀)
REAPER_RADIUS = 14    # 사신의 닿는 범위 (반지름, 픽셀)


class Reaper:
    """사신. 일정 시간마다 경고 불빛을 낸 뒤 화면을 가로지른다"""

    def __init__(self, width, height, interval):
        self.width = width
        self.height = height
        self.interval = interval      # 다음 등장까지 걸리는 시간 (초)
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.warn_x = 0               # 경고 불빛 위치
        self.warn_y = 0
        self.schedule()

    def schedule(self):
        """다음 등장 시각을 정하고 기다리는 상태로 바꾼다"""
        self.state = "wait"           # wait(기다림) → warn(경고) → cross(가로지름)
        self.next_time = time.time() + self.interval

    def start_warning(self):
        """어느 쪽에서 나올지 정하고 경고 불빛을 켠다"""
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.y = random.randint(60, self.height - 30)
            self.x = -20
            self.dx, self.dy = REAPER_SPEED, 0
            self.warn_x, self.warn_y = 0, self.y
        elif side == "right":
            self.y = random.randint(60, self.height - 30)
            self.x = self.width + 20
            self.dx, self.dy = -REAPER_SPEED, 0
            self.warn_x, self.warn_y = self.width - 1, self.y
        elif side == "top":
            self.x = random.randint(25, self.width - 25)
            self.y = 15
            self.dx, self.dy = 0, REAPER_SPEED
            self.warn_x, self.warn_y = self.x, 36
        else:
            self.x = random.randint(25, self.width - 25)
            self.y = self.height + 20
            self.dx, self.dy = 0, -REAPER_SPEED
            self.warn_x, self.warn_y = self.x, self.height - 1
        self.state = "warn"
        self.warn_until = time.time() + WARN_SECONDS

    def update(self):
        now = time.time()
        if self.state == "wait":
            if now >= self.next_time:
                self.start_warning()
        elif self.state == "warn":
            if now >= self.warn_until:
                self.state = "cross"
        elif self.state == "cross":
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            # 화면 밖으로 완전히 나가면 다음 등장을 예약한다
            if (self.x < -25 or self.x > self.width + 25
                    or self.y < 10 or self.y > self.height + 25):
                self.schedule()

    def touches(self, monkey, monkey_r):
        """씨몽키와 닿았는지 알려준다 (두 중심 사이 거리로 판단)"""
        if self.state != "cross":
            return False
        gap_x = self.x - monkey.x
        gap_y = self.y - monkey.y
        distance = (gap_x * gap_x + gap_y * gap_y) ** 0.5
        return distance < REAPER_RADIUS + monkey_r * 0.8

    def draw(self, image, draw, sprite):
        if self.state == "warn":
            # 작은 빨간 불빛이 깜빡인다 (1초에 두 번)
            if int(time.time() * 4) % 2 == 0:
                r = 5
            else:
                r = 3
            x, y = self.warn_x, self.warn_y
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 70, 70))
        elif self.state == "cross":
            if self.dx < 0:                       # 왼쪽으로 갈 땐 좌우 뒤집기
                sprite = ImageOps.mirror(sprite)
            half = sprite.width // 2
            image.paste(sprite, (int(self.x) - half, int(self.y) - half), sprite)
