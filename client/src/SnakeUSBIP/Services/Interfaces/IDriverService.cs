// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025-2026 SnakeFoxu (OscarLosu) - GPL v3

using SnakeUSBIP.Models;

namespace SnakeUSBIP.Services.Interfaces;

public interface IDriverService
{
    string GetDriverStatus();
    Task<bool> IsDriverInstalledAsync();
    Task<bool> InstallDriverAsync();
    Task<bool> UninstallDriverAsync();
}
