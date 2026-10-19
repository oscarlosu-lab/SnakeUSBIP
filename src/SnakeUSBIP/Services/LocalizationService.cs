using SnakeUSBIP.Services.Interfaces;

namespace SnakeUSBIP.Services;

/// <summary>
/// Localization service - Translation dictionaries ES/EN
/// Port from PowerShell $Translations
/// </summary>
public class LocalizationService : ILocalizationService
{
    private readonly Dictionary<string, Dictionary<string, string>> _translations;
    
    public LocalizationService()
    {
        _translations = new Dictionary<string, Dictionary<string, string>>
        {
            ["es"] = new Dictionary<string, string>
            {
                // Buttons
                ["btn_scan"] = "🔍 Escanear",
                ["btn_refresh"] = "📋 Listar",
                ["btn_ssh"] = "🔗 SSH",
                ["btn_vpn"] = "● VPN",
                ["btn_update"] = "⬆️ Actualizar",
                ["btn_install_drivers"] = "Instalar",
                ["btn_uninstall_drivers"] = "Desinstalar",
                
                // Labels
                ["lbl_server"] = "Servidor:",
                
                // TreeView nodes
                ["node_hubs"] = "🖥️ USB Hubs",
                ["node_connected"] = "☑️ Dispositivos Conectados",
                ["node_favorites"] = "⭐ Favoritos",
                
                // Status
                ["status_ready"] = "✓ Listo",
                ["status_scanning"] = "Escaneando...",
                ["status_listing"] = "Listando dispositivos en",
                ["status_connecting"] = "Conectando",
                ["status_disconnecting"] = "Desconectando",
                ["status_servers_found"] = "servidor(es) encontrado(s)",
                ["status_devices_found"] = "dispositivo(s)",
                ["status_no_server"] = "No se encontró servidor en la subred",
                ["status_error"] = "Error",
                
                // Log
                ["log_title"] = "📋 Log de Actividad",
                ["log_clear"] = "Limpiar",
                ["log_connected"] = "Conectado",
                ["log_disconnected"] = "Desconectado",
                ["log_scan_start"] = "Escaneando red...",
                ["log_scan_found"] = "servidor(es) encontrado(s)",
                ["log_scan_none"] = "Ningún servidor encontrado",
                ["log_error"] = "Error",
                ["log_app_start"] = "Aplicación iniciada",
                
                // Context menu
                ["menu_connect"] = "▶️ Conectar",
                ["menu_disconnect"] = "⏹️ Desconectar",
                ["menu_add_favorite"] = "⭐ Añadir a Favoritos",
                ["menu_remove_favorite"] = "❌ Quitar de Favoritos",
                
                // Update
                ["update_checking"] = "Buscando actualizaciones...",
                ["update_available"] = "Nueva versión disponible",
                ["update_current"] = "Tienes la última versión",
                ["update_download"] = "Descargar e instalar",
                ["update_error"] = "Error al buscar actualizaciones",
                
                // Dialogs
                ["enter_ip"] = "Introduce una IP de servidor",
                ["enter_ip_ssh"] = "Introduce la IP del servidor para SSH",
                
                // SSH Dialog
                ["ssh_title"] = "SSH - Configurar Servidor USB/IP",
                ["ssh_instructions"] = "📋 Instrucciones para Linux/Raspberry Pi:",
                ["ssh_step1"] = "1. Instalar paquetes:",
                ["ssh_step2"] = "2. Cargar módulo del kernel:",
                ["ssh_step3"] = "3. Iniciar servicio:",
                ["ssh_step4"] = "4. Ver dispositivos USB disponibles:",
                ["ssh_step5"] = "5. Exportar dispositivo (ej: 1-1.4):",
                ["ssh_step6"] = "6. Auto-inicio (agregar a /etc/rc.local):",
                ["ssh_user"] = "Usuario:",
                ["ssh_connect"] = "🔗 Conectar",
                ["ssh_copy"] = "📋 Copiar comandos",
                ["ssh_close"] = "Cerrar",
                
                // VPN Dialog
                ["vpn_title"] = "VPN / Red Remota",
                ["vpn_status"] = "Estado de la red:",
                ["vpn_online"] = "Online",
                ["vpn_offline"] = "Offline",
                ["vpn_peers"] = "Peers en la red:",
                ["vpn_no_peers"] = "No hay peers online",
                ["vpn_add_all"] = "Añadir Todos",
                ["vpn_connect"] = "Conectar",
                ["vpn_info"] = "ℹ️ Conecta con otros usuarios via Tailscale o ZeroTier",
                
                // System Tray
                ["tray_scan"] = "Escanear",
                ["tray_show"] = "Mostrar",
                ["tray_exit"] = "Salir",
                ["tray_minimized"] = "Minimizado a la bandeja del sistema",
                ["title_main"] = "SnakeUSBIP",
                ["notify_connected"] = "Dispositivo conectado",
                ["notify_connection_lost"] = "Conexión perdida",
                ["notify_reconnected"] = "Reconexión exitosa",
                
                // Favorites
                ["log_favorite_added"] = "Dispositivo añadido a favoritos",
                ["log_favorite_removed"] = "Dispositivo eliminado de favoritos",
                
                // Update extra
                ["update_downloading"] = "Descargando actualización...",
                
                // Activity Log Messages
                ["log_tray_init_error"] = "No se pudo inicializar el icono de la bandeja: {0}",
                ["log_scanning_subnet"] = "Escaneando subred {0}.0/24...",
                ["log_scan_complete"] = "Escaneo completado: encontrados {0} servidor(es)",
                ["log_server_found"] = "  → Servidor: {0}",
                ["log_devices_on_server"] = "{0} dispositivo(s) en {1}",
                ["log_devices_already_connected"] = "Encontrados {0} dispositivo(s) ya conectado(s)",
                ["log_load_connected_error"] = "No se pudieron cargar los dispositivos conectados: {0}",
                ["log_auto_connecting"] = "Auto-conectando {0} favorito(s)...",
                ["log_connected_favorite"] = "Conectado {0} ({1})",
                ["log_connection_failed"] = "Fallo al conectar {0}: {1}",
                ["log_connection_error"] = "Error conectando {0}: {1}",
                ["log_connecting_device"] = "Conectando {0} en {1}...",
                ["log_connection_success"] = "Conectado {0}",
                ["log_connection_general_failed"] = "Conexión fallida",
                ["log_disconnecting"] = "Desconectando {0}...",
                ["log_disconnected_port"] = "Desconectado puerto {0}",
                ["log_disconnect_failed"] = "Desconexión fallida",
                ["log_device_not_found"] = "Dispositivo no encontrado, puede que ya esté desconectado",
                ["log_listing_devices"] = "Listando dispositivos en {0} servidor(es)...",
                ["log_listed_devices"] = "Listados {0} dispositivos en {1} servidores",
                ["log_checking_updates"] = "Buscando actualizaciones...",
                ["log_update_available"] = "Nueva versión disponible: {0}",
                ["log_downloading_update"] = "Descargando actualización...",
                ["log_update_failed"] = "Actualización fallida",
                ["log_latest_version"] = "Tienes la última versión (v{0})",
                ["log_installing_drivers"] = "Instalando drivers...",
                ["log_drivers_installed"] = "Drivers instalados exitosamente",
                ["log_install_drivers_failed"] = "Fallo al instalar drivers",
                ["log_uninstalling_drivers"] = "Desinstalando drivers...",
                ["log_drivers_uninstalled"] = "Drivers desinstalados exitosamente",
                ["log_uninstall_drivers_failed"] = "Fallo al desinstalar drivers",
            },
            
            ["en"] = new Dictionary<string, string>
            {
                // Buttons
                ["btn_scan"] = "🔍 Scan",
                ["btn_refresh"] = "📋 List",
                ["btn_ssh"] = "🔗 SSH",
                ["btn_vpn"] = "● VPN",
                ["btn_update"] = "⬆️ Update",
                ["btn_install_drivers"] = "Install",
                ["btn_uninstall_drivers"] = "Uninstall",
                
                // Labels
                ["lbl_server"] = "Server:",
                
                // TreeView nodes
                ["node_hubs"] = "🖥️ USB Hubs",
                ["node_connected"] = "☑️ Connected Devices",
                ["node_favorites"] = "⭐ Favorites",
                
                // Status
                ["status_ready"] = "✓ Ready",
                ["status_scanning"] = "Scanning...",
                ["status_listing"] = "Listing devices on",
                ["status_connecting"] = "Connecting",
                ["status_disconnecting"] = "Disconnecting",
                ["status_servers_found"] = "server(s) found",
                ["status_devices_found"] = "device(s)",
                ["status_no_server"] = "No server found in subnet",
                ["status_error"] = "Error",
                
                // Log
                ["log_title"] = "📋 Activity Log",
                ["log_clear"] = "Clear",
                ["log_connected"] = "Connected",
                ["log_disconnected"] = "Disconnected",
                ["log_scan_start"] = "Scanning network...",
                ["log_scan_found"] = "server(s) found",
                ["log_scan_none"] = "No servers found",
                ["log_error"] = "Error",
                ["log_app_start"] = "Application started",
                
                // Context menu
                ["menu_connect"] = "▶️ Connect",
                ["menu_disconnect"] = "⏹️ Disconnect",
                ["menu_add_favorite"] = "⭐ Add to Favorites",
                ["menu_remove_favorite"] = "❌ Remove from Favorites",
                
                // Update
                ["update_checking"] = "Checking for updates...",
                ["update_available"] = "New version available",
                ["update_current"] = "You have the latest version",
                ["update_download"] = "Download and install",
                ["update_error"] = "Error checking for updates",
                
                // Dialogs
                ["enter_ip"] = "Enter a server IP",
                ["enter_ip_ssh"] = "Enter the server IP for SSH",
                
                // SSH Dialog
                ["ssh_title"] = "SSH - Configure USB/IP Server",
                ["ssh_instructions"] = "📋 Instructions for Linux/Raspberry Pi:",
                ["ssh_step1"] = "1. Install packages:",
                ["ssh_step2"] = "2. Load kernel module:",
                ["ssh_step3"] = "3. Start service:",
                ["ssh_step4"] = "4. List available USB devices:",
                ["ssh_step5"] = "5. Export device (e.g.: 1-1.4):",
                ["ssh_step6"] = "6. Auto-start (add to /etc/rc.local):",
                ["ssh_user"] = "User:",
                ["ssh_connect"] = "🔗 Connect",
                ["ssh_copy"] = "📋 Copy commands",
                ["ssh_close"] = "Close",
                
                // VPN Dialog
                ["vpn_title"] = "VPN / Remote Network",
                ["vpn_status"] = "Network status:",
                ["vpn_online"] = "Online",
                ["vpn_offline"] = "Offline",
                ["vpn_peers"] = "Peers on network:",
                ["vpn_no_peers"] = "No peers online",
                ["vpn_add_all"] = "Add All",
                ["vpn_connect"] = "Connect",
                ["vpn_info"] = "ℹ️ Connect with other users via Tailscale or ZeroTier",
                
                // System Tray
                ["tray_scan"] = "Scan",
                ["tray_show"] = "Show",
                ["tray_exit"] = "Exit",
                ["tray_minimized"] = "Minimized to system tray",
                ["title_main"] = "SnakeUSBIP",
                ["notify_connected"] = "Device connected",
                ["notify_connection_lost"] = "Connection lost",
                ["notify_reconnected"] = "Reconnection successful",
                
                // Favorites
                ["log_favorite_added"] = "Device added to favorites",
                ["log_favorite_removed"] = "Device removed from favorites",
                
                // Update extra
                ["update_downloading"] = "Downloading update...",
                
                // Activity Log Messages
                ["log_tray_init_error"] = "Could not initialize tray icon: {0}",
                ["log_scanning_subnet"] = "Scanning subnet {0}.0/24...",
                ["log_scan_complete"] = "Scan complete: found {0} server(s)",
                ["log_server_found"] = "  → Server: {0}",
                ["log_devices_on_server"] = "{0} device(s) on {1}",
                ["log_devices_already_connected"] = "Found {0} device(s) already connected",
                ["log_load_connected_error"] = "Could not load connected devices: {0}",
                ["log_auto_connecting"] = "Auto-connecting {0} favorite(s)...",
                ["log_connected_favorite"] = "Connected {0} ({1})",
                ["log_connection_failed"] = "Failed to connect {0}: {1}",
                ["log_connection_error"] = "Error connecting {0}: {1}",
                ["log_connecting_device"] = "Connecting {0} on {1}...",
                ["log_connection_success"] = "Connected {0}",
                ["log_connection_general_failed"] = "Connection failed",
                ["log_disconnecting"] = "Disconnecting {0}...",
                ["log_disconnected_port"] = "Disconnected port {0}",
                ["log_disconnect_failed"] = "Disconnect failed",
                ["log_device_not_found"] = "Device not found, may already be disconnected",
                ["log_listing_devices"] = "Listing devices on {0} server(s)...",
                ["log_listed_devices"] = "Listed {0} devices on {1} servers",
                ["log_checking_updates"] = "Checking for updates...",
                ["log_update_available"] = "New version available: {0}",
                ["log_downloading_update"] = "Downloading update...",
                ["log_update_failed"] = "Update failed",
                ["log_latest_version"] = "You have the latest version (v{0})",
                ["log_installing_drivers"] = "Installing drivers...",
                ["log_drivers_installed"] = "Drivers installed successfully",
                ["log_install_drivers_failed"] = "Failed to install drivers",
                ["log_uninstalling_drivers"] = "Uninstalling drivers...",
                ["log_drivers_uninstalled"] = "Drivers uninstalled successfully",
                ["log_uninstall_drivers_failed"] = "Failed to uninstall drivers",
            }
        };
    }
    
    public string GetText(string key, string language = "es")
    {
        if (_translations.TryGetValue(language, out var dict))
        {
            if (dict.TryGetValue(key, out var text))
                return text;
        }
        return key; // Return key if not found
    }
}
