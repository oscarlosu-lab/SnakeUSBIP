// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

using SnakeUSBIP.Models;

namespace SnakeUSBIP.Services.Interfaces;

public interface IUpdateService
{
    Task<UpdateInfo> CheckForUpdatesAsync(CancellationToken ct = default);
    Task<OperationResult> StartUpdateAsync(
        string downloadUrl,
        string installerName,
        string? hashUrl = null,
        IProgress<double>? progress = null,
        CancellationToken ct = default);
}
