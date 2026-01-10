import tkinter as tk
import threading
import time

class BallThread(threading.Thread):
    def __init__(self, canvas, ball_id, x, y, dx, dy):
        super().__init__(daemon=True)
        self.canvas = canvas
        self.ball_id = ball_id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.running = True
        self.size = 20

    def run(self):
        while self.running:
            self.x += self.dx
            self.y += self.dy

            if self.x <= 20 or self.x >= 480:
                self.dx = -self.dx
            if self.y <= 20 or self.y >= 380:
                self.dy = -self.dy

            self.canvas.coords(
                self.ball_id,
                self.x - self.size, self.y - self.size,
                self.x + self.size, self.y + self.size
            )
            time.sleep(0.03)

class SimpleThreadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3 потока движения")
        self.root.geometry("500x400")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.create_balls()

    def create_balls(self):
        colors = ["red", "blue", "green"]
        positions = [(100, 100), (250, 150), (400, 200)]
        speeds = [(2, 1), (-1, 2), (1, -1)]
        self.threads = []

        for i in range(3):
            x, y = positions[i]
            dx, dy = speeds[i]

            ball = self.canvas.create_oval(
                x - 20, y - 20, x + 20, y + 20,
                fill=colors[i], outline="black"
            )

            thread = BallThread(self.canvas, ball, x, y, dx, dy)
            thread.start()
            self.threads.append(thread)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleThreadApp(root)
    root.mainloop()
