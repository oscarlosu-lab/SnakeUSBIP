# 📖 Uso de SnakeUSBIP

🌐 **Idioma / Language:** [English](USAGE_EN.md) | **Español**

## Interfaz Principal

```
╔═══════════════════════════════════════════════════════════════════╗
║ 🦊 SnakeFoxu   USB/IP Manager   [ESP] [🔄 Actualizar]    🟡 🟢 🔴 ║
╠═══════════════════════════════════════════════════════════════════╣
║  Servidor: ┌──────────────┐ ┌─────────┐┌──────┐┌─────┐┌─────────┐ ║
║            │192.168.1.100 │ │🔍Escanear││🔄Listar││🖥️SSH││🌐 VPN │ ║
║            └──────────────┘ └─────────┘└──────┘└─────┘└─────────┘ ║
╠═══════════════════════════════════════════════════════════════════╣
║  📡 USB Hubs (3)                                                  ║
║   ├─ 🖥️ 192.168.1.100 (2)                                        ║
║   │   ├─ 📱 1-1.2: Arduino Uno (2341:0043)                        ║
║   │   └─ 🖨️ 1-1.4: HP LaserJet (03f0:002a)                       ║
║   └─ 🖥️ 192.168.1.101 (1)                                        ║
║       └─ 💾 1-1.1: SanDisk USB (0781:5567)                        ║
║                                                                   ║
║  ✅ Dispositivos Conectados (1)                                   ║
║   └─ 🔌 Puerto 00: Arduino Uno ← 192.168.1.100                    ║
║                                                                   ║
║  ⭐ Favoritos (2)                                                 ║
║   ├─ 🖨️ 1-1.4 @ 192.168.1.100                                    ║
║   └─ 💾 1-1.1 @ 192.168.1.101                                     ║
╠═══════════════════════════════════════════════════════════════════╣
║ 📋 Log de Actividad                                    [Limpiar]  ║
╠───────────────────────────────────────────────────────────────────╣
║ [14:32:15] ✅ Conectado: Arduino Uno (1-1.2) desde 192.168.1.100  ║
║ [14:32:10] 🔍 Escaneando red 192.168.1.0/24...                    ║
║ [14:32:12] ✅ 2 servidor(es) encontrado(s)                        ║
║ [14:30:05] ⚠️ Timeout conectando a 192.168.1.50                   ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Listo         Drivers: ✅ Instalados    [Instalar][Desinstalar]║
╚═══════════════════════════════════════════════════════════════════╝
```

### Barra de Título (estilo macOS)
```
┌──────────────────────────────────────────────────────────────────┐
│ 🦊 SnakeFoxu   USB/IP Manager   [🌐ESP] [🔄Actualizar]  🟡 🟢 🔴 │
└──────────────────────────────────────────────────────────────────┘
                                                          │  │  │
                                              Minimizar ──┘  │  │
                                              Maximizar ─────┘  │
                                              Cerrar ───────────┘
```

### Panel de Servidor
```
┌──────────────────────────────────────────────────────────────────────┐
│ Servidor: [__192.168.1.100__] [🔍Escanear][🔄Listar][🖥️SSH][🌐 VPN] │
└──────────────────────────────────────────────────────────────────────┘
                │                    │          │        │       │
  IP del servidor│    Buscar en red ──┘          │        │       │
  (editable)     │    (escanea subred)           │        │       │
                 │                               │        │       │
                 │         Listar dispositivos ──┘        │       │
                 │         del servidor actual            │       │
                 │                                        │       │
                 │              Configuración SSH ────────┘       │
                 │              para Raspberry Pi                 │
                 │                                                │
                 │                     Conexión por Internet ─────┘
                 │                     (Tailscale/ZeroTier)
```

## Acciones Principales

### 🔍 Escanear
Busca servidores USB/IP en tu red local (puerto 3240).

### 🔄 Listar
Muestra los dispositivos USB disponibles en el servidor.

