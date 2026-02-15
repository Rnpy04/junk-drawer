import tkinter as tk
import random

class SuperKidsIQGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Adventure 🧠🎮")
        self.root.geometry("520x500")
        self.root.config(bg="#FFFACD")

        self.score = 0
        self.level = 1
        self.hearts = 3
        self.correct_answer = None

        self.title = tk.Label(root, text="Brain Adventure 🧠🎮", font=("Comic Sans MS", 22), bg="#FFFACD")
        self.title.pack(pady=5)

        self.status = tk.Label(root, text=self.get_status(), font=("Comic Sans MS", 14), bg="#FFFACD")
        self.status.pack()

        self.progress = tk.Canvas(root, width=300, height=20, bg="white")
        self.progress.pack(pady=5)
        self.progress_bar = self.progress.create_rectangle(0, 0, 0, 20, fill="green")

        self.character = tk.Label(root, text="😺", font=("Arial", 40), bg="#FFFACD")
        self.character.pack()

        self.question = tk.Label(root, text="", font=("Comic Sans MS", 16), bg="#FFFACD")
        self.question.pack(pady=15)

        self.entry = tk.Entry(root, font=("Comic Sans MS", 14), justify="center")
        self.entry.pack()

        self.submit = tk.Button(root, text="Check ✅", font=("Comic Sans MS", 12),
                                command=self.check_answer, bg="#90EE90")
        self.submit.pack(pady=5)

        self.result = tk.Label(root, text="", font=("Comic Sans MS", 14), bg="#FFFACD")
        self.result.pack()

        self.start_btn = tk.Button(root, text="Start Adventure 🚀", font=("Comic Sans MS", 12),
                                   command=self.next_question, bg="#87CEFA")
        self.start_btn.pack(pady=10)

    def get_status(self):
        return f"⭐ Score: {self.score}   ❤️ Hearts: {self.hearts}   🎯 Level: {self.level}"

    def update_status(self):
        self.status.config(text=self.get_status())
        progress = min(self.score * 10, 300)
        self.progress.coords(self.progress_bar, 0, 0, progress, 20)

    def next_question(self):
        if self.hearts <= 0:
            self.game_over()
            return

        self.entry.delete(0, tk.END)
        self.result.config(text="")

        game_type = random.choice(["math", "pattern", "compare"])

        if game_type == "math":
            max_num = 10 + self.level * 5
            a = random.randint(1, max_num)
            b = random.randint(1, max_num)
            op = random.choice(["+", "-"])
            if op == "+":
                self.correct_answer = a + b
            else:
                self.correct_answer = a - b
            self.question.config(text=f"🧮 {a} {op} {b} = ?")

        elif game_type == "pattern":
            start = random.randint(1, 10)
            step = random.randint(1, self.level + 2)
            seq = [start, start + step, start + 2 * step]
            self.correct_answer = start + 3 * step
            self.question.config(text=f"🔢 Pattern: {seq} ?")

        else:
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

    def check_answer(self):
        user = self.entry.get().strip()

        happy_msgs = ["عااالیی! 🌟", "آفرین! 🎉", " باهوشی! 🧠", "شگفت انگیزه! 😺"]
        sad_msgs = ["Oops 😅", "Try Again 💪", "Don't Give Up! 🚀"]

        if user == str(self.correct_answer):
            self.score += 1
            self.result.config(text=random.choice(happy_msgs))
            self.character.config(text="😸")
        else:
            self.hearts -= 1
            self.result.config(text=f"{random.choice(sad_msgs)} Answer: {self.correct_answer}")
            self.character.config(text="😿")

        if self.score != 0 and self.score % 10 == 0:
            self.level += 1
            self.result.config(text="LEVEL UP! 🏆🎯")
            self.character.config(text="🤩")

        self.update_status()
        self.root.after(1200, self.next_question)

    def game_over(self):
        self.question.config(text="💔 Game Over!\nYou are a Brain Hero! 🏆")
        self.result.config(text=f"Final Score: {self.score} ⭐")
        self.character.config(text="🦸")
        self.entry.config(state="disabled")


root = tk.Tk()
game = SuperKidsIQGame(root)
root.mainloop()
