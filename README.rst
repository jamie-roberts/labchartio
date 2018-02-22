==========
LabChartIO
==========


What does it do?
----------------
This package (labchartio) is a collection of functions necessary for handling the
LabChart Windows binary format files specifically generated with header information
pertaining to the MRI field dosimeters manufactured at Queensland University,
Australia.

How does it work?
-----------------
The binary format standard is available from LabChart so this package just implements the binary unpacking and reading into a pandas dataframe or writes to CSV. The code is presented as a high level command line app. 

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
The code ships with no tests yet and requires some work, but it is in a good enough condition that it can be used for research. Because the code is in beta stage (user testing) it is imperative the user test the code's ability to decode a binary file they already have a CSV for and then they can confirm for themselves the code works. I can only test the code on my laptop I cannot at this stage make any guarentees that it will work on your computer. That being said if you have any issues you should post them on the Github page for the code with a description of what have gone wrong and any messages that popped up. I will try to fix bgs and update the code as and when I can. 

What do I need?
---------------
Code is tested on Windows. Wants Python 3 environment.

Install all dependencies first then clone repo and run from it.


How do I install python?
------------------------
Go to `python.org <https://www.python.org/downloads/>`_ then use pip to install the rest of the dependencies::

  pip install numpy pandas datetime click

How do I install labchartio?
--------------------
The simplest way to install labchartio is by downloading zip from repo from::




Where can I get help?
---------------------
There's me on Github issues or for any general python issues I suggest `Stack Overflow <https://stackoverflow.com/questions/tagged/python>`_
- that's where I would go.

Authors
-------
* **Jamie Roberts** - `jamie-roberts <https://github.com/jamie-roberts>`_

License
-------
This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_
file for details

Acknowledgments
---------------
* This code and the author are not affiliated with LabChart in anyway whatsoever.