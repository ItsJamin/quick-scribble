import tkinter as tk

# Drawing Variables
pencil_size = 4
pencil_color = "black"
previous_point, current_point = [0,0],[0,0]

# Window-Relevant Variables
width = 1200
height = 800
screen_width = None
screen_height = None
resize_after_id = None

alpha_values = [0.4, 0.9, 1.0]
current_alpha_index = 1
lines_drawn = []
undone_lines = []

def _stop_draw(event):
    global previous_point
    previous_point = [0,0]


def _draw(event, size = -1, color = -1):
    global previous_point, current_point, canvas

    if size == -1:
        size = pencil_size
    if color == -1:
        color = pencil_color
    

    current_point = [event.x, event.y]
    x, y = event.x, event.y

    
    if previous_point != [0,0]:
        line_id = canvas.create_line(previous_point[0],previous_point[1],current_point[0],current_point[1], 
                           fill=color, width=size, capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True)
    else:
        line_id  = canvas.create_line(current_point[0],current_point[1],current_point[0],current_point[1], 
                           fill=color, width=size, capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True)
        lines_drawn.append([])
    lines_drawn[len(lines_drawn)-1].append(line_id)
    
    previous_point = current_point


def _toggle_alpha(event):
    global current_alpha_index
    current_alpha_index = (current_alpha_index + 1) % len(alpha_values)
    new_alpha = alpha_values[current_alpha_index]
    root.attributes("-alpha", new_alpha)

def _clear_canvas(event):
    global canvas
    canvas.delete("all")

    undone_lines = []
    lines_drawn = []
    


def _adjust_pencil_size(event):
    global pencil_size
    if event.delta > 0:  # Scroll Up
        pencil_size += 1
    elif event.delta < 0:  # Scroll Down
        pencil_size = max(4, pencil_size - 1)  # Ensure size is at least 1

def _mouse_motion(event):
    canvas.delete("cursor")

    # Draw new cursor circle
    x, y = event.x, event.y
    canvas.create_oval(x - pencil_size/2, y - pencil_size/2, x + pencil_size/2, y + pencil_size/2,
                       fill=pencil_color, width=2, tags="cursor")

def _set_color(color):
    global pencil_color
    pencil_color = color    

def _undo_last_line(event):
    global canvas, lines_drawn
    if lines_drawn:
        last_line_group = lines_drawn.pop()
        for line_id in last_line_group:
            if line_id:
                canvas.delete(line_id)
    
    print(lines_drawn)
        

#--- Creating Interface ---#

root = tk.Tk()
root.title("Quick Scribble")
#root.config(cursor="none")

screen_width = root.winfo_screenwidth()/2
screen_height = root.winfo_screenheight()/2
root.geometry(f"{width}x{height}+{int(screen_width-width/2)}+{int(screen_height-height/2)}")
_toggle_alpha(None)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)



#gives extra parameters through lambda function to cdraw functions
canvas.bind("<B1-Motion>", _draw) 
canvas.bind("<ButtonPress-1>", _draw)
canvas.bind("<ButtonRelease-1>", _stop_draw)
canvas.bind("<B3-Motion>", lambda event: _draw(event, pencil_size*2, "white"))  # Right-click to erase
canvas.bind("<ButtonPress-3>", lambda event: _draw(event, pencil_size*2, "white"))
canvas.bind("<ButtonRelease-3>", _stop_draw)

root.bind("<MouseWheel>", _adjust_pencil_size)
root.bind('<Motion>', _mouse_motion)

root.bind("<Control-d>", _clear_canvas)
root.bind("<Control-z>", _undo_last_line)
root.bind("<Control-Tab>", _toggle_alpha)

root.bind("0", lambda event: _set_color("black"))
root.bind("1", lambda event: _set_color("red"))
root.bind("2", lambda event: _set_color("blue"))
root.bind("3", lambda event: _set_color("green"))
root.bind("4", lambda event: _set_color("yellow"))


# Start the Interface Loop
root.mainloop()
