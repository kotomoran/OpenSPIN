import struct
import numpy as np
import matplotlib.pyplot as plt

fin  = open('Cs+Co_AL=2.cmp', "rb").read()
#name
name=['','','','','','','','']
for j in range(2,10):
    fields=struct.unpack('1s', fin[j:j+1])
    print(j)
    if j%2==0:
        name[j-1]=fields[0].decode('utf-8')
    else:
        name[j-3]=fields[0].decode('utf-8')
str1 = ''.join(name)

fields=struct.unpack('<H', fin[10:10+2])
print('5 целая часть времени: '+str(fields[0]))
fields=struct.unpack('<H', fin[12:12+2])
print('6 длина спектра:'+str(fields[0]))
fields=struct.unpack('<H', fin[14:14+2])
print('7 дробная часть времени:'+str(fields[0]))

fields=struct.unpack('<H', fin[16:16+2])
print('Канал 1:'+str(fields[0]))

fields=struct.unpack('<H', fin[20:20+2])
print('Канал 2:'+str(fields[0]))

fields=struct.unpack('<H', fin[24:24+2])
print('E1:'+str(fields[0]))
fields=struct.unpack('<H', fin[26:26+2])
print('E1.:'+str(fields[0]))
fields=struct.unpack('<H', fin[28:28+2])
print('E1:'+str(fields[0]))
fields=struct.unpack('<H', fin[30:30+2])
print('E1.:'+str(fields[0]))
fields=struct.unpack('<b', fin[32:32+1])
print('День начала:'+str(fields[0]))
fields=struct.unpack('<b', fin[33:33+1])
print('День начала:'+str(fields[0]))

fields=struct.unpack('<b', fin[34:34+1])
print('День начала:'+str(fields[0]))
fields=struct.unpack('<b', fin[35:35+1])
print('День начала:'+str(fields[0]))

#31 Номер зонда
fields=struct.unpack('<H', fin[62:62+2])
print('Номер зонда:'+str(fields[0]))

