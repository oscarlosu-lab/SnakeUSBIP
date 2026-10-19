// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

using SnakeUSBIP.Models;

namespace SnakeUSBIP.Services.Interfaces;

public interface IDriverService
{
    string GetDriverStatus();
    Task<bool> IsDriverInstalledAsync();
    Task<bool> InstallDriverAsync();
    Task<bool> UninstallDriverAsync();
}
