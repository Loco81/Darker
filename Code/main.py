import subprocess, darkdetect, os, sys, time, datetime
from startup import set_autostart_registry, check_autostart_registry


if not check_autostart_registry('Darker'):
    set_autostart_registry("Darker", sys.argv[0], autostart=True)

def time_diff(start, end):
    if isinstance(start, datetime.time): # convert to datetime
        assert isinstance(end, datetime.time)
        start, end = [datetime.datetime.combine(datetime.datetime.min, t) for t in [start, end]]
    if start <= end: # e.g., 10:33:26-11:15:49
        return end - start
    else: # end < start e.g., 23:55:00-00:25:00
        end += datetime.timedelta(1) # +day
        assert end > start
        return end - start


while True:
    if not os.path.exists('Config.txt'):    
        file = open('Config.txt', 'w')
        file.write('dark_start=19:00\ndark_end=07:00')
        file.close()
        start, end = '19:00', '07:00'
    else:
        file = open('Config.txt', 'r')
        start = file.readline().strip('\n').split('=')[1]
        end = file.readline().strip('\n').split('=')[1]
        file.close()


    current = str(datetime.datetime.now().time()).split(':')[0]+':'+str(datetime.datetime.now().time()).split(':')[1]

    tm = str(time_diff(datetime.datetime.strptime(start, '%H:%M'), datetime.datetime.strptime(current, '%H:%M')))
    tm2 = str(time_diff(datetime.datetime.strptime(current, '%H:%M'), datetime.datetime.strptime(end, '%H:%M')))
    if (float(tm.split(':')[0]+'.'+tm.split(':')[1]) + float(tm2.split(':')[0]+'.'+tm2.split(':')[1])) < 24.0:
        if darkdetect.isLight():
            print(subprocess.getstatusoutput('powershell.exe Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 0')[1])
            print(subprocess.getstatusoutput('powershell.exe Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 0')[1])
            print(subprocess.getstatusoutput("powershell.exe Set-ItemProperty -Path HKCU:\Software\Microsoft\Office\16.0\Common -Name 'UI Theme' -Value 4")[1])
            print(subprocess.getstatusoutput("powershell.exe Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Office\16.0\Common\Roaming\Identities\<<MODIFY_USERNAME_HERE>>\Settings\1186\{00000000-0000-0000-0000-000000000000}\PendingChanges' -Name 'Data' -Value ([byte[]](4, 0, 0, 0)) -Type Binary")[1])
            subprocess.getstatusoutput("taskkill /f /im explorer.exe")
            os.startfile("C:\\Windows\\explorer.exe")
    else:
        if darkdetect.isDark():
            print(subprocess.getstatusoutput('powershell.exe Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 1')[1])
            print(subprocess.getstatusoutput('powershell.exe Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 1')[1])
            print(subprocess.getstatusoutput("powershell.exe Set-ItemProperty -Path HKCU:\Software\Microsoft\Office\16.0\Common -Name 'UI Theme' -Value 0")[1])
            print(subprocess.getstatusoutput("powershell.exe Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Office\16.0\Common\Roaming\Identities\<<MODIFY_USERNAME_HERE>>\Settings\1186\{00000000-0000-0000-0000-000000000000}\PendingChanges' -Name 'Data' -Value ([byte[]](0, 0, 0, 0)) -Type Binary")[1])
            subprocess.getstatusoutput("taskkill /f /im explorer.exe")
            os.startfile("C:\\Windows\\explorer.exe")

    time.sleep(60)
