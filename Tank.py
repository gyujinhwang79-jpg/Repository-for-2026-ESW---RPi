import time
import json
import random
from PIL import Image
from SeaMonkey import SeaMonkey
from Food import Food

# ===== 설정 =====
SPEED = 60          # 시간 배속 (60: 실제 1분 = 게임 1시간)
HATCH_HOURS = 0.5   # 부화까지 걸리는 게임 시간
DAY_HOURS = 1       # 게임 속 하루 길이
MAX_R = 20          # 최대 크기 (반지름)
FOOD_DROP = 10      # 게임 1시간마다 줄어드는 배부름
PLAY_DROP = 8       # 게임 1시간마다 줄어드는 즐거움
SAVE_FILE = "save.json"


class Tank:
    """어항. 씨몽키들, 먹이, 게임 상태(나이, 배부름, 즐거움)를 관리한다"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 이미지 불러오기
        self.background = Image.open("background.png").convert("RGB").resize((width, height))
        self.sprite = Image.open("seamonkey.png").convert("RGBA")
        self.sprite_dead = self.sprite.convert("LA").convert("RGBA")   # 흑백 버전

        self.monkeys = [SeaMonkey(width, height) for _ in range(5)]
        self.foods = []
        self.play_timer = 0
        self.load()

    # ----- 상태 -----
    def reset(self):
        now = time.time()
        self.start = now
        self.last = now
        self.food = 100.0
        self.play = 100.0
        self.alive = True
        self.foods = []

    def load(self):
        try:
            with open(SAVE_FILE) as f:
                data = json.load(f)
            self.start = data["start"]
            self.last = data["last"]
            self.food = data["food"]
            self.play = data["play"]
            self.alive = data["alive"]
        except (OSError, ValueError, KeyError):
            self.reset()

    def save(self):
        data = {"start": self.start, "last": self.last,
                "food": self.food, "play": self.play, "alive": self.alive}
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def age(self):
        return (time.time() - self.start) * SPEED / 3600

    def hatched(self):
        return self.age() >= HATCH_HOURS

    # ----- 버튼 동작 -----
    def feed(self):
        if self.alive and self.hatched():
            self.food = min(100, self.food + 25)
            for _ in range(6):
                self.foods.append(Food(random.uniform(40, self.width - 40)))

    def play_with(self):
        if self.alive and self.hatched():
            self.play = min(100, self.play + 25)
            self.play_timer = 30

    # ----- 한 바퀴 계산 -----
    def update(self, flow_x, flow_y):
        now = time.time()
        passed = (now - self.last) * SPEED / 3600
        self.last = now

        if self.alive and self.hatched():
            self.food = max(0, self.food - FOOD_DROP * passed)
            self.play = max(0, self.play - PLAY_DROP * passed)
            if self.food == 0 or self.play == 0:
                self.alive = False

        if self.alive:
            speed = 3 if self.play_timer > 0 else 1
            for monkey in self.monkeys:
                monkey.move(speed, flow_x, flow_y)

        for food in self.foods:
            food.move(flow_x, flow_y)
        self.foods = [food for food in self.foods if food.y < self.height - 5]

        if self.play_timer > 0:
            self.play_timer -= 1

    # ----- 그리기 -----
    def draw(self, image, draw, flow_x, flow_y):
        image.paste(self.background, (0, 0))                 # 배경 이미지 깔기

        if flow_x or flow_y:                                 # 물살 선
            for _ in range(8):
                x = random.randint(0, self.width)
                y = random.randint(40, self.height)
                draw.line((x, y, x + flow_x * 6, y + flow_y * 6), fill=(200, 230, 255))

        for food in self.foods:
            food.draw(draw)

        if self.hatched():
            r = int(min(MAX_R, 1 + (self.age() - HATCH_HOURS) / DAY_HOURS * 2))
            if self.alive:
                sprite = self.sprite
            else:
                sprite = self.sprite_dead
            sprite = sprite.resize((r * 2, r * 2))           # 나이에 맞는 크기로 줄이기
            for monkey in self.monkeys:
                monkey.draw(image, sprite)

        # 상태창
        draw.rectangle((0, 0, self.width, 34), fill=(0, 0, 0))
        day = int(self.age() // DAY_HOURS) + 1
        draw.text((5, 3), "DAY " + str(day), fill=(255, 255, 255))
        draw.text((60, 3), "FOOD", fill=(255, 255, 255))
        draw.rectangle((100, 4, 100 + int(self.food * 1.3), 12), fill=(0, 200, 0))
        draw.text((60, 19), "PLAY", fill=(255, 255, 255))
        draw.rectangle((100, 20, 100 + int(self.play * 1.3), 28), fill=(255, 180, 0))
        if not self.alive:
            draw.text((60, 120), "RIP... press CENTER", fill=(255, 80, 80))
