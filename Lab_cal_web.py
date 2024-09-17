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
    if request.method == 'POST':
        initcon = request.form.get('initcon', '0')
        initvol = request.form.get('initvol', '0')
        finalcon = request.form.get('finalcon', '0')
        finalvol = request.form.get('finalvol', '0')
        initcon_unit = request.form.get('initcon_unit')
        initvol_unit = request.form.get('initvol_unit')
        finalcon_unit = request.form.get('finalcon_unit')
        finalvol_unit = request.form.get('finalvol_unit')
        
        calc = concentration_cal(initcon, initvol, finalcon, finalvol)
        calc.unit(initcon_unit, initvol_unit, finalcon_unit, finalvol_unit)

        if calc.finalcon * calc.final1 > calc.initcon * calc.init1:
            warn_text = "Oopz！小的只负责稀释，不负责浓缩"
        elif calc.initcon == 0:
            result1 = calc.initcon_number()*calc.final1*calc.final2/(calc.init1*calc.final1)
            

            result2 = calc.initvol
            result3 = calc.finalcon
            result4 = calc.finalvol

        elif calc.initvol == 0:
            result1 = calc.initcon
            result2 = calc.initvol_number()*calc.final1*calc.final2/(calc.init1*calc.final1)
            result3 = calc.finalcon
            result4 = calc.finalvol
        elif calc.finalcon == 0:
            result3 = calc.finalcon_number()
        elif calc.finalvol == 0:
            result4 = calc.finalvol_number()
        
        temp_text = calc.init1

        #return render_template('result.html', result=result)
    
    return render_template('dilution.html', initcon_result = result1, initvol_result=result2, finalcon_result=result3, finalvol_result=result4
                           ,temp = temp_text)

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

        return render_template('result.html', sovvol=sovvol, solidmass=solidmass)
    
    return render_template('solid.html')

# 质粒用量计算
@app.route('/plasmid', methods=['GET', 'POST'])
def plasmid():
    if request.method == 'POST':
        total_weight = request.form.get('total_weight', '0')
        p1_num = request.form.get('p1_num', '0')
        p2_num = request.form.get('p2_num', '0')
        p3_num = request.form.get('p3_num', '0')
        p4_num = request.form.get('p4_num', '0')

        calc = plasmid_cal(p1_num, p2_num, p3_num, p4_num)
        total_weight = calc.total_weight(total_weight)

        p1_con = float(request.form.get('p1_con', '1'))
        p2_con = float(request.form.get('p2_con', '1'))
        p3_con = float(request.form.get('p3_con', '1'))
        p4_con = float(request.form.get('p4_con', '1'))

        calc.plasmid_con(p1_con, p2_con, p3_con, p4_con)

        p1_vol = round(total_weight * calc.p1_ratio / calc.p1_con, 2)
        p2_vol = round(total_weight * calc.p2_ratio / calc.p2_con, 2)
        p3_vol = round(total_weight * calc.p3_ratio / calc.p3_con, 2)
        p4_vol = round(total_weight * calc.p4_ratio / calc.p4_con, 2)

        return render_template('result.html', p1_vol=p1_vol, p2_vol=p2_vol, p3_vol=p3_vol, p4_vol=p4_vol)
    
    return render_template('plasmid.html')

if __name__ == '__main__':
    app.run(debug=False)
