import tkinter as tk

# Drawing Variables
pencil_size = 8
previous_point, current_point = [0,0],[0,0]

# Window-Relevant Variables
width = 600
height = 400
screen_width = None
screen_height = None
resize_after_id = None

alpha_values = [0.2, 0.6, 1.0]
current_alpha_index = 0

def _stop_draw(event):
    global previous_point
    previous_point = [0,0]


def _draw(event, size = 8, color = "black"):
    global previous_point, current_point, canvas

    current_point = [event.x, event.y]
    
    if previous_point != [0,0]:
        x, y = event.x, event.y
        #canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='black')
        canvas.create_line(previous_point[0],previous_point[1],current_point[0],current_point[1], 
                           fill=color, width=size, capstyle=tk.ROUND, joinstyle=tk.BEVEL)
    
    previous_point = current_point


def _toggle_alpha(event):
    global current_alpha_index
    current_alpha_index = (current_alpha_index + 1) % len(alpha_values)
    new_alpha = alpha_values[current_alpha_index]
    root.attributes("-alpha", new_alpha)

def _clear_canvas():
    global canvas
    canvas.delete("all")

#--- Creating Interface ---#

root = tk.Tk()
root.title("Quick Scribble")

screen_width = root.winfo_screenwidth()/2
screen_height = root.winfo_screenheight()/2
root.geometry(f"{width}x{height}+{int(screen_width-width/2)}+{int(screen_height-height/2)}")
root.attributes("-alpha", 0.8)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)



#gives extra parameters through lambda function to cdraw functions
canvas.bind("<B1-Motion>", _draw) 
canvas.bind("<ButtonPress-1>", _draw)
canvas.bind("<ButtonRelease-1>", _stop_draw)
canvas.bind("<B3-Motion>", lambda event: _draw(event, pencil_size*2, "white"))  # Right-click to erase
canvas.bind("<ButtonPress-3>", lambda event: _draw(event, pencil_size*2, "white"))
canvas.bind("<ButtonRelease-3>", _stop_draw)
root.bind("<Tab>", _toggle_alpha)

# Start the Interface Loop
root.mainloop()
