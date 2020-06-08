@echo off
title CALLER
taskkill /f /im chrome.exe
python scripts/call.py