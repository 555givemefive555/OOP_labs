import tkinter as tk
from abc import ABC, abstractmethod

class LogicOperation(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def symbol(self):
        pass

    @abstractmethod
    def calculate(self, a, b):
        pass

class AND(LogicOperation):
    def name(self):
        return "AND"

    def symbol(self):
        return "∧"

    def calculate(self, a, b):
        return int(bool(a) and bool(b))


class OR(LogicOperation):
    def name(self):
        return "OR"

    def symbol(self):
        return "∨"

    def calculate(self, a, b):
        return int(bool(a) or bool(b))


class XOR(LogicOperation):
    def name(self):
        return "XOR"

    def symbol(self):
        return "⊕"

    def calculate(self, a, b):
        return int(bool(a) != bool(b))

class SimpleLogicCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Логические операции")
        self.root.geometry("300x250")

        self.operations = [AND(), OR(), XOR()]

        tk.Label(root, text="Логические операции", font=("Arial", 14)).pack(pady=10)

        self.op_var = tk.StringVar(value="AND")
        for op in self.operations:
            tk.Radiobutton(root, text=op.name(),
                           variable=self.op_var, value=op.name()).pack()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="A:").grid(row=0, column=0)
        self.entry_a = tk.Entry(frame, width=5)
        self.entry_a.grid(row=0, column=1)
        self.entry_a.insert(0, "1")

        tk.Label(frame, text="B:").grid(row=0, column=2, padx=(10, 0))
        self.entry_b = tk.Entry(frame, width=5)
        self.entry_b.grid(row=0, column=3)
        self.entry_b.insert(0, "0")

        tk.Button(root, text="Вычислить", command=self.calculate).pack(pady=10)

        self.result_label = tk.Label(root, text="Результат: ", font=("Arial", 12))
        self.result_label.pack()

    def calculate(self):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())

            for op in self.operations:
                if op.name() == self.op_var.get():
                    result = op.calculate(a, b)
                    self.result_label.config(
                        text=f"Результат: {a} {op.symbol()} {b} = {result}"
                    )
                    break
        except:
            self.result_label.config(text="Ошибка ввода!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleLogicCalculator(root)
    root.mainloop()
