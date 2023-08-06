import arcade

for name in dir(arcade.color):
    if not name.startswith('__'):
        globals()[name] = getattr(arcade.color, str(name))

JOBASE_BLUE = (0, 119, 221)