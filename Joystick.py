import board
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display import st7789


class Joystick:
    """LCD 화면과 조이스틱, 버튼을 한데 묶은 클래스 (조교님 예제와 같은 구조)"""

    def __init__(self):
        # 화면
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.disp = st7789.ST7789(
            board.SPI(),
            height=240,
            y_offset=80,
            rotation=180,
            cs=self.cs_pin,
            dc=self.dc_pin,
            rst=self.reset_pin,
            baudrate=24000000,
        )

        # 버튼 (누르면 False)
        self.button_A = self.make_button(board.D5)   # 먹이
        self.button_B = self.make_button(board.D6)   # 놀이
        self.button_L = self.make_button(board.D27)
        self.button_R = self.make_button(board.D23)
        self.button_U = self.make_button(board.D17)
        self.button_D = self.make_button(board.D22)
        self.button_C = self.make_button(board.D4)

        # 백라이트
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        self.width = self.disp.width
        self.height = self.disp.height

    def make_button(self, pin):
        button = DigitalInOut(pin)
        button.direction = Direction.INPUT
        return button

    def flow(self):
        """조이스틱 방향을 물살 (x, y)로 바꿔서 돌려준다"""
        flow_x = 0
        flow_y = 0
        if self.button_C.value:              # 가운데를 누를 땐 방향 무시
            if not self.button_L.value:
                flow_x = -2
            if not self.button_R.value:
                flow_x = 2
            if not self.button_U.value:
                flow_y = -2
            if not self.button_D.value:
                flow_y = 2
        return flow_x, flow_y

    def off(self):
        self.backlight.value = False
