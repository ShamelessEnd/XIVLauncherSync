cls
@pushd %~dp0
@echo off
python SyncXIVLauncher.py 3
python LaunchXIV.py 3
@popd