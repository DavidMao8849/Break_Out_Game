from tkinter import *

class Sprite():
    def __init__(self, canvas, item):
        self.canvas = canvas	# 캔버스 객체
        self.item = item		# 캔버스 안에 있는 도형의 식별 번호
        self.speedx = 10		# x 방향 속도
        self.speedy = 10    	# y 방향 속도
        self.x = 0				# 현재 x좌표  
        self.y = 0				# 현재 x좌표 

	  # 도형의 위치와 크기를 반환한다. 
    def get_coords(self):
        return self.canvas.coords(self.item)

	  # 도형의 위치를 반환한다. 
    def get_position(self):
        pos = self.canvas.coords(self.item)
        x = pos[0]
        y = pos[1]
        return x, y

	  # 객체의 상태를 변경한다. 
    def update(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy

	  # 객체를 움직인다. 
    def move(self):
        self.canvas.move(self.item, self.speedx, self.speedy)

	  # 객체를 캔버스에서 삭제한다. 
    def delete(self):
        self.canvas.delete(self.item)


class Ball(Sprite):
    def __init__(self, canvas, x, y, radius):
        self.radius = radius
        item = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill='red')
        self.x = x
        self.y = y
        super().__init__(canvas, item)		# 부모 클래스 생성자 호출

    def update(self):
        x, y = self.get_position()
        width = self.canvas.winfo_width()
 		 
        # 벽에 부딪히면 방향을 변경한다. 
        if x <= 0 or x >= width:
            self.speedx *= -1		# x 방향 변경
        if y <= 0:
            self.speedy *= -1		# y 방향 변경

    def collide(self, obj_list):
        x, y = self.get_position()
        
        # 공이 패들이나 벽돌에 맞으면 y방향을 반대로 한다. 
        if len(obj_list):
            self.speedy *= -1

        for obj in obj_list:
            if isinstance(obj, Brick):
                obj.handle_collision()


class Paddle(Sprite):
    def __init__(self, canvas, x, y):
        self.width = 200
        self.height = 20
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2, fill='black')
        super().__init__(canvas, item)  # 부모 클래스 생성자 호출
        self.x = x                      # 현재 위치 저장
        self.y = y

    # 패들을 dx, dy만큼 이동한다. 키보드 이벤트에서 호출된다. 
    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.canvas.move(self.item, dx, dy)

class Brick(Sprite):
    def __init__(self, canvas, x, y):
        self.width = 52
        self.height = 25
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2, fill='yellow', tags='brick')
        super().__init__(canvas, item)

    # 벽돌과 공이 충돌하면 벽돌을 삭제한다. 
    def handle_collision(self):
            self.delete()

