from PIL import ImageGrab
import os
from time import sleep




tile_width = 10
tile_height = 10

crop_x = 2445
crop_y = 1267#1342
crop_w = 230
crop_h = 410#260

def update_screen():
    screenshot = ImageGrab.grab()
    screenshot = screenshot.crop((crop_x, crop_y, crop_x+crop_w, crop_y+crop_h))
    screenshot = screenshot.convert("RGB")

    # Directory to save tiles
    output_dir = "static/android/"
    output_name = "screenshot"
    # screenshot.save(os.path.join(output_dir, f"{output_name}.png"))
    
    output_path = os.path.join(output_dir, f"{output_name}.jpg")
    with open(output_path, "wb") as f:
        screenshot.save(f, format="JPEG", quality=85, optimize=True)
        f.flush()
        os.fsync(f.fileno())  # Force write to disk

#screen_x = 5120
#screen_y = 2880
screen_vx = 2560
screen_vy = 1500

crop_vx = 1223
crop_vy = 634
crop_vx_max = 1223 + 114
crop_vy_max = 634 + 204

def get_tile_center(tile_index, cols, rows):
    tile_width = (crop_vx_max - crop_vx) / cols
    tile_height = (crop_vy_max - crop_vy) / rows
    
    col_index = tile_index % cols
    row_index = tile_index // cols

    center_x = crop_vx + col_index * tile_width + tile_width / 2
    center_y = crop_vy + row_index * tile_height + tile_height / 2

    return round(center_x), round(center_y)

def click(tile_index):
    cols = crop_w // tile_width
    rows = crop_h // tile_height
    
    vx, vy = get_tile_center(tile_index, cols, rows)
    
    #cursor_x = crop_x + 1
    #cursor_y = crop_y - 50
    #cursor_vx = round(cursor_x * (screen_vx / screen_x))
    #cursor_vy = round(cursor_y * (screen_vy / screen_y))
    #print(cursor_vx, cursor_vy)
    os.system("ydotool mousemove -x 9999999 -y 9999999 && ydotool mousemove -x -"+str(screen_vx)+" -y -"+str(screen_vy)+" && sleep .1 && ydotool mousemove -x "+str(vx)+" -y 0 && sleep .1 && ydotool mousemove -x 0 -y "+str(vy))
    sleep(0.1)
    os.system("ydotool click 0xC0")
