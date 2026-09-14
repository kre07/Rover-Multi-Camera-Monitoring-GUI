import subprocess

class CameraManager:
    def __init__(self):
        # This maps the GUI panels to the permanent hardware names.
        # "HD User Facing" the front cam from lap
        self.camera_map = {

            "Orbbec / Front": {"friendly_name": "HD User Facing"}, # Normal lap webcam
            
            "WebCam / Back": {"friendly_name": "Elgato Facecam"}, # The webcam
            
            "IP Cam / Top": {"friendly_name": "USB Camera"},
            "IR Cam / ARM": {"friendly_name": "IR"},
        }
        self._cached_names = {}
        self._devices = self._get_windows_camera_list()

    def _get_windows_camera_list(self):
        try:
            result = subprocess.check_output(
                ["powershell", "-Command", "Get-PnpDevice -Class Camera | Select -Expand FriendlyName"],
                text=True, stderr=subprocess.DEVNULL
            )
            return [line.strip() for line in result.splitlines() if line.strip()]
        except Exception as e:
            print(f"[CameraManager ERROR] Failed to list cameras: {e}")
            return []

    def resolve_device_name(self, camera_name):
        if camera_name in self._cached_names:
            return self._cached_names[camera_name]

        if camera_name not in self.camera_map:
            print(f"[CameraManager ERROR] Unknown GUI slot: {camera_name}")
            return None

        target_name = self.camera_map[camera_name]["friendly_name"].lower().strip()

        for dev in self._devices:
            if target_name in dev.lower().strip():
                self._cached_names[camera_name] = dev
                return dev

        print(f"[CameraManager WARNING] Hardware not plugged in for: {camera_name}")
        return None