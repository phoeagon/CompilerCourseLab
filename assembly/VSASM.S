#include "stdafx.h"

void my_qsort(int a[], int l, int r) {
001B14A0  push        ebp  
001B14A1  mov         ebp,esp  
001B14A3  sub         esp,0F0h  
001B14A9  push        ebx  
001B14AA  push        esi  
001B14AB  push        edi  
001B14AC  lea         edi,[ebp-0F0h]  
001B14B2  mov         ecx,3Ch  
001B14B7  mov         eax,0CCCCCCCCh  
001B14BC  rep stos    dword ptr es:[edi]  
	int pivot = a[l];
001B14BE  mov         eax,dword ptr [l]  
001B14C1  mov         ecx,dword ptr [a]  
001B14C4  mov         edx,dword ptr [ecx+eax*4]  
001B14C7  mov         dword ptr [pivot],edx  
	int i = l;
001B14CA  mov         eax,dword ptr [l]  
001B14CD  mov         dword ptr [i],eax  
	int j = r;
001B14D0  mov         eax,dword ptr [r]  
001B14D3  mov         dword ptr [j],eax  

	while (i <= j) {
001B14D6  mov         eax,dword ptr [i]  
001B14D9  cmp         eax,dword ptr [j]  
001B14DC  jg          my_qsort+0B6h (1B1556h)  
		while (a[i] < pivot)
001B14DE  mov         eax,dword ptr [i]  
001B14E1  mov         ecx,dword ptr [a]  
001B14E4  mov         edx,dword ptr [ecx+eax*4]  
001B14E7  cmp         edx,dword ptr [pivot]  
001B14EA  jge         my_qsort+57h (1B14F7h)  
			i++;
001B14EC  mov         eax,dword ptr [i]  
001B14EF  add         eax,1  
001B14F2  mov         dword ptr [i],eax  
001B14F5  jmp         my_qsort+3Eh (1B14DEh)  
		while (a[j] > pivot)
001B14F7  mov         eax,dword ptr [j]  
001B14FA  mov         ecx,dword ptr [a]  
001B14FD  mov         edx,dword ptr [ecx+eax*4]  
001B1500  cmp         edx,dword ptr [pivot]  
001B1503  jle         my_qsort+70h (1B1510h)  
			j--;
001B1505  mov         eax,dword ptr [j]  
001B1508  sub         eax,1  
001B150B  mov         dword ptr [j],eax  
001B150E  jmp         my_qsort+57h (1B14F7h)  
		if (i <= j) {
001B1510  mov         eax,dword ptr [i]  
001B1513  cmp         eax,dword ptr [j]  
001B1516  jg          my_qsort+0B4h (1B1554h)  
			int t = a[i];
001B1518  mov         eax,dword ptr [i]  
001B151B  mov         ecx,dword ptr [a]  
001B151E  mov         edx,dword ptr [ecx+eax*4]  
001B1521  mov         dword ptr [t],edx  
			a[i] = a[j];
001B1524  mov         eax,dword ptr [i]  
001B1527  mov         ecx,dword ptr [a]  
001B152A  mov         edx,dword ptr [j]  
001B152D  mov         esi,dword ptr [a]  
001B1530  mov         edx,dword ptr [esi+edx*4]  
001B1533  mov         dword ptr [ecx+eax*4],edx  
			a[j] = t;
001B1536  mov         eax,dword ptr [j]  
001B1539  mov         ecx,dword ptr [a]  
001B153C  mov         edx,dword ptr [t]  
001B153F  mov         dword ptr [ecx+eax*4],edx  
			i++;
001B1542  mov         eax,dword ptr [i]  
001B1545  add         eax,1  
001B1548  mov         dword ptr [i],eax  
			j--;
001B154B  mov         eax,dword ptr [j]  
001B154E  sub         eax,1  
001B1551  mov         dword ptr [j],eax  
		}
	}
001B1554  jmp         my_qsort+36h (1B14D6h)  
	if (l < j)
001B1556  mov         eax,dword ptr [l]  
001B1559  cmp         eax,dword ptr [j]  
001B155C  jge         my_qsort+0D2h (1B1572h)  
		my_qsort(a, l, j);
001B155E  mov         eax,dword ptr [j]  
001B1561  push        eax  
001B1562  mov         ecx,dword ptr [l]  
001B1565  push        ecx  
001B1566  mov         edx,dword ptr [a]  
001B1569  push        edx  
001B156A  call        my_qsort (1B105Fh)  
001B156F  add         esp,0Ch  
	if (i < r)
001B1572  mov         eax,dword ptr [i]  
001B1575  cmp         eax,dword ptr [r]  
001B1578  jge         my_qsort+0EEh (1B158Eh)  
		my_qsort(a, i, r);
001B157A  mov         eax,dword ptr [r]  
001B157D  push        eax  
001B157E  mov         ecx,dword ptr [i]  
001B1581  push        ecx  
001B1582  mov         edx,dword ptr [a]  
001B1585  push        edx  
001B1586  call        my_qsort (1B105Fh)  
001B158B  add         esp,0Ch  
}
001B158E  pop         edi  
001B158F  pop         esi  
001B1590  pop         ebx  
001B1591  add         esp,0F0h  
001B1597  cmp         ebp,esp  
001B1599  call        @ILT+415(__RTC_CheckEsp) (1B11A4h)  
001B159E  mov         esp,ebp  
001B15A0  pop         ebp  
001B15A1  ret