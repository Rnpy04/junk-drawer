#include <iostream>
#include <conio.h>  // برای _kbhit() و _getch()
#include <windows.h> // برای Sleep()
using namespace std;

cout << " helloo";
// const int WIDTH = 30;   // عرض صفحه
// const int HEIGHT = 20;  // ارتفاع صفحه
// int x = WIDTH / 2, y = HEIGHT - 2; // موقعیت سفینه
// bool running = true;

// void draw() {
//     system("cls"); // صفحه رو پاک کن
//     for (int i = 0; i < HEIGHT; i++) {
//         for (int j = 0; j < WIDTH; j++) {
//             if (i == y && j == x)
//                 cout << "A"; // سفینه
//             else
//                 cout << " ";
//         }
//         cout << "\n";
//     }
// }

// void input() {
//     if (_kbhit()) { // اگه کلیدی فشار داده شده
//         char key = _getch();
//         if (key == 'a' && x > 0) x--; // چپ
//         if (key == 'd' && x < WIDTH - 1) x++; // راست
//         if (key == 'w' && y > 0) y--; // بالا
//         if (key == 's' && y < HEIGHT - 1) y++; // پایین
//         if (key == 'q') running = false; // خروج
//     }
// }

// int main() {
//     while (running) {
//         draw();
//         input();
//         Sleep(50); // 50 میلی‌ثانیه مکث
//     }
//     return 0;
// }
