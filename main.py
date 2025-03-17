import pygame
import os
import json

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Last Job")

# Fuente y colores
FONT = pygame.font.Font(None, 50)
WHITE = (255, 255, 255)
BLUE = (50, 50, 200)
HOVER_BLUE = (100, 100, 255)

# Botones del menú
button_start = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
button_exit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

# Rutas
ESCENARIO_PATH = os.path.join("Escenarios", "escenario_1")
IMAGES_PATH = os.path.join(ESCENARIO_PATH, "Imagenes")
TEXT_PATH = os.path.join(ESCENARIO_PATH, "texto.json")

class Escenario1:
    """Clase que maneja el primer escenario del juego."""
    def __init__(self, screen):
        self.screen = screen
        self.text = "Texto no encontrado"
        self.image = None
        self.load_data()
        
        # Configuración del botón
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        self.button_text = FONT.render("Continuar", True, WHITE)

    def load_data(self):
        """Carga la imagen y el texto del escenario."""
        # Cargar texto desde JSON
        if os.path.exists(TEXT_PATH):
            with open(TEXT_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.text = data.get("descripcion", "No hay descripción.")
        
        # Cargar imagen (asumiendo que hay una imagen llamada 'fondo.png')
        image_path = os.path.join(IMAGES_PATH, "fondo.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

    def draw(self):
        """Dibuja la escena del escenario."""
        self.screen.fill((0, 0, 0))

        # Dibujar imagen de fondo si existe
        if self.image:
            self.screen.blit(self.image, (0, 0))

        # Dibujar caja de texto
        text_surface = FONT.render(self.text, True, WHITE)
        self.screen.blit(text_surface, (50, HEIGHT - 150))

        # Dibujar botón "Continuar"
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER_BLUE if self.button_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(self.screen, color, self.button_rect, border_radius=10)
        text_rect = self.button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(self.button_text, text_rect)

    def handle_event(self, event):
        """Maneja los eventos de pygame."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                print("Botón 'Continuar' presionado.")  # Aquí puedes hacer que pase al siguiente escenario

def menu():
    """Bucle del menú principal."""
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fondo negro

        # Título
        title_text = FONT.render("One Last Job", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Botones
        mouse_pos = pygame.mouse.get_pos()

        # Botón "Iniciar"
        start_color = HOVER_BLUE if button_start.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, start_color, button_start, border_radius=10)
        start_text = FONT.render("Iniciar", True, WHITE)
        screen.blit(start_text, (button_start.x + 50, button_start.y + 5))

        # Botón "Salir"
        exit_color = HOVER_BLUE if button_exit.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, exit_color, button_exit, border_radius=10)
        exit_text = FONT.render("Salir", True, WHITE)
        screen.blit(exit_text, (button_exit.x + 60, button_exit.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    print("Iniciando Escenario 1...")
                    escenario_1()
                if button_exit.collidepoint(event.pos):
                    running = False

    pygame.quit()

def escenario_1():
    """Ejecuta el primer escenario dentro del mismo juego."""
    manager = Escenario1(screen)
    running = True

    while running:
        screen.fill((0, 0, 0))
        manager.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

    menu()  # Regresar al menú si el escenario termina

if __name__ == "__main__":
    menu()
