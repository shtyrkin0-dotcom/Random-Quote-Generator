"""
Random Quote Generator
Приложение для генерации случайных цитат с историей и фильтрацией
Автор: Мускалов Артур
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os
from datetime import datetime

class QuoteApp:
    """Главный класс приложения для генерации цитат"""
    
    # Предопределённые цитаты
    DEFAULT_QUOTES = [
        {"text": "Будь изменением, которое ты хочешь видеть в мире", "author": "Махатма Ганди", "theme": "мотивация"},
        {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы", "author": "Джон Леннон", "theme": "жизнь"},
        {"text": "Тьма не может изгнать тьму: только свет может это сделать", "author": "Мартин Лютер Кинг", "theme": "мудрость"},
        {"text": "Единственный способ делать великую работу - любить то, что ты делаешь", "author": "Стив Джобс", "theme": "работа"},
        {"text": "Не судите о моих успехах по моим неудачам", "author": "Нельсон Мандела", "theme": "мудрость"},
        {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью", "author": "Стив Джобс", "theme": "жизнь"},
        {"text": "Встань и иди, не бойся темноты", "author": "Конфуций", "theme": "мотивация"},
        {"text": "Знание - сила", "author": "Фрэнсис Бэкон", "theme": "образование"},
        {"text": "Сложно в учении - легко в бою", "author": "Александр Суворов", "theme": "образование"},
        {"text": "Делу время - потехе час", "author": "Царь Алексей Михайлович", "theme": "работа"},
    ]
    
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator - Мускалов Артур")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Файл для сохранения данных
        self.data_file = "quotes_data.json"
        
        # Загрузка данных
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
    def load_data(self):
        """Загрузка цитат и истории из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes = data.get('quotes', self.DEFAULT_QUOTES.copy())
                    self.history = data.get('history', [])
            except (json.JSONDecodeError, FileNotFoundError):
                self.quotes = self.DEFAULT_QUOTES.copy()
                self.history = []
        else:
            self.quotes = self.DEFAULT_QUOTES.copy()
            self.history = []
    
    def save_data(self):
        """Сохранение цитат и истории в JSON файл"""
        data = {
            'quotes': self.quotes,
            'history': self.history
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # ===== Верхняя панель: генерация цитаты =====
        generate_frame = ttk.LabelFrame(main_frame, text="Генерация цитаты", padding="10")
        generate_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.generate_btn = ttk.Button(generate_frame, text="🎲 Сгенерировать случайную цитату", 
                                       command=self.generate_quote)
        self.generate_btn.pack(fill=tk.X)
        
        # ===== Область отображения текущей цитаты =====
        quote_frame = ttk.LabelFrame(main_frame, text="Текущая цитата", padding="10")
        quote_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.quote_text = tk.Text(quote_frame, height=4, wrap=tk.WORD, font=("Arial", 11))
        self.quote_text.pack(fill=tk.BOTH, expand=True)
        
        # ===== Панель добавления новой цитаты =====
        add_frame = ttk.LabelFrame(main_frame, text="Добавить новую цитату", padding="10")
        add_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Поля ввода
        ttk.Label(add_frame, text="Текст цитаты:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.quote_entry = tk.Text(add_frame, height=3, width=50)
        self.quote_entry.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.author_entry = ttk.Entry(add_frame, width=47)
        self.author_entry.grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.theme_entry = ttk.Entry(add_frame, width=47)
        self.theme_entry.grid(row=2, column=1, pady=2, padx=5)
        
        self.add_btn = ttk.Button(add_frame, text="➕ Добавить цитату", command=self.add_quote)
        self.add_btn.grid(row=3, column=1, pady=10, sticky=tk.W)
        
        # ===== Панель фильтрации =====
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация истории", padding="10")
        filter_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, sticky=tk.W)
        self.author_filter = ttk.Entry(filter_frame, width=20)
        self.author_filter.grid(row=0, column=1, padx=5)
        self.author_filter.bind('<KeyRelease>', self.apply_filters)
        
        ttk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0, sticky=tk.W)
        self.theme_filter = ttk.Entry(filter_frame, width=20)
        self.theme_filter.grid(row=1, column=1, padx=5)
        self.theme_filter.bind('<KeyRelease>', self.apply_filters)
        
        self.clear_filter_btn = ttk.Button(filter_frame, text="Очистить фильтры", command=self.clear_filters)
        self.clear_filter_btn.grid(row=2, column=1, pady=5, sticky=tk.W)
        
        # ===== Панель истории =====
        history_frame = ttk.LabelFrame(main_frame, text="История цитат", padding="10")
        history_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Список истории
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, 
                                          height=12, font=("Arial", 9))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Кнопки управления историей
        history_buttons_frame = ttk.Frame(history_frame)
        history_buttons_frame.pack(side=tk.RIGHT, padx=5)
        
        self.clear_history_btn = ttk.Button(history_buttons_frame, text="Очистить историю", 
                                           command=self.clear_history)
        self.clear_history_btn.pack(pady=2)
        
        # Настройка весов
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Обновление отображения истории
        self.update_history_display()
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "Нет доступных цитат. Добавьте хотя бы одну.")
            return
        
        quote = random.choice(self.quotes)
        
        # Отображение цитаты
        display_text = f'"{quote["text"]}"\n\n— {quote["author"]} (Тема: {quote["theme"]})'
        self.quote_text.delete(1.0, tk.END)
        self.quote_text.insert(1.0, display_text)
        
        # Добавление в историю с временем
        history_entry = quote.copy()
        history_entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(history_entry)
        
        # Сохранение и обновление
        self.save_data()
        self.update_history_display()
    
    def add_quote(self):
        """Добавление новой цитаты с валидацией"""
        text = self.quote_entry.get(1.0, tk.END).strip()
        author = self.author_entry.get().strip()
        theme = self.theme_entry.get().strip()
        
        # Валидация ввода
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        if not theme:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
        
        # Добавление цитаты
        new_quote = {
            "text": text,
            "author": author,
            "theme": theme
        }
        self.quotes.append(new_quote)
        self.save_data()
        
        # Очистка полей
        self.quote_entry.delete(1.0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.theme_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")
    
    def apply_filters(self, event=None):
        """Применение фильтров к истории"""
        self.update_history_display()
    
    def clear_filters(self):
        """Очистка всех фильтров"""
        self.author_filter.delete(0, tk.END)
        self.theme_filter.delete(0, tk.END)
        self.update_history_display()
    
    def update_history_display(self):
        """Обновление отображения истории с учётом фильтров"""
        self.history_listbox.delete(0, tk.END)
        
        # Получение фильтров
        author_filter = self.author_filter.get().strip().lower()
        theme_filter = self.theme_filter.get().strip().lower()
        
        # Фильтрация истории
        filtered_history = self.history
        if author_filter:
            filtered_history = [h for h in filtered_history if author_filter in h['author'].lower()]
        if theme_filter:
            filtered_history = [h for h in filtered_history if theme_filter in h['theme'].lower()]
        
        # Отображение
        if not filtered_history:
            self.history_listbox.insert(tk.END, "Нет цитат в истории")
        else:
            for i, entry in enumerate(filtered_history, 1):
                display = f"{i}. {entry['text'][:50]}... — {entry['author']} [{entry['theme']}]"
                if 'timestamp' in entry:
                    display += f" ({entry['timestamp']})"
                self.history_listbox.insert(tk.END, display)
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_data()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()