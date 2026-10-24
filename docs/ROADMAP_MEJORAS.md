# 🗺️ Roadmap de Mejoras Técnicas y Futuras — USBAnywhere

Este documento recopila las áreas de optimización, mejoras de arquitectura y nuevas funcionalidades planificadas para evolucionar el cliente USBAnywhere en Windows.

---

## ⚡ 1. Rendimiento y Protocolo USB/IP

| Mejora | Impacto | Descripción Técnica |
|---|---|---|
| **Soporte de Modos de Recepción (`--receive-mode`)** | **Alto** | Permitir seleccionar entre `zero-copy` (máximo throughput para discos y cámaras) y `low-latency` (callbacks WSK en kernel para HID, ratones y teclados de alta tasa de sondeo). *(Implementado en v2.0.4+)* |
| **Desconexión Limpia en Apagado / Salida (`Graceful Detach`)** | **Alto** | Liberar automáticamente todos los puertos USB activos al cerrar la aplicación o ante señales de cierre de sesión de Windows (`WM_QUERYENDSESSION`), evitando que el servidor Linux mantenga el bus en estado *busy*. *(Implementado en v2.0.4+)* |
| **Compresión de Tráfico en Redes Lentas** | **Medio** | Soporte opcional de compresión LZ4/ZSTD sobre el túnel TCP para conexiones con ancho de banda limitado (útil sobre VPN y Tailscale). |
| **Soporte de Sobrescritura de Número de Serie USB** | **Medio** | Aprovechar el flag `--serial <ID>` de `usbipw` para permitir asignar números de serie personalizados a periféricos clónicos o duplicados. |

---

## 🛡️ 2. Resiliencia de Drivers y Windows Kernel

| Mejora | Impacto | Descripción Técnica |
|---|---|---|
| **Detección PnP en Tiempo Real** | **Alto** | Sustituir la comprobación pasiva por consulta activa a `pnputil /enum-devices /class USB` buscando el nodo `ROOT\USBIP_WIN2\UDE` para garantizar que la controladora host emulada esté efectivamente en estado `Iniciado`. *(Implementado en v2.0.4+)* |
| **Prevención de Controladoras Duplicadas** | **Alto** | Validar antes de invocar `devnode.exe install` si ya existe un host controller instanciado para evitar acumular nodos `ROOT\USB\0001`, `0002`... que degradan la pila USB. *(Implementado en v2.0.4+)* |
| **Watchdog de Estado del Servicio UDE** | **Medio** | Monitorizar el estado del servicio en segundo plano (`usbip2_ude`) y alertar al usuario si Windows suspende la controladora por ahorro de energía (Selective Suspend). |
| **Script Autónomo de Diagnóstico de Drivers (`RepairDrivers`)** | **Medio** | Botón en UI que ejecute un ciclo de reparación automatizado: parada de servicios, eliminación de dispositivos fantasma y recreación limpia del nodo UDE. |

---

## 💻 3. Interfaz Gráfica y Experiencia de Usuario (WPF / UI)

| Mejora | Impacto | Descripción Técnica |
|---|---|---|
| **Selector Visual de Modo de Latencia por Dispositivo** | **Medio** | Menú contextual conmutador en cada dispositivo: `[x] Modo Baja Latencia (HID/Gaming)` vs `[ ] Modo Alto Rendimiento (Almacenamiento)`. |
| **Gráficos de Tráfico y Métricas en Tiempo Real** | **Medio** | Visualización en tiempo real de KB/s transmitidos y recibidos por puerto conectado, ping al servidor remoto y tasa de paquetes perdidos. |
| **Temas Modernos Dinámicos (Fluent / Mica / Acrylic)** | **Bajo** | Soporte nativo de `DwmSetWindowAttribute` para integrar efectos *Mica / Backdrop* en Windows 11. |
| **Exportación / Importación de Perfiles y Favoritos** | **Bajo** | Capacidad de exportar e importar listas de servidores y dispositivos favoritos en formato JSON cifrado o plano para facilitar despliegues en múltiples PCs. |

---

## 🌐 4. Conectividad y Redes Remotas (VPN / Cloud)

| Mejora | Impacto | Descripción Técnica |
|---|---|---|
| **Reconexión Exponencial Inteligente (Backoff)** | **Alto** | Algoritmo de reintento progresivo (2s, 5s, 10s, 30s) cuando el servidor remoto se reinicia o sufre fluctuaciones de WiFi, evitando saturar el socket de conexión. |
| **Integración Nativa con WireGuard** | **Medio** | Detectar y levantar túneles WireGuard directamente desde el diálogo VPN sin requerir clientes externos. |
| **Keep-Alive a Nivel de Socket TCP** | **Medio** | Habilitar `SO_KEEPALIVE` con sondeos cada 5 segundos para detectar caídas de enlaces de fibra o 4G/5G antes de que el timeout de Windows expire (20s). |

---

## 🧪 5. Calidad, Testing y CI/CD

| Mejora | Impacto | Descripción Técnica |
|---|---|---|
| **Verificación Criptográfica Fail-Closed** | **Alto** | Validación estricta por hash SHA-256 de todos los binarios nativos empaquetados (`usbipw.exe`, `devnode.exe`) antes de cualquier ejecución con privilegios elevados. *(Implementado en v2.0.4+)* |
| **Tests de Persistencia Atómica** | **Alto** | Tests unitarios que certifiquen que la configuración y favoritos sobreviven a interrupciones abruptas del proceso. *(Implementado en v2.0.4+)* |
| **Pipeline de GitHub Actions Automatizado** | **Medio** | Flujo de CI que compile la solución en Windows runner, ejecute los 49 tests unitarios, genere el paquete firmado y publique el release automáticamente con sumas SHA-256. |
