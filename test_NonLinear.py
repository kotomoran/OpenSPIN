import numpy as np

import matplotlib.pyplot as plt

import time
import SPINLib
       

start_time = time.time()
sp_sum=SPINLib.spectr()


sp_sum.open_spe(r'spe\gauss_sum.spe')

s=[r'spe\gauss_100.spe',
   r'spe\gauss_300.spe',
   r'spe\gauss_500.spe',
   r'spe\gauss_700.spe',
   r'spe\gauss_900.spe']
base = []
for nm in s:
    base.append(SPINLib.spectr())
    base[-1].open_spe(nm)
    
x=[i for i in range(1000)]
# for sp in base:
#     plt.plot(x, sp.sp)
plt.plot(x, sp_sum.sp)

print(sp_sum.split(base), sum(sp_sum.sp))
#-0.00007*I2*I2 + 0.99*I2 + 0.1
sp_sum.A1=0.1
sp_sum.A2=0.99
sp_sum.A3=-0.00007
sp_sum.ShiftComp(1,0,True)
print(sp_sum.split(base), sum(sp_sum.sp))
plt.plot(x, sp_sum.sp)

#sp3=SPINLib.spectr()
#sp1.plot_sp_lg()
#ip,wp=sp2.find_peaks(0.1,0,0.003,3)
#print(ip)
#
#for j in ip:
#    x, y = [j,j], [0, sp2.sp[int(j)]]
#    plt.plot(x, y)
#

#sp2.open_spe('spe\g4_Cs_60.spe')
##sp3.open_spe('spe\Pb.12mm.spe')
#sp3 = sp1*2.222+sp2*3.333
#sp2=sp1*3
#x=sp3.split((sp1,sp2),(100,500),1)
#print(x)
#ind=np.arange(len(sp1.sp))
#plt.plot(ind,sp1.sp,'.')
#plt.plot(ind,sp2.sp,'.')
#plt.plot(ind,sp3.sp,'-')

#plt.plot(ind,sp2.sp,'.-')

#plt.plot(ind,sp1.sp,'.-')

#sp.open_cmp('Cs+Co_AL=2.cmp')
#sp0=sp.ShiftComp(-10,2)
#sp1=sp.spread(0,0.003,3)
#sp.find_peaks()
#print(sp.peaks)
#ind=np.arange(len(sp0))
#plt.plot(ind,sp0,'.-')
#plt.plot(ind,sp.sp,'.-')
#plt.plot(ind,sp1,'.-')
#print(sp.history)
#sp.save_json()
 

print("--- %s seconds ---" % (time.time() - start_time))

