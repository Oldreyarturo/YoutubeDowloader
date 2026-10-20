import os
import sys
import subprocess
import threading
import tkinter as tk

from tkinter import ttk, filedialog, messagebox


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Detectar correctamente la ubicación cuando se ejecuta como
# programa Python o como EXE creado con PyInstaller.

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Carpeta donde están yt-dlp y FFmpeg
TOOLS_DIR = os.path.join(
    BASE_DIR,
    "tools"
)


YTDLP = os.path.join(
    TOOLS_DIR,
    "yt-dlp.exe"
)


FFMPEG = os.path.join(
    TOOLS_DIR,
    "ffmpeg.exe"
)


# ============================================================
# CARPETA DE DESCARGAS
# ============================================================

# Las descargas NO se guardan junto al EXE.
# Esto evita problemas de permisos cuando el programa
# está instalado en C:\Program Files.

USER_DOWNLOADS = os.path.join(
    os.path.expanduser("~"),
    "Downloads"
)


DEFAULT_OUTPUT = os.path.join(
    USER_DOWNLOADS,
    "YouTube Downloader"
)


# Crear carpeta de descargas si no existe
os.makedirs(
    DEFAULT_OUTPUT,
    exist_ok=True
)


# ============================================================
# VARIABLES
# ============================================================

downloading = False


# ============================================================
# LOG
# ============================================================

def log(text):

    console.insert(
        tk.END,
        text + "\n"
    )

    console.see(
        tk.END
    )


# ============================================================
# COMPROBAR HERRAMIENTAS
# ============================================================

def check_tools():

    missing = []

    if not os.path.isfile(YTDLP):

        missing.append(
            "yt-dlp.exe"
        )

    if not os.path.isfile(FFMPEG):

        missing.append(
            "ffmpeg.exe"
        )

    if missing:

        messagebox.showerror(
            "Faltan herramientas",
            "No se encontraron:\n\n"
            + "\n".join(missing)
            + "\n\n"
            + "Colócalos en:\n"
            + TOOLS_DIR
        )

        return False

    return True


# ============================================================
# SELECCIONAR CARPETA
# ============================================================

def select_folder():

    folder = filedialog.askdirectory(
        title="Selecciona la carpeta de destino"
    )

    if folder:

        folder_entry.delete(
            0,
            tk.END
        )

        folder_entry.insert(
            0,
            folder
        )


# ============================================================
# PROGRESO
# ============================================================

def process_output(line):

    line = line.strip()

    if not line:
        return

    log(line)

    # Intentar detectar porcentaje
    if "%" in line:

        try:

            parts = line.split()

            for part in parts:

                if "%" in part:

                    value = (
                        part
                        .replace("%", "")
                        .strip()
                    )

                    value = float(value)

                    root.after(
                        0,
                        lambda v=value: progress.configure(
                            value=v
                        )
                    )

                    break

        except Exception:
            pass


# ============================================================
# DESCARGAR
# ============================================================

def download():

    global downloading

    if downloading:
        return

    if not check_tools():
        return

    url = url_entry.get().strip()

    output_folder = (
        folder_entry
        .get()
        .strip()
    )

    if not url:

        messagebox.showwarning(
            "URL",
            "Introduce una URL de YouTube."
        )

        return

    if not output_folder:

        messagebox.showwarning(
            "Carpeta",
            "Selecciona una carpeta de destino."
        )

        return

    try:

        os.makedirs(
            output_folder,
            exist_ok=True
        )

    except PermissionError:

        messagebox.showerror(
            "Permiso denegado",
            "No tienes permisos para escribir en esa carpeta.\n\n"
            "Selecciona otra carpeta, por ejemplo:\n"
            + DEFAULT_OUTPUT
        )

        return

    downloading = True

    download_button.config(
        state="disabled"
    )

    progress["value"] = 0

    threading.Thread(
        target=run_download,
        args=(
            url,
            output_folder
        ),
        daemon=True
    ).start()


# ============================================================
# PROCESAR DESCARGA
# ============================================================

