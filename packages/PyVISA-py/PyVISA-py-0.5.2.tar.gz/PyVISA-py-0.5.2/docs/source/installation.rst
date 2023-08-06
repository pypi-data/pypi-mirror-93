.. _installation:


Installation
============

Pyvisa-py is available on PyPI_ and can be easily installed using pip:

    pip install pyvisa-py


Pyvisa-py runs on Python 3.6+.

If you do not install any extra library pyvisa-py will only be able to access
tcpip resources. The following sections will describe what extra libraries you
need to install and how to configure them to use other resources.


Ethernet resources: TCPIP INSTR/SOCKET
--------------------------------------

Pyvisa-py relies on :py:mod:`socket` module in the Python Standard Library to
interact with the instrument which you do not need to install any extra library
to access those resources.


Serial resources: ASRL INSTR
----------------------------

To access serial resources, you should install PySerial_. Version 3.0 or newer
is required. No special configuration is required.


GPIB resources: GPIB INSTR
--------------------------

On all platforms, using **GPIB** resources requires to install a gpib driver.
On Windows, it is install as part of NI-VISA or Keysight VISA for example. On
MacOSX, you should install the NI-488 library from National instrument. On
Linux, you can use a commercial driver (NI) or the `linux-gpib`_ project.

On Linux, `linux-gpib`_ comes with Python bindings so you do not have to
install any extra library.
On all systems with GPIB device drivers, GPIB support is available through
`gpib-ctypes`_.

You should not have to perform any special configuration after the install.


USB resources: USB INSTR/RAW
----------------------------

For **USB** resources, you need to install PyUSB_. PyUSB_ relies on USB driver
library such as libusb 0.1, libusb 1.0, libusbx, libusb-win32 and OpenUSB
that you should also install. Please refer to PyUSB_ documentation for more
details.

On Unix system, one may have to modify udev rules to allow non-root access to
the device you are trying to connect to. The following tutorial describes how
to do it http://ask.xmodulo.com/change-usb-device-permission-linux.html.

On Windows, you may have to uninstall the USBTMC specific driver installed by
Windows and re-install a generic driver.

Note that on Windows, devices that are already open cannot be detected and will
not be returned by ``ResourceManager.list_resources``.

Another useful reference for how to configure your system is h
ttps://github.com/python-ivi/python-usbtmc.


How do I know if PyVISA-py is properly installed?
-------------------------------------------------

Using the pyvisa information tool. Run in your console::

  python -m visa info

You will get info about PyVISA, the installed backends and their options.


Using the development version
-----------------------------

You can install the latest development version (at your own risk) directly
form GitHub_::

    $ pip install -U git+https://github.com/pyvisa/pyvisa-py.git


.. _PySerial: https://pythonhosted.org/pyserial/
.. _PyVISA: http://pyvisa.readthedocs.org/
.. _PyUSB: https://github.com/pyusb/pyusb
.. _PyPI: https://pypi.python.org/pypi/PyVISA-py
.. _GitHub: https://github.com/pyvisa/pyvisa-py
.. _`National Instruments's VISA`: http://ni.com/visa/
.. _`LibreVISA`: http://www.librevisa.org/
.. _`issue tracker`: https://github.com/pyvisa/pyvisa-py/issues
.. _`linux-gpib`: http://linux-gpib.sourceforge.net/
.. _`gpib-ctypes`: https://pypi.org/project/gpib-ctypes/