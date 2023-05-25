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
c.pack()



color_cycle = cycle(["black"])
egg_width = 45
egg_height = 55
egg_score = 5
bonus_score = 10
egg_speed = 50
egg_interval = 3000

catcher_color = "black"
catcher_width = 100
catcher_height = 120   
catcher_img = c.create_arc(0, 0, catcher_width, catcher_height, start=200, extent=140, style="arc", outline=catcher_color, width=2)

grass = c.create_rectangle(0,canvas_height,canvas_width,canvas_height-50, fill="#547943",width=0.1, outline="grey")
catcher_positions = {
    "upper_left": {"x": 130, "y": 100},
    "upper_right": {"x": 530, "y": 100},
    "left": {"x": 190, "y": 220},
    "right": {"x": 470, "y": 220}
}
catcher_initial_position = "upper_left"
c.move(catcher_img, catcher_positions[catcher_initial_position]["x"], catcher_positions[catcher_initial_position]["y"])
game_font = font.nametofont("TkFixedFont")
game_font.config(size=24)


score = 0
best_result = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="#8C0000", text="Очки: "+ str(score).zfill(4))
best_result_text = c.create_text(10, 35, anchor="nw", font = game_font, fill="#8C0000", text="Рекорд: "+ str(best_result).zfill(4))

lives_left = 3

lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="#8C0000", text="Жизни: "+ str(lives_left))

eggs = []
egg_colors = ["snow","#EDD5B6","#FFD700"]

def creating_catcher():
    global catcher_img, catcher_initial_position, grass
    catcher_color = "black"
    catcher_width = 100
    catcher_height = 120
   
    catcher_img = c.create_arc(0, 0, catcher_width, catcher_height, start=200, extent=140, style="arc", outline=catcher_color, width=2)
    catcher_positions = {
	"upper_left": {"x": 180, "y": 100},
	"upper_right": {"x": 580, "y": 100},
	"left": {"x": 240, "y": 220},
	"right": {"x": 520, "y": 220}
    }
    catcher_initial_position = "upper_left"
    c.move(catcher_img, catcher_positions[catcher_initial_position]["x"], catcher_positions[catcher_initial_position]["y"])

def creating_egg():
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
    root.after(egg_interval, creating_egg)

def throwing_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 5)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, throwing_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lost_life()
    if lives_left == 0:
        result = "Игра окончена!\nВаш результат: " + str(score)
        answer = messagebox.askquestion("Игра окончена!", result + "\nХотите сыграть еще раз?")
        if answer == "yes":
            root.after_cancel(creating_egg)
            root.after_cancel(throwing_eggs)
            start_game(egg_speed,egg_interval)
        else:
            root.destroy()

def lost_life():
    global lives_left
    lives_left -= 1
    if lives_left<=0:
        lives_left = 0
    
    c.itemconfigure(lives_text, text="Жизни: "+ str(lives_left))

def checking_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher_img)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if eggx > catcherx and catchery < eggy2 and catcherx2 > eggx2:
            if c.itemcget(egg, 'fill') == "#FFD700":
                update_score(bonus_score)
            else:
                update_score(egg_score)       
            eggs.remove(egg)
            c.delete(egg)
    root.after(100, checking_catch)

def update_score(points):
    global score
    if lives_left>0:
        score += points
        if score>best_result:
            best_result = score
    c.itemconfigure(best_result_text, text="Рекорд: "+str(best_result).zfill(4))
    c.itemconfigure(score_text, text="Очки: "+ str(score).zfill(4))

def moving_catcher(position):
    c.move(catcher_img, catcher_positions[position]["x"] - c.coords(catcher_img)[0], catcher_positions[position]["y"] - c.coords(catcher_img)[1])

def moving_to_upper_left(event):
    moving_catcher("upper_left")

def moving_to_left(event):
    moving_catcher("left")

def moving_to_upper_right(event):
    moving_catcher("upper_right")

def moving_to_right(event):
    moving_catcher("right")

c.bind("q", moving_to_upper_left)
c.bind("a", moving_to_left)
c.bind("e", moving_to_upper_right)
c.bind("d", moving_to_right)
c.focus_set()
difficulty_frame = Frame(root)
def display_score():
    global score_text
    score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="white", text="Очки: "+ str(score).zfill(4))

def display_record():
    global best_result_text
    best_result_text = c.create_text(10, 35, anchor="nw", font = game_font, fill="white", text="Рекорд: "+ str(best_result).zfill(4))

def display_lives():
    global lives_text
    lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="white", text="Жизни: "+ str(lives_left))
    
chicken_up_l = c.create_rectangle(120,10,250,0, fill="#F6C033", outline="grey")
chicken_up_r = c.create_rectangle(canvas_width-160,10,canvas_width-290,0, fill="#F6C033", outline="grey")
chicken_l = c.create_rectangle(170,150,300,140, fill="#F6C033", outline="grey")
chicken_r = c.create_rectangle(canvas_width-210,150,canvas_width-340,140, fill="#F6C033", outline="grey")

def start_game(speed,interval):
    global eggs, score, egg_speed,egg_interval, lives_left, catcher_img,score_text,lives_text,best_result, best_result_text,grass, chicken_up_l, chicken_up_r, chicken_l, chicken_r
    difficulty_frame.pack_forget()
    start_button.pack_forget()
    c.delete("all")
    egg_speed=speed
    egg_interval=interval
    lives_left = 3
    score = 0
    eggs = []
    
    grass = c.create_rectangle(0,canvas_height,canvas_width,canvas_height-50, fill="#547943",width=0.1, outline="grey")
    chicken_up_l = c.create_rectangle(120,10,250,0, fill="#F6C033", outline="grey")
    chicken_up_r = c.create_rectangle(canvas_width-160,10,canvas_width-290,0, fill="#F6C033", outline="grey")
    chicken_l = c.create_rectangle(170,150,300,140, fill="#F6C033", outline="grey")
    chicken_r = c.create_rectangle(canvas_width-210,150,canvas_width-340,140, fill="#F6C033", outline="grey")
    creating_catcher()
    display_lives()
    display_score()
    display_record()

    root.after(egg_interval, creating_egg)
    root.after(egg_speed, throwing_eggs)
    root.after(1000, checking_catch)

def choose_difficulty():
    global difficulty_frame
    difficulty_frame = Frame(root)
    start_button.pack_forget()
    
    difficulty_frame.pack(side="left",padx=10, pady=10)

    difficulty_label = Label(difficulty_frame, text="Выберите уровень:")
    difficulty_label.pack()
    
    level1_button = Button(difficulty_frame, text="Простой", command=lambda: start_game(50,3000))
    level1_button.pack()

    level2_button = Button(difficulty_frame, text="Средний", command=lambda: start_game(35,2500))
    level2_button.pack()

    level3_button = Button(difficulty_frame, text="Сложный", command=lambda: start_game(20,2000))
    level3_button.pack()
        
def exit_game():
    root.destroy()

    
start_button = Button(root, text="Играть", command=choose_difficulty)
start_button.pack(side="left", padx=10,pady=10)

exit_button = Button(root, text="Выйти", command=exit_game)
exit_button.pack(side="right", padx=10, pady=10)

root.mainloop()
