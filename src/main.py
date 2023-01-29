# Trash code :)

from pe2d import Pe2D, TKINTER
from json import loads
from functools import partial

from tkinter.messagebox import showerror
from tkinter import Tk, Text, Canvas, Toplevel
import resources.export as image

DISABLE_URSINA = True
from pypenk import *

import resources.check as check
from tkinter.ttk import Notebook
from os.path import exists
import math, random, time
from sys import exit

def _read(file_name):
    if exists(file_name) != True:
        show_error("Reading file", "file " + file_name + " does not exist")
    else:
        with open(file_name, "r") as file:
            content = file.read()
        return content

def _shift_coords(coord, offset):
    return [coord[0] + offset[0], coord[1] + offset[1]]

from numpy import floor

def math_clamp(x, y): # magic, idk how this works
	divider = int(floor(x / y))
	
	if divider % 2 != 0:
		out = y - (x - y * divider)
	elif divider % 2 == 0:
		out = x - y * divider
	
	return out

CLAMP_CLAMP = 0
CLAMP_MODULO = 1
CLAMP_MATH = 2

class MathifulApp(Pe2D):
    def __init__(self, title, *args, **kwargs):
        super().__init__(type=TKINTER, title=title, *args, **kwargs)

        settings = loads(
            _read("resources/settings.json")
        )

        self.resolution = (self.resolution[0], self.resolution[1] - 25)

        self.grid_offset = 5

        self.grid_border_color = "#000000"
        self.grid_border_size = 2

        self.grid_size = [50, 50]

        self.default_grid_color = "#cccccc"

        self.gui_background = "#cccccc"
        self.gui_border_color = "#000000"
        self.gui_border_size = 2

        self.label_offset = 10
        self.label_background = "#bbbbbb"
        self.label_border_size = 2
        self.label_border_color = "#000000"

        self.button_background = "#aaaaaa"
        self.button_border_size = 2
        self.button_border_color = "#000000"

        self.inject_path = None

        self.clamp_type = CLAMP_MATH

        self.font = "monospace"
        self.times = 0

        self.challange_one_block = 40
        self.challenge_border_size = 2
        self.challenge_block_fill = "#dddddd"
        self.challenge_block_enabled_fill = "#bbbbbb"
        self.challenge_offset = 100

        self.start_button_x = 40
        self.start_button_y = 15
        self.start_button_width = 2
        self.start_button_fill = "#999999"

        self.options_resolution = (500, 300)
        self.options_offset = 5
        self.options_fill = "#bbbbbb"
        self.options_border_size = 2

        self.options_element_fill = "#999999"
        self.options_element_border_size = 2

        self.options_element2_fill = "#666666"
        self.options_element3_fill = "#444444"

        self.options_slider_circle_radius = 15
        self.options_radio_circle_radius = 10
        self.options_radio_circle2_radius = 6
        self.options_radio_spacing = 4

        self.challenge_delay = 500
        self.challenge_prewiev_frames = 10

        self.update_delay = 2

        self.bar_position = self.options_resolution[0] // 2 - 5
        self.bar2_position = self.options_resolution[0] // 2 - 70
        self.selected = 1

        for key, value in settings.items():
            setattr(self, key, value)

        self.one_grid = [
            ((self.resolution[0] - self.grid_offset * 4) / self.grid_size[0]) / 2,
            ((self.resolution[1] - self.grid_offset * 2) / self.grid_size[1])
        ]

        self.grid_start = [
            self.resolution[0] / 2 + self.grid_offset,
            self.grid_offset
        ]

        self.grid_end = [
            self.resolution[0] - self.grid_offset,
            self.resolution[1] - self.grid_offset
        ]

        self.gui_start = [
            self.grid_offset,
            self.grid_offset
        ]

        self.gui_end = [
            self.resolution[0] / 2 - self.grid_offset,
            self.resolution[1] - self.grid_offset
        ]

        self.label1_start = [
            self.label_offset * 2,
            self.label_offset * 2
        ]

        self.label1_end = [
            self.resolution[0] / 2 - self.label_offset * 2,
            self.resolution[1] / 2 - self.label_offset
        ]

        self.label1_avg = [
            (self.label1_start[0] + self.label1_end[0]) / 2,
            (self.label1_start[1] + self.label1_end[1]) / 2
        ]

        self.label2_start = [self.label1_start[0], self.label1_start[1] + (self.resolution[1] / 2)]
        self.label2_end = [self.label1_end[0], self.label1_end[1] + (self.resolution[1] / 2 - self.label_offset)]

        self.label2_avg = [
            (self.label2_start[0] + self.label2_end[0]) / 2,
            (self.label2_start[1] + self.label2_end[1]) / 2
        ]

        self.grid = []
        for _ in range(self.grid_size[1]):
            self.grid.append([])
            for _ in range(self.grid_size[0]):
                self.grid[-1].append(self.default_grid_color)
        
        self.notebook = Notebook(self.window)
        self.running = False

        self.drawable.destroy()

        self.drawable = Canvas(self.notebook, width=self.resolution[0], height=self.resolution[1])
        self.drawable.pack()

        self.challenges = {
            "One Color": [1, "Goal: Display a color (any color except black and white)", "Hint: Use the variable \"i\"", False, check.one_color],
            "Changing Color": [2, "Goal: Display a changing color", "Hint: Use the variable \"t\"", False, check.changing_color],
            "Gradient": [2, "Goal: Display a gradient according to x and y axis", "Hint: Use the variables \"x\" and \"y\"", False, check.gradient],
            "Chess Board": [3, "Goal: Display a chess board", "Hint: Modulo can help you", False, check.chess_board],
            "Grassy": [5, "Goal: Display a simple grassy place", "Hint: Nothing", False, check.grassy],
            "TV": [5, "Goal: Display a television with 3 pixels border", "Hint: Range class will help you", False, check.tv]
        }

        self.chall_drawable = Canvas(self.notebook, width=self.resolution[0], height=self.resolution[1])
        self.chall_drawable.pack()

        self.notebook.add(self.drawable, text="Main")

        self.notebook.add(self.chall_drawable, text="Challenges")

        self.notebook.pack()

        self.points = 0
        self.challange = False

        self.challupdate()

    def click(self, name, event):
        self.challenges[name][3] = not self.challenges[name][3]
        self.challupdate()

    def start(self, name, event):
        self.challange = name
        self.window.title("Mathiful - " + name)
        self.challupdate()
        self.notebook.select(self.drawable)
        self.tkupdate()

    def challupdate(self):
        self.chall_drawable.delete("all")
        y = 5
        index = 0
        for key, value in self.challenges.items():
            _x = (3 + self.resolution[0] - 5) // 2
            _y = (y * 2 + self.challange_one_block) // 2
            if value[3]: # is enabled?
                self.chall_drawable.tag_unbind("start" + str(index), "<Button-1>")
                self.chall_drawable.create_rectangle(3, y, self.resolution[0] - 5, y + (self.challange_one_block * 3 - 5), width=self.challenge_border_size, tags="button" + str(index), fill=self.challenge_block_enabled_fill)
                self.chall_drawable.create_text(_x, _y + self.challange_one_block, text=value[1], font=(self.font, 17))
                offset = len(value[2]) * 5.5
                self.chall_drawable.create_text(_x-offset, (_y + self.challange_one_block * 2) - 10, text=value[2], font=(self.font, 17))
                _x2, _y2 = _x+offset, (_y + self.challange_one_block * 2) - 10
                self.chall_drawable.create_rectangle(_x2 - self.start_button_x, _y2 - self.start_button_y, _x2 + self.start_button_x, _y2 + self.start_button_y, width=self.start_button_width, fill=self.start_button_fill, tags=("start" + str(index) if self.challange == False else "no"))
                self.chall_drawable.create_text(_x2, _y2, text="Start", tags="start" + str(index), font=(self.font, 15), fill="#000000" if self.challange == False else "#777777")
                if self.challange == False:
                    self.chall_drawable.tag_bind("start" + str(index), "<Button-1>", partial(self.start, key))
            self.chall_drawable.create_rectangle(3, y, self.resolution[0] - 5, y + self.challange_one_block, width=self.challenge_border_size, tags="button" + str(index), fill=self.challenge_block_fill)
            if type(value[0]) == bool:
                self.chall_drawable.create_text(self.resolution[0] - self.challenge_offset, _y, text="Wrong" if not value[0] else "Correct", font=(self.font, 15, "bold"), tags="button" + str(index), fill="green" if value[0] else "red")
            # ➡ ⬇
            self.chall_drawable.create_text(_x, _y, text=key + " " + ("➡" if value[3] == False else "⬇"), font=(self.font, 15, "bold"), tags="button" + str(index))
            self.chall_drawable.tag_bind("button" + str(index), "<Button-1>", partial(self.click, key))
            y += self.challange_one_block if not value[3] else self.challange_one_block * 3
            index += 1

    def run_loop(self):
        if self.running:
            self.step_button(None)
            self.window.after(self.update_delay, self.run_loop)

    def _run_times(self, times):
        if self.times <= times:
            self.step_button(None)
            self.window.after(self.update_delay, partial(self._run_times, times))
        self.times += 1

    def run_times(self, times):
        self.times = 0
        self._run_times(times)

    def challange_redirect(self):
        self.challange = False
        self.tkupdate()
        self.challupdate()
        self.window.title("Mathiful")
        self.notebook.select(self.chall_drawable)

    def challange_win(self):
        text = self.text.get("1.0", "end").strip()
        self.points += self.challenges[self.challange][0]
        self.challenges[self.challange][0] = True
        self.run_times(self.challenge_prewiev_frames if "t" in text or "c" in text else 2)
        self.window.after(int(self.challenge_delay * (self.challenge_prewiev_frames/2)), self.challange_redirect)

    def challange_lose(self):
        text = self.text.get("1.0", "end").strip()
        self.points -= self.challenges[self.challange][0]
        self.challenges[self.challange][0] = False
        self.run_times(self.challenge_prewiev_frames if "t" in text or "c" in text else 2)
        self.window.after(int(self.challenge_delay * (self.challenge_prewiev_frames/2)), self.challange_redirect)

    """128 if (x in range(0,3) or x in range(r[0]-3,r[0])) and \
	(y in range(0,3) or y in range(r[1]-3,r[1])) else \
	random(0,255)"""

    def run_button(self, *args):
        if self.challange:
            self.step_button(None)
            text = self.text.get("1.0", "end").strip()
            if self.challenges[self.challange][4](self.grid, text):
                self.challange_win()
            else:
                self.challange_lose()
        else:
            self.running = True
            self.run_loop()

    def center(self, window: Tk):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()
    
    def stop_button(self, *args):
        if self.challange:
            self.challange_redirect()
        else:
            self.running = False

    def export(self, *args):
        image.export_png(self)

    def export_gif(self, *args):
        image.export_gif(self)

    def drag(self, event):
        self.bar_position = max(self.options_resolution[0]//2-75, min(event.x, self.options_resolution[0]//2+205))
        self.options_update()

    def drag2(self, event):
        self.bar2_position = max(self.options_resolution[0]//2-75, min(event.x, self.options_resolution[0]//2+205))
        self.options_update()

    def switch(self, number, event):
        self.selected = number
        self.options_update()

    def options_update(self):
        self.options_drawable.delete("all")

        self.options_drawable.create_rectangle(self.options_offset, self.options_offset, self.options_resolution[0] - self.options_offset, self.options_resolution[1] - self.options_offset, fill=self.options_fill, width=self.options_border_size)
        
        def create_button(x0, y0, x1, y1, text="?", command=lambda x:0):
            position = [x0, y0, x1, y1]
            id = text.lower().replace(" ", "_") + "_button"

            self.options_drawable.create_rectangle(*position,
                fill=self.options_element_fill, width=self.options_element_border_size, tags=id)

            avg = [(position[0] + position[2]) // 2, (position[1] + position[3]) // 2]

            self.options_drawable.create_text(*avg, text=text, font=(self.font, 15), tags=id)

            self.options_drawable.tag_bind(id, "<Button-1>", command)

        def export_button(text, fx, x):
            create_button(self.options_resolution[0] // 2 - self.options_resolution[0] // 6 + x, self.options_resolution[1] - 65,
                self.options_resolution[0] // 2 + self.options_resolution[0] // 6 + x, self.options_resolution[1] - 15,
                text=text, command=fx)
        
        export_button("Export PNG", self.export, -105)
        export_button("Export GIF", self.export_gif, 105)

        # Slider rect
        self.options_drawable.create_rectangle(self.options_resolution[0]//2-75, self.options_resolution[1]//2-7,
            self.options_resolution[0]//2+205, self.options_resolution[1]//2-2, width=self.options_element_border_size, fill=self.options_element_fill, tags="slider_button")

        # Slider circle + text
        _y = self.options_resolution[1]/2-5
        self.options_drawable.create_oval(self.bar_position - self.options_slider_circle_radius, _y-self.options_slider_circle_radius, self.bar_position+self.options_slider_circle_radius, _y+self.options_slider_circle_radius, fill=self.options_element2_fill, width=self.options_element_border_size, tags="slider_button")
        self.options_drawable.tag_bind("slider_button", "<Button-1>", self.drag)

        self.options_drawable.create_text(self.bar_position, _y + 22, text=self._map(self.bar_position,
            self.options_resolution[0]//2-75,
            self.options_resolution[0]//2+205,
            2, 45), font=(self.font, 10))

        # Slider2 rect
        self.options_drawable.create_rectangle(self.options_resolution[0]//2-75, self.options_resolution[1]//2+45,
            self.options_resolution[0]//2+205, self.options_resolution[1]//2+40, width=self.options_element_border_size, fill=self.options_element_fill, tags="slider2_button")

        # Slider2 circle + text
        _y = self.options_resolution[1]/2+42.5
        self.options_drawable.create_oval(self.bar2_position - self.options_slider_circle_radius, _y-self.options_slider_circle_radius, self.bar2_position+self.options_slider_circle_radius, _y+self.options_slider_circle_radius, fill=self.options_element2_fill, width=self.options_element_border_size, tags="slider2_button")
        self.options_drawable.tag_bind("slider2_button", "<Button-1>", self.drag2)

        self.update_delay = self._map(self.bar2_position,
            self.options_resolution[0]//2-75,
            self.options_resolution[0]//2+205,
            0, 2000)
        self.options_drawable.create_text(self.bar2_position, _y + 22, text=str(self.update_delay) + " ms", font=(self.font, 10))

        

        self.options_drawable.create_text(self.options_resolution[0]//2-165, self.options_resolution[1]//2-5, text="GIF Frames", font=(self.font, 13))
        self.options_drawable.create_text(self.options_resolution[0]//2-165, self.options_resolution[1]/2+42.5, text="Update delay", font=(self.font, 13))

        _y = self.options_offset*8
        self.options_drawable.create_text(self.options_resolution[0]//2, _y, text="Clamp type", font=(self.font, 13))

        for n in range(3):
            x = (self.options_resolution[0]//2 - self.options_resolution[0]//self.options_radio_spacing) if n == 0 else \
                (self.options_resolution[0]//2) if n == 1 else \
                (self.options_resolution[0]//2 + self.options_resolution[0]//self.options_radio_spacing)
            
            self.options_drawable.create_oval(x - self.options_radio_circle_radius, _y + 35 - self.options_radio_circle_radius, 
                x + self.options_radio_circle_radius, _y + 35 + self.options_radio_circle_radius,
                width=self.options_element_border_size, fill=self.options_element2_fill, tags="radio" + str(n))

            self.options_drawable.tag_bind("radio" + str(n), "<Button-1>", partial(self.switch, n))

            text = "Basic clamp" if n == 0 else \
                "Math clamp" if n == 1 else \
                "Modulo clamp"

            self.options_drawable.create_text(x, _y + 60, text=text, font=(self.font, 10))

            if self.selected == n:
                self.clamp_type = CLAMP_CLAMP if n == 0 else \
                    CLAMP_MATH if n == 1 else \
                    CLAMP_MODULO
                self.options_drawable.create_oval(x - self.options_radio_circle2_radius, _y + 35 - self.options_radio_circle2_radius, 
                    x + self.options_radio_circle2_radius, _y + 35 + self.options_radio_circle2_radius,
                    width=self.options_element_border_size, fill=self.options_element3_fill)

    def options(self, *args):
        self.options_window = Toplevel()
        self.options_window.resizable(False, False)
        self.options_window.title("Options")
        
        self.options_window.geometry("%ix%i" % self.options_resolution)
        self.center(self.options_window)

        self.options_drawable = Canvas(self.options_window, width=self.options_resolution[0], height=self.options_resolution[1])
        self.options_drawable.pack()

        self.options_update()

        self.options_window.mainloop()

    def tkupdate(self):
        for tag in self.drawable.find_all():
            if hasattr(self, "tid"):
                if tag == self.tid: continue
            self.drawable.delete(tag)

        self.drawable.create_rectangle(
            *self.grid_start,
            *self.grid_end,
            fill="#ff0000",
            width=self.grid_border_size + 1,
            outline=self.grid_border_color
        )

        self.drawable.create_rectangle(
            *self.gui_start,
            *self.gui_end,
            fill=self.gui_background,
            width=self.gui_border_size,
            outline=self.gui_border_color
        )

        if hasattr(self, "text") != True:
            self.text = Text(self.drawable, bg=self.label_background, borderwidth=self.label_border_size, highlightcolor=self.label_border_color)
            mix = [
                (self.label1_start[0] + self.label1_end[0]) // 2,
                (self.label1_start[1] + self.label1_end[1]) // 2
            ]
            self.tid = self.drawable.create_window(
                *mix,
                window=self.text,
                width=self.label1_end[0] - self.label1_start[0],
                height=self.label1_end[1] - self.label1_start[1],
                tags="nodelete"
            )

            if self.inject_path != None:
                with open(self.inject_path, "r") as inject:
                    self.text.insert("end", inject.read())

        self.drawable.create_rectangle(
            *self.label2_start,
            *self.label2_end,
            fill=self.label_background,
            width=self.label_border_size,
            outline=self.label_border_color
        )

        if not self.challange:
            self.coords = [
                *_shift_coords(self.label2_avg, [-180, -100]),
                *_shift_coords(self.label2_avg, [-25, -25])
            ]

            self.drawable.create_rectangle(
                *self.coords,
                fill=self.button_background,
                outline=self.button_border_color,
                width=self.button_border_size,
                tags="step_button"
            )

            self.drawable.create_text(
                [(self.coords[0] + self.coords[2]) / 2],
                [(self.coords[1] + self.coords[3]) / 2],
                font=(self.font, 15 if not self.challange else 13),
                text="Step" if not self.challange else "Example result",
                tags="step_button"
            )

        self.coords = [
            *(_shift_coords(self.label2_avg, [25, -100]) if not self.challange else \
                _shift_coords(self.label2_avg, [-75, -100])),
            *(_shift_coords(self.label2_avg, [180, -25]) if not self.challange else \
                _shift_coords(self.label2_avg, [75, -25])),
        ]

        self.drawable.create_rectangle(
            *self.coords,
            fill=self.button_background,
            outline=self.button_border_color,
            width=self.button_border_size,
            tags="options_button"
        )

        self.drawable.create_text(
            [(self.coords[0] + self.coords[2]) / 2],
            [(self.coords[1] + self.coords[3]) / 2],
            font=(self.font, 15),
            text="Options",
            tags="options_button"
        )

        self.coords = [
            *_shift_coords(self.label2_avg, [-180, 10]),
            *_shift_coords(self.label2_avg, [-25, 95])
        ]

        self.drawable.create_rectangle(
            *self.coords,
            fill=self.button_background,
            outline=self.button_border_color,
            width=self.button_border_size,
            tags="run_button"
        )

        self.drawable.create_text(
            [(self.coords[0] + self.coords[2]) / 2],
            [(self.coords[1] + self.coords[3]) / 2],
            font=(self.font, 15),
            text="Run" if not self.challange else "Submit",
            tags="run_button"
        )

        self.coords = [
            *_shift_coords(self.label2_avg, [25, 10]),
            *_shift_coords(self.label2_avg, [180, 95])
        ]

        self.drawable.create_rectangle(
            *self.coords,
            fill=self.button_background,
            outline=self.button_border_color,
            width=self.button_border_size,
            tags="stop_button"
        )

        self.drawable.create_text(
            [(self.coords[0] + self.coords[2]) / 2],
            [(self.coords[1] + self.coords[3]) / 2],
            font=(self.font, 15 if not self.challange else 12),
            text="Stop" if not self.challange else "Stop challenge",
            tags="stop_button"
        )

        self.drawable.tag_bind("step_button", "<Button-1>", self.step_button)
        self.drawable.tag_bind("run_button", "<Button-1>", self.run_button)
        self.drawable.tag_bind("stop_button", "<Button-1>", self.stop_button)
        self.drawable.tag_bind("options_button", "<Button-1>", self.options)

        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                self.drawable.create_rectangle(
                    self.grid_start[0] + (x * self.one_grid[0]),
                    self.grid_start[1] + (y * self.one_grid[1]),
                    self.grid_start[0] + ((x + 1) * self.one_grid[0]),
                    self.grid_start[1] + ((y + 1) * self.one_grid[1]),
                    fill=self.grid[y][x],
                    width=0
                )

    @staticmethod
    def hex2rgb(hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[1:][i:i+2], 16)
            rgb.append(decimal)
        
        return rgb

    @staticmethod
    def rgb2hex(rgb):
        if not all([c in range(0, 256) for c in rgb]):
            raise ValueError("invalid rgb: " + str(rgb))
        return "#%02x%02x%02x" % tuple(rgb)

    @staticmethod
    def clamp(number, largest):
        return max(0, min(number, largest))

    @staticmethod
    def prime(number):
        # if number is equal to or less than 1, return False
        if number <= 1:
            return False

        for x in range(2, number):
            # if number is divisble by x, return False
            if not number % x:
                return False
        return True


    @staticmethod
    def diff(x, y):
        if x < y:
            return y - x
        else:
            return x - y

    @staticmethod
    def _map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
	
    def step_button(self, event):
        self.expr = self.text.get(1.0, "end").strip()

        clamp_modulo = lambda x, y: x % y

        if(self.clamp_type == CLAMP_MODULO):
            clamp_fx = clamp_modulo
        elif(self.clamp_type == CLAMP_CLAMP):
            clamp_fx = self.clamp
        elif(self.clamp_type == CLAMP_MATH):
            clamp_fx = math_clamp

        dictionary = {**math.__dict__, "random": random.randint, "clamp": self.clamp, "mclamp": math_clamp, "diff": self.diff, "prime": self.prime, "nummap": self._map, "numexec": lambda n: int(str(n)[0:0]+"0"), "vget": lambda x: globals()["local_"+x] if x in globals() else 0, "vset": lambda x,y: int(str(globals().update({"local_"+x: y}))[0:0]+"0")} 

        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                channels = self.hex2rgb(self.grid[y][x])
                color = []
                for index, channel in enumerate(channels):
                    dictionary["c"] = channel
                    dictionary["x"] = x
                    dictionary["y"] = y
                    dictionary["i"] = index
                    dictionary["t"] = round(time.time() * 1000)
                    dictionary["r"] = [len(self.grid[0]), len(self.grid)]
                    try:
                        out = eval(self.expr, dictionary)
                    except Exception as e:
                        self.stop_button()
                        self.times = 100000
                        showerror("Exception occurred", "Error: " + str(e))
                        self.expr = "255 if i == 0 else 0"
                        out = 255 if index == 0 else 0
                    color.append(out)


                color = [clamp_fx(channel, 255) for channel in color]
                self.grid[y][x] = self.rgb2hex(color)

        self.tkupdate()

if __name__ == "__main__":
    try:
        app = MathifulApp("Mathiful", icon="resources/app.png")
        app.run()
    except Exception as exception:
        root = Tk()
        root.geometry("0x0+0+0")
        root.withdraw()
        root.title("")
        showerror("Error", "Error occured: " + (str(exception) if str(exception) != "" else "<empty>"))
        exit(1)