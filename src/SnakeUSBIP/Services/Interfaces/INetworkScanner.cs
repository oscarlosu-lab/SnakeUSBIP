// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

namespace SnakeUSBIP.Services.Interfaces;

public interface INetworkScanner
{
    Task<List<string>> ScanNetworkAsync(string subnetBase);
}
