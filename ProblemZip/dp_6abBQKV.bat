@echo off
:loop
	C:\Users\yuan\Desktop\test\rand.exe > data.txt
	C:\Users\yuan\Desktop\test\my_program.exe < data.txt > WA.txt
	C:\Users\yuan\Desktop\test\AC_program.exe < data.txt > AC.txt
	fc WA.txt AC.txt
	if not errorlevel 1 goto loop
pause
goto loop
