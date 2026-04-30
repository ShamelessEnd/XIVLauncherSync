cls
@pushd %~dp0
@echo off
python SyncXIVLauncher.py 2
python LaunchXIV.py 2 %*
@popd