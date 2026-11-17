class Food:
    """먹이 알갱이 하나"""

    def __init__(self, x):
        self.x = x
        self.y = 40

    def move(self, flow_x, flow_y):
        self.x = self.x + flow_x * 0.5
        self.y = self.y + 1 + flow_y * 0.5      # 천천히 가라앉는다

    def draw(self, draw):
        draw.ellipse((self.x - 2, self.y - 2, self.x + 2, self.y + 2), fill=(200, 150, 60))
