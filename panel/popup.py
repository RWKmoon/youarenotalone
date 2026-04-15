import tkinter as tk
import threading
import time
import queue


_queue = queue.Queue()

_notifications = []

def _process_queue():
    while not _queue.empty():
        func, args = _queue.get()
        func(*args)

    _root.after(50, _process_queue)

_root = None

def init_notifier():
    global _root

    if _root is None:
        _root = tk.Tk()
        _root.withdraw()
        _process_queue()

def _get_root():
    global _root
    if _root is None:
        _root = tk.Tk()
        _root.withdraw()
    return _root

def _ease_out(t):
    return 1 - (1 - t) ** 3

def _play_sound():
    try:
        import winsound
        winsound.MessageBeep()
    except:
        pass

def _show_toast(message, icon, color, duration, sound):
    root = _root

    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)

    # 🔥 transparência geral
    toast.attributes("-alpha", 0.92)

    # fundo estilo Windows 11
    bg_color = "#000000"

    container = tk.Frame(toast, bg=bg_color, bd=0, highlightthickness=0)
    container.pack(fill="both", expand=True)

    # borda suave (fake)
    border = tk.Frame(container, bg="#000000")
    border.pack(fill="both", expand=True, padx=1, pady=1)

    content = tk.Frame(border, bg=bg_color)
    content.pack(fill="both", expand=True, padx=12, pady=10)

    icon_label = tk.Label(
        content, text=icon, fg=color, bg=bg_color,
        font=("Segoe UI", 14, "bold")
    )
    icon_label.pack(side="left", padx=(0, 10))

    text = tk.Label(
        content, text=message, fg="#eaeaea",
        bg=bg_color, font=("Segoe UI", 10)
    )
    text.pack(side="left")

    # barra de progresso moderna
    progress_bg = tk.Frame(border, bg="#000000", height=3)
    progress_bg.pack(fill="x", side="bottom")

    progress = tk.Frame(progress_bg, bg=color, height=3)
    progress.pack(fill="y", side="left")

    toast.update_idletasks()

    width = toast.winfo_width()
    height = toast.winfo_height()
    screen_width = toast.winfo_screenwidth()
    screen_height = toast.winfo_screenheight()

    offset = len(_notifications) * (height + 12)
    y = screen_height - height - 40 - offset

    start_x = screen_width
    target_x = screen_width - width - 12

    toast.geometry(f"{width}x{height}+{start_x}+{y}")
    _notifications.append(toast)

    if sound:
        _play_sound()

    # 🎞️ animação suave
    duration_anim = 0.3
    fps = 60
    steps = int(duration_anim * fps)

    def animate_in(step=0):
        if step <= steps:
            t = _ease_out(step / steps)
            x = int(start_x + (target_x - start_x) * t)
            toast.geometry(f"+{x}+{y}")
            toast.after(int(1000 / fps), animate_in, step + 1)

    animate_in()

    # ⏳ progresso
    start_time = time.time()

    def update_progress():
        elapsed = time.time() - start_time
        total = duration / 1000
        remaining = max(0, total - elapsed)

        w = int((remaining / total) * width)
        progress.config(width=w)

        if remaining > 0:
            toast.after(30, update_progress)

    update_progress()

    # saída
    def destroy():
        def animate_out(step=0):
            if step <= steps:
                t = _ease_out(step / steps)
                x = int(target_x + (screen_width - target_x) * t)
                toast.geometry(f"+{x}+{y}")
                toast.after(int(1000 / fps), animate_out, step + 1)
            else:
                toast.destroy()
                _notifications.remove(toast)
        animate_out()

    toast.after(duration, destroy)


def _thread_toast(message, icon, color, duration, sound):
    threading.Thread(
        target=_show_toast,
        args=(message, icon, color, duration, sound),
        daemon=True
    ).start()


# 🔥 API limpa

def notify_success(msg="Sucesso!", duration=3000, sound=True):
    _queue.put((_show_toast, (msg, "✔", "#22c55e", duration, sound)))


def notify_error(msg="Erro!", duration=3000, sound=True):
    _queue.put((_show_toast, (msg, "✖", "#ef4444", duration, sound)))


def notify_warning(msg="Aviso!", duration=3000, sound=True):
    _queue.put((_show_toast, (msg, "⚠", "#facc15", duration, sound)))
    
def test():
    notify_success("Operação concluída com sucesso!")
    notify_error("Ocorreu um erro inesperado.")
    notify_warning("Atenção: Verifique os dados inseridos.")

init_notifier()