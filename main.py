import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, Listbox, Scrollbar, Frame
import subprocess
import webbrowser

# Функция для поиска файлов по типу
def search_files_by_type(file_type):
    results = []
    home_directory = os.path.expanduser("~")  # Получаем домашнюю директорию
    extensions = {
        "игры": [".exe", ".bat", ".sh", ".game"],  # Расширения для игр
        "рабочие приложения": [".exe", ".msi", ".app"],  # Расширения для рабочих приложений
        "изображения": [".jpg", ".jpeg", ".png", ".gif"],  # Расширения для изображений
        "видео": [".mp4", ".avi", ".mov"],  # Расширения для видео
    }

    try:
        for root, dirs, files in os.walk(home_directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions.get(file_type, [])):
                    results.append(os.path.join(root, file))  # Полный путь к файлу
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при поиске файлов: {e}")
    return results

# Функция для выполнения команды
def execute_command(command):
    try:
        if command.lower() == "выключить компьютер":
            subprocess.call(["shutdown", "/s", "/t", "1"])  # Выключение компьютера
            return "Компьютер выключается..."
        else:
            result = os.popen(command).read()
            return result if result else "Команда выполнена, но нет вывода."
    except Exception as e:
        return str(e)

# Обработка ввода пользователя
def handle_input():
    user_input = entry.get().strip().lower()
    results = []

    if "найти" in user_input:
        if "игры" in user_input:
            results = search_files_by_type("игры")
        elif "рабочие приложения" in user_input or "приложения" in user_input:
            results = search_files_by_type("рабочие приложения")
        elif "изображения" in user_input:
            results = search_files_by_type("изображения")
        elif "видео" in user_input:
            results = search_files_by_type("видео")
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Неизвестный запрос.")
            return
        
        # Очистка списка и добавление результатов
        listbox.delete(0, tk.END)
        if results:
            for item in results:
                listbox.insert(tk.END, item)
        else:
            listbox.insert(tk.END, "Файлы не найдены.")
    elif "открой" in user_input:
        selected_file = listbox.curselection()
        if selected_file:
            file_path = listbox.get(selected_file)
            os.startfile(file_path)  # Открытие файла
        else:
            messagebox.showwarning("Предупреждение", "Сначала выберите файл.")
    elif "поиск" in user_input:
        query = user_input.replace("поиск", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")

# Создание простого интерфейса
root = tk.Tk()
root.title("ИИ Ассистент")
root.geometry("600x400")  # Установка размера окна

# Инструкции
instructions = tk.Label(root, text="Обращайтесь к ассистенту: например, 'найти игры' или 'выключить компьютер'")
instructions.pack(pady=10)

# Подсказки
hints = tk.Label(root, text="Подсказки:\n"
                             "- Найти игры\n""- Найти рабочие приложения\n"
                             "- Найти изображения\n"
                             "- Найти видео\n"
                             "- Откройте файл\n"
                             "- Поиск в интернете", justify=tk.LEFT)
hints.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

button = tk.Button(root, text="Отправить", command=handle_input)
button.pack(pady=5)

# Создание фрейма для списка файлов
frame = Frame(root)
frame.pack(pady=10)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = Listbox(frame, width=70, height=10, yscrollcommand=scrollbar.set)
listbox.pack()
scrollbar.config(command=listbox.yview)

# Поле для отображения результатов
output_text = scrolledtext.ScrolledText(root, width=70, height=5)
output_text.pack(pady=10)

root.mainloop()