# 检查是否已安装 Python
function CheckPythonInstalled() {
    $pythonVersion = "3.11"  # 指定要安装的 Python 版本
    $pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonInstalled -eq $null) {
        Write-Host "Python 未安装，正在安装 Python $pythonVersion ..."
        # 下载 Python 安装程序并执行安装步骤
        Start-Process -FilePath "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1"
        # 等待 Python 安装完成
        Start-Sleep -Seconds 300
    } else {
        Write-Host "Python 已安装"
    }
}

# 检查是否已安装指定的 Python 包
function CheckPythonPackageInstalled($packageName) {
    $package = Get-Package -Name $packageName -ErrorAction SilentlyContinue
    if ($package -ne $null) {
        Write-Host "$packageName 已安装"
        return $true
    } else {
        Write-Host "$packageName 未安装"
        return $false
    }
}

# 安装指定的 Python 包
function InstallPythonPackage($packageName) {
    Write-Host "正在安装 $packageName ..."
    # 使用 pip 安装指定的 Python 包
    pip install $packageName
}

# 检查并安装 Python
CheckPythonInstalled

# 检查并安装 Python 包
$packages = @("opencv-python", "Pillow", "numpy", "pyautogui", "configparser")
foreach ($package in $packages) {
    if (!(CheckPythonPackageInstalled $package)) {
        InstallPythonPackage $package
    }
}

# 继续执行其他操作
Write-Host "脚本执行完毕"
