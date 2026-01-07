import tkinter as tk
from tkinter import messagebox


class SimpleCoffeeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор кофе")
        self.root.geometry("300x400")
        self.prices = {
            "Эспрессо": 100,
            "Американо": 120,
            "Капучино": 150,
            "Латте": 170
        }
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Калькулятор стоимости кофе",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="Выберите кофе:").pack()
        self.coffee_var = tk.StringVar(value="Эспрессо")
        coffee_frame = tk.Frame(self.root)
        coffee_frame.pack(pady=5)
        for coffee in self.prices:
            rb = tk.Radiobutton(coffee_frame, text=f"{coffee} - {self.prices[coffee]} руб.",
                                variable=self.coffee_var, value=coffee)
            rb.pack(anchor="w")

        tk.Label(self.root, text="Количество чашек:").pack()
        self.quantity_var = tk.IntVar(value=1)
        tk.Spinbox(self.root, from_=1, to=10, textvariable=self.quantity_var,
                   width=10).pack()

        tk.Label(self.root, text="Добавить:").pack(pady=(10, 0))
        self.sugar_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Сахар (+10 руб.)",
                       variable=self.sugar_var).pack()
        self.milk_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Молоко (+15 руб.)",
                       variable=self.milk_var).pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Рассчитать",
                  command=self.calculate, width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Сбросить",
                  command=self.reset, width=10).pack(side="left", padx=5)

        self.result_label = tk.Label(self.root, text="Стоимость: 0 руб.",
                                     font=("Arial", 12, "bold"), fg="green")
        self.result_label.pack(pady=10)

    def calculate(self):
        try:
            coffee_type = self.coffee_var.get()
            base_price = self.prices[coffee_type]

            additions = 0
            if self.sugar_var.get():
                additions += 10
            if self.milk_var.get():
                additions += 15

            quantity = self.quantity_var.get()
            price_per_cup = base_price + additions
            total = price_per_cup * quantity

            self.result_label.config(text=f"Стоимость: {total} руб.")

            details = f"""
            Детали заказа:
            {coffee_type}: {base_price} руб.
            Количество: {quantity}
            Добавки: {additions} руб.
            Итого: {total} руб.
            """
            messagebox.showinfo("Результат", details)

        except Exception as e:
            messagebox.showerror("Ошибка", "Проверьте введенные данные")

    def reset(self):
        self.coffee_var.set("Эспрессо")
        self.quantity_var.set(1)
        self.sugar_var.set(False)
        self.milk_var.set(False)
        self.result_label.config(text="Стоимость: 0 руб.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCoffeeCalculator(root)
    root.mainloop()
