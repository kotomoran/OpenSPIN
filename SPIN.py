import numpy as np

import matplotlib.pyplot as plt

import time
import SPINLib
       

start_time = time.time()
sp1=SPINLib.spectr()
sp3=SPINLib.spectr(1024)

s=[r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N01-build\014_00-N01-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N02-build\014_00-N02-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N03-build\014_00-N03-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N04-build\014_00-N04-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N05-build\014_00-N05-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N06-build\014_00-N06-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N07-build\014_00-N07-build.spe',
   r'c:\MailCloud\vniia\geant_vniia\NeutronLaBr\15new\014_00-N08-build\014_00-N08-build.spe']
for nm in s:
    sp1.open_spe(nm)
    sp3=sp3+sp1
    print(sp1.name)

sp3.spread(0,0.003,3)
sp3.plot_sp_line()

sp=SPINLib.spectr()
sp.open_spe(r'c:\MailCloud\vniia\geant_vniia\GammaLaBr\exp\123_h2o_4000s.spe')
n=220
sp=sp/(float(sp.sp[n]/sp3.sp[n]))
sp.plot_sp_lg()
    
#sp1=SPINLib.spectr()
sp2=SPINLib.spectr()
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

