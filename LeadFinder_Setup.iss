; -----------------------
; LeadFinder Installer Script
; By Caarya
; -----------------------

[Setup]
AppName=LeadFinder
AppVersion=1.0
AppPublisher=Caarya
DefaultDirName={pf}\Caarya\LeadFinder
DefaultGroupName=LeadFinder
OutputDir=.
OutputBaseFilename=LeadFinder_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=leadfinder.ico
WizardStyle=modern
DisableWelcomePage=no
PrivilegesRequired=admin

[Files]
Source: "lead_scraping.exe"; DestDir: "{app}"; DestName: "LeadFinder.exe"; Flags: ignoreversion
Source: "leadfinder.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\LeadFinder"; Filename: "{app}\LeadFinder.exe"; IconFilename: "{app}\leadfinder.ico"
Name: "{commondesktop}\LeadFinder"; Filename: "{app}\LeadFinder.exe"; IconFilename: "{app}\leadfinder.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Run]
Filename: "{app}\LeadFinder.exe"; Description: "Launch LeadFinder"; Flags: nowait postinstall skipifsilent

[LicenseFile]
LicenseFile=license.txt
