import __main__ as main

def one_color(arr, cmd):
    hex2rgb = main.MathifulApp.hex2rgb

    color = None
    for y, y_list in enumerate(arr):
        for x in range(len(y_list)):
            if(y == 0 and x == 0):
                color = arr[y][x]
                rgb_color = hex2rgb(color)
                if(rgb_color[0] < 50 and rgb_color[1] < 50 and rgb_color[2] < 50):
                    return False
                if len(set(rgb_color)) <= 1:
                    return False

            if(arr[y][x] != color):
                return False

    return True

def changing_color(arr, cmd):
    def prev(list, x, y):
        try:
            return list[y][x - 4]
        except:
            try:
                return list[y - 1][0]
            except:
                return list[y][x]

    changed = []
    for y, y_list in enumerate(arr):
        for x in range(len(y_list)):
            if(arr[y][x] == prev(arr, x, y)):
                changed.append(True)
            else:
                changed.append(False)

    return False if changed.count(True) > len(changed) // 2 else (True if "t" in cmd else False)

def chess_board(arr, cmd):
    first = ""
    second = ""
    prev = ""
    for y, y_list in enumerate(arr):
        for x in range(len(y_list)):
            if arr[y][x] == prev and not x == 0:
                return False
            else:
                prev = arr[y][x]

            if x == 0 and y == 0:
                first = arr[y][x]
                continue
            elif x == 1 and y == 0:
                second = arr[y][x]
                continue

            if first == second:
                return False

            if arr[y][x] not in (first, second):
                return False

    return True

def grassy(arr, cmd):
    hex2rgb = main.MathifulApp.hex2rgb

    green = 0
    space = 0
    for y, y_list in enumerate(arr):
        for x in range(len(y_list)):
            if hex2rgb(arr[y][x])[1] > 240 and hex2rgb(arr[y][x])[2] < 240:
                if y < len(arr) // 2:
                    return False
                green += 1

            elif hex2rgb(arr[y][x])[2] > 240:
                if y > (len(arr) // 2) + (len(arr) // 3):
                    return False
                space += 1

    r = (len(arr[0]), len(arr))
    return True if green > r[0] * 2 and space > r[0] * (r[1] // 2) else False

def tv(arr, cmd):
    r = (len(arr[0]), len(arr))
    cpixels = 0
    bad = 0

    for y, y_list in enumerate(arr):
        for x in range(len(y_list)):
            if (x in range(0, 3) or x in range(r[0] - 3, r[0])) or \
                (y in range(0, 3) or y in range(r[1] - 3, r[1])):
                if x == 0 and y == 0:
                    bcolor = arr[y][x]
                else:
                    if arr[y][x] != bcolor:
                        return False
            else:
                if cpixels == 0:
                    ccolor = arr[y][x]
                else:
                    if arr[y][x] == ccolor:
                        bad += 1

                cpixels += 1

    return True if bad < 5 else False

def gradient(arr, cmd):
    cmd = cmd.replace(" ","").replace("\t","").replace("\\\n", "")
    return True if len(cmd) == 3 and (
        cmd == "x+y" or
        cmd == "y+x"
    )  else False