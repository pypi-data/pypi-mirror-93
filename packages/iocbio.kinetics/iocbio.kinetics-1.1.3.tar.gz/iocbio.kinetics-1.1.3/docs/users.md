# Users Guide

The use of the application is made as straightforward as possible. At
the first start of the application, database connection has to be
established.


## IOCBIO Kinetics application

The application can be started from the command line as
`iocbio-kinetics`. Please note that it has to be in the default PATH and
arranging it will depend on your operating system. In Linux, if
installing using `pip` into user's home, the application is installed
into `~/.local/bin` folder. In MacOS, the location will be different.

When using Anaconda in Windows, you can start the application by starting
Anaconda Navigator and launching it through the Navigator.


### Database connection

On start, the application will create an SQLite database in user's home
folder by default. To connect to the laboratory database, click on the
"Change database" button located towards the top right of the
application window. This will allow you to select PostgreSQL database
and will open the window with the connection details, as shown below.

![database connection](img/database-connection.png)

*Above: Database connection settings*

When connecting to PostgreSQL, you will be asked to provide the database
server host name, name of the database, and the schema to be used
(latter is usually `public`). After entering that data, you will be
asked for user login information and whether you want to store it
safely in a keyring provided by the operating system (details in the
[manual](https://pypi.org/project/keyring/) of the used library).

Stored password and username can be removed at any time by opening
database connection settings again.


### Application

Application has only one window with all information available to the
user.

![Application GUI](img/application-scheme.png)

*Above: Overall scheme of the application GUI*


On the left, the data in the database are listed and organized by the
protocol of the experiment (top of the list) and the date of the
experiment (bottom of the list). The experiments are available in
both sections allowing you to look through experiments either by
protocol or date.

When selected from the database, the experimental data will be loaded
in read-only form. To make corrections to the regions of interest,
event names, switch read-only mode off using the toggle on the bottom
left. This will change the toggle text into the red, indicating that
the subsequent changes will be saved into the database.

Data can be imported either by using dedicated dialog through "Open
new experiment" button on the top right or using the command line
interface. All protocol options required by the import are available
through both interfaces (GUI and command line options). When
loading an [example dataset](example-data/18-06-04_1_ch3.txt) only
file fas to be specified as all required experiment details are
detected automatically by the analysis module.

On data import, the database is open in read-write mode with all the
changes saved by default. When you open an experiment that was in the
database already, the program switches to the read only mode. In this
case, read-write can be enabled using the toggle.

With the experiment opened, you can add the new regions of interest
(ROI) by the right-click on the mouse in the raw data section next to
the region of interest and selecting "Add ROI". The ROI will be marked
by randomly selected color and can be adjusted by moving it (press the
left mouse button in the middle of ROI, hold it and move the selected
region), resizing it (select ROI border by mouse and move it). ROI can
be deleted by the right click on it and selecting "Remove ROI".

ROIs can be associated with the event names. Event names can be
entered and changed in the dedicated box inside the primary analysis
area. Press Enter after changing the text to write the changes into
the database. Secondary analysis modules can take the information provided
by events and use it for secondary data fitting. For example, the
Michealis-Menten analysis protocol may interpret the entered event name as
a number indicating a concentration and use it for fitting, as shown
in the figure above.

Results of the primary and secondary data analysis are shown using the
graph and table in the corresponding sections of the main window of
the application.

See demo videos for how to interact with the application in practice
and adjust individual window elements.


## Use of scripts for data fetching and Bayesian ANOVA analysis

Together with the main application, we provide scripts for data
fetching from the database together with the script for the simple
ANOVA analysis. Scripts are

* `iocbio-fetch` Fetch data in long form
* `iocbio-fetch-repeated` Fetch data in wide form
* `iocbio-banova` Fetch data and perform Bayesian ANOVA analysis

If you wish to use the included scripts, you will have to establish a
database connection first using `iocbio-kinetics` application. This
includes saving the password on login page as the scripts are not
using any GUI when they run and cannot request the password.

The scripts will all require the SQL SELECT statement which is stored in a
separate text file. All scripts are run from the command line and use
command line arguments to obtain the required input. Each script has
help information with the description of the arguments available using
`--help` option (as in `iocbio-fetch --help`).


### Fetching data in long form

This is the simplest of the provided scripts and will just either
store the result of the provided SQL statement in comma separated value
(CSV) file (if the file name is given as an argument) or print out on
standard output if `-` is used instead of the file name. The first
line of the output will contain the names of the columns.


### Fetching data in wide form

When you have the SQL SELECT query returning a data in a long form as

```
cellID, condition-name, value
```

and you want to get data in a wide form as in

```
cellID, value-in-condition-1, value-in-condition-2, ..., value-in-condition-n
```

there is a script included to fetch the data in such form:
`iocbio-fetch-repeated`. In addition to the SQL SELECT statement file,
the script will require the name of the column containing numerical
values that will be assembled into the resulting table (`value` in the
example above), condition value that will be used for naming columns
in the resulting table (`condition-name` in the example), and unique
ID identifying the result of the experiment, which has to be on the same
row (`cellID` in the example).

As in the case of `iocbio-fetch`, the resulting table can be either stored
in CSV file or printed out in standard output.


### Bayesian ANOVA analysis

The included script `iocbio-banova` allows performing the Bayesian ANOVA
test on the data fetched from the database using the SQL SELECT statement
file. To use `iocbio-banova` script, you have to install R and `rpy2`
Python package.

The script will analyze the data fetched from the database, compare
the results obtained by different models, and will plot the results as
requested. It uses the same approach as used by
[JASP](https://jasp-stats.org/) in the same analysis with the
simplicity of the data fetching and automatic analysis. However, we
recommend the new users first to get familiar with the analysis using
JASP interface and tutorials. When the concepts and how to interpret
the results is clear, you could use `iocbio-banova` to perform the
analysis routinely with the up-to-date data.


## Extraction of the data

With the use of the laboratory database for analysis, it is possible
to extract the relevant datasets from the database and share them
separately from the other records. For example, extraction and sharing
of the data as a part of the publishing of a study. In this respect,
the extracted data should cover all relevant database records as well
as all external files used to analyze the data. Here, we describe one
of the ways for achieving such data extraction.

When working on some study, we have been using a separate database table
that lists all experiments performed in the study. The study table
consists of rows with reference to a record in
`kinetics_experiments` table through `experiment_id` and, usually, a
field for a comment regarding a particular experiment, if any, as well
as whether the experiment was successful. In addition, `experiment_id`
is used throughout the database to link experiments with the data
describing the experiment, such as preparation used in it, solutions,
temperature. As a result, we have several tables linked to
`experiment_id` and possibly linked further with the other tables that
are all needed to form the full dataset.

For data extraction, we will use the study table as a starting point
and proceed with the extraction from there. As an extraction
tool, we recommend using [Jailer](http://jailer.sourceforge.net/)
that is built for such data extraction.

Jailer user manual covers data extraction very well. Here we will go
only through the overall description of the process. First, the
database connection would have to be established. With the connection
established, Jailer will have to learn the data model describing
associations between records in the database. For that, you would have
to analyze the database. If you use multiple schemas in PostgreSQL,
each schema has to be analyzed by doing analysis one after another and
keeping the old analysis results intact (default in Jailer). With the
analysis done and the data model complete, Jailer main window can be
opened. In that window, select the study table as the one to get
exported. On how to formulate the data extraction model and how to
limit the data that is extracted, please see tutorials and FAQ in
[Jailer documentation](http://jailer.sourceforge.net).

Jailer allows extracting data in the form of SQL statements,
[DbUnit](http://dbunit.sourceforge.net/) and XML formats. When
extracting in SQL statements, one can complement the script generated
by Jailer with the database schema description to set up a copy of the
database that can be used by Kinetics software directly. For example,
if you wish to provide an externally accessible database with your data
and want to support access to it through Kinetics software as well.

In addition to the database data extraction, it is sometimes required
to export the used files. This is in a case when the original
recordings are not imported into the database by Kinetics plugins. For
example, it is impractical to load large image files into the database,
and it is much more efficient to store them separately. In this case,
those separate files have to be added to the set describing the
experiment.

Finally, to make analysis steps fully reproducible, the extracted data
has to be accompanied by the software used in the analysis. In the
case of Kinetics, it is sufficient to specify version number or, if the
development version was used, the commit ID as reported in [project
page](https://gitlab.com/iocbio/kinetics/-/commits/master). If
additional modules were used, then either module code or, if developed
in open, the version information has to be provided.

Notice that the data extraction does not cover a description of the
connection between data tables, nor a standards-based description of the
data records content. For that, the extracted dataset would have to be
annotated using the dedicated tools which are developed by others as a
part of research data publishing initiatives.
