// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025-2026 SnakeFoxu (OscarLosu) - GPL v3

namespace SnakeUSBIP.Services.Interfaces;

public interface ILocalizationService
{
    string GetText(string key, string language);
    string GetText(string key, string language, params object[] args);
}
