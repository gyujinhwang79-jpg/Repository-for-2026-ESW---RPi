import time
from PIL import Image, ImageDraw
from Joystick import Joystick
from Tank import Tank

joystick = Joystick()
image = Image.new("RGB", (joystick.width, joystick.height))
draw = ImageDraw.Draw(image)
tank = Tank(joystick.width, joystick.height)

prev_A = True
prev_B = True
last_save = time.time()

try:
    while True:
        # 1) 입력
        flow_x, flow_y = joystick.flow()

        now_A = joystick.button_A.value
        now_B = joystick.button_B.value
        if prev_A and not now_A:          # 방금 누른 순간에만
            tank.feed()
        if prev_B and not now_B:
            tank.play_with()
        prev_A = now_A
        prev_B = now_B

        if not tank.alive and not joystick.button_C.value:
            tank.reset()

        # 2) 계산
        tank.update(flow_x, flow_y)

        # 3) 그리기
        tank.draw(image, draw, flow_x, flow_y)
        joystick.disp.image(image)

        # 4) 10초마다 저장
        if time.time() - last_save > 10:
            tank.save()
            last_save = time.time()

        time.sleep(1 / 15)

except KeyboardInterrupt:
    draw.rectangle((0, 0, joystick.width, joystick.height), fill=(0, 0, 0))
    joystick.disp.image(image)
    joystick.off()
    tank.save()
    print("saved")
