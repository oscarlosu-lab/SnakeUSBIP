// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

using System;
using System.IO;
using SnakeUSBIP.Services.Interfaces;

namespace SnakeUSBIP.Services;

/// <summary>
/// Resolves all application paths.
/// Portable mode: everything lives next to the .exe
/// Installed mode: data goes to %AppData%\SnakeUSBIP
/// </summary>
public class EnvironmentService : IEnvironmentService
{
    private string _appDataPath = string.Empty;

    public string AppDataPath => _appDataPath;
    public string LogsPath    => Path.Combine(_appDataPath, "logs");
    public string TempPath    => Path.Combine(_appDataPath, "temp");
    public bool   IsPortableMode { get; private set; }
    public bool   IsPortable     => IsPortableMode;

    /// <summary>
    /// BinPath: where usbipw.exe lives.
    /// Portable → next to exe (BaseDirectory). Installed → BaseDirectory/bin.
    /// </summary>
    public string BinPath
    {
        get
        {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            // Prefer BaseDirectory/bin if it contains usbip binaries
            var subDir = Path.Combine(baseDir, "bin");
            if (Directory.Exists(subDir) && 
                (File.Exists(Path.Combine(subDir, "usbipw.exe")) || 
                 File.Exists(Path.Combine(subDir, "usbip.exe"))))
                return subDir;
            // Fallback: binaries next to exe (portable layout)
            return baseDir;
        }
    }

    /// <summary>
    /// DriversPath: where .inf/.sys driver files live.
    /// </summary>
    public string DriversPath
    {
        get
        {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            var subDir = Path.Combine(baseDir, "drivers");
            if (Directory.Exists(subDir)) return subDir;
            // Fallback: BaseDirectory itself
            return baseDir;
        }
    }

    public void Initialize()
    {
        // Portable mode STRICT: only if "portable.flag" exists next to the exe
        var baseDir   = AppDomain.CurrentDomain.BaseDirectory;
        var portFlag  = Path.Combine(baseDir, "portable.flag");
        var dataLocal = Path.Combine(baseDir, "data");

        IsPortableMode = File.Exists(portFlag);

        _appDataPath = IsPortableMode
            ? dataLocal
            : Path.Combine(
                System.Environment.GetFolderPath(System.Environment.SpecialFolder.ApplicationData),
                "SnakeUSBIP");

        EnsureDirectories();
        CleanTempDirectory();
    }

    public string GetConfigFilePath() => Path.Combine(_appDataPath, "config.json");

    // ── private ──────────────────────────────────────────────────────────────

    private void EnsureDirectories()
    {
        foreach (var dir in new[] { _appDataPath, LogsPath, TempPath })
        {
            if (!Directory.Exists(dir))
                Directory.CreateDirectory(dir);
        }
    }

    private void CleanTempDirectory()
    {
        try
        {
            if (Directory.Exists(TempPath))
            {
                var files = Directory.GetFiles(TempPath);
                foreach (var file in files)
                {
                    try
                    {
                        File.Delete(file);
                    }
                    catch
                    {
                        // Ignore files in use
                    }
                }
            }
        }
        catch
        {
            // Fail silently on IO errors during cleanup
        }
    }
}
