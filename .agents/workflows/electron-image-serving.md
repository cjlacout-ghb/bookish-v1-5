---
description: Guía de implementación para el servicio de imágenes locales en apps Electron + Python (.exe).
---

# Workflow: Local Image Serving in Electron + Python (.exe) Apps

Este workflow describe el patrón de arquitectura, el análisis de la causa raíz y la guía completa de implementación para servir imágenes locales en una aplicación de escritorio distribuida como .exe.

## Contexto y Alcance

Utiliza este patrón siempre que necesites guardar, almacenar o mostrar archivos de imagen locales en una aplicación con el siguiente stack:
- **Contenedor**: Electron (main.cjs)
- **Frontend**: React + Vite
- **Backend**: Python + FastAPI + Uvicorn
- **Distribución**: PyInstaller (.exe) + Electron Builder
- **Almacenamiento**: Carpeta Documentos del usuario (ruta resuelta por el SO)

## El Problema: FastAPI no puede servir imágenes locales de forma fiable

FastAPI falla al usar `StaticFiles` en producción (.exe) por tres razones críticas:
1. **Montaje en tiempo de importación**: Las rutas pueden no existir todavía o el servidor no las encuentra.
2. **Corrupción de rutas de PyInstaller**: `os.path.abspath()` resuelve relativo a `_MEIPASS` (carpeta temporal), lo que invalida las rutas locales.
3. **Fallas silenciosas**: `StaticFiles` no lanza errores si la carpeta no existe al arrancar, fallando en el cliente.

## La Solución: Protocolo Personalizado de Electron (`app://`)

La solución es omitir el backend (Python) para la entrega de imágenes y usar un protocolo nativo de Electron.

**Flujo corregido:**
`React` → `app://covers/photo.jpg` → `Electron protocol handler` → `Disk` (Directo, sin Python).

## Implementación Paso a Paso

### 1. Modificar `main.cjs` (Electron)

**Paso A: Importar dependencias**
```javascript
const { app, BrowserWindow, protocol, net } = require('electron');
```

**Paso B: Registrar el esquema antes de `app.whenReady()`**
```javascript
protocol.registerSchemesAsPrivileged([
  {
    scheme: 'app',
    privileges: {
      secure: true,
      standard: true,
      supportFetchAPI: true
    }
  }
]);
```

**Paso C: Definir `getCoversPath()` (Espejo de `config.py`)**
```javascript
function getCoversPath() {
  const documents = app.getPath('documents');
  return path.join(documents, 'Bookish', 'data', 'portadas');
}
```

**Paso D: Registrar el handler dentro de `app.whenReady()`**
```javascript
app.whenReady().then(() => {
  protocol.handle('app', (request) => {
    const url = new URL(request.url);
    if (url.hostname === 'covers') {
      const filename = url.pathname.replace(/^\//, '');
      const filePath = path.join(getCoversPath(), filename);
      return net.fetch(`file:///${filePath}`);
    }
    return new Response('Not found', { status: 404 });
  });
  // ... resto del arranque ...
});
```

### 2. Limpiar `main.py` (FastAPI)

Elimina el montaje de `StaticFiles` para las portadas. Python ya no sirve las imágenes.

```python
# ELIMINAR estas líneas de main.py:
from fastapi.staticfiles import StaticFiles
from config import COVERS_DIR
PORTADAS_ABS_PATH = os.path.abspath(COVERS_DIR)
app.mount('/portadas', StaticFiles(directory=PORTADAS_ABS_PATH), name='portadas')
```

### 3. Actualizar el Frontend (React)

Las URLs de las imágenes deben usar el nuevo protocolo.

```javascript
// Helper recomendado
export const getCoverUrl = (filename) =>
  filename ? `app://covers/${filename}` : null;

// Uso en componente
<img src={getCoverUrl(book.cover)} alt={book.titulo} />
```

## Reglas de Oro

### ✅ HACER (Correcto)
- **Usar `app.getPath('documents')`**: Siempre resuelve la carpeta Documentos vía Electron API.
- **Usar `app://` para archivos locales**: Registra un protocolo personalizado. Nunca expongas rutas `file://` directamente al React.
- **Guardar solo nombres de archivo en la DB**: Nunca guardes rutas absolutas.
- **Asegurar directorios**: Llama a `os.makedirs` (Python) o `fs.mkdirSync` (Node) antes del acceso.

### ✕ NO HACER (Prohibido)
- **Nunca usar `StaticFiles` para contenido de usuario**: Falla en producción al estar ligado al tiempo de importación.
- **Nunca usar `os.path.abspath()` en un .exe**: Se rompe con el sistema de archivos de PyInstaller.
- **Nunca servir archivos locales vía `localhost`**: Ata la disponibilidad de las imágenes al estado del backend.

---
