import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog # 파일 선택 / 삭제 창을 사용하기 위해
import tkinter.messagebox as msgbox # messagebox를 사용하기 위해
from PIL import Image

root = Tk()
root.title("Image Combine")

# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요",  # askopenfilenames : 사용자에게 오픈할 파일들을 선택할 수 있도록
        filetypes=(("PNG 파일", "*.png"), ("모든 파일", "*.*")),  # "PNG 파일", "*.png" : 모든 .png 형식을 가진 이미지를 보여주는 것
        initialdir = "C:/")  # initialdir : 최초에 띄어줄 디렉토리 명시
        # r"C:/Users/SeungJun/Desktop" 처음에 r을 붙인 후 경로를 지정해주면 경로 그대로 사용하겠다는 의미

    # 사용자가 선택한 파일 목록
    for file in files:
        list_file.insert(END, file)  # file을 넣으면 file이 있는 경로를 나타내줌

def del_file():
    # 0번째 인덱스 부터 삭제할 경우 뒤에 있는 인덱스가 바뀌기 때문에 다른 파일이 삭제 될수 있다.
    # 따라서 뒤에서부터 삭제를 해주어야 한다.

    for index in reversed(list_file.curselection()): # reversed : 거꾸로 반환(실제 값에는 영향x) / reverse : 실제 값에 영향을 끼친다.
        list_file.delete(index)


# 저장 경로(폴더)
def browsw_dest_path():
    folder_selected = filedialog.askdirectory() # askdirectory : 폴더 선택하는 창
    if folder_selected == '':  # 사용자가 취소를 누를 때
        return

    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# 이미지 통합 작업
def merge_image():
    # print("가로 넓이 : ", cmb_width.get())
    # print("간격 : ", cmb_space.get())
    # print("포맷 : ", cmb_format.get())

    # 가로넓이
    img_width = cmb_width.get()
    if img_width == "원본유지":
        img_width = -1 # -1일때는 원본 기준으로 통합
    else:
        img_width = int(img_width)

    # 간격
    img_space = cmb_space.get()
    if img_space == "좁게":
        img_space = 30
    elif img_space == "보통":
        img_space = 60
    elif img_space == "넓게":
        img_space = 90
    else:
        img_space = 0

    # 포맷
    img_format = cmb_format.get().lower() # lower() : 소문자로 변경해주는 메소드


    # print(list_file.get(0, END)) # 모든 파일 목록을 가지고 오기
    images = [Image.open(x) for x in list_file.get(0, END)]

    # 이미지 사이즈 리스트에 넣어서 하나씩 처리
    image_sizes = [] # (width1, height1), (width2, height2), ....
    if img_width > -1:
        image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
    else:
        image_sizes = [(x.size[0], x.size[1]) for x in images] # 원본사이즈 사용

    # size -> size[0] : width, size[1] : height
    # widths = [x.size[0] for x in images]
    # heights = [x.size[1] for x in images]

    # 위의 코드와 동일
    widths, heights = zip(*(image_sizes))

    # max_width : max(widths) widths중에 max값을 찾아 대입 / total_height : sum(heights) heights값을 모두 더한 값을 대입
    max_width, total_height = max(widths), sum(heights)

    if img_space > 0: # 이미지 간격 옵션 적용
        total_height += ((img_space * len(images) - 1))

    result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255)) # new : 새로 만들어주는 것 (max_width, total_height)크기만큼 하얀색으로 생성
    y_offest = 0 # 이미지를 붙일 때 순서

    for idx, img in enumerate(images): # enumerate : images를 열거하여 idx, img 값에 대입
        # width가 원본이 아닐 경우 이미지 크기 조절
        if img_width > -1:
            img = img.resize(image_sizes[idx]) # resize() : 크기 변경 메소드

        result_img.paste(img, (0, y_offest)) # paste(img, (0, y_offset)) : 붙여넣기(img를 (0, y_offset)위치에)
        y_offest += (img.size[1] + img_space) # height 값 + 사용가자 지정한 간격 만큼 더해줌

        progress = (idx + 1) / len(images) * 100 # 실제 퍼센트 정보를 계산
        p_var.set(progress)
        progress_bar.update()


    # 포맷 옵션 처리
    file_name = "SeungJun Images." + img_format
    dest_path = os.path.join(txt_dest_path.get(), file_name) # dest_path에 txt_dest_path를 얻어와서 join
    result_img.save(dest_path) # save : dest_path에 저장
    msgbox.showinfo("알림", "작업이 완료되었습니다.")
# 시작
def start():
    # 각 옵션들 값 확인
    # print("가로 넓이 : ", cmb_width.get())
    # print("간격 : ", cmb_space.get())
    # print("포맷 : ", cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0: # 파일이 하나도 선택되지 않았다면
        msgbox.showwarning("경고", "이미지 파일을 추가하십시오.")
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0: # 파일이 하나도 선택되지 않았다면
        msgbox.showwarning("경고", "저장 경로를 추가하십시오.")
        return

    # 이미지 통합 작업
    merge_image()
# 파일 프레임 *(파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5) # fill="x" : x축 방향으로 채워짐

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일추가", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택삭제", command=del_file)
btn_del_file.pack(side="right")

# 리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 저장 경로 프레임
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # ipad : in padding : 안쪽 padding을 조절

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browsw_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(padx=5, pady=5, ipady=5)

# 가로 넓이 옵션
lbl_width = Label(frame_option, text="가로 넓이", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

opt_wdith = ["원본유지", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_wdith, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

# 간격 옵션
lbl_space = Label(frame_option, text="간격", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

opt_space = ["없음", "좁게", "보통", "넓게"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

# 파일 포맷 옵션
lbl_format = Label(frame_option, text="포맷", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

# 진행 상황 progressbar
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

# 오른쪽에 시작버튼을 먼저넣으면 그 다음에 닫기 버튼을 쌓아서 닫기 / 시작 순으로 버튼이 생성
# 따라서 닫기 버튼 먼저 생성
btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)


root.resizable(False, False)
root.mainloop()