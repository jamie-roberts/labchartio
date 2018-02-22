==========
LabChartIO
==========


What does it do?
----------------
This package (labchartio) is a collection of functions necessary for handling the LabChart Windows binary format files specifically generated with header information pertaining to the MRI field dosimeters manufactured at Queensland University, Australia.

How does it work?
-----------------
The binary format standard is available from LabChart so this package just implements the binary unpacking and reading into a pandas dataframe or writes to CSV. The code is presented as a high level command line app.

The CSV will have the 6 channels of data with a time and date stamp in the first column. The data is aggregated to one second intervals by taking the average. If the user requires the ability to write the CSV at its full time resolution of 50 Hz then please either drop me an email or open an issue on the `issue tracker <https://github.com/jamie-roberts/labchartio/issues>`_ and I will add it as a feature when I get the time. 

Show me a quick example
-----------------------
To demo labchartio on an example data set::

  $ labchartio --filename "./test_data.bin"

The terminal should produce::

  Reading/Writing file.
  Done.
  Written CSV to ./test_data.bin.csv
  You may read csv using script:
  >>> import pandas as pd
  >>> fname = "test_data.bin"
  >>> pd.read_csv((fname + ".csv"), index_col=0).head()

Is it ready?
------------
The code ships with no tests yet (working on it) and requires some work, but it is in a good enough condition that it can be used for research. Because the code is in beta stage (user testing) it is imperative the user test the code's ability to decode a binary file they already have a CSV for and then they can confirm for themselves the code works. I can only test the code on my laptop I cannot at this stage make any guarentees that it will work on your computer. That being said if you have any issues you should post them on the Github page for the code with a description of what have gone wrong and any messages that popped up. I will try to fix bgs and update the code as and when I can. I appreciate any feed back and will consider feature requests if they I can make the time for them.

What do I need?
---------------
Code is tested on Windows Python 3 environment.

First install all dependencies then install repo and enter command::
  labchartio --filename=./test_file.bin`


How do I install python?
------------------------
Go to `python.org <https://www.python.org/downloads/>`_ and select python 3. Then use pip to install the rest of the dependencies::

  pip install numpy pandas click

How do I install labchartio?
--------------------
The simplest way to install labchartio is via pip::

pip install git+https://github.com/jamie-roberts/labchartio.git

or by downloading zip from `repo <https://github.com/jamie-roberts/labchartio/>`_ and running `python setup.py install` form within repo.


Where can I get help?
---------------------
There's me on Github issues or for any general python issues I suggest `Stack Overflow <https://stackoverflow.com/questions/tagged/python>`_
- that's where I would go.

Authors
-------
* **Jamie Roberts** - `jamie-roberts <https://github.com/jamie-roberts>`_ jrobertsink <at> gmail <dot> com

License
-------
This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_
file for details

Acknowledgments
---------------
* This code and the author are not affiliated with LabChart in anyway whatsoever.