shft=64
y=np.zeros((len(fin) - shft ) // 2)
for i in range((len(fin) - shft ) // 2 ):
    fields = struct.unpack('<H', fin[shft+2*i:shft+2*i+2])
   # print(str(i)+':'+str(fields[0]))
    dv=fields[0]//16384
    md=fields[0]%16384
    if (dv==0):
        y[i]=md
    elif (dv==1):
        y[i]=md*4
    elif (dv==2):
        y[i]=md*16
    elif (dv==3):
        y[i]=md*64

plt.plot(y)
"""
  
A1 := TempW div 16384;
    A2 := TempW mod 16384;
    A0 := 0;
    case A1 of
      0: A0 := A2;
      1: A0 := A2 * 4;
      2: A0 := A2 * 16;
      3: A0 := A2 * 64;
    end;

  //количество спектров одном кадре, для cpr
  //День начала                  and
Read(FileIn, TempW);
  Spec[Last].DateStart := '';
  Spec[Last].DateFinish := '';
  //       Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr(Lo(TempW) and 15);
  //       Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr((Lo(TempW) shr 4)and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr(Hi(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr((Hi(TempW) shr 4) and  15);
  //   Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr(Lo(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + ':';
  //Месяц начала
  //Год начала
Read(FileIn, TempW);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr((Lo(TempW) shr 4) and
    15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr(Lo(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + ':';
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr(Hi(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr((Hi(TempW) shr 4) and
    15);
  // Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr(Hi(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + ':';
  //Час начала
  //Минута начала
Read(FileIn, TempW);
  {    Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr((Hi(TempW) shr 4) and 15);
      Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr(Hi(TempW) and 15);
      Spec[Last].DateStart:=Spec[Last].DateStart+':';
      Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr((Lo(TempW) shr 4) and 15);
      Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr(Lo(TempW) and 15);
      }
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr(Lo(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr((Lo(TempW) shr 4) and
    15);
  Spec[Last].DateStart := Spec[Last].DateStart + ':';
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr(Hi(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr((Hi(TempW) shr 4) and
    15);
  Spec[Last].DateStart := Spec[Last].DateStart + ':';
  //Секунда начала
  //Час конца
Read(FileIn, TempW);
  {       Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr((Hi(TempW) shr 4) and 15);
         Spec[Last].DateStart:=Spec[Last].DateStart+IntToStr(Hi(TempW) and 15);
         Spec[Last].DateStart:=Spec[Last].DateStart+':';
         Spec[Last].DateFinish:=Spec[Last].DateFinish+IntToStr((Lo(TempW) shr 4) and 15);
         Spec[Last].DateFinish:=Spec[Last].DateFinish+IntToStr(Lo(TempW) and 15);
         Spec[Last].DateFinish:=Spec[Last].DateFinish+':';
  }

  Spec[Last].DateFinish := Spec[Last].DateFinish + IntToStr(Hi(TempW) and 15);
  Spec[Last].DateFinish := Spec[Last].DateFinish + IntToStr((Hi(TempW) shr 4)
    and
    15);
  Spec[Last].DateFinish := Spec[Last].DateFinish + ':';
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr(Lo(TempW) and 15);
  Spec[Last].DateStart := Spec[Last].DateStart + IntToStr((Lo(TempW) shr 4) and
    15);
  //       Spec[Last].DateStart:=Spec[Last].DateStart+':';

         //Минута конца
         //Секунда конца
Read(FileIn, TempW);
  Spec[Last].DateFinish := Spec[Last].DateFinish + IntToStr(Lo(TempW) and 15);
  Spec[Last].DateFinish := Spec[Last].DateFinish + IntToStr((Lo(TempW) shr 4)
    and
    15);
  Spec[Last].DateFinish := Spec[Last].DateFinish + ':';
  Spec[Last].DateFinish := Spec[Last].DateFinish + IntToStr(Hi(TempW) and 15);
  Spec[Last].DateFinish := Spec[Last].DateFinish + IntToStr((Hi(TempW) shr 4)
    and
    15);
  //       Spec[Last].DateFinish:=Spec[Last].DateFinish+':';
         //21 .. 25 Коментарий
  Spec[Last].Koment := '';
for i := 21 to 25 do
  begin
Read(FileIn, TempW);
    Spec[Last].Koment := Spec[Last].Koment + IntToStr(TempW);
  end;
  //26..28 Глубина
Read(FileIn, TempW);
  Spec[Last].Depth := Spec[Last].Depth + IntToStr(Lo(TempW) and 15) + ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr((Lo(TempW) shr 4) and 15) +
    ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr(Hi(TempW) and 15) + ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr((Hi(TempW) shr 4) and 15) +
    ':';
Read(FileIn, TempW);
  Spec[Last].Depth := Spec[Last].Depth + IntToStr(Lo(TempW) and 15) + ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr((Lo(TempW) shr 4) and 15) +
    ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr(Hi(TempW) and 15) + ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr((Hi(TempW) shr 4) and 15) +
    ':';
Read(FileIn, TempW);
  Spec[Last].Depth := Spec[Last].Depth + IntToStr(Lo(TempW) and 15) + ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr((Lo(TempW) shr 4) and 15) +
    ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr(Hi(TempW) and 15) + ':';
  Spec[Last].Depth := Spec[Last].Depth + IntToStr((Hi(TempW) shr 4) and 15) +
    ':';
  //29 Масса образца
Read(FileIn, TempW);
  //30 объем образца
Read(FileIn, TempW);
  //31 Номер зонда
Read(FileIn, TempW);
  //Далее считываем данные
  SetLength(Spec[Last].Data, 0);
  while not Eof(FileIn) do
  begin
    Read(FileIn, TempW);
    //     TempB1:=Hi(TempW);
    //     TempB2:=Lo(TempW);
    A1 := TempW div 16384;
    A2 := TempW mod 16384;
    A0 := 0;
    case A1 of
      0: A0 := A2;
      1: A0 := A2 * 4;
      2: A0 := A2 * 16;
      3: A0 := A2 * 64;
    end;
    SetLength(Spec[Last].Data, Length(Spec[Last].Data) + 1);
    Spec[Last].Data[High(Spec[Last].Data)] := A0;
    if Max < A0 then
      Max := A0;
  end;
  S1 := Spec[Last].DateStart;
  S2 := Spec[Last].DateFinish;
  S3 := Spec[Last].Name;
  if Max > 0 then
    for i := 0 to Length(Spec[Last].Data) - 1 do
      if Spec[Last].Data[i] <> 0 then
        PaintBox2.Canvas.Pixels[Trunc(i * 519 / Spec[Last].Length), Trunc(367 -
          Spec[Last].Data[i] * 367 / Max)] := clBlack;
  CloseFile(FileIn);
"""

