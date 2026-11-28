# SnakeUSBIP Workspace Delta (Local Project Memory)
- **Monorepo**: Windows Client WPF, Server (.NET 9, macOS Swift, Linux), Android app (`com.snakeusbip`).
- **Versión Oficial**: `1.4.1` (`v1.4.1` estable). En migración hacia `USBAnywhere` (rama de pruebas/staging frente al producto final `USBAnywhere`). Incl. emparejamiento 6 dígitos/`UA2:` + TLS 1.3 `:3243`, handoff multi-proveedor, API REST `:13241` + MCP, aislamiento WTS, `[Rev:XXXX]`, `VhciNativeClient` IOCTL + persistencia boot, `allowed_ips` + `control_token` HMAC, parches `rpi-dwc-usbip-host` 01-04 y Android webhook auth.
- **Build Protegida**: ReadyToRun Single-File (`PublishReadyToRun=true`, `PublishSingleFile=true`, sin PDBs).
- **Incompatibilidad WinForms**: No usar `PublishAot` ni `PublishTrimmed` por `NETSDK1175` en bandeja del sistema.
- **Inno Setup**: `ISCC.exe` requiere `SourceDir` y `OutputDir` en rutas absolutas normalizadas.
- **Release CI Multiplataforma**: `release.yml` matriz Windows, macOS Swift, Linux tarball y Android APK con Sigstore.
- **Integridad**: Hashes SHA-256 en `SHA256SUMS.txt` y atestación Sigstore ($0).
- **Financiación**: `.github/FUNDING.yml` con `ko_fi: oscarlosu`.
