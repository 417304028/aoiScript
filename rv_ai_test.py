import tkinter as tk
from tkinter import ttk, messagebox
import os
from scripts.rv import rv_ai_test
from utils import setup_logger

def submit():
    train_eval_paths = [path.strip() for path in entry_train_eval_path.get().split(';')]  # 支持多个由;分隔开的路径，并去除每个路径前后的空白符
    result_path = entry_result_path.get().strip()  # 去除路径前后的空白符
    mode = mode_var.get()
    if not os.path.exists(result_path):
        root.attributes('-topmost', True)
        messagebox.showerror("错误", "结果路径不存在，请重新输入！", parent=root)
        root.attributes('-topmost', False)
        return
    if mode == "正常":
        status, train_statuses = rv_ai_test(train_eval_paths, result_path, "normal")
    elif mode == "存在good/ng":
        status, train_statuses = rv_ai_test(train_eval_paths, result_path, "good_ng")
    
    if not train_statuses:
        root.attributes('-topmost', True)
        messagebox.showerror("错误", "train_statuses 为空，请检查脚本运行情况", parent=root)
        root.attributes('-topmost', False)
        return
    
    update_train_paths_status(train_statuses)
    
    root.attributes('-topmost', True)
    if status == 0:
        messagebox.showinfo("成功", "程序运行完毕，生成文档在结果文件夹下script_log文件夹内", parent=root)
    else:
        messagebox.showerror("错误", "程序运行失败，请查看日志", parent=root)
    root.attributes('-topmost', False)
    root.update()

def update_train_paths_status(train_statuses):
    for widget in train_paths_frame.winfo_children():
        widget.destroy()
    
    for train_path, status in train_statuses:
        color = get_status_color(status)
        label = tk.Label(train_paths_frame_inner, text=train_path, fg=color, cursor="hand2")
        label.pack(anchor='w', padx=5, pady=2)
        label.bind("<Button-1>", lambda e, path=train_path: (root.clipboard_clear(), root.clipboard_append(path), root.update(), root.event_generate('<Control-c>'), show_copied_message()))

def get_status_color(status):
    status_colors = {
        "训练完成": "green",
        "训练失败": "red",
        "待训练": "yellow"
    }
    return status_colors.get(status, "black")

def show_copied_message():
    copied_label = tk.Label(root, text="已复制", fg="blue")
    copied_label.place(relx=0.5, rely=0.5, anchor='center')
    root.after(3000, copied_label.destroy)

def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")  # 删除所有文本
        entry.config(fg='black')

def on_focusout(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')

if __name__ == '__main__':
    setup_logger()
    
    root = tk.Tk()
    root.title("路径输入界面")

    window_width = 600
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    left_frame = tk.Frame(root, width=50)
    left_frame.pack(side='left', fill='both', expand=True, padx=20)

    right_frame = tk.Frame(root)
    right_frame.pack(side='right', fill='both', expand=True)

    tk.Label(left_frame, text="输入总路径(包含train,test文件夹)").pack(anchor='w', pady=(0, 5))
    entry_train_eval_path = tk.Entry(left_frame, fg='grey')
    default_text = "可以输入多个路径，以;分隔开"
    entry_train_eval_path.insert(0, default_text)
    entry_train_eval_path.bind('<FocusIn>', lambda event: on_entry_click(event, entry_train_eval_path, default_text))
    entry_train_eval_path.bind('<FocusOut>', lambda event: on_focusout(event, entry_train_eval_path, default_text))
    entry_train_eval_path.pack(fill='x', pady=(0, 10))

    tk.Label(left_frame, text="输入结果路径（含定位图片及输出数据文档）").pack(anchor='w', pady=(0, 5))
    entry_result_path = tk.Entry(left_frame)
    entry_result_path.pack(fill='x', pady=(0, 10))

    tk.Label(left_frame, text="选择模式：").pack(anchor='w', pady=(0, 5))
    mode_var = tk.StringVar(left_frame)
    mode_var.set("正常")
    mode_options = ["正常", "存在good/ng"]
    mode_combobox = ttk.Combobox(left_frame, textvariable=mode_var, values=mode_options, state="readonly")
    mode_combobox.pack(fill='x', pady=(0, 10))

    submit_button = tk.Button(left_frame, text="执行脚本", command=submit)
    submit_button.pack(pady=(10, 20))

    tk.Label(left_frame, text="Tips：总路径为空，结果路径非空，则根据csv获取图片，生成结果在pyd目录下", wraplength=280).pack(anchor='w', pady=(0, 10))

    tk.Label(right_frame, text="训练路径及运行状态：").pack(anchor='w')
    
    train_paths_frame = tk.Canvas(right_frame)
    train_paths_frame.pack(side='left', fill='both', expand=True)

    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=train_paths_frame.yview)
    scrollbar.pack(side='right', fill='y')

    train_paths_frame.configure(yscrollcommand=scrollbar.set)
    train_paths_frame.bind('<Configure>', lambda e: train_paths_frame.configure(scrollregion=train_paths_frame.bbox("all")))

    train_paths_frame_inner = tk.Frame(train_paths_frame)
    train_paths_frame.create_window((0, 0), window=train_paths_frame_inner, anchor='nw')

    root.mainloop()
