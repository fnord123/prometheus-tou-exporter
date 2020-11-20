# Prometheus Wemo Exporter
#
# David Putzolu, based on code by Scott Baker(http://www.smbaker.com/)

from prometheus_client import start_http_server, Gauge
import requests
import pywemo
import sys
from time import sleep
from envargparse import EnvArgParser, EnvArgDefaultsHelpFormatter

class wemoPrometheusExporter:
  def __init__(self):
    try:
      self._args = {}
      self.main()
    except Exception as e:
      print('Error - {}'.format(e))
      sys.exit(1)

  def process_args(self):
    parser = EnvArgParser\
          ( prog="Wemo Prometheus Exporter"
          , formatter_class=EnvArgDefaultsHelpFormatter
          )
    parser.add_argument\
        ( '--interval'
        , required=False
        , env_var="INTERVAL"
        , type=int
        , nargs="?"
        , default=15
        , const=True
        , help="How often data should be pulled from the Wemo and exported to influxdb"
        )
    parser.add_argument\
        ( '--wemo_ip'
        , required=True
        , env_var="WEMO_IP"
        , nargs="?"
        , default="localhost"
        , const=True
        , help="IP address for the Wemo to pull data from"
        )
    parser.add_argument\
        ( '--wemo_device'
        , required=False
        , env_var="WEMO_DEVICE"
        , nargs="?"
        , default="Wemo Insight"
        , const=True
        , help="name of the Wemo device being queried"
        )
    parser.add_argument\
        ( '--port'
        , required=False
        , env_var="EXPORTER_PORT"
        , type=int
        , default=8000
        , const=True
        , nargs="?"
        , help="Port number the exporter should bind to"
        )
    parser.add_argument\
        ( '--verbose'
        , required=False
        , env_var="EXPORTER_VERBORSE"
        , action='store_true'
        , default=False
        , help="Enable verbose debug outputs"
        )
    self._args = parser.parse_args()
    print(self._args)

  def update_field(self, prometheus_field, wemo_field_value):
    prometheus_field.labels(self._args.wemo_device) \
      .set(wemo_field_value)
    if self._args.verbose:
      print("%s is %s" % (prometheus_field, wemo_field_value))

  def collect(self):
    device = pywemo.discovery.device_from_description( \
      self._wemo_url, None)
    self.update_field(self._power, device.current_power / 1000)

  def main(self):
    self.process_args()
    port = pywemo.ouimeaux_device.probe_wemo(self._args.wemo_ip)
    self._wemo_url = 'http://%s:%i/setup.xml' \
      % (self._args.wemo_ip, port)
    if self._args.verbose:
      print("wemo url is %s" % self._wemo_url)
      print("Device is %s" % \
        pywemo.discovery.device_from_description(self._wemo_url, None))
    self._power = \
      Gauge('power', 'Instantaneous power consumption', ['device'])
    start_http_server(self._args.port)

    while True:
      self.collect()
      sleep(self._args.interval)

wemoPrometheusExporter()
