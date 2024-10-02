WINDOW_HEIGHT = 1800  # modify this to rescale (or fuck up) everything
WINDOW_WIDTH = int(WINDOW_HEIGHT * 1.6)
HOLDER_SIZE = int(.8 * WINDOW_HEIGHT)
SERVO_SIZE = int(HOLDER_SIZE // 2.2)


SETTINGS = {
    'title': 'Stewart Platform',
    'height': WINDOW_HEIGHT,
    'width': WINDOW_WIDTH,
    'holder': {
        'size': HOLDER_SIZE,
    },
    'servo': {
        'size': SERVO_SIZE,
    }
}


print(SETTINGS)
