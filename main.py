import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import os
import random
import pygame

WIDTH, HEIGHT = 1000, 700
IMAGE_FILES = [f"img{i}.jpg" for i in range(1, 10)]
CAPTIONS = [
    "Your eyes hold galaxies that no telescope can find ✨",
    "Every smile of yours paints joy on my soul 🎨",
    "You walk like poetry, and breathe like art 🎭",
    "Your elegance dances like petals in the breeze 🌸",
    "The sparkle in your eyes outshines the stars 🌟",
    "You are the sunrise my heart waits for each day 🌅",
    "In your presence, time forgets to move ⏳",
    "You’re not just beautiful, you're breathtaking 💫",
    "You are my forever kind of magic ❤️"
]
SONG_PATH = "song.mp3"
SLIDE_DURATION = 2
BG_OPACITY = 0.3

class RomanticShow:
    def __init__(self, root):
        self.root = root
        self.root.title("💕 Romantic Surprise 💕")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()

        self.bg_image = self.load_faded_background("img1.jpg")
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)

        self.images = self.load_images()
        self.tk_img_refs = []

        self.title = self.canvas.create_text(
            WIDTH // 2, 100, text="Welcome Gorgeous 💖",
            font=("Segoe Script", 36, "bold"), fill="#C71585"
        )

        self.button = tk.Button(
            root, text="Click Here for Surprise ✨",
            font=("Helvetica", 16, "bold"), bg="#ff69b4", fg="white",
            command=self.start_surprise
        )
        self.canvas.create_window(WIDTH // 2, 540, window=self.button)

        self.caption = None
        self.floaters = []
        self.animate_floaters()

    def load_faded_background(self, file):
        if os.path.exists(file):
            img = Image.open(file).resize((WIDTH, HEIGHT)).convert("RGBA")
            overlay = Image.new("RGBA", img.size, (255, 255, 255, int(255 * (1 - BG_OPACITY))))
            faded = Image.alpha_composite(img, overlay)
            return ImageTk.PhotoImage(faded)
        return None

    def load_images(self):
        imgs = []
        for file in IMAGE_FILES:
            if os.path.exists(file):
                img = Image.open(file).resize((400, 600)).convert("RGBA")  # Portrait size
                imgs.append(img)
        return imgs

    def animate_floaters(self):
        def spawn():
            x = random.randint(50, WIDTH - 50)
            y = HEIGHT + 30
            shape = random.choice(["♥", "★", "❣", "✦"])
            color = random.choice(["#ff99cc", "#ff66b2", "#ff1493", "#ffd700"])
            size = random.randint(15, 30)
            floater = self.canvas.create_text(x, y, text=shape, fill=color, font=("Arial", size, "bold"))
            self.floaters.append((floater, random.uniform(-2, -4)))

        def move():
            for floater, speed in list(self.floaters):
                self.canvas.move(floater, 0, speed)
                _, y = self.canvas.coords(floater)
                if y < -30:
                    self.canvas.delete(floater)
                    self.floaters.remove((floater, speed))
            self.root.after(50, move)

        def loop():
            spawn()
            self.root.after(300, loop)

        move()
        loop()

    def play_music(self):
        if os.path.exists(SONG_PATH):
            pygame.mixer.init()
            pygame.mixer.music.load(SONG_PATH)
            pygame.mixer.music.play(-1)

    def start_surprise(self):
        self.canvas.delete(self.title)
        self.button.destroy()
        threading.Thread(target=self.play_music, daemon=True).start()
        threading.Thread(target=self.slideshow_once, daemon=True).start()

    def slideshow_once(self):
        for i, img in enumerate(self.images):
            self.transition_image(img, CAPTIONS[i], i)
            time.sleep(SLIDE_DURATION)
        self.show_final_message()

    def transition_image(self, img, caption, index):
        self.canvas.delete("IMG", "CAPTION")
        steps = 20
        img_orig = img.copy()
        img_width, img_height = img_orig.size

        for step in range(steps + 1):
            self.canvas.delete("IMG")
            progress = step / steps
            x, y = WIDTH // 2, HEIGHT // 2
            img_tk = None

            if index % 9 == 0:  # Fade Zoom
                scale = 0.6 + 0.4 * progress
                w, h = int(img_width * scale), int(img_height * scale)
                frame = img_orig.resize((w, h))
                frame.putalpha(int(255 * progress))
                img_tk = ImageTk.PhotoImage(frame)

            elif index % 9 == 1:  # Slide from left
                x = int(WIDTH * progress - WIDTH)
                img_tk = ImageTk.PhotoImage(img_orig)

            elif index % 9 == 2:  # Slide from top
                y = int(HEIGHT * progress - HEIGHT)
                img_tk = ImageTk.PhotoImage(img_orig)

            elif index % 9 == 3:  # Horizontal bounce (reel)
                offset = int(100 * (1 - progress) * (-1 if step % 2 == 0 else 1))
                img_tk = ImageTk.PhotoImage(img_orig)
                x += offset

            elif index % 9 == 4:  # Curtain reveal vertical
                img_cut = img_orig.crop((0, 0, img_width, int(img_height * progress)))
                img_tk = ImageTk.PhotoImage(img_cut)

            elif index % 9 == 5:  # Rotation Zoom (simulated)
                scale = 0.5 + 0.5 * progress
                w, h = int(img_width * scale), int(img_height * scale)
                frame = img_orig.resize((w, h))
                img_tk = ImageTk.PhotoImage(frame)

            elif index % 9 == 6:  # Flash fade
                img_copy = img_orig.copy()
                img_copy.putalpha(int(255 * progress))
                img_tk = ImageTk.PhotoImage(img_copy)

            elif index % 9 == 7:  # Shrink pop
                scale = 1 - 0.5 * (1 - progress)
                w, h = int(img_width * scale), int(img_height * scale)
                frame = img_orig.resize((w, h))
                img_tk = ImageTk.PhotoImage(frame)

            elif index % 9 == 8:  # Soft dissolve
                img_copy = img_orig.copy()
                img_copy.putalpha(int(255 * progress))
                img_tk = ImageTk.PhotoImage(img_copy)

            if img_tk:
                self.canvas.create_image(x, y, image=img_tk, tags="IMG")
                self.tk_img_refs = [img_tk]
            self.root.update()
            time.sleep(0.03)

        self.canvas.delete("IMG", "CAPTION")
        final_img = ImageTk.PhotoImage(img_orig)
        self.canvas.create_image(WIDTH // 2, HEIGHT // 2, image=final_img, tags="IMG")
        self.tk_img_refs = [final_img]
        self.caption = self.canvas.create_text(
            WIDTH // 2, HEIGHT - 60,
            text=caption,
            font=("Segoe UI", 20, "italic"),
            fill="#cc0066",
            tags="CAPTION"
        )

    def show_final_message(self):
        self.canvas.delete("IMG", "CAPTION")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#fff0f5", outline="")
        msg = "UR SOO BEAUTIFUL❤️"
        for size in range(10, 45):
            self.canvas.delete("FINAL")
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text=msg,
                font=("Segoe Script", size, "bold"),
                fill="#ff1493",
                tags="FINAL"
            )
            self.root.update()
            time.sleep(0.05)
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text=msg,
            font=("Segoe Script", 42, "bold"),
            fill="#ff1493",
            tags="FINAL"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RomanticShow(root)
    root.mainloop()
