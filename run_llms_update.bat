@echo off
echo Starting Lively LLMS.txt update process...
cd /d "C:\Users\ldron\OneDrive\Documenten\Lively Website - Webflow\llms"

echo.
echo [1/2] Generating llms.txt from website content...
python update_llms_txt.py

echo.
echo [2/2] Uploading llms.txt to website...
python auto_upload_llms.py

echo.
echo ✅ Process completed at %date% %time%
echo.
echo Press any key to close...
pause 