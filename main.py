import pygame
import os
import json
import time
import sys

pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WHAT IF ... SAINT - PETERSBURG !")
SCENES_JSON_PATH = os.path.join("Final-Project_1", "scenes.json")
# ["x", "y", width, height]

FONT = pygame.font.Font(None, 50)
WHITE = (255, 255, 255)
BLUE = (50, 50, 200)
HOVER_BLUE = (100, 100, 255)
# BLUE = (160,82,45)          # Đậm hơn
# HOVER_BLUE = (139,69,19)    # Đậm hơn chút khi hover

MENU_BUTTON_COLOR = (34, 78, 74)         # Xanh rêu đậm
MENU_BUTTON_HOVER = (64, 128, 124)       # Xanh rêu sáng hơn
MENU_TEXT_COLOR = (255, 255, 224)        # Vàng nhạt kiểu "ivory"

CLICK_SOUND = pygame.mixer.Sound(os.path.join("Final-Project_1", "Sounds", "Sound effect", "click.mp3"))
HOVER_SOUND = pygame.mixer.Sound(os.path.join("Final-Project_1", "Sounds", "Sound effect", "hover.mp3"))
FONT_PATH = os.path.join("Final-Project_1", "fonts", "Montserrat-Bold.ttf")
TITLE_FONT = pygame.font.Font(FONT_PATH, 64)
TITLE_FONT_2 = pygame.font.Font(FONT_PATH, 55)
BUTTON_FONT = pygame.font.Font(FONT_PATH, 40)

hover_states = {}  # dict lưu trạng thái hover từng nút theo id
pygame.mixer.init()

def render_text_with_shadow(text, font, color, shadow_color, offset=(3, 3)):
    base = font.render(text, True, color)
    shadow = font.render(text, True, shadow_color)
    surface = pygame.Surface((base.get_width() + offset[0]*2, base.get_height() + offset[1]*2), pygame.SRCALPHA)

    # Vẽ bóng nhiều lần để đậm hơn
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            surface.blit(shadow, (offset[0]+dx, offset[1]+dy))
    surface.blit(base, (offset[0], offset[1]))
    return surface

title_surface = render_text_with_shadow("WHAT IF ... SAINT - PETERSBURG !", TITLE_FONT, (255, 255, 255), (0, 0, 0))
screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 80))

def play_music(path):
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)  # -1 để loop vô hạn
    else:
        print(f"[WARN] Không tìm thấy nhạc nền: {path}")

