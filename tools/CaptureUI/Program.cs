using System;
using System.IO;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using SnakeUSBIP.Models;
using SnakeUSBIP.Services;
using SnakeUSBIP.Services.Interfaces;
using SnakeUSBIP.Views;

namespace CaptureUI;

public static class Program
{
    [STAThread]
    public static void Main()
    {
        var outDir = @"D:\REPOS_GITHUB\SnakeUSBIP-WPF\docs\assets\captures";
        Directory.CreateDirectory(outDir);

        var app = new SnakeUSBIP.App();
        app.InitializeComponent();

        var services = new ServiceCollection();
        services.AddLogging(b => b.AddConsole().SetMinimumLevel(LogLevel.Debug));
        services.AddSingleton<IEnvironmentService, EnvironmentService>();
        services.AddSingleton<ILoggerService, LoggerService>();
        services.AddSingleton<IConfigService, ConfigService>();
        services.AddSingleton<IUsbipService, UsbipService>();
        services.AddSingleton<IUpdateService, UpdateService>();
        services.AddSingleton<IVpnService, VpnService>();
        services.AddSingleton<IDriverService, DriverService>();
        services.AddSingleton<IUsbIdsService, UsbIdsService>();
        services.AddSingleton<ILocalizationService, LocalizationService>();
        services.AddSingleton<IFavoritesService, FavoritesService>();
        services.AddSingleton<IConnectionMonitorService, ConnectionMonitorService>();
        services.AddSingleton<INetworkScanner, NetworkScanner>();
        services.AddTransient<SnakeUSBIP.MainWindow>();

        var sp = services.BuildServiceProvider();
        var loc = sp.GetRequiredService<ILocalizationService>();

        // 1. MainWindow Dark Capture
        var mainWindow = sp.GetRequiredService<SnakeUSBIP.MainWindow>();
        PopulateMockUi(mainWindow);
        mainWindow.Width = 720;
        mainWindow.Height = 820;
        mainWindow.Show();
        mainWindow.UpdateLayout();
        RenderWindowToPng(mainWindow, Path.Combine(outDir, "capture_01_mainwindow_dark.png"), 720, 820);

        // 2. Light Theme Capture
        var applyThemeMethod = typeof(SnakeUSBIP.MainWindow).GetMethod("ApplyTheme", BindingFlags.NonPublic | BindingFlags.Instance);
        if (applyThemeMethod != null)
        {
            applyThemeMethod.Invoke(mainWindow, new object[] { "light" });
            mainWindow.UpdateLayout();
            RenderWindowToPng(mainWindow, Path.Combine(outDir, "capture_04_mainwindow_light.png"), 720, 820);
        }

        // 3. SSH Dialog Capture
        var sshDialog = new SshDialog(loc, "es", "192.168.1.180");
        sshDialog.Width = 530;
        sshDialog.Height = 470;
        sshDialog.Show();
        sshDialog.UpdateLayout();
        RenderWindowToPng(sshDialog, Path.Combine(outDir, "capture_02_ssh_dialog.png"), 530, 470);
        sshDialog.Close();

        // 4. VPN Dialog Capture
        var vpnDialog = new VpnDialog(loc, "es");
        PopulateVpnUi(vpnDialog);
        vpnDialog.Width = 500;
        vpnDialog.Height = 420;
        vpnDialog.Show();
        vpnDialog.UpdateLayout();
        RenderWindowToPng(vpnDialog, Path.Combine(outDir, "capture_03_vpn_dialog.png"), 500, 420);
        vpnDialog.Close();

        mainWindow.Close();
        Console.WriteLine($"SUCCESS: All captures saved to {outDir}");
    }

    private static void PopulateVpnUi(VpnDialog vpn)
    {
        var lblStatusValue = vpn.FindName("lblStatusValue") as TextBlock;
        var listPeers = vpn.FindName("listPeers") as ListBox;
        if (lblStatusValue != null)
        {
            lblStatusValue.Text = "Online (Tailscale 1.58)";
            lblStatusValue.Foreground = new SolidColorBrush(Color.FromRgb(0x89, 0xD1, 0x85));
        }
        if (listPeers != null)
        {
            listPeers.Items.Clear();
            listPeers.Items.Add(new CheckBox { Content = "🟢 raspberrypi-homelab (100.84.12.34) - USB/IP Active", IsChecked = true, Foreground = Brushes.White });
            listPeers.Items.Add(new CheckBox { Content = "🟢 simrig-livingroom (100.92.55.12) - USB/IP Active", IsChecked = true, Foreground = Brushes.White });
            listPeers.Items.Add(new CheckBox { Content = "🟢 unraid-storage (100.105.88.90) - USB/IP Active", IsChecked = false, Foreground = Brushes.White });
        }
    }

