import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import sys

Gst.init(None)

# Testing local camera only with device-index=0 (No UDP network code at all)
pipeline_str = "mfvideosrc device-index=0 ! videoconvert ! autovideosink"

pipeline = Gst.parse_launch(pipeline_str)

bus = pipeline.get_bus()
def on_message(bus, message):
    if message.type == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"\n❌ [INDEX 0 ERROR]: {err}")
        sys.exit(1)

bus.add_signal_watch()
bus.connect("message", on_message)

pipeline.set_state(Gst.State.PLAYING)
print("👀 Testing device-index=0 raw...")

loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)