# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.start_time = time.time()
        self.point = 0

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        #시간
        diff_time = time.time() - self.start_time
        diff_time = round(diff_time,1)
        
        is_catched = self.is_catched()
        
        #point
        if (is_catched):
            self.point += 1
            position = random.randint(-300,300)
            self.runner.goto(position,position)
               
        if(self.point > 5):
            self.runner.speed(8)
            self.runner.color('green')
            self.runner.shapesize(2,2,2)
            
        
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}  Counting Time : {diff_time}\nYour score is {self.point}',font=("",20))

        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

class MyMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        dist = random.randint(10,30)
        self.step_move = dist
        angle = random.randint(-90,90)
        self.step_turn = angle

    def run_ai(self, opp_pos, opp_heading):            
            mode = random.randint(0, 2)
            if mode == 0:
                self.forward(self.step_move)
            elif mode == 1:
                self.left(self.step_turn)
            elif mode == 2:
                self.right(self.step_turn)


if __name__ == '__main__':
    canvas = turtle.Screen()
    canvas.bgcolor('#DDFFFF')
    runner = MyMover(canvas)
    chaser = ManualMover(canvas)

    game = RunawayGame(canvas, runner, chaser)
    game.start()
    canvas.mainloop()