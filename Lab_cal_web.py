# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:09:36 2024

@author: mikey
"""
import random
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, jsonify
from calculator import concentration_cal, solid_cal, plasmid_cal
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


app = Flask(__name__)
current_time = datetime.now()
format_time = current_time.strftime("%Y-%m-%d--%H:%M:%S")
PDF_FOLDER = os.path.join(app.root_path, 'static/lab_protocols')
DATA_FILE = 'plasmid_data.json'


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
        finalvol_unit = request.form.get('finalvol_unit','mL')
        
        calc = concentration_cal(initcon, initvol, finalcon, finalvol)
        calc.unit(initcon_unit, initvol_unit, finalcon_unit, finalvol_unit)

        
        if calc.initcon == 0:
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
            result1 = calc.initcon
            result2 = calc.initvol
            result3 = calc.finalcon
            result4 = calc.finalvol_number()*(calc.init1*calc.init2)/(calc.final1*calc.final2)
        
        with open('quotes.txt', 'r', encoding='utf-8') as file:
            quotes = file.readlines()
        quote_selected = random.choice(quotes).strip()
        
        #temp_text = f'{calc.init1},{calc.init2},{calc.final1},{calc.final2},{calc.initcon}'
        return render_template('dilution.html', initcon_result = result1, initvol_result=result2, finalcon_result=result3, finalvol_result=result4
                           , initcon_selected_unit=initcon_unit,initvol_selected_unit=initvol_unit,finalcon_selected_unit=finalcon_unit,
                           finalvol_selected_unit=finalvol_unit,
                           quote=quote_selected)
        #return render_template('result.html', result=result)
    
    return render_template('dilution.html',
                           quote="Hemogene.  For internal use only ")
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

        with open('quotes.txt', 'r', encoding='utf-8') as file:
            quotes = file.readlines()
        quote_selected = random.choice(quotes).strip()


        return render_template('solid.html', mwsolid_result=mwsolid,
                               workcon_result=workcon,savvol_result=savvol,sovvol_result=sovvol,solidmass_result=solidmass,
                               workcon_selected_unit=workcon_unit,savvol_selected_unit=savvol_unit,
                               sovvol_selected_unit=sovvol_unit,solidmass_selected_unit=solidmass_unit,
                               quote=quote_selected)
    
    return render_template('solid.html',
                           quote="Hemogene.  For internal use only ")

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

        history_sav_state = request.form.get('history_option')
        if history_sav_state == 'yes':
            with open('plasmid_history.txt', 'a', encoding='utf-8') as file:
                file.write(f'{format_time},{total_weight2},{p1_num},{p2_num},{p3_num},{p4_num},{p1_con},{p2_con},{p3_con},{p4_con},{p1_vol},{p2_vol},{p3_vol},{p4_vol}\n')

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
                           plasmid_ratio_result='0',
                           plasmid_con_result='1',
                           )
#质粒用量历史记录读取
@app.route('/solid_history', methods=['GET'])
def solid_history():
    records = []
    with open('plasmid_history.txt', 'r', encoding='utf-8') as file:
        for line in file:
            records.append(line.strip().split(','))

    return render_template('solid_history.html', records=records)

#辅助函数：读写 JSON 数据
def load_plasmids():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_plasmids(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#常用protocol库索引
@app.route('/protocols', methods=['GET'])
def protocols():
    files = os.listdir(PDF_FOLDER)
    protocol_files = [f for f in files if f.endswith('.pdf')]
    return render_template('protocols.html', protocol_files = protocol_files)

@app.route('/pdfs/<filename>')
def pdf_viewer(filename):
    return send_from_directory(PDF_FOLDER, filename)


@app.route('/lab_protocol', methods=['GET'])
def lab_protocol():
    return render_template('lab_protocol.html')

#滴度计算(暂未实现)
@app.route('/p24', methods = ['GET', 'POST'])
def p24_cal():
    if request.method == 'POST':
        std_2000 = float(request.form.get('con_2000'))
        std_1000 = float(request.form.get('con_1000'))
        std_500 = float(request.form.get('con_500'))
        std_250 = float(request.form.get('con_250'))
        std_125 = float(request.form.get('con_125'))
        std_62 = float(request.form.get('con_62'))
        std_31 = float(request.form.get('con_31'))
        std_0 = float(request.form.get('con_0'))
        x = [std_0, std_31, std_62, std_125, std_250, std_500, std_1000, std_2000]
        y = [0, 31.25, 62.5, 125, 250, 500, 1000, 2000]
        x_axies = np.array(x)
        y_axies = np.array(y)
        func_std = np.polyfit(x_axies, y_axies, 1)
        line_std = np.poly1d(func_std)
        yvals = line_std(x_axies)
        plot1 = plt.plot(x_axies, yvals, 'r')
        plot2 = plt.scatter(x,y)
        plt.title(f'y = {line_std}')
        plt.savefig(f'static/figs/new_plot.png')
    return render_template('p24.html')

#质粒库索引
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plasmid_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PlasmidInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)               # 质粒名称
    prep_date = db.Column(db.String(20), nullable=False)          # 制备时间（字符串格式）
    quantity = db.Column(db.String(32), nullable=False)           # 库存量（可带单位）

    def __repr__(self):
        return f'<Plasmid {self.name}>'

#质粒库功能
# ---新增功能：管理员登录---
ALLOWED_USERS_FILE = 'allowed_users.txt'

def is_user_allowed(username):
    if not username:
        return False
    if not os.path.exists(ALLOWED_USERS_FILE):
        return False # 如果文件不存在，谁都不能操作，安全起见
    
    with open(ALLOWED_USERS_FILE, 'r', encoding='utf-8') as f:
        # 读取所有行，去空格，转大写
        allowed = [line.strip().upper() for line in f.readlines()]
        return username.strip().upper() in allowed
# --- 新增功能：质粒管理页面路由 ---
@app.route('/plasmid_manager')
def plasmid_manager():
    return render_template('plasmid_manager.html')

# --- 登录验证接口
@app.route('/api/login', methods=['POST'])
def login_check():
    username = request.json.get('username')
    if is_user_allowed(username):
        return jsonify({'status': 'success', 'message': '登录成功'})
    else:
        return jsonify({'status': 'fail', 'message': '无权限或名字不在名单中'}), 403
    
# --- 新增 API：处理数据的增删改查 ---
@app.route('/api/plasmids', methods=['GET', 'POST'])
def handle_plasmids():
    data = load_plasmids()
    
    if request.method == 'GET':
        # 获取所有数据
        return jsonify(data)
    
    if request.method == 'POST':
        #检查是否是正确用户
        current_user = request.headers.get('X-User-ID')
        if not is_user_allowed(current_user):
            return jsonify({'error': 'Unauthorized'}), 401 # 401代表未授权
        # 添加新质粒
        new_item = request.json
        # 简单的后端校验
        if not new_item.get('name'):
            return jsonify({'error': 'Name is required'}), 400
            
        # 生成唯一 ID (简单的处理方式：找到当前最大的ID + 1，或者用时间戳)
        # 这里为了配合前端逻辑，我们直接信任前端发来的时间戳ID，或者在这里重新生成
        # 为简单起见，直接追加
        data.append(new_item)
        save_plasmids(data)
        return jsonify({'message': 'Saved', 'data': new_item}), 201

@app.route('/api/plasmids/<int:p_id>', methods=['DELETE', 'PUT'])
def handle_single_plasmid(p_id):
    #检查用户权限
    current_user = request.headers.get('X-User-ID')
    if not is_user_allowed(current_user):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = load_plasmids()
    
    if request.method == 'DELETE':
        # 删除指定 ID
        data = [p for p in data if p['id'] != p_id]
        save_plasmids(data)
        return jsonify({'message': 'Deleted'})
    
    if request.method == 'PUT':
        # 更新状态 (例如：是否需要提取)
        update_data = request.json
        for p in data:
            if p['id'] == p_id:
                p['extract'] = update_data.get('extract', p['extract'])
        save_plasmids(data)
        return jsonify({'message': 'Updated'})
    
if __name__ == '__main__':
    app.run(debug=True)
