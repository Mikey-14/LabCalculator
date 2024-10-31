# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 12:41:26 2024

@author: mikey
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import messagebox
from calculator import concentration_cal
from calculator import solid_cal
from calculator import plasmid_cal
main = tk.Tk()
main.geometry("870x800")
def on_closing():
    main.quit()
    main.destroy()
def func1_show_result():
    initcon_input = initcon_entry.get()
    initvol_input = initvol_entry.get()
    finalvol_input = finalvol_entry.get()
    finalcon_input = finalcon_entry.get()
    x = concentration_cal(initcon_input,initvol_input,finalcon_input,finalvol_input)
    x.unit(initcon_unit.get(),initvol_unit.get(),finalcon_unit.get(),finalvol_unit.get())
    
    
    '''
    initcon_unit_input = initcon_unit.get()
    initvol_unit_input = initvol_unit.get()
    finalcon_unit_input = finalcon_unit.get()
    finalvol_unit_input = finalvol_unit.get()
    '''
    if x.finalcon*x.final1>x.initcon*x.init1:
        messagebox.showwarning('Oopz！','小的只负责稀释，不负责浓缩')
    elif x.initcon == 0:
        result = x.initcon_number()*x.final1*x.final2/(x.init1*x.init2)
        initcon_entry.insert(0,f'{result}')
    elif x.initvol == 0:
        result = x.initvol_number()*x.final1*x.final2/(x.init1*x.init2)
        initvol_entry.insert(0,f'{result}')
    elif x.finalcon == 0:
        result = x.finalcon_number()*x.init1*x.init2/(x.final2*x.final1)
        finalcon_entry.insert(0,f'{result}')
    elif x.finalvol == 0:
        result = x.finalvol_number()*x.init1*x.init2/(x.final1*x.final2)
        finalvol_entry.insert(0,f'{result}')
    else:
        messagebox.showwarning('Oopz!', '请清空已有数据')
def func2_show_result():
    mwsolid_input = mwsolid_entry.get()
    workcon_input = workcon_entry.get()
    savvol_input = savvol_entry.get()
    x = solid_cal(mwsolid_input,workcon_input,savvol_input)
    x.unit(workcon_unit.get(), savvol_unit.get(),sovvol_unit.get(),solidmass_unit.get())
    result1 = x.savvol * x.unit2 /x.unit3
    sovvol_result.config(text=f'{result1}',bd=1,relief='solid')
    result2 = x.result_number() * 0.001 * x.unit1 *x.unit2 /x.unit4
    solidmass_result.config(text=f'{result2}',bd=1,relief='solid')
def func3_show_result():
    pld_total = packvol_number.get()
    x = plasmid_cal(pld1_ratio.get(),pld2_ratio.get(),pld3_ratio.get(),pld4_ratio.get())
    weight = x.total_weight(pld_total)
    x.plasmid_con(pldcon1_ratio.get(),pldcon2_ratio.get(),pldcon3_ratio.get(),pldcon4_ratio.get())
    p1_vol = round(weight * x.p1_ratio / x.p1_con, 2)
    p2_vol = round(weight * x.p2_ratio / x.p2_con, 2)
    p3_vol = round(weight * x.p3_ratio / x.p3_con, 2)
    p4_vol = round(weight * x.p4_ratio / x.p4_con, 2)
    pldvol1_ratio.config(text=f'{p1_vol}',bd=1,relief='solid')
    pldvol2_ratio.config(text=f'{p2_vol}',bd=1,relief='solid')
    pldvol3_ratio.config(text=f'{p3_vol}',bd=1,relief='solid')
    pldvol4_ratio.config(text=f'{p4_vol}',bd=1,relief='solid')
def func3_custom():
    button3.grid(row = 14, column = 9, rowspan = 3)
    custom_button.destroy()
    pld4_title.grid(row=14,column=7)
    pld4_ratio.grid(row=14,column=8)
    pldcon4_title.grid(row=15,column=7)
    pldcon4_ratio.grid(row=15,column=8)
    pldvol4_title.grid(row=16,column=7)
    pldvol4_ratio.grid(row=16,column=8)
