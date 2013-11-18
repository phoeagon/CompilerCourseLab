// compiler-qsort.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"

void my_qsort(int a[], int l, int r) {
	int pivot = a[l];
	int i = l;
	int j = r;

	while (i <= j) {
		while (a[i] < pivot)
			i++;
		while (a[j] > pivot)
			j--;
		if (i <= j) {
			int t = a[i];
			a[i] = a[j];
			a[j] = t;
			i++;
			j--;
		}
	}
	if (l < j)
		my_qsort(a, l, j);
	if (i < r)
		my_qsort(a, i, r);
}

int _tmain(int argc, _TCHAR* argv[])
{
	int arr[10];
	for (int i = 0; i < 10; i++) {
		std::cin >> arr[i];
	}
	my_qsort(arr, 0, 9);
	for (int i = 0; i < 10; i++) {
		std::cout << arr[i] << " ";
	}
	std::cout << std::endl;

	char a;
	std::cin >> a;
	return 0;
}

