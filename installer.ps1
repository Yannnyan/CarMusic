$dest_dir = "$env:appdata\CarMusic"
$source_dir = "$PSScriptRoot"
$exe_files = (get-childitem -Path $source_dir -Depth 0 | Where-Object { $_.Name -like "*.exe"})
if (($exe_files | Measure-Object).Count -gt 1)
{
    exit 1
}
$target_name = $exe_files[0].Name
$shortcut_path = ($pwd.Path + "\" + $target_name.split('.')[0] + ".lnk")

if (Test-Path -Path $dest_dir)
    {Remove-Item -Force -Recurse -Path $dest_dir}
mkdir $dest_dir
Copy-Item -Recurse -Force -Path "$source_dir\*" -Destination $dest_dir
if ((Test-Path -Path $shortcut_path))
    {Remove-Item -Force -Path $shortcut_path}
$shell = New-Object -comObject WScript.Shell
$shortcut_exe = $shell.CreateShortCut($shortcut_path)
$shortcut_exe.TargetPath = "$dest_dir\$target_name"
$shortcut_exe.Save()
powershell.exe "$dest_dir\$target_name"
