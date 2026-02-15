import tkinter as tk
import random
import time
import winsound

import pygame

pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)  # -1 یعنی loop بی‌نهایت
pygame.mixer.music.set_volume(0.3)  # حجم مناسب

# ---------------- THEMES ----------------

THEMES = {
    "Space": {"bg": "#0B132B", "fg": "#FFFFFF", "btn": "#5BC0BE"},
    "Jungle": {"bg": "#2D6A4F", "fg": "#FFFFFF", "btn": "#95D5B2"},
    "Candy": {"bg": "#FFC8DD", "fg": "#590D22", "btn": "#FFAFCC"},
    "Fire": {"bg": "#9B2226", "fg": "#FFF1C1", "btn": "#E85D04"},
}

CHARACTERS = {
    "Robot": "🤖",
    "Dragon": "🐉",
    "Astronaut": "🧑‍🚀",
    "Cat": "😺",
}

# ---------------- MAIN GAME CLASS ----------------

class BrainAdventureGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Adventure 🧠🎮")
        self.root.geometry("600x650")

        self.theme = THEMES["Candy"]
        self.character = "Cat"

        self.score = 0
        self.level = 1
        self.hearts = 3
        self.correct_answer = None
        self.current_game = None
        self.memory_numbers = []

        self.create_start_screen()
        
    def sound_correct(self):
        winsound.Beep(1200, 150)

    def sound_wrong(self):
        winsound.Beep(400, 300)

    def sound_level_up(self):
        winsound.Beep(1500, 400)


    # ---------------- UI HELPERS ----------------

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def styled_label(self, text, size=14):
        return tk.Label(
            self.root,
            text=text,
            font=("Comic Sans MS", size),
            bg=self.theme["bg"],
            fg=self.theme["fg"],
        )

    def styled_button(self, text, command):
        return tk.Button(
            self.root,
            text=text,
            command=command,
            font=("Comic Sans MS", 12),
            bg=self.theme["btn"],
            fg="black",
            width=20,
        )

    # ---------------- START SCREEN ----------------

    def create_start_screen(self):
        self.clear_screen()
        self.root.config(bg=self.theme["bg"])
        pygame.mixer.music.play(-1)  # -1 یعنی loop بی‌نهایت
        pygame.mixer.music.set_volume(0.3)  # حجم مناسب


        title = self.styled_label("Brain Adventure 🧠🎮", 24)
        title.pack(pady=20)

        start_btn = self.styled_button("Start Game 🚀", self.create_character_screen)
        start_btn.pack(pady=10)

        theme_btn = self.styled_button("Choose Theme 🎨", self.create_theme_screen)
        theme_btn.pack(pady=10)

    # ---------------- THEME SELECTION ----------------

    def create_theme_screen(self):
        self.clear_screen()
        self.root.config(bg=self.theme["bg"])

        title = self.styled_label("Choose Theme 🎨", 20)
        title.pack(pady=20)

        for t in THEMES:
            btn = tk.Button(
                self.root,
                text=t,
                font=("Comic Sans MS", 12),
                bg=THEMES[t]["btn"],
                width=15,
                command=lambda x=t: self.set_theme(x),
            )
            btn.pack(pady=5)

        back = self.styled_button("Back", self.create_start_screen)
        back.pack(pady=20)

    def set_theme(self, theme_name):
        self.theme = THEMES[theme_name]
        self.create_start_screen()

    # ---------------- CHARACTER SELECTION ----------------

    def create_character_screen(self):
        self.clear_screen()
        self.root.config(bg=self.theme["bg"])

        title = self.styled_label("Choose Your Hero 🧙", 20)
        title.pack(pady=20)

        for c in CHARACTERS:
            btn = tk.Button(
                self.root,
                text=f"{CHARACTERS[c]}  {c}",
                font=("Comic Sans MS", 14),
                width=15,
                command=lambda x=c: self.set_character(x),
            )
            btn.pack(pady=5)

    def set_character(self, char):
        self.character = char
        self.start_game()

    # ---------------- GAME SCREEN ----------------

    def start_game(self):
        self.score = 0
        self.level = 1
        self.hearts = 3
        self.clear_screen()
        self.root.config(bg=self.theme["bg"])

        self.status = self.styled_label("", 14)
        self.status.pack(pady=5)

        self.progress = tk.Canvas(self.root, width=300, height=20, bg="white")
        self.progress.pack()
        self.progress_bar = self.progress.create_rectangle(0, 0, 0, 20, fill="green")

        self.hero = tk.Label(
            self.root,
            text=CHARACTERS[self.character],
            font=("Arial", 50),
            bg=self.theme["bg"],
        )
        self.hero.pack(pady=10)

        self.question = self.styled_label("", 16)
        self.question.pack(pady=15)

        self.entry = tk.Entry(self.root, font=("Comic Sans MS", 14), justify="center")
        self.entry.pack()

        self.submit = self.styled_button("Check ✅", self.check_answer)
        self.submit.pack(pady=10)

        self.result = self.styled_label("", 14)
        self.result.pack(pady=5)

        self.update_status()
        self.next_question()

    # ---------------- STATUS ----------------

    def update_status(self):
        self.status.config(
            text=f"⭐ Score: {self.score}    ❤️ Hearts: {self.hearts}    🎯 Level: {self.level}"
        )
        progress = min((self.score % 10) * 30, 300)
        self.progress.coords(self.progress_bar, 0, 0, progress, 20)

    # ---------------- QUESTIONS ----------------

    def next_question(self):
        if self.hearts <= 0:
            self.game_over()
            return

        self.entry.delete(0, tk.END)
        self.result.config(text="")
        self.hero.config(text=CHARACTERS[self.character])

        self.current_game = random.choice(
            ["math", "pattern", "compare", "memory"]
        )

        if self.current_game == "math":
            self.math_question()
        elif self.current_game == "pattern":
            self.pattern_question()
        elif self.current_game == "compare":
            self.compare_question()
        else:
            self.memory_question()

    # ----- MATH -----
    def math_question(self):
        max_num = 10 + self.level * 5
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        op = random.choice(["+", "-"])
        if op == "+":
            self.correct_answer = a + b
        else:
            self.correct_answer = a - b
        self.question.config(text=f"🧮 {a} {op} {b} = ?")

    # ----- PATTERN -----
    def pattern_question(self):
        start = random.randint(1, 10)
        step = random.randint(1, self.level + 2)
        seq = [start, start + step, start + 2 * step]
        self.correct_answer = start + 3 * step
        self.question.config(text=f"🔢 Pattern: {seq} ?")

    # ----- COMPARE -----
    def compare_question(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        left = a + b
        right = c + random.randint(0, 5)

        if left > right:
            self.correct_answer = "L"
        elif right > left:
            self.correct_answer = "R"
        else:
            self.correct_answer = "E"

        self.question.config(
            text=f"⚖️ Left: {a}+{b}   Right: {right}\nWhich is bigger? (L / R / E)"
        )

    # ----- MEMORY -----
    def memory_question(self):
        self.memory_numbers = [random.randint(1, 9) for _ in range(5)]
        self.correct_answer = "".join(map(str, self.memory_numbers))
        self.question.config(text=f"🧠 Remember: {self.memory_numbers}")
        self.root.after(2000, self.hide_memory)

    def hide_memory(self):
        self.question.config(text="Type the numbers:")

    # ---------------- CHECK ANSWER ----------------

    def check_answer(self):
        user = self.entry.get().strip()

        if user == str(self.correct_answer):
            self.sound_correct()
            self.score += 1
            self.hero.config(text="😸")
            self.result.config(text="Awesome! 🌟")
        else:
            self.sound_wrong()
            self.hearts -= 1
            self.hero.config(text="😿")
            self.result.config(text=f"Oops! Answer: {self.correct_answer}")

        if self.score > 0 and self.score % 10 == 0:
            self.sound_level_up()
            self.level += 1
            self.result.config(text="LEVEL UP! 🏆")
            self.hero.config(text="🤩")

        self.update_status()
        self.root.after(1200, self.next_question)

    # ---------------- GAME OVER ----------------

    def game_over(self):
        pygame.mixer.music.fadeout(2000)  # ۲ ثانیه کم‌کم قطع شود

        self.clear_screen()
        self.root.config(bg=self.theme["bg"])

        medal = "🥉"
        if self.score >= 30:
            medal = "🥇"
        elif self.score >= 15:
            medal = "🥈"

        title = self.styled_label("Game Over 💔", 22)
        title.pack(pady=20)

        hero = tk.Label(
            self.root,
            text="🦸",
            font=("Arial", 60),
            bg=self.theme["bg"],
        )
        hero.pack()

        result = self.styled_label(
            f"Final Score: {self.score} ⭐   Medal: {medal}", 16
        )
        result.pack(pady=10)
        

        back = self.styled_button("Play Again 🔁", self.create_start_screen)
        back.pack(pady=20)


# ---------------- RUN ----------------

root = tk.Tk()
game = BrainAdventureGame(root)
root.mainloop()
