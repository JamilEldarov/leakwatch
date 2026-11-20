@echo off
cd /d "C:\Users\Student\Desktop\leakwatch-starter"

if not exist logs mkdir logs

echo ==== Scan started: %date% %time% ==== >> logs\scan.log

".venv\Scripts\python.exe" -u run_scan.py --telegram >> logs\scan.log 2>&1

".venv\Scripts\python.exe" -u run_scan.py --pastes >> logs\scan.log 2>&1

echo ==== Scan completed: %date% %time% ==== >> logs\scan.log