def func4_std():
    blank = float(blank_num.get())
    std1 = float(std1_num.get()) - blank
    std2 = float(std2_num.get()) - blank
    std3 = float(std3_num.get()) - blank
    std4 = float(std4_num.get()) - blank
    std5 = float(std5_num.get()) - blank
    x = [std1, std2, std3, std4, std5, 0]
    y = [2000, 1000, 500, 250, 125, 0]
    x_axies = np.array(x)
    y_axies = np.array(y)
    func = np.polyfit(x_axies, y_axies, 1)
    global line
    line = np.poly1d(func)
    y_appx = line(x_axies)
    plot1.plot(x_axies, y_appx,'r')
    plot1.scatter(x,y,s=10)
    plot1.set_title(f'y={line}')
    canvas.draw()
    canvas.get_tk_widget().grid(row = 19,rowspan=4, column=2,columnspan=3)
def func4_cal():
    for i in range(1,8):
        sap_num_str = globals()[f'sap_entry_{i}'].get()
        sap_num = float(sap_num_str) if sap_num_str else 0
        mult_time_str = globals()[f'mult_times_{i}'].get()
        mult_time = float(mult_time_str) if mult_time_str else 1
        sap_result = line(sap_num)*mult_time*1.25*10**4
        sap_result_sci = format(sap_result,".2e")
        globals()[f'result_{i}'].config(text=f'{sap_result_sci}',bd=1,relief='solid')


    

title = tk.Label(main, text = '实验室综合计算器', font=('微软雅黑',15,'bold'))
title.grid(row=0,column=0,columnspan=9)

'''
以下是功能1：
稀释计算
- 给出某个试剂的初始浓度，体积，目标浓度，体积，四个中的任意三个，计算出第四个，同时要完成单位的转化，
'''
#功能1
func1_title = tk.Label(main, text = '稀释计算')
func1_title.grid(row=1,column=0)
#初始浓度
initcon_title = tk.Label(main, text = '初始浓度：')
initcon_entry = tk.Entry(main,width=8)
unit1 = tk.StringVar()
initcon_unit = ttk.Combobox(main,width=7,textvariable=unit1)
initcon_unit['values'] = ('mol/L','mmol/L','ng/μL','g/L')
initcon_unit.current(0)
initcon_title.grid(row=2,column=0)
initcon_entry.grid(row=2,column=1)
initcon_unit_Lable = tk.Label(main,text='单位')
initcon_unit_Lable.grid(row=2,column=2)
initcon_unit.grid(row=2,column=3)
#初始体积
initvol_title = tk.Label(main,text='初始体积：')
initvol_entry = tk.Entry(main,width=8)
unit2 = tk.StringVar()
initvol_unit = ttk.Combobox(main,width=7,textvariable=unit2)
initvol_unit['values'] = ('mL','μL','L')
initvol_unit.current(0)
initvol_title.grid(row=2,column=5)
initvol_entry.grid(row=2,column=6)
initvol_unit_Lable = tk.Label(main,text='单位')
initvol_unit_Lable.grid(row=2,column=7)
initvol_unit.grid(row=2,column=8)
#目标浓度
finalcon_title = tk.Label(main, text = '目标浓度：')
finalcon_entry = tk.Entry(main,width=8)
unit3 = tk.StringVar()
finalcon_unit = ttk.Combobox(main,width=7,textvariable=unit3)
finalcon_unit['values'] = ('mol/L','mmol/L','ng/μL','g/L')
finalcon_unit.current(0)
finalcon_title.grid(row=4,column=0)
finalcon_entry.grid(row=4,column=1)
finalcon_unit_Lable = tk.Label(main,text='单位')
finalcon_unit_Lable.grid(row=4,column=2)
finalcon_unit.grid(row=4,column=3)
#目标体积
finalvol_title = tk.Label(main,text='目标体积：')
finalvol_entry = tk.Entry(main,width=8)
unit4 = tk.StringVar()
finalvol_unit = ttk.Combobox(main,width=7,textvariable=unit4)
finalvol_unit['values'] = ('mL','μL','L')
finalvol_unit.current(0)
finalvol_title.grid(row=4,column=5)
finalvol_entry.grid(row=4,column=6)
finalvol_unit_Lable = tk.Label(main,text='单位')
finalvol_unit_Lable.grid(row=4,column=7)
finalvol_unit.grid(row=4,column=8)
#提示信息
warn = tk.Label(main,text = '')
warn.grid(row = 5, column = 0)
#计算按钮1
button1 = tk.Button(main,text = '确定',
                    width = 5,
                    bg = 'orange',
                    command = func1_show_result)
