$MP4_PATH = If ($null -ne $Env:DOWNLOAD_DESTINATION) {$Env:DOWNLOAD_DESTINATION} Else {'E:\mp3'}

$mp4_files = (Get-ChildItem -Path $MP4_PATH | Where-Object {$_.Name -like '*`.mp4'}).Name
foreach ($mp4_file in $mp4_files)
{
    $full_path = (Join-Path -Path $MP4_PATH -ChildPath $mp4_file)
    ffmpeg.exe -i $full_path -vn (Join-Path -Path $MP4_PATH -ChildPath ($mp4_file.split('.')[0] + '.mp3'))
    Remove-Item -Path $full_path
}
