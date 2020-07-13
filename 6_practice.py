from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title("Image Combine Practice")

# 파일 프레임
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

file_add_btn = Button(file_frame, text="파일 추가", padx=5, pady=5)
file_add_btn.pack(side="left")

file_del_btn = Button(file_frame, text="파일 삭제", padx=5, pady=5)
file_del_btn.pack(side="right")

# 리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 저장 경로 프레임
save_frame = Frame(root)
save_frame.pack(fill="x", padx=5, pady=5)

save_file = Entry(save_frame)
save_file.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=3)

save_file_btn = Button(save_frame, text="찾아보기", padx=5, pady=5)
save_file_btn.pack(side="right")

# 옵션 프레임
option_frame = LabelFrame(root, text="옵션")
option_frame.pack(padx=5, pady=5, ipady=5)

# 가로 옵션
label_width = Label(option_frame, text="가로 넓이", width=8)
label_width.pack(side="left", padx=5, pady=5)

option_width = ["원본유지", "1024", "800", "600"]
cmb_width = ttk.Combobox(option_frame, state="readonly", values=option_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

# 간격 옵션
label_space = Label(option_frame, text="간격", width=5)
label_space.pack(side="left", padx=5, pady=5)

option_space = ["없음", "좁게", "보통", "넓게"]
cmb_space = ttk.Combobox(option_frame, state="readonly", values=option_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

# 파일 포맷 옵션
label_width = Label(option_frame, text="파일 포맷", width=8)
label_width.pack(side="left", padx=5, pady=5)

option_format = ["png", "jpg", "bmp"]
cmb_format = ttk.Combobox(option_frame, state="readonly", values=option_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

# 진행 상황 프레임
progress_frame = LabelFrame(root, text="진행상황")
progress_frame.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress = ttk.Progressbar(progress_frame, maximum=100, variable=p_var)
progress.pack(fill="x", padx=5, pady=5)

# 시작 / 닫기 버튼
end_button = Button(root, text="닫기", width=12, command=root.quit)
end_button.pack(side="right", padx=5, pady=5)

start_button = Button(root, text="시작", width=12)
start_button.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()