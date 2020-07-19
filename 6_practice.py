from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image
import os
import tkinter.messagebox as msgbox

root = Tk()
root.title("Image Combine Practice")

# 파일 추가 지정
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", filetypes=(("PNG파일", "*.png"), ("모든파일", "*.*")), initialdir="C:/")
    for file in files:
        list_file.insert(END, file)

# 파일 삭제 지정
def del_file():
    for i in reversed(list_file.curselection()):
        list_file.delete(i)

# 저장 경로 지정
def save_dest_file():
    folder = filedialog.askdirectory()
    if folder == '':
        return

    save_file.delete(0, END)
    save_file.insert(0, folder)

# 옵션 지정
def merge_image():

    try:
        # 가로 넓이 지정
        img_width = cmb_width.get()
        if img_width == "원본유지":
            img_width = -1
        else:
            img_width = int(img_width)

        # 간격 지정
        img_space = cmb_space.get()
        if img_space == "없음":
            img_space = 0
        elif img_space == "좁게":
            img_space = 30
        elif img_space == "보통":
            img_space = 60
        elif img_space == "넓게":
            img_space = 90

        # 파일 포맷 지정
        img_format = cmb_format.get().lower()

        images = [Image.open(x) for x in list_file.get(0, END)]
        image_sizes = []
        if img_width > -1:
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        widths, heights = zip(*(image_sizes))

        max_width, total_height = max(widths), sum(heights)

        if img_space > 0:
            total_height +=((img_space * len(images) - 1))

        result_image = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0

        for idx, img in enumerate(images):
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_image.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space)

            _progress = (idx + 1) / len(images) * 100
            p_var.set(_progress)
            progress.update()

        # 파일 옵션 처리 완료
        file_name = "SeungJun Image Combine." + img_format
        dest_path = os.path.join(save_file.get(), file_name)
        result_image.save(dest_path)
        msgbox.showinfo("알림", "작업이 완료되었습니다")
    except Exception as err:
        msgbox.showerror("오류", err)


# 시작 지정
def start():
    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하십시오.")
        return

    # 저장 경로 확인
    if len(save_file.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 추가하십시오.")
        return

    # 이미지 통합 작업
    merge_image()

# 파일 프레임
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

file_add_btn = Button(file_frame, text="파일 추가", padx=5, pady=5, command=add_file)
file_add_btn.pack(side="left")

file_del_btn = Button(file_frame, text="파일 삭제", padx=5, pady=5, command=del_file)
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

save_file_btn = Button(save_frame, text="찾아보기", padx=5, pady=5, command=save_dest_file)
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

start_button = Button(root, text="시작", width=12, command=start)
start_button.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()