button1.grid(row = 2, column = 9, rowspan = 3)
#分割线1
separator1 = ttk.Separator(main, orient='horizontal')
separator1.grid(row=6,column=0,columnspan=10,sticky="ew")
'''
以下是功能2
溶解计算
- 给出某个固体的摩尔质量、需要加入到培养基中的质量、需要加的体积，计算出如何溶解稀释
	固体摩尔质量（单位固定），工作浓度（单位mol/L,mmol/L,μmol/L），需要配置的体积（单位ml, μl），计算需要的溶剂量(单位ml)、固体质量（单位g） 
'''
#功能2
func2_title = tk.Label(main,text='固体溶解计算')
func2_title.grid(row=7,column=0)
#摩尔质量
mwsolid_title = tk.Label(main,text='摩尔质量：')
mwsolid_entry = tk.Entry(main,width=8)
mwsolid_unit1 = tk.Label(main,text='单位')
mwsolid_unit2 = tk.Label(main,text='g/M')
mwsolid_title.grid(row=8,column=0)
mwsolid_entry.grid(row=8,column=1)
mwsolid_unit1.grid(row=8,column=2)
mwsolid_unit2.grid(row=8,column=3)
#工作浓度
workcon_title = tk.Label(main,text='工作浓度：')
workcon_entry = tk.Entry(main,width=8)
workcon_unit_Label = tk.Label(main,text='单位')
unit5=tk.StringVar()
workcon_unit = ttk.Combobox(main,width=7,textvariable=unit5)
workcon_unit['values']=('mol/L','mmol/L','μmol/L')
workcon_unit.current(0)
workcon_title.grid(row=8,column=5)
workcon_entry.grid(row=8,column=6)
workcon_unit_Label.grid(row=8,column=7)
workcon_unit.grid(row=8,column=8)
#存储体积
savvol_title = tk.Label(main,text='需要体积：')
savvol_entry = tk.Entry(main,width=8)
savvol_unit_Label = tk.Label(main,text='单位')
unit6 = tk.StringVar()
savvol_unit = ttk.Combobox(main,width=5,textvariable=unit6)
savvol_unit['values'] = ('mL','μL')
savvol_unit.current(0)
savvol_title.grid(row=9,column=0)
savvol_entry.grid(row=9,column=1)
savvol_unit_Label.grid(row=9,column=2)
savvol_unit.grid(row=9,column=3)
#需要溶剂体积
sovvol_title = tk.Label(main,text='需要溶剂体积：')
sovvol_result = tk.Label(main,text='',width=8)
sovvol_unit_Label = tk.Label(main,text='单位')
unit7 = tk.StringVar()
sovvol_unit = ttk.Combobox(main,width=5,textvariable=unit7)
sovvol_unit['values'] = ('mL','μL')
sovvol_unit.current(0)
sovvol_title.grid(row=10,column=0)
sovvol_result.grid(row=10,column=1)
sovvol_unit_Label.grid(row=10,column=2)
sovvol_unit.grid(row=10,column=3)
#需要固体质量
solidmass_title = tk.Label(main,text='需要固体质量:')
solidmass_result = tk.Label(main,text='',width=8)
solidmass_unit_Label = tk.Label(main,text='单位')
unit8=tk.StringVar()
solidmass_unit = ttk.Combobox(main,width=5,textvariable=unit8)
solidmass_unit['values']=('g','mg')
solidmass_unit.current(0)
solidmass_title.grid(row=10,column=5)
solidmass_result.grid(row=10,column=6)
solidmass_unit_Label.grid(row=10,column=7)
solidmass_unit.grid(row=10,column=8)
#计算按钮2
button2 = tk.Button(main,text = '确定',
                    width = 5,
                    bg = 'orange',
                    command = func2_show_result)
