// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

namespace SnakeUSBIP.Services.Interfaces;

public interface ILocalizationService
{
    string GetText(string key, string language);
}
