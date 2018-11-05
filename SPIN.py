import numpy as np

import matplotlib.pyplot as plt

import time
import SPINLib
       

start_time = time.time()
sp1=SPINLib.spectr()
sp2=SPINLib.spectr()
sp3=SPINLib.spectr()
sp1.open_spe('spe\g4_Co_60.spe')
sp2.open_spe('spe\g4_Cs_60.spe')
sp3.open_spe('spe\Pb.12mm.spe')
sp3 = sp1*2.222+sp2*3.333
#sp2=sp1*3
x=sp3.split((sp1,sp2),(100,500),1)
print(x)
ind=np.arange(len(sp1.sp))
plt.plot(ind,sp1.sp,'.')
plt.plot(ind,sp2.sp,'.')
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

