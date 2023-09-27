@echo off
echo.-- Split off the first date token, i.e. day of the week
for /f %%a in ("%date%") do set d=%%a
echo.Date   : %date%
echo.d      : %d%
echo.

echo.-- Split the date into weekday, month, day, and year, using slash and space as delimiters
for /f "tokens=1,2,3,4 delims=/ " %%a in ("%date%") do set wday=%%a&set month=%%b&set day=%%c&set year=%%d
echo.Weekday: %wday%
echo.Month  : %month%
echo.Day    : %day%
echo.Year   : %year%