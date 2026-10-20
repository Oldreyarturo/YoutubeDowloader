# YouTube Downloader

Aplicación de escritorio para Windows desarrollada en **Python** con una interfaz gráfica basada en **Tkinter**. Permite descargar videos de YouTube en formato **MP4** y obtener el audio en **MP3**, utilizando **yt-dlp** y **FFmpeg**.

## Características

- Interfaz gráfica sencilla para ingresar enlaces de YouTube.
- Descarga de videos en formato MP4.
- Extracción y conversión de audio a MP3.
- Selección de la carpeta de destino.
- Procesamiento multimedia mediante FFmpeg.
- Distribución para Windows mediante ejecutable e instalador.

## Tecnologías utilizadas

| Tecnología | Función |
| --- | --- |
| Python | Lógica de la aplicación |
| Tkinter | Interfaz gráfica |
| yt-dlp | Obtención de información y descarga de contenido |
| FFmpeg | Conversión y procesamiento de audio y video |
| PyInstaller | Generación del ejecutable de Windows |
| Inno Setup | Creación del instalador |

## Instalación

### Opción 1: instalador para Windows

1. Descarga el instalador `YouTube Downloader Setup.exe` desde la sección **Releases** del repositorio, si está disponible.
2. Ejecuta el instalador y sigue las instrucciones.
3. Abre **YouTube Downloader** desde el acceso directo creado.

### Opción 2: ejecutar desde el código fuente

**Requisitos:** Windows, Python 3 y los ejecutables `yt-dlp.exe` y `ffmpeg.exe`.

1. Clona o descarga el repositorio.
2. Coloca las herramientas en la carpeta `tools`:

   ```text
   YouTubeDownloader/
   ├── YouTubeDownloader.py
   └── tools/
       ├── yt-dlp.exe
       └── ffmpeg.exe
   ```

3. Desde la carpeta del proyecto, ejecuta:

   ```powershell
   python YouTubeDownloader.py
   ```

> Si el repositorio incluye un archivo `requirements.txt`, instala sus dependencias con `python -m pip install -r requirements.txt` antes de iniciar la aplicación.

## Uso

1. Abre **YouTube Downloader**.
2. Pega el enlace del video.
3. Selecciona el formato de salida: **MP4** o **MP3**.
4. Elige la carpeta donde guardar el archivo.
5. Inicia la descarga y espera a que termine el procesamiento.

## Estructura del proyecto

```text
YouTubeDownloader/
├── YouTubeDownloader.py
├── tools/
│   ├── yt-dlp.exe
│   └── ffmpeg.exe
├── icono.ico                 # Opcional
└── README.md
```

Los archivos generados por PyInstaller y el instalador pueden encontrarse en carpetas como `dist/` e `installer/`, si se incluyen en el proyecto.

## Cómo funciona

1. La aplicación recibe y valida el enlace ingresado.
2. **yt-dlp** identifica el contenido y gestiona su descarga.
3. **FFmpeg** combina pistas o convierte el audio cuando es necesario.
4. El archivo final se guarda en la carpeta seleccionada.

## Consideraciones

- El programa depende del funcionamiento y compatibilidad de **yt-dlp** con la plataforma.
- No utiliza directamente la API oficial de YouTube ni requiere una clave de YouTube Data API.
- Descarga únicamente contenido para el que tengas autorización y respeta los derechos de autor y las condiciones de uso aplicables.

## Autor

**Oldrey**

---

Proyecto desarrollado con fines de aprendizaje y práctica en Python, interfaces gráficas, automatización y procesamiento multimedia.
