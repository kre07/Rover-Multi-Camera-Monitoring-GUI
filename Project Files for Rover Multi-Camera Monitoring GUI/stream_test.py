import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)

# Using your working device-index to feed the network pipeline
# (Make sure to change index=0 to index=1 if it was 1 that worked!)
pipeline_str = (
    "mfvideosrc device-index=0 ! "
    "videoconvert ! "
    "jpegenc ! "
    "rtpjpegpay ! "
    "udpsink host=127.0.0.1 port=5001"
)

pipeline = Gst.parse_launch(pipeline_str)
pipeline.set_state(Gst.State.PLAYING)

print("🚀 Streaming real webcam feed over UDP on Port 5001...")

loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)