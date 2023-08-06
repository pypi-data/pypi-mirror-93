About
-----

Python Module for manipulating SMPTE timecode. Supports 23.976, 23.98, 24, 25, 
29.97, 30, 50, 59.94, 60 frame rates and milliseconds (1000 fps).

This library is a fork of the original PyTimeCode python library. You should
not use the two library together (PyTimeCode is not maintained and has known
bugs).

The math behind the drop frame calculation is based on the
`blog post of David Heidelberger`_ .

.. _`blog post of David Heidelberger`: http://www.davidheidelberger.com/blog/?p=29

Simple math operations like, addition, subtraction, multiplication or division
with an integer value or with a timecode is possible. Math operations between
timecodes with different frame rates are supported. So::

    from timecode import Timecode

    tc1 = Timecode('29.97', '00:00:00:00')
    tc2 = Timecode('24', '00:00:00:10')
    tc3 = tc1 + tc2
    assert tc3.framerate == '29.97'
    assert tc3.frames == 12
    assert tc3 == '00:00:00:11'

Creating a Timecode instance with a start timecode of '00:00:00:00' will
result a timecode object where the total number of frames is 1. So::

    tc4 = Timecode('24', '00:00:00:00')
    assert tc4.frames == 1

Use the ``frame_number`` attribute if you want to get a 0 based frame number::

    assert tc4.frame_number == 0

Frame rates 29.97 and 59.94 are always drop frame, and all the others are non
drop frame.

The timecode library supports rational frame rates passed as a either a string
 or tuple::

    tc5 = Timecode('30000/1001', '00:00:00;00')
    assert tc5.framerate == '29.97'

    tc6 = Timecode((30000, 1001), '00:00:00;00')
    assert tc6.framerate == '29.97'

You may also pass a big "Binary Coded Decimal" integer as start timecode::

    tc7 = Timecode('24', 421729315)
    assert repr(tc7) == '19:23:14:23'

This is useful for parsing timecodes stored in OpenEXR's and extracted through
OpenImageIO for instance.

Timecode also supports passing start timecodes formatted like HH:MM:SS.sss where
SS.sss is seconds and fractions of seconds::

    tc8 = Timecode(25, '00:00:00.040')
    assert tc8.frame_number == 1

You may set any timecode to be represented as fractions of seconds::

    tc9 = Timecode(24, '19:23:14:23')
    assert repr(tc9) == '19:23:14:23'

    tc9.set_fractional(True)
    assert repr(tc9) == '19:23:14.958'

Fraction of seconds is useful when working with tools like FFmpeg.


The SMPTE standard limits the timecode with 24 hours. Even though, Timecode
instance will show the current timecode inline with the SMPTE standard, it will
keep counting the total frames without clipping it.

Please report any bugs to the `GitHub`_ page.

.. _`GitHub`: https://github.com/eoyilmaz/timecode

Copyright 2014 Joshua Banton and PyTimeCode developers.