def draw_button(screen, rect, text, font, mouse_pos, color_normal, color_hover, tooltip_text=None, hover_sound=None):
    is_hovered = rect.collidepoint(mouse_pos)
    rect_id = id(rect)

    # Phát âm thanh hover nếu hover lần đầu
    if is_hovered and not hover_states.get(rect_id, False):
        if hover_sound:
            hover_sound.play()
        hover_states[rect_id] = True
    elif not is_hovered:
        hover_states[rect_id] = False

    color = color_hover if is_hovered else color_normal
    alpha = 255 if is_hovered else 100          # Sáng khi di chuột vàovào

    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    button_surface.fill((*color, alpha))
    pygame.draw.rect(button_surface, (*color, alpha), button_surface.get_rect(), border_radius=20)
    screen.blit(button_surface, rect.topleft)

    text_surface = font.render(text, True, MENU_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    # Vẽ tooltip nếu hover và có tooltip_text
    if is_hovered and tooltip_text:
        draw_tooltip(screen, tooltip_text, font, rect.topright)

def draw_tooltip(screen, text, font, pos, max_width=400, padding=10):
    # Tách text thành các dòng vừa max_width
    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = line + (' ' if line else '') + word
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    line_height = font.get_height() + 2
    height = line_height * len(lines) + padding * 2
    width = max(font.size(line)[0] for line in lines) + padding * 2

    # Tạo surface tooltip
    tooltip_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(tooltip_surf, (255, 255, 255, 255), tooltip_surf.get_rect(), border_radius=8)
    pygame.draw.rect(tooltip_surf, (0, 0, 0, 255), tooltip_surf.get_rect(), 2, border_radius=8)

    # Vẽ text lên tooltip
    y = padding
    for line in lines:
        line_surf = font.render(line, True, (0, 0, 0))
        tooltip_surf.blit(line_surf, (padding, y))
        y += line_height

    # Tính vị trí vẽ tooltip, tránh ra ngoài màn hình
    x, y = pos
    if x + width > WIDTH:
        x = WIDTH - width - 10
    if y + height > HEIGHT:
        y = HEIGHT - height - 10

    screen.blit(tooltip_surf, (x, y))

def save_game(slot, data):
    print(f"[DEBUG SAVE] Slot {slot}, Data: {data}")  # Thêm dòng này
    save_folder = os.path.join("Final-Project_1","Saves")
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    save_path = os.path.join(save_folder, f"slot{slot}.json")
    with open(save_path, "w") as f:
        json.dump(data, f)

def load_game(slot):
    save_path = os.path.join("Final-Project_1", "Saves", f"slot{slot}.json")
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            data = json.load(f)
            # Đảm bảo trả về đúng dict gồm 3 trường hoặc mặc định
            return {
                "slot": data.get("slot", slot),
                "scene": data.get("scene", "menu"),
                "title": data.get("title", "No title")
            }
    return None

def assign_default_tooltips(buttons):
    letters = ['A', 'B', 'C']
    for i, btn in enumerate(buttons):
        # Gán label ngắn cho nút nếu chưa có tooltip_text
        if "tooltip_text" not in btn or not btn["tooltip_text"]:
            if i < len(letters):
                btn["tooltip_text"] = f"OPTION {letters[i]}"
            else:
                btn["tooltip_text"] = f"OPTION {i+1}"
    return buttons

def parse_position(pos, size, screen_size):
    if isinstance(pos, str):
        if pos == "center":
            return screen_size // 2 - size // 2
        elif pos == "left":
            return 20
        elif pos == "right":
            return screen_size - size - 20
        elif pos == "top":
            return 20
        elif pos == "bottom":
            return screen_size - size - 20
        else:
            return 0  # fallback
    return pos  # nếu là số thì giữ nguyên

def save_slot_menu(action="save", current_save_data=None, scene_name=None, scene_title=None):
    running = True
    slots = []
    slot_rects = []
    slot_width, slot_height = 700, 70
    start_y = 200
    font = pygame.font.Font(None, 40)

    hovered_buttons = {}

    for i in range(5):
        rect = pygame.Rect(WIDTH // 2 - slot_width // 2, start_y + i*(slot_height + 20), slot_width, slot_height)
        slot_rects.append(rect)
        slots.append(i+1)

    # Tạo nút menu ở menu save slot
    menu_rect = pygame.Rect(WIDTH // 2 - slot_width // 2, start_y + len(slots)*(slot_height + 20), slot_width, slot_height)

    while running:
        screen.fill((30, 30, 30))
        title = "Select Save Slot to Save Game"
        title_surf = font.render(title, True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()

        # --- Cập nhật và phát hiệu ứng hover ---
        all_rects = slot_rects + [menu_rect]
        for rect in all_rects:
            rect_id = id(rect)  # Dùng id làm key
            is_hovered = rect.collidepoint(mouse_pos)
            was_hovered = hovered_buttons.get(rect_id, False)
            if is_hovered and not was_hovered:
                HOVER_SOUND.play()
            hovered_buttons[rect_id] = is_hovered


        for i, rect in enumerate(slot_rects):
            slot_num = slots[i]
            save_data = load_game(slot_num)
            if save_data is None:
                text = f"Slot {slot_num} - Empty"
            else:
                slot_scene_name = save_data.get("scene", "Unknown scene")
                slot_scene_title = scenes_data.get(slot_scene_name, {}).get("title", "No title")
                text = f"Slot {slot_num} - {slot_scene_name} - {slot_scene_title}"
            draw_button(screen, rect, text, font, mouse_pos, BLUE, HOVER_BLUE)

        # Vẽ nút menu
        draw_button(screen, menu_rect, "Menu", font, mouse_pos, BLUE, HOVER_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(slot_rects):
                    if rect.collidepoint(event.pos):
                        CLICK_SOUND.play()  
                        slot_num = slots[i]
                        if action == "save":
                            if current_save_data is not None and scene_name is not None and scene_title is not None:
                                print("Debug scene_name:", scene_name)
                                # Chuẩn bị dữ liệu lưu chỉ gồm slot, scene, title
                                save_data_to_write = {
                                    "slot": slot_num,
                                    "scene": scene_name,
                                    "title": scene_title
                                }
                                save_game(slot_num, save_data_to_write)
                                print(f"Game saved to slot {slot_num}!")
                            running = False
                            return slot_num
                        
                        elif action == "new_game":
                            new_save = {
                                "slot": slot_num,
                                "scene": "scene1",
                                "title": scene_title
                            }
                            save_game(slot_num, new_save)
                            print(f"New game saved to slot {slot_num}")
                            running = False
                            return new_save
                        
                        elif action == "continue":
                            save_data = load_game(slot_num)
                            if save_data:
                                print(f"Loaded slot {slot_num}")
                                running = False
                                return save_data
                            else:
                                print(f"Slot {slot_num} is empty!")
                    
                if menu_rect.collidepoint(event.pos):
                    CLICK_SOUND.play()  
                    # Trả về giá trị đặc biệt để quay lại menu
                    running = False
                    return "menu"


        pygame.display.flip()

def load_scenes_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for scene_name, scene_data in data.items():
        buttons = scene_data.get("buttons", [])

        # Tự động chia đều nếu y = "auto"
        auto_buttons = [b for b in buttons if b["rect"][1] == "auto"]
        if auto_buttons:
            total_height = sum(b["rect"][3] for b in auto_buttons)
            spacing = 20
            total_spacing = spacing * (len(auto_buttons) - 1)
            start_y = (HEIGHT - (total_height + total_spacing)) // 2
            for i, btn in enumerate(auto_buttons):
                btn["rect"][1] = start_y + i * (btn["rect"][3] + spacing)

        for btn in buttons:
            rect = btn["rect"]
            x = parse_position(rect[0], rect[2], WIDTH)
            y = parse_position(rect[1], rect[3], HEIGHT)
            btn["rect"] = pygame.Rect(x, y, rect[2], rect[3])

    return data

scenes_data = load_scenes_data(SCENES_JSON_PATH)

class Scene:
    def __init__(self, screen, scene_name, title, text, image_path, buttons, save_data=None):
        self.screen = screen
        self.scene_name = scene_name      # lưu tên scene
        self.title = title
        self.full_text = text
        self.image = None
        if image_path and os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.buttons = buttons
        self.save_data = save_data or {"slot": 1, "scene": "", "title": ""}
        self.message = ""
        self.message_time = 0
        self.text_finished = False

        # Gán tooltip mặc định nếu chưa có
        self.buttons = assign_default_tooltips(self.buttons)

        # Tách buttons thành 2 nhóm
        support_actions = ("save", "menu", "exit", "new_game", "continue")
        self.support_buttons = [btn for btn in self.buttons if btn["action"] in support_actions]
        self.main_buttons = [btn for btn in self.buttons if btn["action"] not in support_actions]

        

        # ---- CHỈNH PHẦN CHẠY CHỮ ----
        self.lines = self.full_text.split('\n')  # tách text theo dòng
        self.current_line_index = 0
        self.char_index = 0
        self.displayed_text = ""
        self.text_speed = 40  # ký tự/giây
        self.last_update_time = time.time()

        # Khung thoại
        self.dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH - 100, 250)

        # --- THÊM PHẦN CHIA VỊ TRÍ BUTTON NẰM NGANG ---
        if self.scene_name != "menu":
            self.arrange_buttons_horizontally()

        # Chạy nhạc nền nếu có
        music_path = scenes_data.get(scene_name, {}).get("music")
        if music_path:
            play_music(music_path)

    def arrange_buttons_horizontally(self):
        n = len(self.main_buttons)
        if n == 0:
            return
        # Giả sử tất cả button có cùng kích thước (lấy của button đầu)
        btn_width = self.main_buttons[0]["rect"][2]
        btn_height = self.main_buttons[0]["rect"][3]
        spacing = 50  # khoảng cách giữa các nút

        total_width = n * btn_width + (n - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        fixed_y = HEIGHT // 2 - btn_height // 2  # có thể chỉnh y theo ý

        for i, btn in enumerate(self.main_buttons):
            x = start_x + i * (btn_width + spacing)
            # giữ y cũ hoặc dùng fixed_y
            btn["rect"] = pygame.Rect(x, fixed_y, btn_width, btn_height)

    def draw_dialog_box(self, rect, text, font, text_color = (255,255,255), box_color = (0,0,0,180), border_color = (255,255,255), padding = 20):
        # Vẽ nền hộp thoại đen có alpha (mờ)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill(box_color)
        self.screen.blit(s, rect.topleft)
        # Vẽ viền
        pygame.draw.rect(self.screen, border_color, rect, 3)

        max_width = rect.width - 2*padding
        max_height = rect.height - 2*padding
        line_height = font.get_height() + 5

        # Tách text theo dòng có sẵn \n trước
        paragraphs = text.split('\n')
        y = rect.top + padding

        # Xuống dòng thủ côngg
        for para in paragraphs:
            words = para.split(' ')
            line = ''
            for word in words:
                test_line = (line + ' ' + word).strip()
                if font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    # Vẽ dòng hiện tại
                    line_surf = font.render(line, True, text_color)
                    if y + line_height > rect.top + max_height:
                        # Đã vượt quá chiều cao hộp thoại, dừng vẽ
                        return
                    self.screen.blit(line_surf, (rect.left + padding, y))
                    y += line_height
                    line = word
            # Vẽ dòng cuối cùng của đoạn
            if line:
                line_surf = font.render(line, True, text_color)
                if y + line_height > rect.top + max_height:
                    return
                self.screen.blit(line_surf, (rect.left + padding, y))
                y += line_height

    def update_text(self):
        if self.text_finished:
            return

        now = time.time()  # Lấy thời gian hiện tại (giây từ epoch)
        elapsed = now - self.last_update_time  # Thời gian trôi qua kể từ lần cập nhật cuối
        chars_to_add = int(elapsed * self.text_speed)  # Số ký tự cần thêm dựa trên tốc độ text_speed

        if chars_to_add > 0:
            current_line = self.lines[self.current_line_index]
            self.char_index = min(self.char_index + chars_to_add, len(current_line))
            self.displayed_text = current_line[:self.char_index]
            self.last_update_time = now

            # Nếu đã hiển thị hết dòng hiện tại thì thôi chờ click để chuyển dòng
            if self.char_index == len(current_line):
                # Có thể set flag chờ click nếu muốn, hoặc để ở đây thôi
                pass
      
    def draw(self):
        self.screen.fill((0,0,0))
        if self.image:
            self.screen.blit(self.image, (0,0))

        if self.scene_name == "menu":
            # Vẽ tiêu đề đẹp có đổ bóng
            title_text = "WHAT IF ... SAINT - PETERSBURG !"
            title_surface = render_text_with_shadow(title_text, TITLE_FONT, (150, 150, 150), (50, 50, 50))
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))  # Canh giữa ngang, cách trên 100 px
            self.screen.blit(title_surface, title_rect)

            # Vẽ chữ Main Menu trên đầu, ví dụ ở giữa ngang, y = 150 px
            main_menu_text = "Main Menu"
            main_menu_surface = render_text_with_shadow(main_menu_text, TITLE_FONT_2, (32,178,170), (0,0,0))
            main_menu_rect = main_menu_surface.get_rect(topleft=(WIDTH * 0.75, 350))  # Cách tiêu đề khoảng 80 px
            self.screen.blit(main_menu_surface, main_menu_rect)

            # Dịch các nút sang phải
            btn_x = int(WIDTH * 0.76)
            btn_y_start = main_menu_rect.bottom + 40  # Cách "Main Menu" khoảng 40px
            spacing = 20

            for i, btn in enumerate(self.buttons):
                btn_width, btn_height = btn["rect"].size
                new_x = btn_x
                new_y = btn_y_start + i * (btn_height + spacing)
                btn["rect"].topleft = (new_x, new_y)

        else:
            # Cập nhật chữ chạy dần
            self.update_text()
            # Vẽ khung thoại với chữ chạy dần
            self.draw_dialog_box(self.dialog_rect, self.displayed_text, FONT)

        mouse_pos = pygame.mouse.get_pos()
        
        # Chỉ vẽ button khi đã chạy full_text
        if self.scene_name == "menu" or self.text_finished:
            # Vẽ tất cả nút bình thường (không vẽ tooltip trong draw_button)
            for btn in self.main_buttons:
                draw_button(self.screen, btn["rect"], btn.get("tooltip_text", btn["text"]), FONT, mouse_pos, BLUE, HOVER_BLUE, hover_sound=HOVER_SOUND)
            
            # Tìm nút main nào đang hover, vẽ tooltip cho nút đó
            for btn in self.main_buttons:
                if btn["rect"].collidepoint(mouse_pos):
                    tooltip_text = btn.get("text")
                    draw_tooltip(self.screen, tooltip_text, FONT, btn["rect"].topright)
                    break  # chỉ vẽ tooltip cho nút đầu tiên được hover

        for btn in self.support_buttons:
                draw_button(self.screen, btn["rect"], btn["text"], FONT, mouse_pos, MENU_BUTTON_COLOR, MENU_BUTTON_HOVER, hover_sound=HOVER_SOUND)

        if self.message and time.time() - self.message_time < 2:
            msg_surf = FONT.render(self.message, True, (255, 255, 0))                           # Tạo surface chữ màu vàng
            self.screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, HEIGHT - 250))      # Vẽ chữ ở giữa dưới màn hình
        else:
            self.message = ""           # Nếu hết 2 giây hoặc không có message, xóa tin nhắn đi

    def handle_event(self, event):
        # Khi người chơi click, ta có thể hiện luôn hết chữ đang chạy dần đễ đỡ chờ
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ✅ Luôn cho phép click support buttons
            for btn in self.support_buttons:
                if btn["rect"].collidepoint(event.pos):
                    CLICK_SOUND.play()
                    return self.process_action(btn["action"])
                

            if not self.text_finished:
                # Hiện hết text từng dòng nếu chưa xong
                current_line = self.lines[self.current_line_index]
                if self.char_index < len(current_line):
                    # Hiện hết dòng hiện tại nếu chưa hết
                    self.char_index = len(current_line)
                    self.displayed_text = current_line
                else:
                    # Chuyển sang dòng tiếp theo hoặc kết thúc text
                    if self.current_line_index < len(self.lines) - 1:
                        self.current_line_index += 1
                        self.char_index = 0
                        self.displayed_text = ""
                        self.last_update_time = time.time()
                    else:
                        self.text_finished = True
                return None
            
            # Kiểm tra main buttons
            for btn in self.main_buttons:
                if btn["rect"].collidepoint(event.pos):
                    CLICK_SOUND.play()
                    return self.process_action(btn["action"])

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        return None

    def process_action(self, action):
        if action == "save":
            slot = save_slot_menu(action="save", current_save_data=self.save_data, scene_name=self.scene_name, scene_title=self.title)
            if isinstance(slot, int):
                self.message = f"Game saved to slot {slot}!"
                self.message_time = time.time()
            return slot

        elif action == "continue":
            save_data = save_slot_menu(action="continue")
            if isinstance(save_data, dict):
                return save_data.get("scene", "scene1")
            else:
                return save_data

        elif action == "new_game":
            save_data = save_slot_menu(action="new_game")
            if isinstance(save_data, dict):
                return save_data.get("scene", "scene1")
            else:
                return save_data

        elif action == "menu":
            return "menu"

        elif action == "exit":
            return "exit"

        elif action.startswith("scene"):
            return action

        return action

def create_scene(name, save_data=None):
    data = scenes_data.get(name)
    if not data:
        return None
    return Scene(screen, name, data["title"], data["text"], data["image_path"], data["buttons"], save_data)

def run_scene(scene_manager):
    running = True
    while running:
        scene_manager.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            action = scene_manager.handle_event(event)
            if action == "exit":
                running = False
            elif action == "menu":
                running = False
                return "menu"
            elif isinstance(action, str) and action.startswith("scene"):
                running = False
                return action
            # Nếu action là int (ví dụ slot số), hoặc None thì ignore hoặc xử lý tùy mục đích
    return None

def run_scene_name(name, save_data=None):
    scene = create_scene(name, save_data)
    if scene is None:
        return None
    return run_scene(scene)

def main():
    current_scene = "menu"
    current_save_data = None
    while True:
        next_scene = run_scene_name(current_scene, current_save_data)
        if next_scene in [None, "exit"]:
            break
        
        # Nếu next_scene là dict chứa save_data
        if isinstance(next_scene, dict):
            current_save_data = next_scene
            current_scene = current_save_data.get("scene", current_scene) # Giữ nguyên nếu không có scene mới
        else:
            current_scene = next_scene
            # Cập nhật scene vào save_data nếu có
            if current_save_data:
                current_save_data["scene"] = current_scene

    pygame.quit()

if __name__ == "__main__":
    main()
