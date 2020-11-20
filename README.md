# dputzolu Time of Use Exporter

This is a simple prometheus exporter that exports information
relevant to the current electrical tariff, which varies when
one uses an electrical utility that offers Time Of Use billing.
This exporter currently just exports a single integer that
represents the current tariff, mapped as follows:
1 - Peak Tariff
2 - Mid-Peak
3 - Off-Peak

Integers are exported because Grafana can then use those
values with Thesholds to show colors (e.g. Peak tarriff in
red).  Grafana can also map those integers to strings, that is
where 1 is remapped to show as "Peak Tariff" (in red), etc.

Potential improvements:
* Export current time as a metric
* Export cost/KwH for the current tariff as a metric
* Remove hardcoding of peak/mid-peak/off-peak times, days,
  and season and have it be driven by an input file of some
  sort.
