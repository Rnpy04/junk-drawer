import tkinter as tk
import random
import time
import threading

class IQGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate IQ Trainer")
        self.root.geometry("600x400")

        self.score = 0
        self.level = 1
        self.time_limit = 8
        self.correct_answer = None
        self.current_mode = None

        self.title = tk.Label(root, text="Ultimate IQ Trainer", font=("Arial", 20))
        self.title.pack(pady=10)

        self.info = tk.Label(root, text="Score: 0 | Level: 1", font=("Arial", 12))
        self.info.pack()

        self.question = tk.Label(root, text="", font=("Arial", 16))
        self.question.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack()

        self.submit = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit.pack(pady=10)

        self.result = tk.Label(root, text="", font=("Arial", 12))
        self.result.pack()

        self.start_btn = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_btn.pack(pady=10)

        self.timer_label = tk.Label(root, text="", font=("Arial", 12))
        self.timer_label.pack()

    def start_game(self):
        self.score = 0
        self.update_info()
        self.next_question()

    def update_info(self):
        self.info.config(text=f"Score: {self.score} | Level: {self.level}")

    def next_question(self):
        self.entry.delete(0, tk.END)
        self.result.config(text="")
        self.current_mode = random.choice(
            ["math", "pattern", "missing", "compare"]
        )

        if self.current_mode == "math":
            self.math_question()
        elif self.current_mode == "pattern":
            self.pattern_question()
        elif self.current_mode == "missing":
            self.missing_question()
        elif self.current_mode == "compare":
            self.compare_question()

        self.start_timer()

    def start_timer(self):
        self.time_left = max(3, self.time_limit - self.level)
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.timer_running = True

        def countdown():
            while self.time_left > 0 and self.timer_running:
                time.sleep(1)
                self.time_left -= 1
                self.timer_label.config(text=f"Time: {self.time_left}")
            if self.time_left == 0:
                self.result.config(text="Time Up!")
                self.timer_running = False
                self.root.after(1000, self.next_question)

        threading.Thread(target=countdown, daemon=True).start()

    def math_question(self):
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])

        if op == "+":
            self.correct_answer = a + b
        elif op == "-":
            self.correct_answer = a - b
        else:
            self.correct_answer = a * b

        self.question.config(text=f"{a} {op} {b} = ?")

    def pattern_question(self):
        start = random.randint(1, 10)
        step = random.randint(2, 6)
        seq = [start + i * step for i in range(5)]
        self.correct_answer = seq[-1] + step
        self.question.config(text=f"Pattern: {seq} ?")

    def missing_question(self):
        a = random.randint(2, 20)
        b = random.randint(2, 20)
        op = random.choice(["+", "*"])

        if op == "+":
            result = a + b
        else:
            result = a * b

        if random.choice([True, False]):
            self.correct_answer = a
            self.question.config(text=f"? {op} {b} = {result}")
        else:
            self.correct_answer = b
            self.question.config(text=f"{a} {op} ? = {result}")

    def compare_question(self):
        a1 = random.randint(10, 50)
        b1 = random.randint(2, 10)
        a2 = random.randint(10, 50)
        b2 = random.randint(2, 10)

        expr1 = a1 * b1
        expr2 = a2 + b2

        if expr1 > expr2:
            self.correct_answer = "1"
        elif expr2 > expr1:
            self.correct_answer = "2"
        else:
            self.correct_answer = "equal"

        self.question.config(
            text=f"1) {a1} * {b1}    2) {a2} + {b2}\nWhich is bigger? (1 / 2 / equal)"
        )

    def check_answer(self):
        self.timer_running = False
        user = self.entry.get().strip()

        if user == str(self.correct_answer):
            self.score += 10 * self.level
            self.result.config(text="Correct!")
        else:
            self.result.config(text=f"Wrong! Answer: {self.correct_answer}")

        if self.score >= 100:
            self.level += 1
            self.score = 0
            self.result.config(text="Level Up!")

        self.update_info()
        self.root.after(1000, self.next_question)


root = tk.Tk()
game = IQGame(root)
root.mainloop()