### 🖥️ SSH
Abre configuración para conectar a Raspberry Pi vía SSH.

### 🌐 VPN
Conectar a servidores USB/IP remotos por Internet usando Tailscale o ZeroTier.
Ver [VPN_INTERNET.md](VPN_INTERNET.md) para configuración completa.

## Menú Contextual (Click Derecho)

```
┌─────────────────────────────────────┐
│ 📱 1-1.4: Arduino Uno              │ ← Click derecho aquí
└─────────────────────────────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │ 🔌 Conectar             │
        │ ❌ Desconectar          │
        ├─────────────────────────┤
        │ ⭐ Añadir a Favoritos   │
        │ ❌ Quitar de Favoritos  │
        │ 🗑️ Quitar servidor      │
        ├─────────────────────────┤
        │ 📋 Propiedades          │
        └─────────────────────────┘
```

| Opción | Descripción |
|--------|-------------|
| 🔌 Conectar | Conecta el dispositivo USB remoto a tu PC |
| ❌ Desconectar | Libera el dispositivo USB conectado |
| ⭐ Añadir a Favoritos | Guarda el dispositivo para reconexión rápida |
| ❌ Quitar de Favoritos | Elimina de la lista de favoritos |
| 🗑️ Quitar servidor | Elimina el servidor del árbol |
| 📋 Propiedades | Muestra información detallada (VID:PID, fabricante, etc.) |

## Atajos

- **Doble-click** en dispositivo → Conectar
- **Enter** en campo IP → Listar dispositivos
- **F5** → Actualizar lista

## Favoritos y Modos de Rendimiento

Los favoritos se guardan en `config.json` y pueden reconectarse automáticamente al iniciar la aplicación.

### ⚡ Modos de Rendimiento USB/IP

SnakeUSBIP soporta perfiles de conexión optimizados mediante el parámetro `--receive-mode`:

| Modo | Ideal para | Descripción técnica |
|---|---|---|
| **Zero-Copy** *(Predeterminado)* | Discos duros, pendrives, webcams HD | Utiliza buffers de red directos sin copia intermedia, logrando el máximo ancho de banda posible en la red. |
| **Low-Latency** | Ratones, teclados, mandos gaming, HID | Basado en callbacks de eventos WSK a nivel de kernel de Windows. Minimiza la latencia de entrada para periféricos interactivos de alta frecuencia. |

### 🔌 Desconexión Limpia Automática

Al cerrar la aplicación o apagar el PC (`AutoDetachOnExit: true`), SnakeUSBIP libera y desacopla ordenadamente todos los puertos USB activos antes de finalizar. Esto garantiza que el servidor Linux no deje los puertos en estado bloqueado (*busy*), permitiendo reconectarlos inmediatamente sin necesidad de reiniciar el daemon del servidor.

## 📝 Log de Actividad

```
╔════════════════════════════════════════════════════════════════╗
║ 📋 Log de Actividad                                  [Limpiar] ║
╠════════════════════════════════════════════════════════════════╣
║ [14:35:22] ✅ Conectado: Arduino Uno (1-1.2) desde 192.168.1.10║
║ [14:35:20] 🔍 Listando dispositivos en 192.168.1.100...        ║
║ [14:35:15] ✅ 2 servidor(es) encontrado(s)                     ║
║ [14:35:10] 🔍 Escaneando red 192.168.1.0/24...                 ║
║ [14:34:55] ❌ Error: Timeout conectando a 192.168.1.50         ║
║ [14:34:50] ⚠️ Drivers no detectados, instalando...            ║
║ [14:34:45] ✅ Drivers verificados OK                           ║
╚════════════════════════════════════════════════════════════════╝
```

El panel inferior muestra un historial de eventos en tiempo real:

