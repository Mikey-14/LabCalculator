# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 12:24:28 2024

@author: mikey
"""

class concentration_cal:
    def __init__(self,initcon='0',initvol='0',finalcon='0',finalvol='0'):
        self.initcon = float(initcon) if initcon else 0
        self.initvol = float(initvol) if initvol else 0
        self.finalcon = float(finalcon) if finalcon else 0
        self.finalvol = float(finalvol) if finalvol else 0
        
    def unit(self,initcon_unit='',initvol_unit='',finalcon_unit='',finalvol_unit=''):  
        self.initcon_unit=initcon_unit
        self.initvol_unit=initvol_unit
        self.finalcon_unit=finalcon_unit
        self.finalvol_unit=finalvol_unit
        if self.initcon_unit == 'mol/L':
            self.init1 = 1
        elif self.initcon_unit == 'mmol/L':
            self.init1 = 0.001
        elif self.initcon_unit == 'ng/μL':
            self.init1 = 0.001
        elif self.initcon_unit == 'g/L':
            self.init1 = 1
        if self.initvol_unit == 'mL':
            self.init2 = 1
        elif self.initvol_unit == 'L':
            self.init2 = 1000
        elif self.initvol_unit == 'μL':
            self.init2 = 0.001
            
        if self.finalcon_unit == 'mol/L':
            self.final1 = 1
        elif self.finalcon_unit == 'mmol/L':
            self.final1 = 0.001
        elif self.finalcon_unit == 'ng/μL':
            self.final1 = 0.001
        elif self.finalcon_unit == 'g/L':
            self.final1 = 1
        if self.finalvol_unit == 'mL':
            self.final2 = 1
        elif self.finalvol_unit == 'L':
            self.final2 = 1000
        elif self.finalvol_unit == 'μL':
            self.final2 = 0.001
    
    def initcon_number(self):
        result = self.finalcon * self.finalvol / self.initvol
        return result
    
    def initvol_number(self):
        result = self.finalcon * self.finalvol / self.initcon
        return result
    
    def finalcon_number(self):
        result = self.initvol * self.initcon / self.finalvol
        return result
    
    def finalvol_number(self):
        result = self.initvol * self.initcon / self.finalcon
        return result

        
class solid_cal:
    def __init__(self,mwsolid='',workcon='',savvol=''):
        self.mwsolid = float(mwsolid) if mwsolid else 0
        self.workcon = float(workcon) if workcon else 0
        self.savvol = float(savvol) if savvol else 0
    
    def unit(self,workcon_unit,savvol_unit,sovvol_unit,solidmass_unit):
        self.workcon_unit = workcon_unit
        self.savvol_unit = savvol_unit
        self.sovvol_unit = sovvol_unit
        self.solidmass_unit = solidmass_unit
        
        if self.workcon_unit =='mol/L':
            self.unit1 = 1
        elif self.workcon_unit == 'mmol/L':
            self.unit1 = 0.001
        elif self.workcon_unit == 'μmol/L':
            self.unit1 = 0.000001
        if self.savvol_unit == 'mL':
            self.unit2 = 1
        elif self.savvol_unit == 'μL':
            self.unit2 = 0.001
        if self.sovvol_unit == 'mL':
            self.unit3 = 1
        elif self.sovvol_unit == 'μL':
            self.unit3 = 0.001
        if self.solidmass_unit == 'g':
            self.unit4 = 1
        elif self.solidmass_unit == 'mg':
            self.unit4 = 0.001
    def result_number(self):
        result = self.savvol * self.workcon * self.mwsolid
        return result
    
class plasmid_cal:
    def __init__(self,x,y,z,p):
        self.p1_num = float(x) if x else 0
        self.p2_num = float(y) if y else 0
        self.p3_num = float(z) if z else 0
        self.p4_num = float(p) if p else 0
        total_num = self.p1_num +self.p2_num+self.p3_num +self.p4_num
        self.p1_ratio = self.p1_num / total_num
        self.p2_ratio = self.p2_num / total_num
        self.p3_ratio = self.p3_num / total_num
        self.p4_ratio = self.p4_num / total_num
        
    def total_weight(self,x):
        total_w = float(x) if x else 0
        return total_w* 1000
    
    def plasmid_con(self,x,y,z,p):
        self.p1_con = float(x) if x else 0
        self.p2_con = float(y) if y else 0
        self.p3_con = float(z) if z else 0
        self.p4_con = float(p) if p else 1
    

''' 
    def get_initcon_unit(self):
        if initvol_unit == 'mL':
            if finalcon_unit == ''
'''