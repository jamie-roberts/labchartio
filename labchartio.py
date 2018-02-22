""" This module is a collection of functions necessary for handling the
LabChart Windows binary format files. Specifically with header information
pertaining to the MRI field dosimeters manufactured at Queensland University,
Australia.

Author:Jamie Roberts

Examples:
========

Command line example:

    >>> python labchartio.py --help
    >>> python labchartio.py --filename=test_data.bin

High level example:
    
    >>> from labchartio import read_channels
    >>> import pandas as pd
    >>> fname = "test_data.bin"
    >>> 
    >>> data = read_channels(filename=fname) # you have the decoded data as a pandas dataframe.
    >>> data.to_csv((fname + '.csv')) # Write data to CSV.
    >>> pd.read_csv((fname + '.csv'), index_col=0).head() # Read saved data from CSV.


Minimal working example to get working with labchartio's binary parsing ability. Here only the Channel data is retrieved.

    >>> from labchartio.funcs import read_channels
    >>> data = pd.DataFrame(read_channels(filename=bin_fname))
`data' is a Pandas Dataframe containing the sample number and the 6 channels of data.

A minimal working example to show how the header file  reading feature of the labchartio parser works.

    >>> from labchartio.funcs import read_file_header, decode_byte_list
    >>> list_file_header = read_file_header(binfile, offset=0)
    >>> list_file_header = decode_byte_list(list_file_header)
    >>> file_tags = list_file_header[2:9] # sec
    >>> file_tags.append(list_file_header[11])
    >>> file_tags # secPerTick, year, month, day, hour, minute, seconds, samplesPerChannel


"""
from __future__ import division, absolute_import, print_function

import logging

import struct

import re
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import click

# from IPython import embed # embed() # Open terminal instance during execution

# Connect to parent logger
log = logging.getLogger()

def read_file_header(filename, offset):
    with open(filename, 'rb') as f:
        # Read the header
        f.seek(offset)
        header = f.read(68)
        # Read list of header tags:
            # magic4, version, secPerTick, year, month,
            # day, hour, minute, seconds, trigger, nChannels,
            # samplesPerChannel, timeChannel, dataFormat.
        [*file_header_list] = struct.unpack('<4sidiiiiiddiiii', header)

    return file_header_list


def decode_byte_list(header_list, strip_null=True):
    temp_header_list = list(header_list)
    for index, value in enumerate(header_list):
        if isinstance(value, bytes):
            value_decoded = value.decode()
            if strip_null:
                value_decoded = re.sub('\\x00', '',value_decoded)
            temp_header_list[index] = value_decoded
        else: temp_header_list[index] = value

    return temp_header_list


def read_channel_headers(filename, nChannels):
    all_channels = []
    for n in range(nChannels):
        offset = 68+n*96 # hardcoded byte data of headers
        channel = read_channel_header(filename=filename, offset=offset)
        channel = decode_byte_list(header_list=channel)
        all_channels.append(channel)

    return all_channels

def read_channel_header(filename, offset):
    """Open a binary test file, seek position, read bytes, then assign value to
    channel header tags and return list.

    :returns: List of the unpacked binary value.

    :Example:
        >>> from funcs import read_channel_header
        >>> binfile = './testdata/testdata.bin'
        >>> list_channel_header1 = read_channel_header(filename=binfile, offset=offset)
        >>> list_channel_header1 = decode_byte_list(list_channel_header1)
        >>> list_channel_header1
        ['dBx/dt', 'mTesla per second', 1.0, 0.0, 2.0, -2.0]

    """
    with open(filename, 'rb') as f:
        # Read the header
        f.seek(offset)
        header = f.read(96)
        # create list of channel tags:
            # Title32, Units32, scale,
            # offset, RangeHigh, RangeLow.
        [*channel_header_list] = struct.unpack('<32s32sdddd', header)

    return channel_header_list


def read_data_numpy(filename, offset, nChannels, samplePerChannel):
    with open(filename, 'rb') as f:
        # Read the header
        f.seek(offset)
        nSamples = nChannels*samplePerChannel
        data = np.fromfile(f, dtype='<f4', count = nSamples)

    return data

