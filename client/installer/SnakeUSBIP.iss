; SnakeUSBIP Inno Setup Script
; Copyright (c) 2025-2026 SnakeFoxu (OscarLosu)

#define MyAppName "SnakeUSBIP"
#define MyAppVersion "3.2.0"
#define MyAppPublisher "SnakeFoxu (OscarLosu)"
#define MyAppURL "https://github.com/oscarlosu-lab/SnakeUSBIP"
#define MyAppExeName "SnakeUSBIP.exe"

[Setup]
AppId={{B8F3D2A1-5E7C-4D9A-8B2E-1F6C3A9D0E5B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=SnakeUSBIP_Setup_v{#MyAppVersion}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
AppMutex=SnakeUSBIP_SingleInstance_Mutex
CloseApplications=yes
CloseApplicationsFilter=*.exe,*.dll
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
UsedUserAreasWarning=no
; WizardImageFile and WizardSmallImageFile removed - using Inno Setup defaults

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Iniciar con Windows"; GroupDescription: "Opciones adicionales:"; Flags: unchecked
Name: "installdrivers"; Description: "Instalar drivers USB/IP (requiere reinicio)"; GroupDescription: "Configuración de drivers:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\usb.ids"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\usbipw.exe"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\devnode.exe"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\libusbip.dll"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\resources.dll"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\CleanDrivers.ps1"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#SourceDir}\drivers\*"; DestDir: "{app}\drivers"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist
Source: "{#SourceDir}\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"" --minimized"; Flags: uninsdeletevalue; Tasks: startupicon

[Run]
; Install USB/IP drivers if selected (remove any previous UDE node first to prevent duplicates)
Filename: "pnputil.exe"; Parameters: "/add-driver ""{app}\drivers\usbip2_filter.inf"" /install"; StatusMsg: "Instalando filtro USB/IP..."; Tasks: installdrivers; Flags: runhidden waituntilterminated
Filename: "{app}\devnode.exe"; Parameters: "remove ROOT\USBIP_WIN2\UDE root"; StatusMsg: "Limpiando nodos virtuales previos..."; Tasks: installdrivers; Flags: runhidden waituntilterminated skipifdoesntexist
Filename: "{app}\devnode.exe"; Parameters: "install ""{app}\drivers\usbip2_ude.inf"" ROOT\USBIP_WIN2\UDE"; StatusMsg: "Instalando controlador emulado USB/IP (UDE)..."; Tasks: installdrivers; Flags: runhidden waituntilterminated skipifdoesntexist
; Launch application
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser

[UninstallRun]
; Ensure tray process is terminated and clean up UDE device node before deleting files
Filename: "taskkill.exe"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden waituntilterminated; RunOnceId: "StopSnakeUSBIP"
Filename: "{app}\devnode.exe"; Parameters: "remove ROOT\USBIP_WIN2\UDE root"; Flags: runhidden waituntilterminated skipifdoesntexist; RunOnceId: "RemoveUdeNode"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\temp"
Type: filesandordirs; Name: "{app}\data"
