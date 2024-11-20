import tkinter as tk
from tkinter import ttk  # 导入ttk模块
from tkinter import messagebox
import os
from scripts.rv import rv_ai_test
from utils import setup_logger

def submit():
    train_eval_path = entry_train_eval_path.get()
    result_path = entry_result_path.get()
    mode = mode_var.get()
    if not os.path.exists(train_eval_path):
        root.attributes('-topmost', True)  # 窗口置顶
        messagebox.showerror("错误", "训练评估路径不存在，请重新输入！", parent=root)
        root.attributes('-topmost', False)  # 恢复正常
        return
    if not os.path.exists(result_path):
        root.attributes('-topmost', True)  # 窗口置顶
        messagebox.showerror("错误", "结果路径不存在，请重新输入！", parent=root)
        root.attributes('-topmost', False)  # 恢复正常
        return
    if mode == "正常":
        status = rv_ai_test(train_eval_path, result_path, "normal")
    elif mode == "存在good/ng":
        status = rv_ai_test(train_eval_path, result_path, "good_ng")
    if status == 0:
        messagebox.showinfo("成功", "程序运行完毕，生成文档在结果文件夹下script_log文件夹内", parent=root)
        root.attributes('-topmost', True)  # 窗口置顶
        root.update()  # 确保UI更新
        root.attributes('-topmost', False)  # 恢复正常
    else:
        root.attributes('-topmost', True)  # 窗口置顶
        messagebox.showerror("错误", "程序运行失败，请查看日志", parent=root)
        root.attributes('-topmost', False)  # 恢复正常

if __name__ == '__main__':
    setup_logger()
    
    root = tk.Tk()
    root.title("路径输入界面")

    # 设置窗口大小并居中显示
    window_width = 300
    window_height = 250  # 增加窗口高度以容纳新下拉框
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    tk.Label(root, text="输入总路径(包含train,test文件夹)").pack(anchor='w')
    entry_train_eval_path = tk.Entry(root)
    entry_train_eval_path.pack(fill='x', padx=10)  # 填充整个可用宽度并设置左右内边距

    tk.Label(root, text="输入结果路径（含定位图片及输出数据文档）").pack(anchor='w')
    entry_result_path = tk.Entry(root)
    entry_result_path.pack(fill='x', padx=10)  # 填充整个可用宽度并设置左右内边距

    tk.Label(root, text="选择模式：").pack(anchor='w')
    mode_var = tk.StringVar(root)
    mode_var.set("正常")  # 默认值
    mode_options = ["正常", "存在good/ng"]
    mode_combobox = ttk.Combobox(root, textvariable=mode_var, values=mode_options, state="readonly")
    mode_combobox.pack(fill='x', padx=10)

    submit_button = tk.Button(root, text="执行", command=submit)
    submit_button.place(x=window_width-80, y=window_height-50)  # 调整按钮位置

    root.mainloop()