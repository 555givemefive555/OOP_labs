import tkinter as tk
from tkinter import ttk
import random
from abc import ABC, abstractmethod

class IGenerator(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass
    @abstractmethod
    def get_element(self, i: int, j: int, size: int) -> int:
        pass


class ZeroGenerator(IGenerator):
    def get_name(self) -> str:
        return "Нулевая"
    def get_element(self, i: int, j: int, size: int) -> int:
        return 0

class DiagonalGenerator(IGenerator):
    def get_name(self) -> str:
        return "Диагональная"

    def get_element(self, i: int, j: int, size: int) -> int:
        return random.randint(10, 99) if i == j else 0

class RandomGenerator(IGenerator):
    def get_name(self) -> str:
        return "Случайная"

    def get_element(self, i: int, j: int, size: int) -> int:
        return random.randint(0, 99)

class RandomDiagonalGenerator(IGenerator):
    def get_name(self) -> str:
        return "Две диагонали"

    def get_element(self, i: int, j: int, size: int) -> int:
        if i == j:
            return random.randint(1, 100)
        elif (size-1-i) == j:
            return random.randint(1, 100)
        else:
            return 0

class BorderRandomGenerator(IGenerator):
    def get_name(self) -> str:
        return "Случайные по краям"

    def get_element(self, i: int, j: int, size: int) -> int:
        if i == 0 or i == size - 1 or j == 0 or j == size - 1:
            return random.randint(10, 99)
        return 0

class Matrix:
    def __init__(self, size: int = 10):
        self.size = size
        self.contents = [[0] * size for _ in range(size)]
        self.generator = ZeroGenerator()
        self._listeners = []

    def set_generator(self, generator: IGenerator):
        self.generator = generator

    def update(self):
        for i in range(self.size):
            for j in range(self.size):
                self.contents[i][j] = self.generator.get_element(i, j, self.size)
        self._notify_listeners()

    def get_value(self, i: int, j: int) -> int:
        return self.contents[i][j]

    def get_size(self) -> int:
        return self.size

    def add_listener(self, listener):
        self._listeners.append(listener)

    def _notify_listeners(self):
        for listener in self._listeners:
            listener.matrix_updated(self)

class IMatrixListener(ABC):
    @abstractmethod
    def matrix_updated(self, matrix: Matrix):
        pass


class DisplayMatrixListener(IMatrixListener):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def matrix_updated(self, matrix: Matrix):
        text = ""
        for i in range(matrix.get_size()):
            for j in range(matrix.get_size()):
                text += f"{matrix.get_value(i, j):3d} "
            text += "\n"
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, text)


class CalculateMaxListener(IMatrixListener):
    def __init__(self, label_widget):
        self.label_widget = label_widget

    def matrix_updated(self, matrix: Matrix):
        max_val = matrix.get_value(0, 0)
        for i in range(matrix.get_size()):
            for j in range(matrix.get_size()):
                if matrix.get_value(i, j) > max_val:
                    max_val = matrix.get_value(i, j)
        self.label_widget.config(text=f"Максимум: {max_val}")


class CalculateMinListener(IMatrixListener):
    def __init__(self, label_widget):
        self.label_widget = label_widget

    def matrix_updated(self, matrix: Matrix):
        min_val = matrix.get_value(0, 0)
        for i in range(matrix.get_size()):
            for j in range(matrix.get_size()):
                if matrix.get_value(i, j) < min_val:
                    min_val = matrix.get_value(i, j)
        self.label_widget.config(text=f"Минимум: {min_val}")


class CalculateSumListener(IMatrixListener):
    def __init__(self, label_widget):
        self.label_widget = label_widget

    def matrix_updated(self, matrix: Matrix):
        total = 0
        for i in range(matrix.get_size()):
            for j in range(matrix.get_size()):
                total += matrix.get_value(i, j)
        self.label_widget.config(text=f"Сумма: {total}")

class CalculateAverageListener(IMatrixListener):
    def __init__(self, label_widget):
        self.label_widget = label_widget

    def matrix_updated(self, matrix: Matrix):
        total = 0
        count = matrix.get_size() ** 2

        for i in range(matrix.get_size()):
            for j in range(matrix.get_size()):
                total += matrix.get_value(i, j)

        average = total / count if count > 0 else 0
        self.label_widget.config(text=f"Среднее: {average:.2f}")

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Демонстрация паттернов проектирования")
        self.root.geometry("600x500")

        self.matrix = Matrix(size=8)

        self.generators = [
            ZeroGenerator(),
            DiagonalGenerator(),
            RandomGenerator(),
            RandomDiagonalGenerator(),
            BorderRandomGenerator()
        ]

        self.setup_ui()
        self.setup_listeners()

        self.combo_generators.set(self.generators[0].get_name())
        self.on_generator_changed()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(top_frame, text="Тип матрицы:").grid(row=0, column=0, padx=(0, 10))

        self.combo_generators = ttk.Combobox(top_frame,
                                             values=[g.get_name() for g in self.generators],
                                             state="readonly",
                                             width=25)
        self.combo_generators.grid(row=0, column=1, padx=(0, 20))
        self.combo_generators.bind("<<ComboboxSelected>>", lambda e: self.on_generator_changed())

        self.btn_update = ttk.Button(top_frame, text="Обновить матрицу",
                                     command=self.update_matrix)
        self.btn_update.grid(row=0, column=2, padx=10)

        left_frame = ttk.LabelFrame(main_frame, text="Матрица", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        text_frame = ttk.Frame(left_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar_y = ttk.Scrollbar(text_frame)
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))

        scrollbar_x = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.matrix_text = tk.Text(text_frame,
                                   width=35,
                                   height=15,
                                   wrap=tk.NONE,
                                   yscrollcommand=scrollbar_y.set,
                                   xscrollcommand=scrollbar_x.set)
        self.matrix_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar_y.config(command=self.matrix_text.yview)
        scrollbar_x.config(command=self.matrix_text.xview)

        right_frame = ttk.LabelFrame(main_frame, text="Характеристики", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.labels = {}
        characteristics = [
            ("Максимум", "max"),
            ("Минимум", "min"),
            ("Сумма", "sum"),
            ("Среднее", "average")
        ]

        for i, (text, key) in enumerate(characteristics):
            ttk.Label(right_frame, text=text + ":", font=("Arial", 10)).grid(
                row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))

            self.labels[key] = ttk.Label(right_frame, text="0",
                                         font=("Arial", 10, "bold"),
                                         foreground="blue")
            self.labels[key].grid(row=i, column=1, sticky=tk.W, pady=8)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

    def setup_listeners(self):
        self.listeners = [
            DisplayMatrixListener(self.matrix_text),
            CalculateMaxListener(self.labels["max"]),
            CalculateMinListener(self.labels["min"]),
            CalculateSumListener(self.labels["sum"]),
            CalculateAverageListener(self.labels["average"])
        ]

        for listener in self.listeners:
            self.matrix.add_listener(listener)

    def on_generator_changed(self):
        selected_name = self.combo_generators.get()
        for generator in self.generators:
            if generator.get_name() == selected_name:
                self.matrix.set_generator(generator)
                break

    def update_matrix(self):
        self.matrix.update()

def main():
    root = tk.Tk()
    app = MatrixApp(root)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
