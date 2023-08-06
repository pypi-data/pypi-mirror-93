# Modules supporting Oroboros Instruments

Currently, data can be imported using CSV export from O2K software. As
CSV contains data for the both respiration chambers, chamber of
interest has to be specified on import. In addition, as there is no
information on when the experiment was performed in CSV, date and time
has to be specified as well.

Example of the call:

```
iocbio-kinetics --o2k-chamber A --date-time "2018-10-04 11:12" ~/tmp/2018-10-04\ P4-01_DatLab7_4.csv
```

Modules:

- [CSV import](csv)

