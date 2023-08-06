.. _faq:


FAQ
===


Are all VISA attributes and methods implemented?
------------------------------------------------

No. We have implemented those attributes and methods that are most commonly
needed. We would like to reach feature parity. If there is something that you
need, let us know.


Why are you developing this?
----------------------------

The IVI compliant VISA implementation available (`National Instruments's VISA`_ ,
Keysight, Tektronik, etc) are proprietary libraries that only works on
certain systems. We wanted to provide a compatible alternative.


Can PyVISA-py be used from a VM?
--------------------------------
Because PyVISA-py access hardware resources (such as USB ports) running from a
VM can cause issues, such as unexpected timeouts because the VM does not
receive the response. You may be able to set the VM in such that it works but
you should refer to your VM manual.
(see https://github.com/pyvisa/pyvisa-py/issues/243 for the kind of issue it
can cause)


Why not using LibreVISA?
------------------------

LibreVISA_ is still young and appears mostly unmaintained at this point.
However, you can already use it with the IVI backend as it has the same API.
We think that PyVISA-py is easier to hack and we can quickly reach feature parity
with other IVI-VISA implementation for message-based instruments.


Why putting PyVISA in the middle?
---------------------------------

Because it allows you to change the backend easily without changing your application.
In other projects, we implemented classes to call USBTMC devices without PyVISA.
But this leads to code duplication or an adapter class in your code.
By using PyVISA as a frontend to many backends, we abstract these things
from higher level applications.


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
