using System.Diagnostics;
using System.Security.Principal;
using System.Threading;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using SnakeUSBIP.Services;
using SnakeUSBIP.Services.Interfaces;
using SnakeUSBIP.ViewModels;

namespace SnakeUSBIP;

/// <summary>
/// App entry — Auto-elevation + Single instance (Mutex) + DI container
/// Uses programmatic elevation to avoid .NET 9 WPF crash with requireAdministrator manifest.
/// </summary>
public partial class App : System.Windows.Application
{
    private static Mutex? _mutex;
    private const string MutexName = "SnakeUSBIP_SingleInstance_Mutex";
    public IServiceProvider ServiceProvider { get; private set; } = null!;

    protected override void OnStartup(StartupEventArgs e)
    {
        try
        {
            // ── STEP 1: Auto-elevate if not admin ──────────────────────────
            if (!IsRunningAsAdmin())
            {
                try
                {
                    var exePath = Process.GetCurrentProcess().MainModule?.FileName
                                  ?? System.Environment.ProcessPath
                                  ?? throw new InvalidOperationException("Cannot determine executable path.");

                    var psi = new ProcessStartInfo
                    {
                        FileName = exePath,
                        Verb = "runas",
                        UseShellExecute = true
                    };
                    Process.Start(psi);
                }
                catch (System.ComponentModel.Win32Exception)
                {
                    // User declined UAC — exit silently
                }
                catch (Exception ex)
                {
                    System.Windows.MessageBox.Show(
                        $"No se pudo elevar a administrador:\n{ex.Message}",
                        "SnakeUSBIP", MessageBoxButton.OK, MessageBoxImage.Warning);
                }

                Shutdown();
                return;
            }

            // ── STEP 2: Single instance guard ──────────────────────────────
            _mutex = new Mutex(true, MutexName, out bool createdNew);
            if (!createdNew)
            {
                System.Windows.MessageBox.Show(
                    "SnakeUSBIP ya está en ejecución.\nRevisa la bandeja del sistema.",
                    "SnakeUSBIP",
                    MessageBoxButton.OK,
                    MessageBoxImage.Information);
                Shutdown();
                return;
            }

            // ── STEP 3: Build DI container ─────────────────────────────────
            var services = new ServiceCollection();
            ConfigureServices(services);
            ServiceProvider = services.BuildServiceProvider();

            // Initialize core services — order matters
            ServiceProvider.GetRequiredService<IEnvironmentService>().Initialize();
            ServiceProvider.GetRequiredService<ILoggerService>().Initialize();
            
            // Create and show MainWindow via DI
            var mainWindow = ServiceProvider.GetRequiredService<MainWindow>();
            mainWindow.Show();

            base.OnStartup(e);
        }
        catch (Exception ex)
        {
            System.Windows.MessageBox.Show(
                $"Critical Startup Error: {ex.Message}\n\n{ex.InnerException?.Message}\n\n{ex.StackTrace}", 
                "Fatal Error", 
                MessageBoxButton.OK, 
                MessageBoxImage.Error);
            Shutdown();
        }
    }

    private static void ConfigureServices(IServiceCollection services)
    {
        // Microsoft.Extensions.Logging
        services.AddLogging(b => b.AddConsole().SetMinimumLevel(LogLevel.Debug));

        // Core infrastructure
        services.AddSingleton<IEnvironmentService, EnvironmentService>();
        services.AddSingleton<ILoggerService, LoggerService>();
        services.AddSingleton<IConfigService, ConfigService>();

        // Domain services
        services.AddSingleton<IUsbipService, UsbipService>();
        services.AddSingleton<IUpdateService, UpdateService>();
        services.AddSingleton<IVpnService, VpnService>();
        services.AddSingleton<IDriverService, DriverService>();
        services.AddSingleton<IUsbIdsService, UsbIdsService>();
        services.AddSingleton<ILocalizationService, LocalizationService>();
        services.AddSingleton<IFavoritesService, FavoritesService>();
        services.AddSingleton<IConnectionMonitorService, ConnectionMonitorService>();
        services.AddSingleton<INetworkScanner, NetworkScanner>();

        // ViewModels
        services.AddSingleton<MainViewModel>();

        // UI
        services.AddTransient<MainWindow>();
    }

    /// <summary>
    /// Check if the current process is running with administrator privileges.
    /// </summary>
    private static bool IsRunningAsAdmin()
    {
        using var identity = WindowsIdentity.GetCurrent();
        var principal = new WindowsPrincipal(identity);
        return principal.IsInRole(WindowsBuiltInRole.Administrator);
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _mutex?.ReleaseMutex();
        _mutex?.Dispose();
        base.OnExit(e);
    }
}

