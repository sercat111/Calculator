import tkinter as tk
import math

# Конфигурация эффекта
GLOW_RADIUS = 50
BG_COLOR = "#000000"  # Черный фон


class GlowEffectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Glow Effect")
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)

        # Холст для рисования
        self.canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Привязка событий мыши
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)

        # Позиция мыши
        self.mouse_x, self.mouse_y = 0, 0
        self.glow_ids = []

    def on_mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.draw_glow()

    def on_mouse_leave(self, event):
        self.clear_glow()

    def draw_glow(self):
        self.clear_glow()

        # Создаем градиентное свечение
        for r in range(GLOW_RADIUS, 0, -1):
            intensity = 1 - r / GLOW_RADIUS
            color = self.get_color(intensity)
            glow_id = self.canvas.create_oval(
                self.mouse_x - r, self.mouse_y - r,
                self.mouse_x + r, self.mouse_y + r,
                outline=color, width=2
            )
            self.glow_ids.append(glow_id)

    def get_color(self, intensity):
        """Генерация цвета с учетом интенсивности"""
        green = int(255 * intensity)
        return f"#00{green:02x}00"

    def clear_glow(self):
        for glow_id in self.glow_ids:
            self.canvas.delete(glow_id)
        self.glow_ids = []


if __name__ == "__main__":
    root = tk.Tk()
    app = GlowEffectApp(root)
    root.mainloop()