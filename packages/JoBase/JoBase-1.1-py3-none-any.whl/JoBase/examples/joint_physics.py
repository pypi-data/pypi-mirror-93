from JoBase import *

# JoBase Joint Physics Example

class BORDERS(List):
    # This class handles all the borders on the screen.
    
    def __init__(self):
        super().__init__()
        
        coordinates = self.get_coordinates()
        
        # First, we make all the borders and add them to the list.
        
        for i in range(int(len(coordinates) / 4)):
            line = Line(coordinates[i * 4], coordinates[i * 4 + 1], coordinates[i * 4 + 2], coordinates[i * 4 + 3], 10, GRAY)
            self.append(line)
            engine.add(line, body = STATIC, elasticity = 0.9)
            
    def resize(self):
        # When the screen is resized, this function is called.
        # This function re-positions all the line borders.
        
        coordinates = self.get_coordinates()
        
        for i, line in enumerate(self):
            line.points = ((coordinates[i * 4], coordinates[i * 4 + 1]), (coordinates[i * 4 + 2], coordinates[i * 4 + 3]))
            
    def get_coordinates(self):
        # This returns all the coordinates for each line border.
        
        return [0, Screen.height / 2, Screen.width, Screen.height / 2,
                Screen.width / 3, Screen.height, Screen.width / 3, 0,
                Screen.width / 3 * 2, Screen.height, Screen.width / 3 * 2, 0,
                0, 0, 0, Screen.height,
                Screen.width, 0, Screen.width, Screen.height,
                0, Screen.height, Screen.width, Screen.height,
                0, 0, Screen.width, 0]
    
class OBJECTS():
    # This class handles all the boxes and joints on the screen.
    
    def __init__(self):        
        self.joints = List()
        self.boxes = List()
        
        # Set up the names of all the joints and their values.
        
        names = ['Pin_Joint(box_1, box_2)',
                 'Spring_Joint(box_1, box_2, damping = 1)',
                 'Gear_Joint(box_1, box_2)',
                 'Groove_Joint(box_1, box_2, 50, 50, 150, 150)',
                 'Pivot_Joint(box_1, box_2, box_2.x + 30, box_2.y + 30)',
                 'Motor_Joint(box_1, box_2, 20)']
        
        x = Screen.width / 6
        y = Screen.height / 4 * 3
        
        for name in names:
            # First we make the boxes.
            
            box_1 = Box(x - 50, y, 50, 30, Random_Color(), 0, Random_Angle())
            box_2 = Box(x + 50, y, 50, 30, Random_Color(), 0, Random_Angle())
            
            if name.startswith('Pivot'): body = STATIC
            else: body = DYNAMIC
                
            # Add the boxes to the engine and the list.
            engine.add(box_1, elasticity = 0.9, body = body)
            engine.add(box_2, elasticity = 0.9)
            self.boxes.append(box_1)
            self.boxes.append(box_2)
            
            # Make the joint between the boxes.
            joint = eval(name)
            joint.thickness = 5
            joint.color1 = box_1.color
            joint.color2 = box_2.color
            engine.add(joint, elasticity = 0.9)
            self.joints.append(joint)
            
            # Change the positions for the next set of boxes.
            x += Screen.width / 3
            
            if x > Screen.width / 6 * 5:
                x = Screen.width / 6
                y = Screen.height / 4
            
    def draw(self):
        self.joints.draw()
        self.boxes.draw()
        
class TEXT(List):
    # This class handles the text on the screen.
    
    def __init__(self):
        super().__init__()
        
        # Set up the names of all the joints.
        names = ['Pin', 'Spring', 'Gear', 'Groove', 'Pivot', 'Motor']
        
        x = Screen.width / 6
        y = Screen.height / 4 * 3
        
        for name in names:
            # Make the text and add it to the list.
            
            text = Text(name + ' Joint', x, y)
            self.append(text)
            
            # Change the positions for the next piece of text.
            x += Screen.width / 3
            
            if x > Screen.width / 6 * 5:
                x = Screen.width / 6
                y = Screen.height / 4
                
    def resize(self):
        # When the screen is resized, this function is called.
        # This function re-positions all the text.        
        
        x = Screen.width / 6
        y = Screen.height / 4 * 3
        
        for text in self:
            text.x = x
            text.y = y
            
            x += Screen.width / 3
            
            if x > Screen.width / 6 * 5:
                x = Screen.width / 6
                y = Screen.height / 4            

engine = Engine()
objects = OBJECTS()
borders = BORDERS()
text = TEXT()

Screen.color = LIGHT_GRAY
Mouse.box = None

def loop():
    
    if Screen.resize: resize()
    
    for box in objects.boxes:
        if Mouse.press and Mouse.collide(box):
            Mouse.box = box
            
    if Mouse.box is not None:
        # Move the box to the mouse position.
        
        Mouse.box.x = Mouse.x + Mouse.x_change
        Mouse.box.y = Mouse.y + Mouse.y_change
        
    if Mouse.release: Mouse.box = None
    
    borders.draw()
    text.draw()
    objects.draw()
    
def resize():
    # Resize the borders and text.
    # We don't bother to re-position the boxes.
    
    borders.resize()
    text.resize()
        
run()