// SnakeUSBIP - github.com/oscarlosu-lab/SnakeUSBIP
// (c) 2025 SnakeFoxu - GPL v3

using SnakeUSBIP.Models;

namespace SnakeUSBIP.Services.Interfaces;

public interface IConfigService
{
    AppConfig Load();
    void Save(AppConfig config);
    void SetLanguage(string language);
}
