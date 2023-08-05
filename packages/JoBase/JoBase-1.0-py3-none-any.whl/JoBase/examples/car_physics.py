from JoBase import *

# JoBase Car Physics Example

WHEEL_FRICTION = 0.9
WHEEL_SIZE = 30

CAR_X = 600
CAR_Y = 300
CAR_LENGTH = 100
CAR_HEIGHT = 30
CAR_SPEED = 20

SUSPENTION_MIN = 30
SUSPENTION_MAX = 60
SUSPENTION_ANGLE = 50
SUSPENTION_STIFFNESS = 200
SUSPENTION_DAMPING = 5

# Change the values above to customize your car.

class WHEEL:
    # This class handles the wheels of the car.
    
    def __init__(self, body, pos):
        min_x, min_y = Direction(-SUSPENTION_MIN, SUSPENTION_ANGLE)
        max_x, max_y = Direction(-SUSPENTION_MAX, SUSPENTION_ANGLE)
        
        self.wheel = Circle(body.x + max_x * pos, body.y + max_y, WHEEL_SIZE)
        engine.add(self.wheel, friction = WHEEL_FRICTION)
        
        # We add a box so that you can see the wheels rotating.
        self.box = Box(self.wheel.x, self.wheel.y, 30, 5, ANDROID_GREEN)
        
        # The groove joint keeps the wheels in place.
        self.groove = Groove_Joint(body, self.wheel, min_x * pos, min_y, max_x * pos, max_y, color = RED)
        
        # The spring joint gives the car suspention.
        self.spring = Spring_Joint(body, self.wheel, SUSPENTION_MAX, SUSPENTION_STIFFNESS, SUSPENTION_DAMPING)
        
        # The motor joint makes the wheels turn.
        self.motor = Motor_Joint(body, self.wheel, 0)
        
        # We add everything to the physics engine.
        engine.add(self.groove)
        engine.add(self.spring)
        engine.add(self.motor)
        
    def update(self):
        # This function updates the rotation of the green box on the wheel.
        
        self.box.x = self.wheel.x
        self.box.y = self.wheel.y
        self.box.rotation = self.wheel.rotation
        
    def draw(self):
        self.wheel.draw()
        self.box.draw()
        self.groove.draw()

class CAR:
    
    def __init__(self):
        self.body = Box(CAR_X, CAR_Y, CAR_LENGTH, CAR_HEIGHT, RED)
        engine.add(self.body)
        
        # The code below makes the front and rear wheels.
        self.front = WHEEL(self.body, 1)
        self.rear = WHEEL(self.body, -1)
        
    def draw(self):
        self.body.draw()
        self.front.draw()
        self.rear.draw()
        
    def update(self):
        self.front.update()
        self.rear.update()
        
    def set_speed(self, speed):
        # Change the speed of the car.
        self.front.motor.speed = speed
        self.rear.motor.speed = speed

engine = Engine()
car = CAR()

# Make the black bump shape.
bump = Shape(((0, 0), (100, 50), (400, 60), (500, 0)))
bump.y = 200

# We make the bump really heavy so that the car can't push it.
engine.add(bump, mass = 10, friction = WHEEL_FRICTION)

ground = Box(400, 50, 1000, 20)
engine.add(ground, body = STATIC, friction = WHEEL_FRICTION)

def loop():
    
    car.update()
    car.draw()
        
    ground.draw()
    bump.draw()
                
    if KEY.left: car.set_speed(-CAR_SPEED)
    elif KEY.right: car.set_speed(CAR_SPEED)
    else: car.set_speed(0)
    
    if SCREEN.resize:
        ground.x = SCREEN.width / 2
        ground.width = SCREEN.width

run()