import arcade, sys

from .collision import collide

from .math import Angle
from .math import Distance
from .math import Direction

module = sys.modules['__main__']

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class SCREEN(arcade.Window):
    
    def __init__(self):
        super().__init__(800, 600, 'JoBase', resizable = True,
                         antialiasing = False)
                
        # The code above gets all the colors stored in 'arcade.color' and makes
        # global variables with the same name.        
        
        self.engines = []
        self.module = module
        self.resize = 0
        self.time = 0
        self.quit = 0
        self._color = (255, 255, 255)
        self._rate = 60
        self._fullscreen = 0
        self._visible = 1
        
        arcade.set_background_color(self._color)
        self.set_update_rate(1 / 60)
                
        # The code above finds all the variables starting with 'CURSOR_' and
        # makes new global variables without the 'CURSOR_' prefix.
                
    def collide(self, other):
        # This function checks if 'other' is on the screen.
        return collide(self.boundary(), other.boundary())
        
    def boundary(self):
        # This dictionary is eventually passed into the collision function.
        
        return {'points': arcade.get_rectangle_points(self.width / 2,
                                                      self.height / 2,
                                                      self.width, self.height),
                'type': 'polygon'}
    
    def _get_visible(self):
        return self._visible
    
    def _set_visible(self, value: bool):
        # 'set_visible' is an arcade function.
        self.set_visible(value)
        self._visible = value
        
    visible = property(_get_visible, _set_visible)
    
    def _get_x(self):
        # 'get_location' is an arcade function.
        return self.get_location()[0]
    
    def _set_x(self, value: float):
        # 'set_location' is an arcade function.
        self.set_location(value, self.y)
        
    x = property(_get_x, _set_x)
        
    def _get_y(self):
        return self.get_location()[1]
    
    def _set_y(self, value: float):
        self.set_location(self.x, value)
        
    y = property(_get_y, _set_y)
    
    def _get_title(self):
        return self.caption
    
    def _set_title(self, value: str):
        self.set_caption(value)
        
    title = property(_get_title, _set_title)
    
    def _get_fullscreen(self):
        return self._fullscreen
    
    def _set_fullscreen(self, value: bool):
        self.set_fullscreen(value)
        self.resize = 1
        # 'resize' becomes true when it enters fullscreen mode.
        
    fullscreen = property(_get_fullscreen, _set_fullscreen)
    
    def _get_rate(self):
        return self._rate
    
    def _set_rate(self, value: float):
        # We write '1 / value' to make the user set the frames per second.
        self.set_update_rate(1 / value)
        self._rate = value
        
    rate = property(_get_rate, _set_rate)
    
    def _get_color(self):
        return self._color
    
    def _set_color(self, value: arcade.Color):
        arcade.set_background_color(value)
        self._color = value
        
    color = property(_get_color, _set_color)
        
    def centralize(self):
        # A JoBase user could just use 'center_window'.
        self.center_window()
        
    def exit(self):
        self.quit = 1
        
    def on_update(self, time):
        self.time = 1 / time
        
        arcade.start_render()
        
        if 'loop' in dir(module):
            module.loop()
            
        for engine in self.engines:
            engine.update()
        
        self.resize = 0
        Key.press = 0
        Key.release = 0
        Mouse.press = 0
        Mouse.release = 0
        Mouse.up = 0
        Mouse.down = 0
        Mouse.move = 0
        Mouse.scroll = 0
        
        if self.quit:
            arcade.close_window()
            
        """
        When the user presses the close button, the 'module.loop()' function
        runs once before the window closes.
        """
        
    def on_close(self):
        self.quit = 1
        
    def on_mouse_motion(self, x, y, dx, dy):
        Mouse.move = 1
        Mouse.x_change = x - Mouse._x
        Mouse.y_change = y - Mouse._y
        Mouse._x = x
        Mouse._y = y        

    def on_mouse_scroll(self, x, y, button, direction):
        Mouse.scroll = 1
        
        if direction == 1.0:
            Mouse.scroll_up = 1
            
        elif direction == -1.0:
            Mouse.scroll_down = 1

    def on_mouse_press(self, x, y, button, modifiers):
        Mouse.press = 1
        
        if button == 1:
            Mouse.left = 1
            
        elif button == 4:
            Mouse.right = 1
            
        elif button == 2:
            Mouse.middle = 1

    def on_mouse_release(self, x, y, button, modifiers):
        Mouse.release = 1
        
        if button == 1:
            Mouse.left = 0
            
        elif button == 4:
            Mouse.right = 0
            
        elif button == 2:
            Mouse.middle = 0
        
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.resize = 1

    def on_key_press(self, key, modifiers):
        Key.press = 1
        
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key, keys):
                keys = keys.lower()
                setattr(Key, keys, 1)
                
                if keys in alphabet:
                    if Key.lshift or Key.rshift:
                        Key.text += keys.upper()
                        
                    else:
                        Key.text += keys
                        
                elif keys == 'backspace':
                    Key.text = Key.text[:-1]
                    
                elif keys.startswith('num_') or keys.startswith('key_'):
                    Key.text += keys[-1]
                
        # The code above finds all the values in 'arcade.key'. If a key is true,
        # we set the same JoBase key to true.

    def on_key_release(self, key, modifiers):
        Key.release = 1
        
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key,
                                                            str(keys)):
                keys = keys.lower()
                setattr(Key, str(keys), 0)
                
class KEY:
    
    def __init__(self):
        self.press = 0
        self.release = 0
        self.text = ''
        
        for keys in dir(arcade.key):
            if not keys.startswith('__'):
                keys = keys.lower()
                setattr(self, str(keys), 0)
                
        # The code above finds all the values in 'arcade.key' and makes a
        # JoBase key with the same name (lowercase).
        
    def clear(self):
        self.text = ''
        
class MOUSE():
    
    def __init__(self):
        
        super()
        
        self.press = 0
        self.release = 0
        self.left = 0
        self.right = 0
        self.middle = 0
        self.scroll_up = 0
        self.scroll_down = 0
        self.move = 0
        self.scroll = 0
        self._x = 0
        self._y = 0
        self.x_change = 0
        self.y_change = 0
        self._visible = 1
        self._cursor = None
        
    def boundary(self):
        return {'x': self._x, 'y': self._y, 'type': 'point'}
    
    def _get_visible(self):
        return self._visible
    
    def _set_visible(self, value: bool):
        Screen.set_mouse_visible(value)
        self._visible = value
        
    visible = property(_get_visible, _set_visible)
    
    def _get_cursor(self):
        return self._cursor
    
    def _set_cursor(self, name):
        Screen.set_mouse_cursor(Screen.get_system_mouse_cursor(name))
        self._cursor = name
        
    cursor = property(_get_cursor, _set_cursor)
        
    def _get_x(self):
        return self._x
    
    def _set_x(self, value: float):
        Screen.set_mouse_position(round(value), round(self._y))
        
        self._x = value
        
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._y
    
    def _set_y(self, value: float):
        Screen.set_mouse_position(round(self._x), round(value))
        
        self._y = value
        
    y = property(_get_y, _set_y)
    
    def collide(self, other):
        return collide(self.boundary(), other.boundary())
    
    def angle(self, other):
        return Angle(self.x, self.y, other.x, other.y)

    def distance(self, other):
        return Distance(self.x, self.y, other.x, other.y)    
    
Key = KEY()
Mouse = MOUSE()
Screen = SCREEN()