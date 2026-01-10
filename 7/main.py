import tkinter as tk
from tkinter import Listbox, END, MULTIPLE, messagebox

class PlayerSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Выбор игроков")
        self.root.geometry("600x450")
        self.all_players = [
            "Иванов", "Сычев", "Месси", "Пеле",
            "Блохин", "Семенов", "Коби Брайант",
            "Давыдов", "Соколов", "Джордан", "Васильев"
        ]

        self.create_widgets()
        self.populate_players_list()

    def create_widgets(self):
        self.create_toolbar()
        self.create_lists_panel()
        self.bind_events()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.info_label = tk.Label(
            toolbar,
            text="Доступно: 11 | Выбрано: 0",
            font=("Arial", 10)
        )
        self.info_label.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            toolbar,
            text="Сбросить",
            command=self.reset_selection,
            bg="lightcoral",
            font=("Arial", 10)
        )
        self.reset_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_lists_panel(self):
        main_panel = tk.Frame(self.root)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        left_frame = tk.LabelFrame(main_panel, text="Доступные игроки", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.players_listbox = Listbox(
            left_frame,
            selectmode=MULTIPLE,
            font=("Arial", 11),
            height=15
        )

        scrollbar_left = tk.Scrollbar(left_frame, orient=tk.VERTICAL)
        scrollbar_left.config(command=self.players_listbox.yview)
        self.players_listbox.config(yscrollcommand=scrollbar_left.set)
        self.players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)
        buttons_frame = tk.Frame(main_panel)
        buttons_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        self.add_button = tk.Button(
            buttons_frame,
            text=">",
            command=self.add_selected,
            font=("Arial", 12, "bold"),
            width=3,
            height=2
        )
        self.add_button.pack(pady=10)
        self.add_all_button = tk.Button(
            buttons_frame,
            text=">>",
            command=self.add_all,
            font=("Arial", 12, "bold"),
            width=3,
            height=2
        )
        self.add_all_button.pack(pady=10)
        self.remove_button = tk.Button(
            buttons_frame,
            text="<",
            command=self.remove_selected,
            font=("Arial", 12, "bold"),
            width=3,
            height=2
        )
        self.remove_button.pack(pady=10)
        self.remove_all_button = tk.Button(
            buttons_frame,
            text="<<",
            command=self.remove_all,
            font=("Arial", 12, "bold"),
            width=3,
            height=2
        )
        self.remove_all_button.pack(pady=10)
        right_frame = tk.LabelFrame(main_panel, text="Выбранные игроки", padx=10, pady=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.selected_listbox = Listbox(
            right_frame,
            selectmode=MULTIPLE,
            font=("Arial", 11),
            height=15
        )

        scrollbar_right = tk.Scrollbar(right_frame, orient=tk.VERTICAL)
        scrollbar_right.config(command=self.selected_listbox.yview)
        self.selected_listbox.config(yscrollcommand=scrollbar_right.set)
        self.selected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)

    def bind_events(self):
        self.players_listbox.bind("<Double-Button-1>", lambda e: self.add_selected())
        self.selected_listbox.bind("<Double-Button-1>", lambda e: self.remove_selected())
        self.players_listbox.bind("<<ListboxSelect>>", self.update_info)
        self.selected_listbox.bind("<<ListboxSelect>>", self.update_info)

    def populate_players_list(self):
        self.players_listbox.delete(0, END)
        for player in sorted(self.all_players):
            self.players_listbox.insert(END, player)

    def add_selected(self):
        selected_indices = self.players_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Внимание", "Выберите игроков для добавления!")
            return

        selected_players = [self.players_listbox.get(i) for i in selected_indices]

        for player in selected_players:
            self.selected_listbox.insert(END, player)

        for i in reversed(selected_indices):
            self.players_listbox.delete(i)

        self.update_info()

    def add_all(self):
        if self.players_listbox.size() == 0:
            messagebox.showinfo("Информация", "Нет доступных игроков для добавления")
            return

        all_players = self.players_listbox.get(0, END)
        for player in all_players:
            self.selected_listbox.insert(END, player)

        self.players_listbox.delete(0, END)

        self.update_info()

    def remove_selected(self):
        selected_indices = self.selected_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Внимание", "Выберите игроков для удаления!")
            return

        selected_players = [self.selected_listbox.get(i) for i in selected_indices]

        for player in selected_players:
            self.players_listbox.insert(END, player)

        items = list(self.players_listbox.get(0, END))
        items.sort()
        self.players_listbox.delete(0, END)
        for item in items:
            self.players_listbox.insert(END, item)

        for i in reversed(selected_indices):
            self.selected_listbox.delete(i)

        self.update_info()

    def remove_all(self):
        if self.selected_listbox.size() == 0:
            messagebox.showinfo("Информация", "Нет выбранных игроков")
            return

        all_players = self.selected_listbox.get(0, END)
        for player in all_players:
            self.players_listbox.insert(END, player)

        items = list(self.players_listbox.get(0, END))
        items.sort()
        self.players_listbox.delete(0, END)
        for item in items:
            self.players_listbox.insert(END, item)

        self.selected_listbox.delete(0, END)
        self.update_info()

    def reset_selection(self):
        self.players_listbox.delete(0, END)
        self.selected_listbox.delete(0, END)
        self.populate_players_list()

        self.update_info()
        messagebox.showinfo("Сброс", "Все выборы сброшены!")

    def update_info(self, event=None):
        total_players = self.players_listbox.size()
        selected_players = self.selected_listbox.size()

        self.info_label.config(
            text=f"Доступно: {total_players} | Выбрано: {selected_players}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerSelectorApp(root)
    root.mainloop()
