# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:02:06 2018
Version: 0.1.0
@author: katamaran
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import json
import struct
import scipy.optimize as scop
import copy


class spectr():
    sp_type={'na':0,'GINR':1,'GIRZ':2,'GINR+RZ':3,'N':4,'GIER':5}
    def __init__(self, N=0):
# инициализирет спектр
        self.name='' # name of spectrum
        self.type=self.sp_type['na'] # type of spectrum
        self.a=0 # a-param of energy E=i*a+b
        self.b=0 # a-param of energy E=i*a+b
        self.a_srd = 0 # a param of speading sigma = a*i^2+b*i+c
        self.b_srd = 0 # b param of speading sigma = a*i^2+b*i+c
        self.c_srd = 0 # c param of speading sigma = a*i^2+b*i+c
        self.N=N # count of chenals
        self.time = 0
        self.history=['Create spectr by _init_']
        self.E=np.zeros(self.N,dtype=float)
        self.sp=np.zeros(self.N,dtype=float)
        self.ipeaks=np.array([])
        self.wpeaks=np.array([])
        pass
    
    def set_E(self): 
        """ формирует массив энергий E=i*a+b """
        self.E=np.arange(len(self.sp))*self.a+self.b
        self.history.append(['set_E: E=i*'+str(self.a)+'+'+str(self.b)])
        
    def open_spe(self, name):
        """ читает спектр в формате SPE """
        f=open(name,'r')
        df=np.loadtxt(f,dtype=np.float)
        self.name=os.path.basename(name).split('.')[0]
        self.a=df[1]
        self.b=df[2]
        self.time =df[3]
        self.sp=np.array(df[4:])
        self.history.append(['Open sp from '+name])
        self.set_E()
        self.N=len(self.sp)
        self.history.append(['Open sp from '+name])
        f.close
    
    def open_cmp(self,name):
        """ читает спектр в формате CMP """
        fin  = open(name, "rb").read()
        #name
        self.name=os.path.basename(name).split('.')[0]
        fields=struct.unpack('<H', fin[10:10+2])
        #print('5 целая часть времени: '+str(fields[0]))
        self.time =fields[0]
      #  fields=struct.unpack('<H', fin[14:14+2])
        #print('7 дробная часть времени:'+str(fields[0]))
        
        fields=struct.unpack('<H', fin[16:16+2])
        #print('Канал 1:'+str(fields[0]))
        c1=fields[0]
        
        fields=struct.unpack('<H', fin[20:20+2])
        #print('Канал 2:'+str(fields[0]))
        c2=fields[0]
        
        fields=struct.unpack('<H', fin[24:24+2])
        #print('E1:'+str(fields[0]))
        s_e1=str(fields[0])
        fields=struct.unpack('<H', fin[26:26+2])
        #print('E1.:'+str(fields[0]))
        s_e1=s_e1+'.'+str(fields[0])
        e1=float(s_e1)
        
        fields=struct.unpack('<H', fin[28:28+2])
        #print('E1:'+str(fields[0]))
        s_e2=str(fields[0])
        fields=struct.unpack('<H', fin[30:30+2])
        #print('E1.:'+str(fields[0]))
        s_e2=s_e2+'.'+str(fields[0])
        e2=float(s_e2)
        self.a=(e2-e1)/(c2-c1)
        self.b=e2-self.a*c2       
#        fields=struct.unpack('<b', fin[32:32+1])
#        print('День начала:'+str(fields[0]))
#        fields=struct.unpack('<b', fin[33:33+1])
#        print('День начала:'+str(fields[0]))
#        
#        fields=struct.unpack('<b', fin[34:34+1])
#        print('День начала:'+str(fields[0]))
#        fields=struct.unpack('<b', fin[35:35+1])
#        print('День начала:'+str(fields[0]))
        