| Icono | Tipo | Descripción |
|-------|------|-------------|
| ✅ | Éxito | Conexiones exitosas, servidores encontrados, drivers OK |
| ❌ | Error | Fallos de conexión, timeouts, dispositivos no disponibles |
| 🔍 | Info | Escaneos en progreso, operaciones informativas |
| ⚠️ | Advertencia | Problemas menores, configuración incompleta |

Usa el botón **[Limpiar]** para borrar el historial.

## 🖥️ System Tray (Bandeja del Sistema)

```
                                    ┌─────────────────────────────┐
                                    │   Bandeja del Sistema       │
                                    │   (junto al reloj)          │
                                    └──────────┬──────────────────┘
                                               │
     ┌─────────────────────────────────────────┼────────────────────┐
     │  🔊  📶  🔋  ⚡ ... 🦊                  │                    │
     └─────────────────────────────────────────┼────────────────────┘
                                               │
                                               ▼ Click derecho
                                    ┌─────────────────────────┐
                                    │ 📡 Escanear Red         │
                                    │ 🔼 Mostrar Ventana      │
                                    ├─────────────────────────┤
                                    │ ❌ Salir                │
                                    └─────────────────────────┘
```

- Al **minimizar**, la aplicación se oculta en la bandeja del sistema (icono 🦊)
- **Doble-click** en el icono para restaurar la ventana
- **Click derecho** para menú rápido: Escanear Red, Mostrar Ventana, Salir
- La aplicación sigue corriendo en segundo plano hasta que pulses "Salir"

## 🌐 Cambiar Idioma

```
┌──────────────────────────────────────────────────────────────────┐
│ 🦊 SnakeFoxu   USB/IP Manager   [🌐ESP] [🔄Actualizar]  🟡 🟢 🔴 │
└──────────────────────────────────────────────────────────────────┘
                                      │
                            Click aquí│
                                      ▼
                            ┌────────────────┐
                            │ 🌐 ESP → ENG   │  (alterna)
                            │ 🌐 ENG → ESP   │
                            └────────────────┘
```

Usa el botón **[🌐 ESP]** o **[🌐 ENG]** en la barra de título para alternar entre Español e Inglés. El idioma se guarda automáticamente en `config.json`.

## 🔧 Barra de Estado y Drivers

```
╔════════════════════════════════════════════════════════════════════╗
║  ✓ Listo         Drivers: ✅ Instalados      [Instalar][Desinstalar]║
╚════════════════════════════════════════════════════════════════════╝
     │                   │                          │          │
     │                   │               Instalar ──┘          │
     │                   │               drivers USB/IP        │
     │                   │                                     │
     │                   │                    Desinstalar ─────┘
     │                   │                    (requiere reinicio)
     │                   │
     Estado actual ──────┘                   
     de la conexión      Estado de drivers ─────┘
                         ✅ Instalados
                         ❌ No instalados
```

> ⚠️ **Importante:** La primera instalación de drivers puede requerir reiniciar Windows.

---

## 🆘 Solución de Problemas

### "No se encontró servidor"
1. Verifica que el servidor USB/IP esté corriendo: `sudo usbipd` en Linux
2. Comprueba que el puerto 3240 esté abierto en el firewall
3. Verifica que estés en la misma subred (ej: 192.168.1.x)

### "Error al conectar dispositivo"
1. Asegúrate de que los drivers están instalados (barra inferior)
2. El dispositivo debe estar "bindeado" en el servidor: `sudo usbip bind -b X-X`
3. Ejecuta SnakeUSBIP como Administrador

### "Dispositivo conectado pero no funciona"
1. Revisa en Administrador de Dispositivos si necesita drivers adicionales
2. Algunos dispositivos USB 3.0 pueden no ser compatibles
3. Prueba con otro puerto USB en el servidor

---

## 📚 Más Información

- **[README.md](../README.md)** - Instalación y características
- **[RASPBERRY_PI_SERVER.md](RASPBERRY_PI_SERVER.md)** - Configurar servidor en Raspberry Pi
- **[CHANGELOG.md](../CHANGELOG.md)** - Historial de versiones
