# ����Ƿ��Ѱ�װ Python
function CheckPythonInstalled() {
    $pythonVersion = "3.11"  # ָ��Ҫ��װ�� Python �汾
    $pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonInstalled -eq $null) {
        Write-Host "Python δ��װ�����ڰ�װ Python $pythonVersion ..."
        # ���� Python ��װ����ִ�а�װ����
        Start-Process -FilePath "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1"
        # �ȴ� Python ��װ���
        Start-Sleep -Seconds 300
    } else {
        Write-Host "Python �Ѱ�װ"
    }
}

# ����Ƿ��Ѱ�װָ���� Python ��
function CheckPythonPackageInstalled($packageName) {
    $package = Get-Package -Name $packageName -ErrorAction SilentlyContinue
    if ($package -ne $null) {
        Write-Host "$packageName �Ѱ�װ"
        return $true
    } else {
        Write-Host "$packageName δ��װ"
        return $false
    }
}

# ��װָ���� Python ��
function InstallPythonPackage($packageName) {
    Write-Host "���ڰ�װ $packageName ..."
    # ʹ�� pip ��װָ���� Python ��
    pip install $packageName
}

# ��鲢��װ Python
CheckPythonInstalled

# ��鲢��װ Python ��
$packages = @("opencv-python", "Pillow", "numpy", "pyautogui", "configparser")
foreach ($package in $packages) {
    if (!(CheckPythonPackageInstalled $package)) {
        InstallPythonPackage $package
    }
}

# ����ִ����������
Write-Host "�ű�ִ�����"
