import tkinter as tk
from tkinter import messagebox

class CalculatorWithExceptions:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор с обработкой исключений")
        self.root.geometry("350x350")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Калькулятор с обработкой исключений",
                 font=("Arial", 12, "bold")).pack(pady=10)
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Число A:").grid(row=0, column=0, padx=5)
        self.entry_a = tk.Entry(input_frame, width=15)
        self.entry_a.grid(row=0, column=1, padx=5)
        self.entry_a.insert(0, "10")
        tk.Label(input_frame, text="Число B:").grid(row=1, column=0, padx=5, pady=10)
        self.entry_b = tk.Entry(input_frame, width=15)
        self.entry_b.grid(row=1, column=1, padx=5, pady=10)
        self.entry_b.insert(0, "2")
        tk.Label(self.root, text="Выберите операцию:").pack()
        self.operation_var = tk.StringVar(value="+")
        operations = ["+", "-", "×", "÷"]
        op_frame = tk.Frame(self.root)
        op_frame.pack(pady=10)

        for i, op in enumerate(operations):
            tk.Radiobutton(op_frame, text=op, variable=self.operation_var,
                           value=op).grid(row=0, column=i, padx=5)

        tk.Button(self.root, text="Рассчитать", command=self.calculate,
                  bg="lightblue", font=("Arial", 10), width=15).pack(pady=15)
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)
        tk.Label(result_frame, text="Результат:",
                 font=("Arial", 12, "bold")).pack(side="left")
        self.result_label = tk.Label(result_frame, text="0",
                                     font=("Arial", 12, "bold"), fg="green",
                                     width=15, relief="sunken", padx=10, pady=5)
        self.result_label.pack(side="left", padx=10)
        tk.Button(self.root, text="Сброс", command=self.reset,
                  width=15).pack(pady=5)
        tk.Label(self.root, text="Возможные исключения:",
                 font=("Arial", 10, "bold")).pack(pady=(20, 5))

    def calculate(self):
        try:
            a_str = self.entry_a.get().strip()
            b_str = self.entry_b.get().strip()
            op = self.operation_var.get()

            if not a_str or not b_str:
                raise ValueError("Оба поля должны быть заполнены")
            try:
                a = float(a_str)
                b = float(b_str)
            except ValueError:
                raise ValueError("Введите числа в правильном формате")

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "×":
                result = a * b
            elif op == "÷":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль невозможно")
                result = a / b
            else:
                raise ValueError("Неизвестная операция")

            self.result_label.config(text=f"{result:.4f}", fg="green")

        except ZeroDivisionError as e:
            self.handle_exception(e, "ZeroDivisionError")
        except ValueError as e:
            self.handle_exception(e, "ValueError")
        except Exception as e:
            self.handle_exception(e, type(e).__name__)

    def handle_exception(self, exception, exception_type):
        messagebox.showerror("Ошибка", f"{exception_type}:\n{str(exception)}")
        self.result_label.config(text="Ошибка!", fg="red")
        self.highlight_problem_fields(exception_type)

    def highlight_problem_fields(self, exception_type):
        self.entry_a.config(bg="white")
        self.entry_b.config(bg="white")

        if exception_type == "ZeroDivisionError":
            self.entry_b.config(bg="#ffe6e6")
        elif exception_type == "ValueError":
            try:
                float(self.entry_a.get().strip())
                self.entry_a.config(bg="white")
            except:
                self.entry_a.config(bg="#ffe6e6")
            try:
                float(self.entry_b.get().strip())
                self.entry_b.config(bg="white")
            except:
                self.entry_b.config(bg="#ffe6e6")

    def reset(self):
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, "10")
        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, "2")
        self.operation_var.set("+")
        self.result_label.config(text="0", fg="green")
        self.entry_a.config(bg="white")
        self.entry_b.config(bg="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorWithExceptions(root)
    root.mainloop()
