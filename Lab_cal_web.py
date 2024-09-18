# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:09:36 2024

@author: mikey
"""

from flask import Flask, render_template, request
from calculator import concentration_cal, solid_cal, plasmid_cal

app = Flask(__name__)

# 主页面
@app.route('/')
def index():
    return render_template('index.html')

# 稀释计算
@app.route('/dilution', methods=['GET', 'POST'])
def dilution():
    result1 = result2 = result3 = result4 = warn_text = temp_text = None
    initcon_selected_unit = initvol_selected_unit = finalcon_selected_unit = finalvol_selected_unit= None
    if request.method == 'POST':
        initcon = request.form.get('initcon', '0')
        initvol = request.form.get('initvol', '0')
        finalcon = request.form.get('finalcon', '0')
        finalvol = request.form.get('finalvol', '0')
        initcon_unit = request.form.get('initcon_unit','mol/L')
        initvol_unit = request.form.get('initvol_unit','mL')
        finalcon_unit = request.form.get('finalcon_unit','mol/L')
        finalvol_unit = request.form.get('finalvol_unit','ml')
        
        calc = concentration_cal(initcon, initvol, finalcon, finalvol)
        calc.unit(initcon_unit, initvol_unit, finalcon_unit, finalvol_unit)

        if calc.finalcon * calc.final1 > calc.initcon * calc.init1:
            warn_text = "Oopz！小的只负责稀释，不负责浓缩"
        elif calc.initcon == 0:
            result1 = calc.initcon_number()*calc.final1*calc.final2/(calc.init1*calc.init2)
            result2 = calc.initvol
            result3 = calc.finalcon
            result4 = calc.finalvol

        elif calc.initvol == 0:
            result1 = calc.initcon
            result2 = calc.initvol_number()*calc.final1*calc.final2/(calc.init1*calc.init2)
            result3 = calc.finalcon
            result4 = calc.finalvol
        elif calc.finalcon == 0:
            result1 = calc.initcon
            result2 = calc.initvol
            result3 = calc.finalcon_number()*(calc.init1*calc.init2)/(calc.final1*calc.final2)
            result4 = calc.finalvol
        elif calc.finalvol == 0:
            result4 = calc.finalvol_number()
        #temp_text = f'{calc.init1},{calc.init2},{calc.final1},{calc.final2},{calc.initcon}'
        return render_template('dilution.html', initcon_result = result1, initvol_result=result2, finalcon_result=result3, finalvol_result=result4
                           , initcon_selected_unit=initcon_unit,initvol_selected_unit=initvol_unit,finalcon_selected_unit=finalcon_unit,
                           finalvol_selected_unit=finalvol_unit)
        #return render_template('result.html', result=result)
    
    return render_template('dilution.html')
    '''
    return render_template('dilution.html', initcon_result = result1, initvol_result=result2, finalcon_result=result3, finalvol_result=result4
                           ,temp = temp_text)
    '''

# 固体溶解计算
@app.route('/solid', methods=['GET', 'POST'])
def solid():
    if request.method == 'POST':
        mwsolid = request.form.get('mwsolid', '0')
        workcon = request.form.get('workcon', '0')
        savvol = request.form.get('savvol', '0')
        workcon_unit = request.form.get('workcon_unit')
        savvol_unit = request.form.get('savvol_unit')
        sovvol_unit = request.form.get('sovvol_unit')
        solidmass_unit = request.form.get('solidmass_unit')

        calc = solid_cal(mwsolid, workcon, savvol)
        calc.unit(workcon_unit, savvol_unit, sovvol_unit, solidmass_unit)

        sovvol = calc.savvol * calc.unit2 / calc.unit3
        solidmass = calc.result_number() * 0.001 * calc.unit1 * calc.unit2 / calc.unit4

        return render_template('solid.html', mwsolid_result=mwsolid,
                               workcon_result=workcon,savvol_result=savvol,sovvol_result=sovvol,solidmass_result=solidmass,
                               workcon_selected_unit=workcon_unit,savvol_selected_unit=savvol_unit,
                               sovvol_selected_unit=sovvol_unit,solidmass_selected_unit=solidmass_unit)
    
    return render_template('solid.html')

# 质粒用量计算
@app.route('/plasmid', methods=['GET', 'POST'])
def plasmid():
    p1_vol=p2_vol=p3_vol=p4_vol=None
    p1_num=p2_num=p3_num=p4_num=None
    p1_con=p2_con=p3_con=p4_con=None

    if request.method == 'POST':
        total_weight2 = request.form.get('total_weight')
        p1_num = request.form.get('helper_ratio')
        p2_num = request.form.get('transfer_ratio')
        p3_num = request.form.get('envelop_g_ratio')
        p4_num = request.form.get('plasmid_ratio','0')

        calc = plasmid_cal(p1_num, p2_num, p3_num, p4_num)
        total_weight1 = calc.total_weight(total_weight2)

        p1_con = request.form.get('helper_con')
        p2_con = request.form.get('transfer_con')
        p3_con = request.form.get('envelop_con')
        p4_con = request.form.get('plasmid_con','1')

        calc.plasmid_con(p1_con, p2_con, p3_con, p4_con)

        p1_vol = round(total_weight1 * calc.p1_ratio / calc.p1_con, 2)
        p2_vol = round(total_weight1 * calc.p2_ratio / calc.p2_con, 2)
        p3_vol = round(total_weight1 * calc.p3_ratio / calc.p3_con, 2)
        p4_vol = round(total_weight1 * calc.p4_ratio / calc.p4_con, 2)

        return render_template('plasmid.html', total_result=total_weight2,
                               helper_ratio_result=p1_num,transfer_ratio_result=p2_num,envelop_ratio_result=p3_num,plasmid_ratio_result=p4_num,
                               helper_con_result=p1_con,transfer_con_result=p2_con,envelop_con_result=p3_con,plasmid_con_result=p4_con,
                               helper_vol_result=p1_vol, transfer_vol_result=p2_vol, envelop_vol_result=p3_vol,plasmid_vol_result=p4_vol
        )
    
    return render_template('plasmid.html', 
                           total_weight2=60,
                           helper_ratio_result='6', 
                           transfer_ratio_result='12', 
                           envelop_ratio_result='5', 
                           )

if __name__ == '__main__':
    app.run(debug=True)