def read_time_tags(filename):
    list_file_header = read_file_header(filename, offset=0)
    list_file_header = decode_byte_list(list_file_header)
    file_tags = list_file_header[2:9] # sec
    file_tags.append(list_file_header[11])
    
    return file_tags # secPerTick, year, month, day, hour, minute, seconds, samplesPerChannel


def read_channels(filename):
    """High level function. Read a LabChart binary file with MrDose structure
    and return the channel data. This function clears up boiler plate code in notebook.

    :returns: Channel data: data_dBx, data_dBy, data_dBz, data_Bx, data_By, data_Bz
              file_tages: # secPerTick, year, month, day, hour, minute, seconds, samplesPerChannel

    """

    # **Read file header**

    # list of header tags
    # magic4, version, secPerTick, year, month, day, hour, minute, seconds, trigger,
    #     nChannels, samplesPerChannel, timeChannel, dataFormat
    # Accompanying formats
    # <4sidiiiiiddiiii

    # Read file header
    list_file_header = read_file_header(filename, offset=0)
    list_file_header = decode_byte_list(list_file_header)

    # **Read channel header**

    # Channel header tags
    # Title32, Units32, scale, offset, RangeHigh, RangeLow
    # channel header tags format
    # <32s32sdddd

    # Read channel header
    channel_headers = read_channel_headers(filename, nChannels=6)

    # **Read MrDose time-series data from channels into a flat list 'data'.**

    # Read 6 channel data

    # Calculate the byte offset of data.
    file_header_bytes = 68
    channel_header_bytes = 96
    nChannels = 6
    offset = file_header_bytes + nChannels*channel_header_bytes

    samplePerChannel =  list_file_header[11] # from header tag

    # Read data
    data = read_data_numpy(
        filename, offset=offset, nChannels=nChannels, samplePerChannel=samplePerChannel
    )

    # **Reshape 'data' into 2d array primed for pandas data analysis.**

    # Reshape data

    assert int(data.size/6) == samplePerChannel # Data check

    rows = samplePerChannel # From header tag
    columns = 6 # no. of channels
    # Reshape the data
    data_2d = np.reshape(data,(rows,columns))

    # **Split 2D data by column, primed for plotting each series.  **

    # Make a dictionary out of data channels
    # Extract channel data
    
    file_tags = read_time_tags(filename) # Timestamp metadata.
    
    data_channels = {
        'dBx':data_2d[:,0], # dB reads as dB/dt
        'dBy':data_2d[:,1],
        'dBz':data_2d[:,2],
        'Bx': data_2d[:,3],
        'By': data_2d[:,4],
        'Bz': data_2d[:,5]
    }

    data = pd.DataFrame(data_channels)
    
    data.index = create_timestamp_index(timestamp=file_tags, data=data)
    
    data = data.resample('S', closed='right').mean()
    
    return data

def create_timestamp_index(timestamp, data):
    date_info = np.array(timestamp[1:7], dtype=int)
    
    start = datetime(*date_info)
    
    timestamp_index = pd.date_range(start=start, periods=len(data), freq='20ms')
    
    return timestamp_index

@click.command()
@click.option('--filename', help='Name of LabChart binary file.')       
def write_csv(filename):
    click.echo('Reading/Writing file.'.format(filename))
    data= read_channels(filename=filename)
    data.to_csv((filename + '.csv'))
    click.echo('Done.')
    click.echo('Written CSV to "{0}.csv"'.format(filename))
    click.echo('You may read csv using script:')
    click.echo('>>> import pandas as pd')
    click.echo('>>> fname = "test_data.bin"')
    click.echo('>>> pd.read_csv((fname + ".csv"), index_col=0).head()')

def main():
    write_csv()
    

if __name__ == "__main__":
    # Execute when run as top level file and setuptools entry point from commandline.
    main()

import pandas as pd
fname = "test_data.bin"
pd.read_csv((fname + ".csv"), index_col=0).head()