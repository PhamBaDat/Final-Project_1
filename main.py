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

FONT_PATH = os.path.join("Final-Project_1", "fonts", "Montserrat-Bold.ttf")
TITLE_FONT = pygame.font.Font(FONT_PATH, 64)
BUTTON_FONT = pygame.font.Font(FONT_PATH, 40)

def render_text_with_shadow(text, font, color, shadow_color, offset=(2, 2)):
    base = font.render(text, True, color)
    shadow = font.render(text, True, shadow_color)
    surface = pygame.Surface((base.get_width() + offset[0], base.get_height() + offset[1]), pygame.SRCALPHA)
    surface.blit(shadow, offset)
    surface.blit(base, (0, 0))
    return surface

title_surface = render_text_with_shadow("WHAT IF ... SAINT - PETERSBURG !", TITLE_FONT, (255, 255, 255), (0, 0, 0))
screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 80))

def draw_button(screen, rect, text, font, mouse_pos, color_normal, color_hover):
    is_hovered = rect.collidepoint(mouse_pos)
    color = color_hover if is_hovered else color_normal
    alpha = 255 if is_hovered else 100  # Sáng khi hover, mờ khi không

    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    button_surface.fill((*color, alpha))
    pygame.draw.rect(button_surface, (*color, alpha), button_surface.get_rect(), border_radius=10)
    screen.blit(button_surface, rect.topleft)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

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

        # Cho chạy chữ dần
        self.char_index = 0
        self.displayed_text = ""
        self.text_speed = 40 # ký tự / giây
        self.last_update_time = time.time()

        # Khung thoại
        self.dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH - 100, 150)

    def draw_dialog_box(self, rect, text, font, text_color = (255,255,255), box_color = (0,0,0,180), border_color = (255,255,255), padding = 20):
        # Vẽ nền hộp thoại đen có alpha (mờ)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill(box_color)
        self.screen.blit(s, rect.topleft)
        # Vẽ viền
        pygame.draw.rect(self.screen, border_color, rect, 3)

        # Xuống dòng thủ côngg
        lines = []
        words = text.split(" ")
        line = ''
        max_width = rect.width - 2*padding
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] > max_width:
                lines.append(line)
                line = word + " "
            else:
                line = test_line
        lines.append(line)

        y = rect.top + padding
        for line in lines:
            line_surf = font.render(line, True, text_color)
            self.screen.blit(line_surf, (rect.left + padding, y))
            y += font.get_height() + 5

    def update_text(self):
        now = time.time()  # Lấy thời gian hiện tại (giây từ epoch)
        elapsed = now - self.last_update_time  # Thời gian trôi qua kể từ lần cập nhật cuối
        chars_to_add = int(elapsed * self.text_speed)  # Số ký tự cần thêm dựa trên tốc độ text_speed

        if chars_to_add > 0:
            # Cập nhật vị trí ký tự hiện tại, tối đa không vượt quá độ dài full_text
            self.char_index = min(self.char_index + chars_to_add, len(self.full_text))

            # Cập nhật đoạn text đang hiển thị: từ đầu đến char_index
            self.displayed_text = self.full_text[:self.char_index]

            # Cập nhật lại thời gian lần cuối đã update
            self.last_update_time = now

            if self.char_index == len(self.full_text):
                self.text_finished = True
      
    def draw(self):
        self.screen.fill((0,0,0))
        if self.image:
            self.screen.blit(self.image, (0,0))

        if self.scene_name == "menu":
            # Vẽ chữ Main Menu trên đầu, ví dụ ở giữa ngang, y = 150 px
            title_surface = FONT.render(self.full_text, True, WHITE)
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 400))
            self.screen.blit(title_surface, title_rect)
        else:
            # Cập nhật chữ chạy dần
            self.update_text()
            # Vẽ khung thoại với chữ chạy dần
            self.draw_dialog_box(self.dialog_rect, self.displayed_text, FONT)

        mouse_pos = pygame.mouse.get_pos()
        # Chỉ vẽ button khi đã chạy full_text
        if self.scene_name == "menu" or self.text_finished:
            for btn in self.buttons:
                draw_button(self.screen, btn["rect"], btn["text"], FONT, mouse_pos, BLUE, HOVER_BLUE)

        if self.message and time.time() - self.message_time < 2:
            msg_surf = FONT.render(self.message, True, (255, 255, 0))
            self.screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, HEIGHT - 200))
        else:
            self.message = ""

    def handle_event(self, event):
        # Khi người chơi click, ta có thể hiện luôn hết chữ đang chạy dần đễ đỡ chờchờ
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.text_finished:
                # Hiện hết text nếu chưa xong
                self.char_index = len(self.full_text)
                self.displayed_text = self.full_text
                self.text_finished = True
                return None
            
            # Các phần xử lý cũ như save, chuyển scene...
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    action = btn["action"]
                    if action == "save":
                        print(f"[DEBUG] Saving scene: {self.scene_name}")
                        print(f"[DEBUG] Saving scene: {self.title}")
                        print(f"[DEBUG] Saving scene: {self.save_data}")
                        slot = save_slot_menu(action="save", current_save_data=self.save_data, scene_name=self.scene_name, scene_title=self.title)
                        if isinstance(slot, int):
                            self.message = f"Game saved to slot {slot}!"
                            self.message_time = time.time()
                        return slot  # có thể là int hoặc "menu"
                    
                    elif action == "continue":
                        save_data = save_slot_menu(action="continue")
                        if isinstance(save_data, dict):
                            return save_data.get("scene", "scene1")
                        else:
                            return save_data  # có thể là "menu" hoặc None

                    elif action == "new_game":
                        save_data = save_slot_menu(action="new_game")
                        if isinstance(save_data, dict):
                            return save_data.get("scene", "scene1")
                        else:
                            return save_data
                        
                    elif action == "menu":
                        return "menu"   # Trở về menu chính
                
                    elif action == "exit":
                        return "exit"   # Thoát game
                    
                    elif action.startswith("scene"):
                        return action  # trả về tên scene, ví dụ "scene1", "scene2", ...
                    
                    return action

                
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        return None

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