def run_download(
    url,
    output_folder
):

    try:

        mode = download_mode.get()

        log("")
        log("=" * 60)
        log("NUEVA DESCARGA")
        log("=" * 60)

        log(
            f"URL: {url}"
        )

        log(
            f"Destino: {output_folder}"
        )


        # ----------------------------------------------------
        # VIDEO
        # ----------------------------------------------------

        if mode == "video":

            log(
                "Modo: VIDEO COMPLETO"
            )

            command = [
                YTDLP,

                "--ffmpeg-location",
                TOOLS_DIR,

                "-f",
                "bv*+ba/b",

                "--merge-output-format",
                "mp4",

                "-o",
                os.path.join(
                    output_folder,
                    "%(title)s.%(ext)s"
                ),

                url
            ]


        # ----------------------------------------------------
        # AUDIO
        # ----------------------------------------------------

        else:

            log(
                "Modo: SOLO AUDIO"
            )

            command = [
                YTDLP,

                "--ffmpeg-location",
                TOOLS_DIR,

                "-x",

                "--audio-format",
                "mp3",

                "--audio-quality",
                "0",

                "-o",
                os.path.join(
                    output_folder,
                    "%(title)s.%(ext)s"
                ),

                url
            ]


        log(
            "Iniciando yt-dlp..."
        )


        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )


        for line in process.stdout:

            root.after(
                0,
                process_output,
                line
            )


        process.wait()


        if process.returncode == 0:

            root.after(
                0,
                download_finished,
                True
            )

        else:

            root.after(
                0,
                download_finished,
                False
            )


    except Exception as error:

        root.after(
            0,
            log,
            f"ERROR: {error}"
        )

        root.after(
            0,
            download_finished,
            False
        )


# ============================================================
# FINALIZAR
# ============================================================

def download_finished(success):

    global downloading

    downloading = False

    download_button.config(
        state="normal"
    )

    if success:

        progress["value"] = 100

        log("")

        log(
            "✓ DESCARGA COMPLETADA"
        )

        messagebox.showinfo(
            "Completado",
            "La descarga terminó correctamente."
        )

    else:

        log("")

        log(
            "✗ LA DESCARGA FALLÓ"
        )

        messagebox.showerror(
            "Error",
            "La descarga no pudo completarse.\n\n"
            "Revisa la consola para ver el motivo."
        )


# ============================================================
# INTERFAZ
# ============================================================

root = tk.Tk()

root.title(
    "YouTube Downloader"
)

root.geometry(
    "900x650"
)

root.minsize(
    750,
    550
)


# ============================================================
# TÍTULO
# ============================================================

title = tk.Label(
    root,
    text="YOUTUBE DOWNLOADER",
    font=(
        "Segoe UI",
        22,
        "bold"
    )
)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(
    root,
    text="Descarga videos o extrae audio",
    font=(
        "Segoe UI",
        10
    )
)

subtitle.pack(
    pady=(0, 20)
)


# ============================================================
# URL
# ============================================================

url_frame = tk.Frame(
    root
)

url_frame.pack(
    fill="x",
    padx=25,
    pady=5
)


tk.Label(
    url_frame,
    text="URL:",
    width=12,
    anchor="w"
).pack(
    side="left"
)


url_entry = tk.Entry(
    url_frame,
    font=(
        "Segoe UI",
        10
    )
)

url_entry.pack(
    side="left",
    fill="x",
    expand=True
)


# ============================================================
# MODO
# ============================================================

mode_frame = tk.LabelFrame(
    root,
    text="Tipo de descarga"
)

mode_frame.pack(
    fill="x",
    padx=25,
    pady=15
)


download_mode = tk.StringVar(
    value="video"
)


tk.Radiobutton(
    mode_frame,
    text="Video completo (MP4)",
    variable=download_mode,
    value="video"
).pack(
    side="left",
    padx=20,
    pady=10
)


tk.Radiobutton(
    mode_frame,
    text="Solo audio (MP3)",
    variable=download_mode,
    value="audio"
).pack(
    side="left",
    padx=20,
    pady=10
)


# ============================================================
# CARPETA
# ============================================================

folder_frame = tk.Frame(
    root
)

folder_frame.pack(
    fill="x",
    padx=25,
    pady=5
)


tk.Label(
    folder_frame,
    text="Destino:",
    width=12,
    anchor="w"
).pack(
    side="left"
)


folder_entry = tk.Entry(
    folder_frame
)

folder_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)


folder_entry.insert(
    0,
    DEFAULT_OUTPUT
)


tk.Button(
    folder_frame,
    text="Cambiar",
    command=select_folder
).pack(
    side="right"
)


# ============================================================
# PROGRESO
# ============================================================

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="determinate"
)

progress.pack(
    fill="x",
    padx=25,
    pady=20
)


# ============================================================
# BOTÓN
# ============================================================

download_button = tk.Button(
    root,
    text="DESCARGAR",
    command=download,
    font=(
        "Segoe UI",
        13,
        "bold"
    ),
    height=2
)

download_button.pack(
    pady=5
)


# ============================================================
# CONSOLA
# ============================================================

console = tk.Text(
    root,
    height=15,
    font=(
        "Consolas",
        9
    )
)

console.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)


# ============================================================
# MENSAJES INICIALES
# ============================================================

log(
    "YouTube Downloader iniciado."
)

log(
    f"yt-dlp: {YTDLP}"
)

log(
    f"FFmpeg: {FFMPEG}"
)

log(
    f"Descargas: {DEFAULT_OUTPUT}"
)


# ============================================================
# INICIAR
# ============================================================

root.mainloop()