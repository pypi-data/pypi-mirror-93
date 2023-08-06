=======
Changes
=======

1.3.1
=====

* **Fix:** Fixed 23.98, 29.97 DF, 29.97 NDF, 59.94 and 59.94 NDF rollover to ``00:00:00:00`` after 24 hours.

1.3.0
=====

* **Fix:** Fixed a huge bug in 29.97 NDF and 59.97 NDF calculations introduced
  in v1.2.3.

* **Fix:** Fixed ``Timecode.framerate`` when it is given as ``23.98``. The
  ``framerate`` attribute will not be forced to ``24`` and it will stay
  ``23.98``.

* **Update:** ``Timecode.tc_to_frames()`` method now accepts Timecode instances
  with possibly different frame rates then the instance itself.

* **Fix:** Fixed ``Timecode.div_frames()`` method.

* **Update:** Test coverage has been increased to 100% (yay!)

1.2.5
=====

* **Fix:** Fixed an edge case when two Timecodes are subtracted the resultant
  Timecode will always have the correct amount of frames. But it is not
  possible to have a Timecode with negative or zero frames as this is changed
  in 1.2.3.

* **Fix:** Fixed ``Timecode.float`` property for drop frames.

1.2.4
=====

* **Update:** It is now possible to supply a ``Fraction`` instances for the
  ``framerate`` argument.

1.2.3
=====
* **Update:** Passing ``frames=0`` will now raise a ValueError. This hopefully
  will clarify the usage of the TimeCode as a duration. If there is no
  duration, hence the ``frames=0``, meaning that the number of frames of the
  duration that this TimeCode represents is 0, which is meaningless.
* **Update:** Also added some validation for the ``frames`` property
  (oh yes it is a property now).

1.2.2.1
=======
* **Fix:** Fixed the ``CHANGELOG.rst`` and ``setup.py`` to be able to properly
  package and upload to PyPI.

1.2.2
=====
* **Fix:** Fixed ``Timecode.parse_timecode`` for int inputs.
* **Update:** ``Timecode`` now accepts a ``fractional`` bool argument that
  forces the timecode to be fractional.
* **Update:** ``Timecode`` now accepts a ```force_non_drop_frame`` argument
  that forces the timecode to be non-drop frame.

1.2.1
=====
* **Update:** Added support for 23.976 fps which is a common variation of 23.98.

1.2.0
=====
* **NEW:** Support for passing a tuple with numerator and denominator when
  passing rational framerate.

* **NEW:** set_fractional method for setting whether or not to represent a
  timecode as fractional seconds.

* **Update:** Updated README's with info on new features

* **FIX:** Some merge issues.

1.1.0
=====

* **New:** Support for passing "binary coded decimal" (BCD) integer to
  timecode argument as it's stored in certain formats like OpenEXR and DPX.
  Useful for parsing timecode from metadata through OpenImageIO for instance.
  Example: ``Timecode(24, 421729315) -> 19:23:14:23``
  https://en.wikipedia.org/wiki/SMPTE_timecode

1.0.1
=====

* **Update:** To prevent confusion, passing 0 for ``start_seconds`` argument
  will raise a ValueError now in ``Timecode.__init__`` method.

1.0.0
=====

* **New:** Added support for passing rational frame rate. 24000/1001 for 23.97
  etc.

* **New:** Added tests for new functionality. Fractional seconds and
  rational frame rates.

* **New:** added __ge__ and __le__ methods for better comparison between two
  timecodes.

* **New:** Added support for fractional seconds in the frame field as used in
  ffmpeg's duration for instance.

* **Important:** When passing fractional second style timecode, the
  Timecode.frs will return a float representing the fraction of a second. This
  is a major change for people expecting int values

0.4.2
=====

* **Update:** Version bump for PyPI.

0.4.1
=====

* **Fix:** Fixed a test that was testing overloaded operators.

0.4.0
=====

* **New:** Frame delimiter is now set to ":" for Non Drop Frame, ";" for Drop
  Frame and "." for millisecond based time codes.
  If ``Timecode.__init__()`` start_timecode is passed a string with the wrong
  delimiter it will be converted automatically.

* **Update:** All tests involving Drop Frame and millisecond time codes are now
  set to use the new delimiter.

* **New:** ``Timecode.tc_to_string()`` method added to present the correctly
  formatted time code.

* **New:** ``Timecode.ms_frame`` boolean attribute added.

* **New:** ``Timecode.__init__()`` now supports strings, ints and floats for
  the framerate argument.

0.3.0
=====

* **New:** Renamed the library to ``timecode``.

0.2.0
=====

* **New:** Rewritten the whole library from scratch.

* **New:** Most important change is the licencing. There was now license
  defined in the previous implementation. The library is now licensed under MIT
  license.

* **Update:** Timecode.__init__() arguments has been changed, removed the
  unnecessary ``drop_frame``, ``iter_returns`` arguments.

  Drop frame can be interpreted from the ``framerate`` argument and
  ``iter_returns`` is unnecessary cause any iteration on the object will return
  another ``Timecode`` instance.

  If you want to get a string representation use ``Timecode.__str__()`` or
  ``str(Timecode)`` or ``Timecode.__repr__()`` or ``\`Timecode\``` or
  ``'%s' % Timecode`` any other thing that will convert it to a string.

  If you want to get an integer use ``Timecode.frames`` or
  ``Timecode.frame_count`` depending on what you want to get out of it.

  So setting the ``iter_returns`` to something and nailing the output was
  unnecessary.

* **Update:** Updated the drop frame calculation to a much better one, which
  is based on to the blog post of David Heidelberger at
  http://www.davidheidelberger.com/blog/?p=29

* **New:** Added ``Timecode.__eq__()`` so it is now possible to check the
  equality of two timecode instances or a timecode and a string or a timecode
  and an integer (which will check the total frame count).

* **Update:** ``Timecode.tc_to_frames()`` now needs a timecode as a string
  and will return an integer value which is the number of frames in that
  timecode.

* **Update:** ``Timecode.frames_to_tc()`` now needs an integer frame count
  and returns 4 integers for hours, minutes, seconds and frames.

* **Update:** ``Timecode.hrs``, ``Timecode.mins``, ``Timecode.secs`` and
  ``Timecode.frs`` attributes are now properties. Because it was so rare to
  check the individual hours, minutes, seconds or frame values, their values
  are calculated with ``Timecode.frames_to_tc()`` method. But in future they
  can still be converted to attributes and their value will be updated each
  time the ``Timecode.frames`` attribute is changed (so add a ``_frames``
  attribute and make ``frames`` a property with a getter and setter, and update
  the hrs, mins, secs and frs in setter etc.).

* **Update:** Removed ``Timecode.calc_drop_frame()`` method. The drop frame
  calculation is neatly done inside ``Timecode.frames_to_tc()`` and
  ``Timecode.tc_to_frames()`` methods.

* **Update:** Updated ``Timecode.parse_timecode()`` method to a much simpler
  algorithm.

* **Update:** Removed ``Timecode.__return_item__()`` method. It is not
  necessary to return an item in that way anymore.

* **Update:** Removed ``Timecode.make_timecode()`` method. It was another
  unnecessary method, so it is removed. Now using simple python string
  templates for string representations.

* **New:** Added ``timecode.__version__`` string, and set the value to
  "0.2.0".

* **Update:** Removed ``Timecode.set_int_framerate()`` method. Setting the
  framerate will automatically set the ``Timecode.int_framerate`` attribute.
