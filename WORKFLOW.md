# 🛡️ SnakeUSBIP: Workflow de Protección y Hardening del Ecosistema

Este documento detalla la arquitectura de seguridad, hardening de compilación y tuberías de distribución continua a **Coste 0 €** implementadas en el monorepo de **SnakeUSBIP**.

---

## 1. Hardening Global (`Directory.Build.props`)

Aplica políticas de compilación protegidas a todos los proyectos .NET de la solución en modo `Release`:

* **Purgado obligatorio de símbolos `.pdb`**: `<DebugType>none</DebugType>` y `<DebugSymbols>false</DebugSymbols>` eliminan los archivos de depuración del ensamblado final, impidiendo el desensamblado asistido por símbolos.
* **Compilaciones Deterministas**: `<Deterministic>true</Deterministic>` garantiza que binarios idénticos generen hashes idénticos independientemente de la máquina o timestamp de compilación.
* **Supresión de Metadatos Internos**: `<GenerateDocumentationFile>false</GenerateDocumentationFile>` evita exponer estructuras internas y comentarios de código en archivos XML.
* **Recorte Parcial de Dependencias**: `<TrimMode>partial</TrimMode>` purga código no utilizado reduciendo la superficie de ataque y el peso del ejecutable.

---

## 2. Pipeline de Construcción Protegida (`tools/build-protected-ecosystem.ps1`)

Script automatizado en PowerShell 7 para la generación local y en CI/CD de entregables blindados:

1. **Servidor y CLI en Native AOT**:
   * Compilación a código máquina x64 puro mediante .NET 9 Native AOT (`/p:PublishAot=true`).
   * Elimina el entorno CLR y el ensamblado CIL legible, neutralizando descompiladores como `dnSpy` o `ILSpy`.
2. **Cliente WPF Endurecido**:
   * Compilación unificada con `ReadyToRun` y empaquetado en un solo ejecutable (`/p:PublishSingleFile=true`).
   * Ofuscación automática de clases, métodos, propiedades y cadenas literales con **Obfuscar** (licencia libre MIT).
3. **Integridad Criptográfica a Coste 0 €**:
   * Cálculo determinista del archivo `SHA256SUMS.txt` para todos los instaladores y archivos comprimidos.

---

## 3. Pipeline de CI/CD en GitHub Actions (`.github/workflows/`)

* **`ci.yml` (Matriz Multiplataforma)**:
  * **Windows**: Valida compilación en .NET 9.0 y ejecuta la suite completa de 133 tests unitarios en cada push/PR.
  * **macOS**: Compila y prueba el servidor nativo Swift para Apple Silicon (`SnakeUSBIP.Server.Mac`).
  * **Android**: Configura JDK 17 y compila el APK de depuración para validar cambios en el servidor móvil.
* **`release.yml` (Lanzamiento Seguro y Atestación)**:
  * Se activa automáticamente ante etiquetas de versión (`v*`).
  * Genera las atestaciones de procedencia criptográfica oficiales de GitHub (**GitHub Artifact Attestations con Sigstore** a coste $0).
  * Publica la release oficial con hashes públicos y aviso legal de marca (*Trademark Notice*).
* **`pages.yml` (Despliegue Continuo de la Web)**:
  * Publica de forma automática la documentación técnica y landing page (`docs/`) en GitHub Pages.

---

## 4. Verificación de Seguridad y Zero-Trust (`tools/verify-protection.ps1`)

El proyecto incorpora un script de auditoría automatizada que valida 4 compuertas antes de cualquier entrega:

```powershell
./tools/verify-protection.ps1
```

* **Gate 1**: Compilación Release limpia (0 errores).
* **Gate 2**: 100% de tests unitarios superados (133 tests).
* **Gate 3**: Ausencia total de archivos `.pdb` expuestos.
* **Gate 4**: Zero-Leak (garantiza la ausencia de rutas privadas o credenciales locales).
