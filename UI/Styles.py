import tkinter as tk
from tkinter import ttk


class Colors:
    BG = "#0f1318"
    PANEL = "#181d24"
    CARD = "#212731"
    BORDER = "#2f3745"
    TEXT = "#a0aab8"
    WHITE = "#ffffff"
    CYAN = "#00e5ff"
    GREEN = "#00e676"
    AMBER = "#ffc400"
    RED = "#ff1744"
    BLUE = "#0288d1"
    PURPLE = "#7b1fa2"
    ORANGE = "#f57c00"
    DARK = "#101419"


def setup_styles(root):
    style = ttk.Style(root)
    style.theme_use("default")

    style.configure(
        "Rigel.Treeview",
        background=Colors.DARK,
        fieldbackground=Colors.DARK,
        foreground=Colors.WHITE,
        rowheight=27,
        borderwidth=0,
        font=("Segoe UI", 9),
    )
    style.configure(
        "Rigel.Treeview.Heading",
        background=Colors.PANEL,
        foreground=Colors.CYAN,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
    )
    style.map(
        "Rigel.Treeview",
        background=[("selected", "#263746")],
        foreground=[("selected", Colors.WHITE)],
    )


def button(parent, text, command, bg, fg=Colors.WHITE, **kwargs):
    options = dict(
        font=("Segoe UI", 9, "bold"),
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        bd=0,
        relief="flat",
        cursor="hand2",
        pady=7,
    )
    options.update(kwargs)
    return tk.Button(parent, text=text, command=command, **options)
