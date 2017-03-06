set proj_base=%cd%
set wpf_name=WpfApplication1
cd ..
if not exist %wpf_name% (
    echo The WPF program not found
    exit
)

set wpf_root=%cd%\%wpf_name%

cd %proj_base%

python run.py %wpf_root%

PAUSE