    private static void PopulateMockUi(SnakeUSBIP.MainWindow w)
    {
        var nodeHubs = w.FindName("nodeHubs") as TreeViewItem;
        var nodeConnected = w.FindName("nodeConnected") as TreeViewItem;
        var nodeFavorites = w.FindName("nodeFavorites") as TreeViewItem;
        var txtLog = w.FindName("txtLog") as TextBox;
        var txtServerIP = w.FindName("txtServerIP") as TextBox;

        if (txtServerIP != null) txtServerIP.Text = "192.168.1.180";

        if (nodeHubs != null)
        {
            nodeHubs.Items.Clear();
            var s1 = new TreeViewItem { Header = "🖥️ 192.168.1.180 (Raspberry Pi 4)  •  ⚡ 0.8 ms", IsExpanded = true };
            s1.Items.Add(new TreeViewItem { Header = "🔌 1-1.2: Logitech G29 Driving Force Racing Wheel (Low-Latency WSK)" });
            s1.Items.Add(new TreeViewItem { Header = "🔌 1-1.4: Xbox Wireless Controller with Full Rumble" });
            s1.Items.Add(new TreeViewItem { Header = "🔌 1-1.1: Creality Ender-3 v2 3D Printer (USB Serial)" });
            s1.Items.Add(new TreeViewItem { Header = "🔌 1-1.3: Logitech C920 HD Pro Webcam (Zero-Copy)" });

            var s2 = new TreeViewItem { Header = "🖥️ 192.168.1.132 (HomeLab / Unraid Server)  •  ⚡ 1.1 ms", IsExpanded = true };
            s2.Items.Add(new TreeViewItem { Header = "🔌 2-1: ConBee II Zigbee Coordinator Gateway" });
            s2.Items.Add(new TreeViewItem { Header = "🔌 2-2: SanDisk Ultra 128GB Flash Drive" });

            nodeHubs.Items.Add(s1);
            nodeHubs.Items.Add(s2);
            nodeHubs.Header = "🖥️ USB Hubs (2)";
        }

        if (nodeConnected != null)
        {
            nodeConnected.Items.Clear();
            nodeConnected.Items.Add(new TreeViewItem { Header = "🔌 1-1.2: Logitech G29 Racing Wheel -> Puerto 1 [CONECTADO ✓]" });
            nodeConnected.Items.Add(new TreeViewItem { Header = "🔌 1-1.4: Xbox Wireless Controller -> Puerto 2 [CONECTADO ✓]" });
            nodeConnected.Header = "☑️ Dispositivos Conectados (2)";
        }

        if (nodeFavorites != null)
        {
            nodeFavorites.Items.Clear();
            nodeFavorites.Items.Add(new TreeViewItem { Header = "⭐ Logitech G29 Wheel (192.168.1.180/1-1.2) [Auto-Connect]" });
            nodeFavorites.Items.Add(new TreeViewItem { Header = "⭐ Xbox Controller (192.168.1.180/1-1.4) [Auto-Connect]" });
            nodeFavorites.Header = "⭐ Favoritos (2)";
        }

        if (txtLog != null)
        {
            txtLog.Text =
                "[12:10:01] [INFO ] SnakeUSBIP v3.0.0 Logger Initialized\n" +
                "[12:10:02] [INFO ] Escaneando subred 192.168.1.0/24...\n" +
                "[12:10:03] [INFO ] Escaneo completado: encontrados 2 servidor(es)\n" +
                "[12:10:03] [INFO ]   → Servidor: 192.168.1.180 (Raspberry Pi) [Latencia: 0.8 ms]\n" +
                "[12:10:03] [INFO ]   → Servidor: 192.168.1.132 (HomeLab) [Latencia: 1.1 ms]\n" +
                "[12:10:04] [INFO ] Conectando 1-1.2 (Logitech G29) en modo Low-Latency WSK...\n" +
                "[12:10:04] [INFO ] Conectado exitosamente en puerto virtual UDE #1\n" +
                "[12:10:05] [INFO ] Conectando 1-1.4 (Xbox Controller) en modo Low-Latency WSK...\n" +
                "[12:10:05] [INFO ] Conectado exitosamente en puerto virtual UDE #2\n" +
                "[12:10:06] [INFO ] Auto-conexión de 2 favoritos completada ✓";
        }
    }

    private static void RenderWindowToPng(Window window, string outPath, int w, int h)
    {
        window.Measure(new Size(w, h));
        window.Arrange(new Rect(0, 0, w, h));
        window.UpdateLayout();

        var bmp = new RenderTargetBitmap(w, h, 96, 96, PixelFormats.Pbgra32);
        bmp.Render(window);

        var encoder = new PngBitmapEncoder();
        encoder.Frames.Add(BitmapFrame.Create(bmp));
        using var fs = new FileStream(outPath, FileMode.Create);
        encoder.Save(fs);
    }
}
