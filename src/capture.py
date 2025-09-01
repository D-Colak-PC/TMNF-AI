from time import perf_counter, sleep
import dxcam
import cv2
from win32gui import FindWindow, GetClientRect, ClientToScreen

TITLE = "TmForever"
FPS = 20


def client_region(hwnd):
    l, t, r, b = GetClientRect(hwnd)
    x, y = ClientToScreen(hwnd, (0, 0))
    return (x, y, x + (r - l), y + (b - t))


# Find window + region
hwnd = FindWindow(None, TITLE)
if not hwnd:
    raise RuntimeError(f"Window '{TITLE}' not found")
region = client_region(hwnd)

camera = dxcam.create(region=region, output_color="BGR")

interval = 1.0 / FPS
t = perf_counter()

camera.start(target_fps=FPS)
while True:
    frame = camera.get_latest_frame()

    cv2.imshow("preview", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

    # throttle to ~20 FPS
    t += interval
    s = t - perf_counter()
    if s > 0:
        sleep(s)
    else:
        t = perf_counter()  # if we fell behind, reset schedule
