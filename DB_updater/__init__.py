frame = None


def change_window(window):
    global frame
    frame = window()
    frame.show()
