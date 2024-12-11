import sys
import os
import tkinter as tk
from tkinter import messagebox
from pypinyin import pinyin, Style

# 處理檔案路徑，支援開發模式和打包後的exe
def get_file_path(filename):
    if getattr(sys, 'frozen', False):  # 如果是打包後的exe
        # 取得臨時資料夾路徑
        return os.path.join(sys._MEIPASS, filename)
    else:
        # 開發模式下使用當前目錄
        return os.path.join(os.getcwd(), filename)

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("拼音和注音轉換器")

        # 設置根視窗的字體
        self.entry = tk.Entry(self.root, font=("標楷體", 18))  # 增大字體
        self.entry.grid(row=0, column=0, columnspan=3, pady=30, padx=30, sticky="nsew")

        self.selected_mode = tk.StringVar(value="拼音")  # 默認選擇拼音模式

        # 設定視窗擴展比例
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # 添加提交按鈕，並放大比例
        submit_button = tk.Button(self.root, text="提交", command=self.on_submit, font=("標楷體", 16))
        submit_button.grid(row=1, column=0, columnspan=3, pady=20)

        # 添加模式選擇按鈕，並放大比例
        pinyin_radio = tk.Radiobutton(self.root, text="拼音", variable=self.selected_mode, value="拼音", font=("標楷體", 16))
        zhuyin_radio = tk.Radiobutton(self.root, text="注音", variable=self.selected_mode, value="注音", font=("標楷體", 16))
        wubi_radio = tk.Radiobutton(self.root, text="無蝦米", variable=self.selected_mode, value="無蝦米", font=("標楷體", 16))

        pinyin_radio.grid(row=2, column=0, pady=10, sticky="nsew")
        zhuyin_radio.grid(row=2, column=1, pady=10, sticky="nsew")
        wubi_radio.grid(row=2, column=2, pady=10, sticky="nsew")

    def convert_to_zhuyin(self, text):
        zhuyin_list = pinyin(text, style=Style.BOPOMOFO)
        result = ''.join([item[0] for item in zhuyin_list])
        return result

    def convert_to_pinyin(self, text):
        pinyin_list = pinyin(text, style=Style.NORMAL)
        result = ' '.join([item[0] for item in pinyin_list])
        return result

    def convert_to_wubi(self, text):
        result = []
        word = len(text)  # 確定字數
        wubi_dict = {}  # 儲存字根對應表

        # 讀取無蝦米字根表
        try:
            wu_file_path = get_file_path('wu.txt')
            with open(wu_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(" ")
                    if len(parts) == 2:
                        wubi_dict[parts[1]] = parts[0]  # 儲存字根與字的對應關係
            print("無蝦米字根表加載成功！")
        except FileNotFoundError:
            messagebox.showerror("錯誤", "未找到 wu.txt 檔案！")
            return ""
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取文件時出錯: {e}")
            return ""

        # 逐字處理
        for char in text:
            if char in wubi_dict:  # 如果字在字典中，添加字根
                result.append(wubi_dict[char] + " ")
            else:
                result.append(char)  # 如果字未找到字根，則直接顯示字符

        print(f"無蝦米轉換結果: {''.join(result)}")  # 打印無蝦米轉換結果
        return ''.join(result).strip()  # 返回最終的無蝦米字根結果

    def show_result(self, result_text):
        result_window = tk.Toplevel(self.root)
        result_window.title("翻譯結果")

        # 設定視窗最大化
        result_window.state("zoomed")

        # 使用Label顯示結果，防止字體被切割
        result_label = tk.Label(result_window, text=result_text, font=("標楷體", 24), justify="left", wraplength=result_window.winfo_screenwidth()-50)
        result_label.pack(pady=50, padx=50, fill="both", expand=True)

    def on_submit(self):
        input_text = self.entry.get()
        if self.selected_mode.get() == "注音":
            zhuyin_text = self.convert_to_zhuyin(input_text)
            self.show_result(zhuyin_text)
        elif self.selected_mode.get() == "拼音":
            pinyin_text = self.convert_to_pinyin(input_text)
            self.show_result(pinyin_text)
        elif self.selected_mode.get() == "無蝦米":
            wubi_text = self.convert_to_wubi(input_text)  # 保持原來的無蝦米轉換邏輯
            self.show_result(wubi_text)
        else:
            messagebox.showerror("錯誤", "請選擇轉換模式")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