button2.grid(row = 8, column = 9, rowspan = 3)
#分割线2
separator2 = ttk.Separator(main, orient='horizontal')
separator2.grid(row=11,column=0,columnspan=10,sticky="ew",pady=10)

'''
以下是功能3
包装质粒用量计算
- 给出病毒包装各质粒的用量比例、总质粒质量、各质粒的浓度，计算每个质粒需要加入的体积
'''
#功能3
func3_title = tk.Label(main,text='病毒包装体系计算')
func3_title.grid(row = 12,column=0)
#质粒总用量
packvol_title = tk.Label(main,text = '质粒总用量：')
default_vol = tk.StringVar()
default_vol.set('60')
packvol_number = tk.Entry(main,width = 8,textvariable=default_vol)
packvol_unit = tk.Label(main,text='μg')
packvol_title.grid(row=13,column=0)
packvol_number.grid(row=13,column=1)
packvol_unit.grid(row=13,column=2)
#质粒用量
pldratio_title = tk.Label(main,text='质粒比例：')
pld1_title = tk.Label(main,text='Helper:')
def_pld1_num = tk.StringVar()
def_pld1_num.set('6')
pld1_ratio = tk.Entry(main,width = 5,textvariable=def_pld1_num)
pld2_title = tk.Label(main,text='Transfer:')
def_pld2_num = tk.StringVar()
def_pld2_num.set('12')
pld2_ratio = tk.Entry(main,width = 5,textvariable=def_pld2_num)
pld3_title = tk.Label(main,text='Envelop G:')
def_pld3_num = tk.StringVar()
def_pld3_num.set('5')
pld3_ratio = tk.Entry(main,width = 5,textvariable=def_pld3_num)
pldratio_title.grid(row = 14, column = 0)
pld1_title.grid(row = 14,column = 1)
pld1_ratio.grid(row = 14, column = 2)
pld2_title.grid(row = 14,column = 3)
pld2_ratio.grid(row = 14, column = 4)
pld3_title.grid(row = 14, column = 5)
pld3_ratio.grid(row = 14,column = 6)
#质粒浓度
pldcon_title = tk.Label(main,text='质粒浓度:')
pldcon1_title = tk.Label(main,text='Helper:')
pldcon1_ratio = tk.Entry(main,width = 8)
pldcon2_title = tk.Label(main,text='Transfer:')
pldcon2_ratio = tk.Entry(main,width = 8)
pldcon3_title = tk.Label(main,text='Envelop G:')
pldcon3_ratio = tk.Entry(main,width = 8)
pldcon_title.grid(row = 15, column = 0)
pldcon1_title.grid(row = 15,column = 1)
pldcon1_ratio.grid(row = 15, column = 2)
pldcon2_title.grid(row = 15,column = 3)
pldcon2_ratio.grid(row = 15, column = 4)
pldcon3_title.grid(row = 15, column = 5)
pldcon3_ratio.grid(row = 15,column = 6)
#各质粒所用体积
pldvol_title = tk.Label(main,text='质粒体积：')
pldvol1_title = tk.Label(main,text='Helper:')
pldvol1_ratio = tk.Label(main,text='',width=8)
pldvol2_title = tk.Label(main,text='Transfer:')
pldvol2_ratio = tk.Label(main,text='',width=8)
pldvol3_title = tk.Label(main,text='Envelop G:')
pldvol3_ratio = tk.Label(main,text='',width=8)
pldvol_title.grid(row = 16, column = 0)
pldvol1_title.grid(row = 16,column = 1)
pldvol1_ratio.grid(row = 16, column = 2)
pldvol2_title.grid(row = 16,column = 3)
pldvol2_ratio.grid(row = 16, column = 4)
pldvol3_title.grid(row = 16, column = 5)
pldvol3_ratio.grid(row = 16,column = 6)
#添加自定义质粒按钮
custom_button = tk.Button(main,text='添加质粒4',command=func3_custom)
custom_button.grid(row = 13,column = 8)
pld4_title = tk.Label(main,text='plasmid:')
pld4_ratio = tk.Entry(main,width = 5)
pldcon4_title = tk.Label(main,text='plasmid:')
pldcon4_ratio = tk.Entry(main,width = 8)
pldvol4_title = tk.Label(main,text='plasmid:')
pldvol4_ratio = tk.Label(main,text='',width=8)

