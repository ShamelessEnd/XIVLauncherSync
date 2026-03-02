cls
@pushd %~dp0
@echo off
python SyncXIVLauncher.py
start "" /d "%USERPROFILE%\AppData\Local\XIVLauncher" "%USERPROFILE%\AppData\Local\XIVLauncher\XIVLauncher.exe" --roamingPath="%APPDATA%\XIVLauncher"
@popd