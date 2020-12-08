from tkinter import *
from random import choice as ch

# ----- settings -----

field_size=10
w, h=500, 530
open_btns_num=10
color_dict={'dot': 'black', 'bomb': 'black', 'flag': 'black', 1: 'blue', 2: 'green', 3: 'red'}

# ----- variables -----

buttons_twodim=[]
buttons_onedim=[]
aux_list=[[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
stop_=False
flags_num=0

# ----- functions -----

def Button_ok():
    global field_size
    if var.get()!=0: field_size=var.get()
    flags_num_lbl.config(text=f'flags: {field_size+1}') 
    Generate_board()

def Put_flag(event):
    global flags_num
    if not stop_:
        if event.widget['text']!='⛳':
            if flags_num<field_size+1:
                event.widget.config(text='⛳', fg=color_dict['flag'], bg='#C0C0C0')
                flags_num+=1
        else:
            event.widget.config(text='', bg='#DCDCDC')
            flags_num-=1
    flags_num_lbl.config(text=f'flags: {field_size+1-flags_num}')

def Check_button(event):
    global stop_
    global flags_num
    if not stop_:
        if event.widget.text=='💣':
            for button in buttons_onedim:
                button.config(text=button.text, fg=button.color)
                stop_=True
        else:
            if event.widget['text']=='⛳':
                flags_num-=1
            event.widget.config(text=event.widget.text, fg=event.widget.color, bg='#DCDCDC')
    flags_num_lbl.config(text=f'flags: {field_size+1-flags_num}')
    
def Field_analysis():
    for x in range(field_size):
        for y in range(field_size):
            a=0
            if buttons_twodim[x][y].text!='💣':
                for elem in aux_list:
                    try:
                        x_pos=x+elem[0]
                        y_pos=y+elem[1]
                        if x_pos>=0<=y_pos:
                            if buttons_twodim[x_pos][y_pos].text=='💣':
                                a+=1
                    except:
                        continue
            if a>0:
                buttons_twodim[x][y].text=str(a)
                if a<3: buttons_twodim[x][y].color=color_dict[a]
                else: buttons_twodim[x][y].color=color_dict[3]
    for i in range(open_btns_num):
        rnd_open_btn=ch(buttons_onedim)
        while True:
            if rnd_open_btn.text=='💣' or rnd_open_btn.text=='.':
                rnd_open_btn=ch(buttons_onedim)
            else:
                break
        rnd_open_btn.config(text=rnd_open_btn.text, fg=rnd_open_btn.color)
    
def Generate_board():
    global buttons_twodim, buttons_onedim
    global stop_, flags_num
    buttons_twodim.clear()
    buttons_onedim.clear()
    stop_=False
    flags_num=0
    for x in range(field_size):
        buttons_twodim.append([])
        for y in range(field_size):
            btn=Button(window, width=int(field_size/2.5), height=int(field_size/5), bg='#DCDCDC', font='arial 14')
            btn.text='.'
            btn.color=color_dict['dot']
            btn.bind('<Button-1>', Check_button)
            btn.bind('<Button-3>', Put_flag)
            buttons_twodim[x].append(btn)
            buttons_onedim.append(btn)
            btn.place(x=x*(w//field_size), y=y*((w//field_size))+h-w)
    for i in range(field_size+1):
        rnd_bomb=ch(buttons_onedim)
        while True:
            if rnd_bomb.text=='💣':
                rnd_bomb=ch(buttons_onedim)
            else:
                break
        rnd_bomb.text='💣'
        rnd_bomb.color=color_dict['bomb']
    Field_analysis()

# ----- widgets -----

window=Tk()
window.geometry(f'{w}x{h}')
window.title('Minesweeper')
window.resizable(False, False)

var=IntVar()
rbutton_10x10=Radiobutton(window, text='10x10', variable=var, value=10)
rbutton_12x12=Radiobutton(window, text='12x12', variable=var, value=12)
rbutton_10x10.place(x=0, y=0)
rbutton_12x12.place(x=70, y=0)

button_ok=Button(window, text='ok', width=5, height=1, bg='#DEB887', font='arial 12', command=Button_ok)
button_ok.place(x=w, y=0, anchor='ne')

flags_num_lbl=Label(window, width=7, height=1, font='arial 12')
flags_num_lbl.place(x=w//3, y=0)

window.mainloop()