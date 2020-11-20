# Prometheus Wemo Exporter
#
# David Putzolu, based on code by Scott Baker(http://www.smbaker.com/)

from prometheus_client import start_http_server, Gauge
import sys
from time import sleep
from envargparse import EnvArgParser, EnvArgDefaultsHelpFormatter
from datetime import datetime
import time

class touPrometheusExporter:
  def __init__(self):
    try:
      self._args = {}
      self.main()
    except Exception as e:
      print('Error - {}'.format(e))
      sys.exit(1)

  def process_args(self):
    parser = EnvArgParser\
          ( prog="Time of Use Exporter"
          , formatter_class=EnvArgDefaultsHelpFormatter
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
        , env_var="EXPORTER_VERBOSE"
        , action='store_true'
        , default=False
        , help="Enable verbose debug outputs"
        )
    self._args = parser.parse_args()
    print(self._args)

  def calculate_tou_value_summer(self, now):
    if now.hour < 6 or now.hour >= 22:
      return 3
    elif now.hour >= 15 and now.hour <= 20:
      return 1
    else:
      return 2

  def calculate_tou_value_winter(self, now):
    if now.hour < 6 or now.hour >= 22:
      return 3
    elif now.hour >= 10 and now.hour < 17:
      return 2
    elif now.hour >= 20 and now.hour < 22:
      return 2
    else:
      return 1

  def calculate_tou_value(self):
    now = datetime.now()
    if now.month > 10 or now.month < 5:
      return self.calculate_tou_value_winter(now)
    else:
      return self.calculate_tou_value_summer(now)

  def update_field(self, prometheus_field, label, field_value):
    prometheus_field.labels(label).set(field_value)
    if self._args.verbose:
      print("%s is %s:%s" % (prometheus_field, label, field_value))

  def collect(self):
    tou_value = self.calculate_tou_value()
    self.update_field(self._tou_gauge, "TOU", tou_value)

  def main(self):
    self.process_args()
    self._tou_gauge = Gauge('tou', 'Time of Use value', ['device'])
    start_http_server(self._args.port)

    now = datetime.now()
    self.collect() # Report current TOU immediately

    next_hour = now.replace(hour=now.hour+1, minute=0, second=1)
    sleep_seconds = int((next_hour - now).total_seconds())
    if self._args.verbose:
      print("Sleeping for %s seconds until next hour" % (sleep_seconds))
    time.sleep(sleep_seconds) # Sleep until just after the next hour
    while True:
      self.collect()
      sleep(60 * 60) # Sleep for an hour before checking TOU again

touPrometheusExporter()
