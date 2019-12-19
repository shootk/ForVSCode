import microbit as mb
while True:

    if mb.button_a.is_pressed():
        mb.display.show(mb.Image.HEART)
        mb.sleep(None, 1000)

    elif mb.button_b.is_pressed():
        mb.display.show(mb.Image.DIAMOND)
        mb.sleep(None, 1000)

    else:
        mb.display.show(" ")
