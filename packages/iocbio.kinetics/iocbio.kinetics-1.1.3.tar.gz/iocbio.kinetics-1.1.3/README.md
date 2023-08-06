# Kinetics analysis program

IOCBIO Kinetics is a cross-platform application for analysis of
different traces, as described by its plugins. While originally
developed for analysis of enzyme kinetics, the other types of traces
can be analyzed as well. It is designed to analyze traces where some
measured parameter depends on one other parameter, such as time or
space. For example, respiration rate measurements via following oxygen
concentration in time and its changes through addition of metabolites.

The analysis of experimental traces is built as a pipeline, with the
data imported from the experiment file, regions of interest
automatically generated or set by user, data fitted and
analyzed. Communication between different plugins is done through the
database backend with the analysis results stored in the
database. Software is modular with the new modules added easily to fit
the new types of experiments.

- User documenation: https://iocbio.gitlab.io/kinetics
- Issues: https://gitlab.com/iocbio/kinetics/issues


# Included third-party software

Distribution includes
[records.py](https://github.com/kennethreitz/records) with the patches
applied to fix issues that have not been merged upstream. Records
license is available at
[LICENSE-records](iocbio/kinetics/thirdparty/LICENSE-records).

## Copyright

Copyright (C) 2018-2020 Laboratory of Systems Biology, Department of
Cybernetics, School of Science, Tallinn University of Technology
(https://sysbio.ioc.ee).

Software license: GPLv3, see [LICENSE](LICENSE).

Contact: Marko Vendelin <markov@sysbio.ioc.ee>
