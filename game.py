# -*- coding: utf-8 -*-
from tkinter import *
from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, ttk
from random import choice

canvas_width = 800
canvas_height = 400

root = Tk()
root.title("Ну погоди! Волк Ловит Яйца")
c = Canvas(root, width=canvas_width, height=canvas_height, background="#848E85")

# c.create_image(0, 0, anchor="nw", image=PhotoImage(file="assets/game_bg.png"))
c.pack()

color_cycle = cycle(["black"])
egg_width = 45
egg_height = 55
egg_score = 5
bonus_score = 10
egg_speed = 150
egg_interval = 4000
difficulty = 0.98
catcher_color = "black"
catcher_width = 100
catcher_height = 120
catcher_img = c.create_arc(0, 0, catcher_width, catcher_height, start=200, extent=140, style="arc", outline=catcher_color, width=2)
#wolf_image = PhotoImage(file="wolf.png")
#wolf = c.create_image(0, 0, image=wolf_image, anchor="nw")
#wolf_x = 130
#wolf_y = 220
#c.move(wolf, wolf_x, wolf_y)
grass = c.create_rectangle(0,canvas_height,canvas_width,canvas_height-50, fill="#547943")
catcher_positions = {
    "upper_left": {"x": 130, "y": 100},
    "upper_right": {"x": 530, "y": 100},
    "left": {"x": 190, "y": 220},
    "right": {"x": 470, "y": 220}
}
catcher_current_position = "upper_left"
c.move(catcher_img, catcher_positions[catcher_current_position]["x"], catcher_positions[catcher_current_position]["y"])
game_font = font.nametofont("TkFixedFont")
game_font.config(size=24)


score = 0
best_result = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="#8C0000", text="Очки: "+ str(score).zfill(4))
best_result_text = c.create_text(10, 35, anchor="nw", font = game_font, fill="#8C0000", text="Рекорд: "+ str(best_result).zfill(4))

lives_remaining = 3
if lives_remaining<0:
    lives_remaining = 0
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="#8C0000", text="Жизни: "+ str(lives_remaining))

eggs = []
egg_colors = ["snow","#EDD5B6","#FFD700"]
def create_catcher():
    global catcher_img, catcher_current_position, grass
    catcher_color = "red"
    catcher_width = 100
    catcher_height = 120
   
    catcher_img = c.create_arc(0, 0, catcher_width, catcher_height, start=200, extent=140, style="arc", outline=catcher_color, width=2)
    catcher_positions = {
	"upper_left": {"x": 180, "y": 100},
	"upper_right": {"x": 580, "y": 100},
	"left": {"x": 240, "y": 220},
	"right": {"x": 520, "y": 220}
    }
    catcher_current_position = "upper_left"
    c.move(catcher_img, catcher_positions[catcher_current_position]["x"], catcher_positions[catcher_current_position]["y"])

def create_egg():
    position = choice(["upper_left", "upper_right", "left", "right"])
    if position == "upper_left":
        x = 160
        y = 10

    elif position=="upper_right":
        x = 550
        y = 10
    
    elif position=="left":
        x = 230
        y = 150
    
    else:
        x = 500
        y = 150	
    
    color = choice(egg_colors)
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=color, width=1.5, outline="grey")
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 5)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        result = "Игра окончена!\nВаш результат: " + str(score)
        answer = messagebox.askquestion("Игра окончена!", result + "\nХотите сыграть еще раз?")
        
        if answer == "yes":
            choose_difficulty()
        else:
            root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Жизни: "+ str(lives_remaining))

def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher_img)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery < eggy2:
            if c.itemcget(egg, 'fill') == "#FFD700":
                increase_score(bonus_score)
            else:
                increase_score(egg_score)       
            eggs.remove(egg)
            c.delete(egg)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval, best_result
    score += points
    if score>best_result:
        best_result = score
    c.itemconfigure(best_result_text, text="Рекорд: "+str(best_result).zfill(4))

    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    if egg_speed <= 100:
        egg_speed = 100
    if egg_interval <=  2000:
        egg_interval = 2000

    c.itemconfigure(score_text, text="Очки: "+ str(score).zfill(4))

def move_catcher(position):
    c.move(catcher_img, catcher_positions[position]["x"] - c.coords(catcher_img)[0], catcher_positions[position]["y"] - c.coords(catcher_img)[1])

def move_upper_left(event):
    move_catcher("upper_left")

def move_upper_right(event):
    move_catcher("upper_right")

def move_left(event):
    move_catcher("left")

def move_right(event):
    move_catcher("right")

c.bind("a", move_left)
c.bind("d", move_right)
c.bind("q", move_upper_left)
c.bind("e", move_upper_right)
c.focus_set()
difficulty_frame = Frame(root)
def create_score_text():
    global score_text
    score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="red", text="Очки: "+ str(score).zfill(4))

def create_record_text():
    global best_result_text
    best_result_text = c.create_text(10, 35, anchor="nw", font = game_font, fill="red", text="Рекорд: "+ str(best_result).zfill(4))

def create_lives_text():
    global lives_text
    lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="red", text="Жизни: "+ str(lives_remaining))
    
chicken_up_l = c.create_rectangle(120,10,250,0, fill="#F6C033")
chicken_up_r = c.create_rectangle(canvas_width-160,10,canvas_width-290,0, fill="#F6C033")
chicken_l = c.create_rectangle(170,150,300,140, fill="#F6C033")
chicken_r = c.create_rectangle(canvas_width-210,150,canvas_width-340,140, fill="#F6C033")
def start_game(level):
    global eggs, score, lives_remaining, catcher_img,score_text,lives_text,best_result, best_result_text,grass, chicken_up_l, chicken_up_r, chicken_l, chicken_r
    difficulty_frame.pack_forget()
    start_button.pack_forget()
    c.delete("all")
    eggs = []
    score = 0
    difficulty=level
    lives_remaining = 3
    grass = c.create_rectangle(0,canvas_height,canvas_width,canvas_height-50, fill="#547943")
    chicken_up_l = c.create_rectangle(120,10,250,0, fill="#F6C033")
    chicken_up_r = c.create_rectangle(canvas_width-160,10,canvas_width-290,0, fill="#F6C033")
    chicken_l = c.create_rectangle(170,150,300,140, fill="#F6C033")
    chicken_r = c.create_rectangle(canvas_width-210,150,canvas_width-340,140, fill="#F6C033")
    create_catcher()
    create_score_text()
    create_lives_text()
    create_record_text()
    root.after(1000, create_egg)
    root.after(1000, move_eggs)
    root.after(1000, check_catch)


def exit_game():
    root.destroy()

def choose_difficulty():
    global difficulty_frame
    difficulty_frame = Frame(root)
    start_button.pack_forget()
    difficulty_frame.pack(side="left",padx=10, pady=10)

    difficulty_label = Label(difficulty_frame, text="Выберите уровень:")
    difficulty_label.pack()
    
 
    level1_button = Button(difficulty_frame, text="Простой", command=lambda: start_game(0.98))
    level1_button.pack()

    level2_button = Button(difficulty_frame, text="Средний", command=lambda: start_game(0.9789))
    level2_button.pack()

    level3_button = Button(difficulty_frame, text="Сложный", command=lambda: start_game(0.977999))
    level3_button.pack()

    
start_button = Button(root, text="Играть", command=choose_difficulty)
start_button.pack(side="left", padx=10,pady=10)

exit_button = Button(root, text="Выйти", command=exit_game)
exit_button.pack(side="right", padx=10, pady=10)

root.mainloop()
