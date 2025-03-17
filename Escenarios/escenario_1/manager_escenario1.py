import pygame
import os
import json

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escenario 1")

# Fuente y colores
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
BUTTON_COLOR = (50, 50, 200)
BUTTON_HOVER = (100, 100, 255)

# Obtener la ruta del directorio del archivo actual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # 📌 Método más confiable

# Rutas de archivos
ESCENARIO_PATH = os.path.join(BASE_PATH, "Escenarios", "escenario_1")
IMAGES_PATH = os.path.join(ESCENARIO_PATH, "OIP.jpeg")
TEXT_PATH = os.path.join(ESCENARIO_PATH, "texto.json")
script_dir = os.path.dirname(os.path.abspath(__file__))  
image_path = os.path.join(script_dir, "OIP.jpeg") 


class EscenarioManager:
    def __init__(self, screen):
        self.screen = screen
        self.text = "Texto no encontrado"
        self.image = None
        self.load_data()
        
        # Configuración del botón
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        self.button_text = FONT.render("Continuar", True, WHITE)

    def load_data(self):
        """Carga la imagen y el texto desde la carpeta del escenario."""
	bg_img = tk.PhotoImage(file=image_path)

        # 📜 Cargar texto desde JSON
        if os.path.exists(TEXT_PATH):
            print(f"Cargando texto desde: {IMAGES_PATH}") 
            try:
                with open(TEXT_PATH, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    print(f"Contenido JSON: {data}")
                    self.text = data.get("descripcion", "No hay descripción.")
            except json.JSONDecodeError:
                print("Error: texto.json tiene un formato incorrecto.")

        # 📸 Cargar imagen
        if os.path.exists(IMAGES_PATH):
            print(f"Cargando imagen desde: {IMAGES_PATH}")  # 📌 Verificar ruta
            try:
                self.image = pygame.image.load(IMAGES_PATH)
                self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
            except pygame.error as e:
                print(f"Error al cargar imagen: {e}")
        else:
            print(f"⚠️ No se encontró la imagen en: {IMAGES_PATH}")

    def draw(self):
        """Dibuja la escena del escenario."""
        self.screen.fill((0, 0, 0))

        #Dibujar imagen de fondo si existe
        if self.image:
            self.screen.blit(self.image, (0, 0))

        #Dibujar caja de texto
        text_surface = FONT.render(self.text, True, WHITE)
        self.screen.blit(text_surface, (50, HEIGHT - 150))

        #Dibujar botón
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.button_rect, border_radius=10)
        text_rect = self.button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(self.button_text, text_rect)

    def handle_event(self, event):
        """Maneja los eventos de pygame (clics en botones)."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                print("Botón 'Continuar' presionado.")  # Aquí se puede agregar transición a otro escenario


def main():
    running = True
    manager = EscenarioManager(screen)

    while running:
        screen.fill((0, 0, 0))
        manager.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

    pygame.quit()


if __name__ == "__main__":
    main()