class BrickBreaker(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.width = 640
        self.height = 480
        self.canvas = Canvas(self, bg='white', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        # shapes에는 화면에 있는 모든 객체가 저장된다. 
        # 키는 도형 식별 번호이고 값은 객체이다. 
        self.shapes = {}
        self.level = 1
        self.score = 0
        self.lives = 3
        self.is_game_won = False
        self.is_game_over = False

        # 패들 객체를 생성하고 shapes에 저장한다. 
        self.paddle = Paddle(self.canvas, self.width/2, 450)
        self.shapes[self.paddle.item] = self.paddle

        # Ball 객체를 생성한다. 
        self.ball = Ball(self.canvas, 310, 200, 10)

        #벽돌 생성 함수인 create_bricks를 호출한다.
        self.create_bricks()

        # Brick 객체를 2차원 모양으로 생성한다. 
    def create_bricks(self):
        for r in range(2, 5): #1행에는 점수와 목숨을 표시하기 위해 2행부터 블럭을 생성
            for c in range(1, 10):
                brick = Brick(self.canvas, c * 60, r * 30)
                self.shapes[brick.item] = brick # Brick 객체를 shapes에 저장한다. 
        self.update_ui()        
        
        # 캔버스가 키보드 이벤트를 받을 수 있도록 설정한다. 
        self.canvas.focus_set()

        # 화살표키에 이벤트를 붙인다.
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-15, 0))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(15, 0))

        #위의 모든 설정이 끝나면 시작화면 함수인 show_start_screen을 호출한다.
        self.show_start_screen()

    def show_start_screen(self):
        self.canvas.create_text(self.width / 2, self.height / 2 - 70, text="벽돌깨기 게임", fill="black", font=("Arial", 24), tags="start_screen")
        self.canvas.create_text(self.width / 2, self.height / 2 , text="키보드에서 왼쪽, 오른쪽 화살표를 누르면 패들이 해당 방향으로 움직입니다.", fill="black", font=("Arial", 13), tags="start_screen")
        self.canvas.create_text(self.width / 2, self.height / 2 + 30, text="벽돌 하나를 깰때마다 점수 10점이 누적되며, 260점이 만점입니다.", fill="black", font=("Arial", 13), tags="start_screen")
        self.canvas.create_text(self.width / 2, self.height / 2 + 70, text="시작버튼을 누르면 게임이 바로 시작됩니다.", fill="black", font=("Arial", 13), tags="start_screen")
        self.start_button = Button(self, text="게임 시작", command=self.start_game)
        self.start_button.place(x=self.width / 2 - 40, y=self.height / 2 + 90)

    def start_game(self):
        self.start_button.destroy()
        self.canvas.delete("start_screen")
        self.start()

    def start(self):
        if not self.is_game_over and not self.is_game_won: #게임 오버상태/게임 승리상태가 아니라면[조건 생성]
            self.game_loop() #게임 루프를 돔
                
    def update_ui(self): #새로이 추가 [UI추가]
        self.canvas.delete("ui")
        self.canvas.create_text(50, 20, text=f"점수: {self.score}", fill="black", tags="ui")
        self.canvas.create_text(150, 20, text=f"목숨: {self.lives}", fill="black", tags="ui")
        self.canvas.tag_raise("ui")

    def game_over(self): #새로이 추가 [진겜]
        self.is_game_over = True
        self.canvas.create_text(self.width/2, self.height/2, text="Game Over", 
                                fill="red", font=("Arial", 24), tags="ui")
        self.canvas.create_text(self.width/2, self.height/2 + 30, text=f"최고 점수: {self.score}", 
                                fill="black", font=("Arial", 18), tags="ui")
        #self.canvas.create_text(self.width/2, self.height/2 + 60, text="스페이스바를 눌러 재도전 하기", fill="white", font=("Arial", 18), tags="ui")
        #self.canvas.bind('<space>', lambda _: self.restart_game())
        self.retry_button = Button(self, text="재도전", command=self.restart_game)
        self.retry_button.place(x=self.width/2 - 50, y=self.height/2 + 60)

    def game_won(self): #새로이 추가 [이긴겜]
        self.is_game_won = True
        self.canvas.create_text(self.width / 2, self.height / 2, text="WIN!", 
                                fill="green", font=("Arial", 24), tags="ui")
        self.canvas.create_text(self.width / 2, self.height / 2 + 30, text=f"최고 점수: {self.score}", 
                                fill="black", font=("Arial", 18), tags="ui")
        #self.canvas.create_text(self.width / 2, self.height / 2 + 60, text="스페이스바를 눌러 새로운 게임 하기", fill="white", font=("Arial", 18), tags="ui")
        #self.canvas.bind('<space>', lambda _: self.restart_game())
        self.retry_button = Button(self, text="새로운 게임", command=self.restart_game)
        self.retry_button.place(x=self.width/2 - 50, y=self.height/2 + 60)


    def restart_game(self): #새로이 추가[재시작]
        self.retry_button.destroy()
        self.canvas.delete("all")
        self.shapes.clear()
        self.paddle = Paddle(self.canvas, self.width/2, 450)
        self.shapes[self.paddle.item] = self.paddle
        self.ball = Ball(self.canvas, 310, 200, 10)
        self.score = 0
        self.lives = 3
        self.create_bricks()
        self.update_ui()
        self.is_game_over = False
        self.is_game_won = False

    def game_loop(self):
        if self.is_game_over or self.is_game_won:
            return
        coords = self.ball.get_coords()# Ball 객체의 위치를 구한다. 
        # 겹치는 모든 도형을 찾는다. 식별 번호가 저장된다. 
        items = self.canvas.find_overlapping(*coords)

        # 겹치는 도형의 식별 번호로 객체를 찾아서 리스트에 저장한다. 
        objects = [self.shapes[x] for x in items if x in self.shapes]

        # 충돌 처리 메소드를 호출한다. 
        self.ball.collide(objects)
        self.ball.update()
        self.ball.move()
        
        if coords[3] >= self.height:  #공이 바닥에 닿으면
            self.lives -= 1 #목숨을 하나 깜
            if self.lives == 0: #목숨이 0이 되면
                self.game_over() #game_over 함수 호출
                return
            else:
                self.ball.delete()
                self.ball = Ball(self.canvas, 310, 200, 10) 
                #목숨 0이 아닐때 해당 위치에 공을 다시 생성

        for obj in objects: #벽돌을 깰때마다 10점씩 추가
            if isinstance(obj, Brick):
                self.score += 10
        
        #남은 벽돌이 있는지 확인후[벽돌을 따깼을때] 없으면 game_won()을 호출함.
        #삭제된 벽돌을 필터링 하는 과정[해당 과정은 우리의 학습지식으론 부족한거같아 GPT의 도움을 받음]
        self.shapes = {k: v for k, v in self.shapes.items() if not isinstance(v, Brick) or self.canvas.coords(v.item)}

        #벽돌이 모두 없어졌는지 확인
        if all(not isinstance(obj, Brick) for obj in self.shapes.values()): 
            self.update_ui()
            self.game_won()
            return

        self.update_ui()
         # game_loop()를 50밀리초 후에 호출한다.
        self.after(50, self.game_loop)

#메인 함수
window = Tk()
game = BrickBreaker(window)
window.mainloop()
