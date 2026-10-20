#define MyAppName "YouTube Downloader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Oldrey"
#define MyAppExeName "YouTubeDownloader.exe"
#define MyAppIcon "icono.ico"

[Setup]
AppId={{8F7E5D92-3A41-4F6B-9C25-YOUTUBE-DOWNLOADER}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\YouTube Downloader
DefaultGroupName=YouTube Downloader

OutputDir=installer
OutputBaseFilename=YouTube Downloader Setup

SetupIconFile={#MyAppIcon}

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

UninstallDisplayName=YouTube Downloader

DisableProgramGroupPage=yes

[Files]

; Aplicación completa generada por PyInstaller
Source: "dist\YouTubeDownloader\*"; \
DestDir: "{app}"; \
Flags: recursesubdirs createallsubdirs

; Icono de la aplicación
Source: "icono.ico"; \
DestDir: "{app}"; \
Flags: ignoreversion

[Icons]

; Acceso directo en el escritorio
Name: "{autodesktop}\YouTube Downloader"; \
Filename: "{app}\YouTubeDownloader.exe"; \
IconFilename: "{app}\icono.ico"

; Acceso directo en el menú Inicio
Name: "{autoprograms}\YouTube Downloader"; \
Filename: "{app}\YouTubeDownloader.exe"; \
IconFilename: "{app}\icono.ico"