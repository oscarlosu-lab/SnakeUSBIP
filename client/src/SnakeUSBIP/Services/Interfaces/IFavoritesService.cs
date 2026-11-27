// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025-2026 SnakeFoxu (OscarLosu) - GPL v3

using SnakeUSBIP.Models;

namespace SnakeUSBIP.Services.Interfaces;

public interface IFavoritesService
{
    List<FavoriteDevice> GetFavorites();
    OperationResult AddFavorite(string serverIP, string busId, string description, bool autoConnect = true, string receiveMode = "zero-copy");
    OperationResult AddFavorite(string serverIP, string busId, string description, bool autoConnect, string receiveMode, string? hardwareId, string? serverHostname = null, string? deviceSerial = null, string? revision = null);
    OperationResult RemoveFavorite(string serverIP, string busId);
    bool IsFavorite(string serverIP, string busId);
    Task<(string ServerIP, string BusId, bool ResolvedChanged)> ResolveFavoriteTargetAsync(FavoriteDevice favorite, CancellationToken ct = default);
    Task<List<FavoriteConnectResult>> ConnectFavoritesAsync();
}
