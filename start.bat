set proj_base=%cd%
set wpf_name=WpfApplication1
set env=palace
cd ..
if not exist %wpf_name% (
    echo The WPF program not found
    exit
)

set wpf_root=%cd%\%wpf_name%
:: activate virtual environment
set vir_env=%env%\Scripts\activate.bat
call %vir_env%

cd %proj_base%

python run.py %wpf_root%

PAUSE