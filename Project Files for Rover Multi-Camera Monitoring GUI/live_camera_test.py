import sys
import subprocess
import gi


gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

class CameraManager:
    def __init__(self):
        self.camera_map = {
          
            "My Laptop Cam": {"friendly_name": "HD User Facing"}, 
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
            return []

    def resolve_device_name(self, camera_name):
        if camera_name not in self.camera_map: 
            return None
            
        target_name = self.camera_map[camera_name]["friendly_name"].lower().strip()
        
        for dev in self._devices:
            if target_name in dev.lower().strip():
                return dev
                
        return None

if __name__ == "__main__":
    Gst.init(None)
    manager = CameraManager()

    print("\n=== HARDWARE DETECTED BY WINDOWS ===")
    for cam in manager._devices:
        print(f" -> {cam}")
    print("====================================\n")

    target_slot = "My Laptop Cam"
    resolved_name = manager.resolve_device_name(target_slot)

    if resolved_name:
        print(f"[SUCCESS] Manager locked onto exact hardware: '{resolved_name}'")
        
       
        pipeline_str = f"mfvideosrc device-name='{resolved_name}' ! videoconvert ! autovideosink"
        print(f"[GSTREAMER] Attempting live feed: {pipeline_str}")
        
        pipeline = Gst.parse_launch(pipeline_str)
        res = pipeline.set_state(Gst.State.PLAYING)
        
       
        if res == Gst.StateChangeReturn.FAILURE:
            print("\n[WARNING] Physical camera is busy or restricted by Windows Privacy Settings.")
            print("[FALLBACK] Launching GStreamer test pattern to verify installation functionality...")
            pipeline.set_state(Gst.State.NULL)
            
           
            pipeline_str = "videotestsrc ! videoconvert ! autovideosink"
            pipeline = Gst.parse_launch(pipeline_str)
            pipeline.set_state(Gst.State.PLAYING)

        print("\n>>> VIDEO WINDOW SHOULD BE OPEN NOW <<<")
        print("Click on the video window and press Ctrl+C in this terminal to exit.")
        
        loop = GLib.MainLoop()
        try:
            loop.run()
        except KeyboardInterrupt:
            print("\nShutting down camera feed...")
            pipeline.set_state(Gst.State.NULL)
    else:
        print("\n[FAILED] Could not resolve 'HD User Facing'. Ensure it shows in the hardware list above.")