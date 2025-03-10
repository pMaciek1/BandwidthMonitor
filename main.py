from tkinter import IntVar, Radiobutton, ttk
import psutil
import datetime
import tkinter


last_upload = 0
last_download = 0
last_total = 0

start_upload = psutil.net_io_counters().bytes_sent
start_download = psutil.net_io_counters().bytes_recv
start_total = start_upload + start_download

wdw = tkinter.Tk()
wdw.title('Bandwidth Monitor')
wdw.geometry('600x400')
wdw.resizable(False,False)

style = ttk.Style()
style.theme_use('clam')
style.configure('blue.Horizontal.TProgressbar', background='lightblue', troughcolor='lightgray', bordercolor='darkblue')
style.configure('red.Horizontal.TProgressbar', background='red', troughcolor='lightgray', bordercolor='darkred')

scale = IntVar()
scale.set(1)
Radiobutton(wdw, text='MB', variable=scale, value=1, font=('Helvatica', 20), ).place(x=240, y=1)
Radiobutton(wdw, text='GB', variable=scale, value=2, font=('Helvatica', 20)).place(x=320, y=1)
p_upload = ttk.Progressbar(wdw, orient='horizontal', length=300, mode='determinate', takefocus=True, maximum=100, style='blue.Horizontal.TProgressbar')
p_upload.place(x=275, y=235)
p_download = ttk.Progressbar(wdw, orient='horizontal', length=300, mode='determinate', takefocus=True, maximum=100, style='red.Horizontal.TProgressbar')
p_download.place(x=275, y=273)


current_time = datetime.datetime.now().strftime('%H:%M')
label1 = tkinter.Label(text=f'Since {current_time}:')
label1.grid(row=0, column=0, columnspan=2)
label_from_start_upload_header = tkinter.Label(text='Upload:')
label_from_start_upload_header.grid(row=1, column=0)
label_from_start_download_header = tkinter.Label(text='Download:')
label_from_start_download_header.grid(row=2, column=0)
label_from_start_total_header = tkinter.Label(text='Total:')
label_from_start_total_header.grid(row=3, column=0)

label_from_start_upload = tkinter.Label(text='0')
label_from_start_upload.grid(row=1, column=1)
label_from_start_download = tkinter.Label(text='0')
label_from_start_download.grid(row=2, column=1)
label_from_start_total = tkinter.Label(text='0')
label_from_start_total.grid(row=3, column=1)

empty_label = tkinter.Label()
empty_label.grid(row=4, column=0, columnspan=2)

label2 = tkinter.Label(text=f'Per second:')
label2.grid(row=5, column=0, columnspan=2)
label_now_upload_header = tkinter.Label(text='Upload:')
label_now_upload_header.grid(row=6, column=0)
label_now_download_header = tkinter.Label(text='Download:')
label_now_download_header.grid(row=7, column=0)
label_now_total_header = tkinter.Label(text='Total:')
label_now_total_header.grid(row=8, column=0)

label_now_upload = tkinter.Label(text='0')
label_now_upload.grid(row=6, column=1)
label_now_download = tkinter.Label(text='0')
label_now_download.grid(row=7, column=1)
label_now_total = tkinter.Label(text='0')
label_now_total.grid(row=8, column=1)

for wid in wdw.winfo_children():
    if isinstance(wid, tkinter.Label):
        if wid.grid_info()['column'] == 0:
            wid.config(font=('Helvatica', 20))
        elif wid.grid_info()['column'] == 1:
            wid.config(font=('Helvatica', 20, 'bold'))
flag = False

def data_check():
    global last_upload, last_download, last_total, flag
    upload = psutil.net_io_counters().bytes_sent
    download = psutil.net_io_counters().bytes_recv
    total = upload + download

    from_start_upload = upload - start_upload
    from_start_download = download - start_download
    from_start_total = total - start_total

    
    if flag:
        new_upload = upload - last_upload
        new_download = download - last_download
        new_total = total - last_total
    elif not flag:
        new_upload = 0
        new_download = 0
        new_total = 0
        flag = True

    
    
    
    #print(f'Data from start: uploaded: {from_start_upload}, downloaded: {from_start_download}, total: {from_start_total}')
    #print(f'Data from last second: uploaded: {new_upload}, downloaded: {new_download}, total: {new_total} (Bytes)')
    if scale.get() == 1:
        mb_from_start_upload = from_start_upload / 1024 / 1024
        mb_from_start_download = from_start_download / 1024 / 1024
        mb_from_start_total = from_start_total / 1024 / 1024
        label_from_start_upload['text'] = f'{mb_from_start_upload:.2f} MB'
        label_from_start_download['text'] = f'{mb_from_start_download:.2f} MB'
        label_from_start_total['text'] = f'{mb_from_start_total:.2f} MB'


    elif scale.get() == 2:
        gb_from_start_upload = from_start_upload / 1024 / 1024 / 1024
        gb_from_start_download = from_start_download / 1024 / 1024 / 1024
        gb_from_start_total = from_start_total / 1024 / 1024 / 1024
        label_from_start_upload['text'] = f'{gb_from_start_upload:.2f} GB'
        label_from_start_download['text'] = f'{gb_from_start_download:.2f} GB'
        label_from_start_total['text'] = f'{gb_from_start_total:.2f} GB'

    mb_new_upload = new_upload / 1024 / 1024
    mb_new_download = new_download / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024
    label_now_upload['text'] = f'{mb_new_upload:.2f} MB'
    p_upload['value'] = mb_new_upload
    label_now_download['text'] = f'{mb_new_download:.2f} MB'
    p_download['value'] = mb_new_download
    label_now_total['text'] = f'{mb_new_total:.2f} MB'

    last_upload = upload
    last_download = download
    last_total = total

    wdw.after(1000, data_check)

wdw.after(1000, data_check)
wdw.mainloop()