#        #31 Номер зонда
#        fields=struct.unpack('<H', fin[62:62+2])
#        print('Номер зонда:'+str(fields[0]))
        
        shft=64
        self.sp=np.zeros((len(fin) - shft ) // 2)
        for i in range((len(fin) - shft ) // 2 ):
            fields = struct.unpack('<H', fin[shft+2*i:shft+2*i+2])
           # print(str(i)+':'+str(fields[0]))
            dv=fields[0]//16384
            md=fields[0]%16384
            if (dv==0):
                self.sp[i]=md
            elif (dv==1):
                self.sp[i]=md*4
            elif (dv==2):
                self.sp[i]=md*16
            elif (dv==3):
                self.sp[i]=md*64
        
        self.history.append(['Open sp from '+name])
        self.set_E()
        self.N=len(self.sp)
        
    
    def plot_sp_line(self):
        """ строит спектр in line"""
        fig = plt.figure()
        ax1 = fig.add_axes((0.1,0.3,0.8,0.6)) # create an Axes with some room below

        X = range(self.N)
        Y = self.sp

        ax1.plot(X,Y)
        ax1.set_xlabel('Chanal')
#        ax1.set_xlim(0,self.N)
        # create second Axes. Note the 0.0 height
        ax2 = fig.add_axes((0.1,0.1,0.8,0.0))
        ax2.yaxis.set_visible(False) # hide the yaxis

 #       new_tick_locations = self.E
    
#        def tick_function(X):
#            V = 1/(1+X)
#            return ["%.3f" % z for z in V]

#        ax2.set_xticks(new_tick_locations)
 #       ax2.set_xticklabels(tick_function(new_tick_locations))
        ax2.plot(self.E,Y)
        ax2.set_xlabel('Energy, KeV')
     #   ax2.set_xlim(min(self.E),max(self.E))
        
        plt.show()
        
    def plot_sp_lg(self):
        """ строит спектр in log"""
        fig = plt.figure()
        ax1 = fig.add_axes((0.1,0.3,0.8,0.6)) # create an Axes with some room below

        X = range(self.N)
        Y = self.sp

        ax1.semilogy(range(self.N),self.sp,label=self.name)
        ax1.set_xlabel('Chanal')
#        ax1.set_xlim(0,self.N)
        # create second Axes. Note the 0.0 height
        ax2 = fig.add_axes((0.1,0.1,0.8,0.0))
        ax2.yaxis.set_visible(False) # hide the yaxis

 #       new_tick_locations = self.E
    
#        def tick_function(X):
#            V = 1/(1+X)
#            return ["%.3f" % z for z in V]

#        ax2.set_xticks(new_tick_locations)
 #       ax2.set_xticklabels(tick_function(new_tick_locations))
        ax2.plot(self.E,Y)
        ax2.set_xlabel('Energy, KeV')
     #   ax2.set_xlim(min(self.E),max(self.E))
        
        plt.show()
                
    
    def ShiftComp(self, comp, shift):
        """ Функция деформирует спектр spe 
        comp - коэффициент сжатия растяжения 
        shift - сдвиг в каналах
        j=i*comp + shift
        """
        sp0=np.zeros_like(self.sp)
        for i in range(len(sp0)):
            start = i*comp+shift
            finish = (i+1)*comp+shift
            if start<0: start=0
            if finish<0: finish=0
            if start>=len(sp0): start=len(sp0)-1
            if finish>=len(sp0): finish=len(sp0)-1
            m=0
            m=self.sp[math.floor(start)]*(1-start%1)
            m=m-self.sp[math.floor(finish)]*(1-finish%1)
            for j in range(int(math.floor(start)+1),int(math.floor(finish))+1):
                m = m + self.sp[j]
            sp0[i]=m
        self.history.append(['Transform Shift='+str(shift)+' Comp='+str(comp)])
        self.sp = sp0.copy()
        return sp0
    
    def spread(self,a=None,b=None,c=None):
        """ Функция Spreading размазывает спектр 
        sigma = a*i^2+b*i+c
        """
        if a==None: 
            a=self.a_srd
        else:
            self.a_srd = a
        if b==None: 
            b=self.b_srd
        else:
            self.b_srd = b
        if c==None: 
            c=self.c_srd
        else:
            self.c_srd = c
            
        sp_srd=np.zeros_like(self.sp)
        l=len(self.sp)
        for i in range(l):
            start=i-100
            finish=i+100
            if (start<0):
                start=0
            if (finish>l-1):
                finish=l-1
            for j in range(start,finish):
                sigma=j*(a*j+b)+c
                if sigma!=0:
                    sigma2=1/(2*sigma*sigma)
                    sp_srd[i]=sp_srd[i]+self.sp[j]/(sigma*5.02)*(math.exp(-(i-j)*(i-j)*sigma2)+math.exp(-(i-j-1)*(i-j-1)*sigma2))
                else:
                    sp_srd[i]=self.sp[i]
                    break
        self.history.append(['Spread a='+str(a)+' b='+str(b)+' c='+str(c)])
        self.sp=sp_srd
        return sp_srd
    
    def save_spe(self, name=''):
        """ сохранение спектра в ормате SPE
        name - имя спектра
        """
        if (name == ''):
            name = self.name + '.spe'
        f = open(name,'w')
        f.write(str(self.type)+'\n')
        f.write(str(self.a)+'\n')
        f.write(str(self.b)+'\n')
        f.write(str(self.time)+'\n')
        for x in self.sp:
            f.write(str(x)+'\n')
        f.close()
        
    
    def save_json(self, name=''):
        """ сохраняет спектр в формате JSON """
        def mas2json(mas):
            if isinstance(mas, np.ndarray):
                return mas.tolist()
        if (name==''):
            name=self.name+'.json'
            with open(name, "w", encoding="utf-8") as file:
                json.dump(self.__dict__,file, default = mas2json, separators=(',', ':'), sort_keys=True, indent=4)
                
    def open_json(self,name):
        """ читает спектр в формате JSON """
        with open(name, "r") as file:
            data=json.load(file)
        #instance = object.__new__(self)
        for key, value in data.items():
            setattr(self, key, value)
            if key=='sp':
                self.sp=np.array(self.sp,dtype=float)
            if key=='E':
                self.E=np.array(self.E,dtype=float)
            
    def find_peaks(self,th=0.1,a=None,b=None,c=None):
        """
        Function for search pikin spectrum by wavevlet 
        A package for gamma-ray spectrum analysis and routine neutron activation analysis
        M E MEDHAT, A ABDEL-HAFIEZ, Z AWAAD and M A ALI
        th- threshold of sensitivity
        a,b,c -  paramets of spreding
        """
        if a==None: 
            a=self.a_srd
        else:
            self.a_srd = a
        if b==None: 
            b=self.b_srd
        else:
            self.b_srd = b
        if c==None: 
            c=self.c_srd
        else:
            self.c_srd = c
        # Производим свёртку с функцией-вейвлетом wv
        L=len(self.sp)
        I=np.arange(L)
        ca=np.zeros_like(self.sp)
        ca2=np.zeros_like(self.sp)
        wv=np.zeros_like(self.sp)
        for b in I:    # перебор всех значений сдвига
            a=self.a_srd*b*b+self.b_srd*b+self.c_srd
            t=(I-b)/a
            wv= (1 -t*t)*np.exp(-0.5*t*t)
            ca[b]=(1/a**0.5) * self.sp.dot(wv)
            ca2[b]=(1/a**0.5) * self.sp.dot(wv*wv)
        ca=ca/max(ca)
        ca[ca<th]=0
        di=5 # width windows for lokation peak
        self.ipeaks=np.array([])
        self.wpeaks=np.array([])
        for i in range(di+1,L-di):
            if ca[i]>0:
                if sum(ca[i-di:i+di]>ca[i])==0:
                    self.ipeaks=np.append(self.ipeaks,i)
                    self.wpeaks=np.append(self.wpeaks,ca[i])
        self.history.append(['fond peaks: '+str(self.ipeaks)])
        return self.ipeaks, self.wpeaks

# mnk
        
    def split(self,base,brd=None,tp=0):
        """
        Function for split spetrum for sum of spectrums from base 
        base - tuple of spectrums
        brd - tuple with boards like (left_board, right_board) in channal 
        tp = 0 - normal least-squares methods without same boundes 
        tp = 1 - non-negative least squares solver
        https://docs.scipy.org/doc/scipy/reference/optimize.html
        """
        bsd=np.zeros((len(base[0].sp),len(base)))
        for i,sp in enumerate(base):
            bsd[:,i]=sp.sp
        y=self.sp
        if brd!=None:
            bsd=bsd[brd[0]:brd[1],:]
            y=y[brd[0]:brd[1]]
        if tp == 0:
            return np.linalg.lstsq(bsd, y)[0]
        elif tp == 1:
            return scop.nnls(bsd,y)[0]
        
    def history_print(self):
        """метод выводит на экран историю спектра"""
        print('*** start history of '+self.name)
        for s in self.history:
            print(s)
        print('*** finish history of '+self.name)
            
            
# math for spectr
         
    def __mul__(self, k):
        """
        multiplication spectr by number k
        """
        sp=copy.copy(self)
        if type(k) in[float, int]:
            sp.sp=sp.sp*k
            sp.history.append('multiplication spectr ' +sp.name + ' by number '+str(k))
        return sp
    
    def __rmul__(self, k):
        """
        multiplication spectr by number k
        """
        sp=copy.copy(self)
        if type(k) in[float, int]:
            sp.sp=sp.sp*k
            sp.history.append('multiplication spectr ' +sp.name + ' by number '+str(k))
        return sp
    
    def __truediv__(self, k,time=None):
        """
        division spectr by number k
        """
        sp=copy.copy(self)
        if (type(k) in[float, int])and(k!=0):
            sp.sp=sp.sp/k
            sp.history.append('division spectr ' +sp.name + ' by number '+str(k))
        return sp
        
    
    def __radd__(self, k):
        """
        sum spectr by number k
        """
        sp=copy.copy(self)
        if type(k) in[float, int]:
            sp.sp=sp.sp+k
            sp.history.append('sum spectr ' +sp.name + ' by number '+str(k))
        elif (str(type(k)) == "<class 'SPINLib.spectr'>"):
            if len(sp.sp)>=len(k.sp):
                sp.sp = sp.sp[0:len(k.sp)]+k.sp
            else:
                sp.sp = sp.sp[0:len(k.sp)]+k.sp[0:len(sp.sp)]
            sp.history.append('sum spectr ' +sp.name + ' by spectr '+k.name)
        return sp
       
    def __add__(self, k):
        """
        sum spectr by number k
        """
        sp=copy.copy(self)
        if type(k) in[float, int]:
            sp.sp=sp.sp+k
            sp.history.append('sum spectr ' +sp.name + ' by number '+str(k))
        elif (str(type(k)) == "<class 'SPINLib.spectr'>"):
            if len(sp.sp)>=len(k.sp):
                sp.sp = sp.sp[0:len(k.sp)]+k.sp
            else:
                sp.sp = sp.sp[0:len(k.sp)]+k.sp[0:len(sp.sp)]
            sp.history.append('sum spectr ' +sp.name + ' by spectr '+k.name)
        return sp
    
    def __rsub__(self, k):
        """
        sub spectr by number k
        """
        sp=copy.copy(self)
        if type(k) in[float, int]:
            sp.sp=sp.sp-k
            sp.history.append('sum spectr ' +sp.name + ' by number '+str(k))
        elif (str(type(k)) == "<class 'SPINLib.spectr'>"):
            if len(sp.sp)>=len(k.sp):
                sp.sp = sp.sp[0:len(k.sp)]-k.sp
            else:
                sp.sp = sp.sp[0:len(k.sp)]-k.sp[0:len(sp.sp)]
            sp.history.append('sub spectr ' +sp.name + ' by spectr '+k.name)
        return sp
    
    def __sub__(self, k):
        """
        sub spectr by number k
        """
        sp=copy.copy(self)
        if type(k) in[float, int]:
            sp.sp=sp.sp-k
            sp.history.append('sum spectr ' +sp.name + ' by number '+str(k))
        elif (str(type(k)) == "<class 'SPINLib.spectr'>"):
            if len(sp.sp)>=len(k.sp):
                sp.sp = sp.sp[0:len(k.sp)]-k.sp
            else:
                sp.sp = sp.sp[0:len(k.sp)]-k.sp[0:len(sp.sp)]
            sp.history.append('sub spectr ' +sp.name + ' by spectr '+k.name)
        return sp
    
    
    
    

