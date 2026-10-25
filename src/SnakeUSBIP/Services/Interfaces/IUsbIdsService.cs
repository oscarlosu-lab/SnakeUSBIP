// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

namespace SnakeUSBIP.Services.Interfaces;

public interface IUsbIdsService
{
    bool IsLoaded { get; }
    Task LoadFromFileAsync(string filePath);
    string GetVendor(string vendorId);
    string GetProduct(string vendorId, string productId);
    string GetDeviceName(string vendorId, string productId);  // alias → GetDeviceDescription
    string GetVendorName(string vendorId);                     // alias → GetVendor
    string GetDeviceDescription(string vendorId, string productId);
    void SetCustomName(string vendorId, string productId, string name);
    void LoadCustomNames(Dictionary<string, string>? names);
}
