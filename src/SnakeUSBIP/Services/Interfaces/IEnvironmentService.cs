// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

namespace SnakeUSBIP.Services.Interfaces;

/// <summary>
/// Provides resolved paths for all app directories (Data, Logs, Bin, Drivers, Temp, Config)
/// </summary>
public interface IEnvironmentService
{
    /// <summary>App data root (portable: next to exe | installed: %AppData%\SnakeUSBIP)</summary>
    string AppDataPath { get; }
    string LogsPath { get; }
    string BinPath { get; }
    string DriversPath { get; }
    string TempPath { get; }

    string GetConfigFilePath();
    void Initialize();
    bool IsPortableMode { get; }
    bool IsPortable { get; }
}
