"""Start BLE devices scaning service."""
from able import BluetoothDispatcher, require_bluetooth_enabled, require_runtime_permissions
from jnius import autoclass
from kivy.app import App
from kivy.lang import Builder


kv = """
BoxLayout:
   Button:
      text: 'Start service'
      on_press: app.scanner.start_service()
   Button:
      text: 'Stop service'
      on_press: app.scanner.stop_service()
"""


class Scanner(BluetoothDispatcher):

    @property
    def service(self):
        return autoclass("test.able.service_scan.ServiceScan")

    @property
    def activity(self):
        return autoclass("org.kivy.android.PythonActivity").mActivity

    # Need to turn on the adapter and obtain permissions, before service is started
    @require_bluetooth_enabled
    @require_runtime_permissions
    def start_service(self):
        self.service.start(self.activity, "")
        self.stop() # Can close the app, service will continue running

    def stop_service(self):
        self.service.stop(self.activity)


class ScannerApp(App):

    def build(self):
        self.scanner = Scanner()
        return Builder.load_string(kv)

    def start_service(self, *args, **kwargs):
        Scanner().start_service()


if __name__ == "__main__":
    ScannerApp().run()
