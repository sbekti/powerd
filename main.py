#!/usr/bin/env python3

import os
import time
from prometheus_client import start_http_server, Gauge, Enum
from dds238 import DDS238

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, meter, polling_interval_seconds=5):
        self.meter = meter
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.current = Gauge("current", "Current")
        self.export_energy = Gauge("export_energy", "Export Energy")
        self.frequency = Gauge("frequency", "Frequency")
        self.import_energy = Gauge("import_energy", "Import Energy")
        self.power = Gauge("power", "Power")
        self.power_factor = Gauge("power_factor", "Power Factor")
        self.reactive_power = Gauge("reactive_power", "Reactive Power")
        self.voltage = Gauge("voltage", "Voltage")

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Update Prometheus metrics with application metrics
        self.current.set(self.meter.current)
        self.export_energy.set(self.meter.export_energy)
        self.frequency.set(self.meter.frequency)
        self.import_energy.set(self.meter.import_energy)
        self.power.set(self.meter.power)
        self.power_factor.set(self.meter.power_factor)
        self.reactive_power.set(self.meter.reactive_power)
        self.voltage.set(self.meter.voltage)

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "60"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))
    modbus_device = os.getenv("MODBUS_DEVICE", "/dev/ttyUSB0")
    meter_id = int(os.getenv("METER_ID", "1"))

    meter = DDS238(modbus_device=modbus_device, meter_id=meter_id)

    app_metrics = AppMetrics(
        meter=meter,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    print(f"Prometheus exporter is listening on port {exporter_port}")
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