#计算按钮3
button3 = tk.Button(main,text = '确定',
                    width = 5,
                    bg = 'orange',
                    command = func3_show_result)
button3.grid(row = 14, column = 8, rowspan = 3)

#分割线3
separator3 = ttk.Separator(main, orient='horizontal')
separator3.grid(row=17,column=0,columnspan=10,sticky="ew",pady=10)
'''
以下是功能4
## p24病毒滴度计算
- 给出酶标仪测量结果、标准曲线方程参数，输出测定的病毒滴度 
'''
#功能4
func4_title = tk.Label(main,text='病毒滴度计算')
func4_title.grid(row=18,column=0)
func4_2_title = tk.Label(main,text='(请先进行标准曲线绘制)')
func4_2_title.grid(row=18,column=1)
#标准曲线绘制
std1_label = tk.Label(main,text='std2000:(pg/mL)')
std1_num = tk.Entry(main,width=8)
std2_label = tk.Label(main,text='std1000:')
std2_num = tk.Entry(main,width=8)
std3_label = tk.Label(main,text='std500:')
std3_num = tk.Entry(main,width=8)
std4_label = tk.Label(main,text='std250:')
std4_num = tk.Entry(main,width=8)
std5_label = tk.Label(main,text='std125:')
std5_num = tk.Entry(main,width=8)
blank_label = tk.Label(main,text='Blank:')
blank_num = tk.Entry(main,width=8)
std1_label.grid(row=19,column=0)
std2_label.grid(row=20,column=0)
std3_label.grid(row=21,column=0)
std4_label.grid(row=22,column=0)
std5_label.grid(row=23,column=0)
blank_label.grid(row=24,column=0)
std1_num.grid(row=19,column=1)
std2_num.grid(row=20,column=1)
std3_num.grid(row=21,column=1)
std4_num.grid(row=22,column=1)
std5_num.grid(row=23,column=1)
blank_num.grid(row=24,column=1)
fig1 = Figure(figsize=(4, 3), dpi=75)
plot1 = fig1.add_subplot(111)

canvas = FigureCanvasTkAgg(fig1, master=main)
canvas.get_tk_widget().grid(row = 19,rowspan=4, column=2,columnspan=3)

button4 = tk.Button(main,text = '绘制标曲',
                    width = 7,
                    bg = 'orange',
                    command = func4_std)
button4.grid(row = 25, column = 0, columnspan=2)

#实验数据输入
sap_label_dict = {}
sap_entry_dict = {}
mult_times_dict = {}
for i in range(1,8):
    globals()[f'sap_label_{i}'] = tk.Label(main,text = f'样品{i}',pady=15)
    globals()[f'sap_label_{i}'].grid(row = 18+i, column =5)
    globals()[f'sap_entry_{i}'] = tk.Entry(main, width = 8)
    globals()[f'sap_entry_{i}'].grid(row = 18+i, column = 6)
    globals()[f'mult_times_{i}'] = tk.Entry(main,width = 8)
    globals()[f'mult_times_{i}'].grid(row = 18+i, column = 7)
    globals()[f'result_{i}'] = tk.Label(main,text = '')
    globals()[f'result_{i}'].grid(row = 18+i, column = 8)



index_title = tk.Label(main,text='酶标仪数值')
mult_times_title = tk.Label(main,text = '稀释倍数')
index_result_title= tk.Label(main,text = '病毒浓度(LP/mL)')
index_title.grid(row=18,column=6)
mult_times_title.grid(row=18,column=7)
index_result_title.grid(row=18,column=8)
#计算按钮
button5 = tk.Button(main,text = '计算滴度',
                    width = 7,
                    bg = 'orange',
                    command=func4_cal
                    )
button5.grid(row = 25, column =  4)

main.protocol("WM_DELETE_WINDOW", on_closing)
main.mainloop()

