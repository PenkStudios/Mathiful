from PIL import Image
from time import sleep
from tkinter.filedialog import asksaveasfile
import __main__

def export_gif(app):

    files = [('GIF Files', '*.gif'),
        ('All Files', '*.*')]
    file = asksaveasfile(filetypes = files, defaultextension = files)

    if file == None: return

    imgs = []

    slider = app._map(app.bar_position,
            app.options_resolution[0]//2-150,
            app.options_resolution[0]//2+150,
            3, 45)

    for _ in range(slider):

        colors = []
        for y, i in enumerate(app.grid):
            for x in range(len(i)):
                colors.extend(app.hex2rgb(app.grid[y][x]))

        colors = bytes(colors)
        imgs.append(Image.frombytes('RGB', (len(app.grid[0]), len(app.grid)), colors))
        sleep(app.update_delay / 1000)
        app.step_button(None)

    file.close()

    gif = []
    for image in imgs:
        gif.append(image.convert("P",palette=Image.ADAPTIVE))
    gif[0].save(file.name, save_all=True,optimize=False, append_images=gif[1:], loop=0, duration=(app.update_delay/13)*slider)

def export_png(app):
    files = [('PNG Files', '*.png'),
        ('All Files', '*.*')]
    file = asksaveasfile(filetypes = files, defaultextension = files)

    if file == None: return

    colors = []
    for y, i in enumerate(app.grid):
        for x in range(len(i)):
            colors.extend(app.hex2rgb(app.grid[y][x]))

    colors = bytes(colors)
    img = Image.frombytes('RGB', (len(app.grid[0]), len(app.grid)), colors)
    img.save(file.name)
    file.close()