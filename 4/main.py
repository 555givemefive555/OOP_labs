import tkinter as tk
from tkinter import ttk, messagebox


class AllEventsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Практическое задание 4 - Все события")
        self.root.geometry("700x500")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="ComboBox событие")
        self.notebook.add(self.tab2, text="CheckBox событие")
        self.notebook.add(self.tab3, text="KeyPress событие")

        self.init_tab1()
        self.init_tab2()
        self.init_tab3()

    def init_tab1(self):
        self.city_data = {
            "Москва": {"страна": "Россия", "население": "12.7 млн", "год основания": "1147"},
            "Берлин": {"страна": "Германия", "население": "3.7 млн", "год основания": "1237"},
            "Париж": {"страна": "Франция", "население": "2.1 млн", "год основания": "52 г. до н.э."},
            "Лондон": {"страна": "Великобритания", "население": "8.9 млн", "год основания": "43 г."},
            "Токио": {"страна": "Япония", "население": "13.9 млн", "год основания": "1457"}
        }

        tk.Label(self.tab1, text="Выбор города",
                 font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.tab1)
        frame.pack(pady=10)

        tk.Label(frame, text="Город:").pack(side="left")

        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(
            frame,
            textvariable=self.city_var,
            values=list(self.city_data.keys()),
            width=15,
            state="readonly"
        )
        self.city_combo.pack(side="left", padx=10)
        self.city_combo.bind("<<ComboboxSelected>>", self.on_city_selected)

        self.city_info = tk.Text(self.tab1, height=8, width=50,
                                 font=("Arial", 10))
        self.city_info.pack(pady=10, padx=20)
        self.city_info.insert("1.0", "Выберите город для получения информации")
        self.city_info.config(state="disabled")

    def on_city_selected(self, event):
        city = self.city_var.get()
        if city in self.city_data:
            info = self.city_data[city]
            self.city_info.config(state="normal")
            self.city_info.delete("1.0", tk.END)

            text = f"Информация о городе {city}:\n\n"
            for key, value in info.items():
                text += f"{key.capitalize()}: {value}\n"

            self.city_info.insert("1.0", text)
            self.city_info.config(state="disabled")

    def init_tab2(self):
        tk.Label(self.tab2, text="Настройки уведомлений",
                 font=("Arial", 14, "bold")).pack(pady=10)

        self.notif_vars = {}
        notifications = [
            ("Новости", "Получать новости"),
            ("Акции", "Уведомления об акциях"),
            ("Сообщения", "Личные сообщения"),
            ("Обновления", "Уведомления об обновлениях"),
            ("Реклама", "Рекламные предложения")
        ]

        for i, (key, text) in enumerate(notifications):
            var = tk.BooleanVar(value=True if i < 2 else False)
            self.notif_vars[key] = var

            cb = tk.Checkbutton(
                self.tab2,
                text=text,
                variable=var,
                command=lambda k=key: self.on_notif_changed(k)
            )
            cb.pack(anchor="w", padx=30, pady=5)

        self.notif_status = tk.Label(self.tab2, text="Активно: 2 уведомления",
                                     font=("Arial", 10))
        self.notif_status.pack(pady=10)

        self.active_list = tk.Listbox(self.tab2, height=4, width=40)
        self.active_list.pack(pady=10)
        self.active_list.insert(0, "Новости")
        self.active_list.insert(1, "Акции")

    def on_notif_changed(self, key):
        active = [k for k, v in self.notif_vars.items() if v.get()]
        count = len(active)

        self.notif_status.config(text=f"Активно: {count} уведомлений")

        self.active_list.delete(0, tk.END)
        for item in active:
            self.active_list.insert(tk.END, item)

    def init_tab3(self):
        tk.Label(self.tab3, text="Конвертер чисел",
                 font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.tab3)
        frame.pack(pady=10)

        tk.Label(frame, text="Введите число:").pack(side="left")

        self.number_var = tk.StringVar()
        self.number_entry = tk.Entry(frame, textvariable=self.number_var,
                                     width=15, font=("Arial", 11))
        self.number_entry.pack(side="left", padx=10)
        self.number_entry.bind("<KeyRelease>", self.on_number_changed)

        results_frame = tk.Frame(self.tab3)
        results_frame.pack(pady=10, padx=20)

        tk.Label(results_frame, text="Двоичная:",
                 font=("Arial", 10, "bold")).grid(row=0, column=0,
                                                  sticky="w", pady=8)
        self.binary_label = tk.Label(results_frame, text="-",
                                     font=("Courier", 10))
        self.binary_label.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        tk.Label(results_frame, text="Восьмеричная:",
                 font=("Arial", 10, "bold")).grid(row=1, column=0,
                                                  sticky="w", pady=8)
        self.octal_label = tk.Label(results_frame, text="-",
                                    font=("Courier", 10))
        self.octal_label.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(results_frame, text="Шестнадцатеричная:",
                 font=("Arial", 10, "bold")).grid(row=2, column=0,
                                                  sticky="w", pady=8)
        self.hex_label = tk.Label(results_frame, text="-",
                                  font=("Courier", 10))
        self.hex_label.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        tk.Label(results_frame, text="Четность:",
                 font=("Arial", 10, "bold")).grid(row=3, column=0,
                                                  sticky="w", pady=8)
        self.parity_label = tk.Label(results_frame, text="-",
                                     font=("Arial", 10, "bold"))
        self.parity_label.grid(row=3, column=1, sticky="w", padx=10, pady=8)

    def on_number_changed(self, event):
        try:
            text = self.number_var.get()
            if text:
                num = int(text)

                binary = bin(num)[2:]
                self.binary_label.config(text=binary)

                octal = oct(num)[2:]
                self.octal_label.config(text=octal)

                hex_val = hex(num)[2:].upper()
                self.hex_label.config(text=hex_val)

                if num % 2 == 0:
                    self.parity_label.config(text="Чётное", fg="blue")
                else:
                    self.parity_label.config(text="Нечётное", fg="red")
            else:
                self.clear_labels()
        except ValueError:
            self.clear_labels()

    def clear_labels(self):
        self.binary_label.config(text="-")
        self.octal_label.config(text="-")
        self.hex_label.config(text="-")
        self.parity_label.config(text="-", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = AllEventsApp(root)
    root.mainloop()
