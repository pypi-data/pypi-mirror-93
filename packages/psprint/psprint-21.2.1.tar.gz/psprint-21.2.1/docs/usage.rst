Substitute python's print
-------------------------

Import in your script

-  ``from psprint import print``

What does it do
---------------

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   print()
   print("*** WITHOUT PSPRINT ***")
   print("An output statement which informs the user")
   print("This statement requests the user to act")
   print("A debugging output useless to the user")
   print()

   from psprint import print
   print()
   print("*** WITH PSPRINT ***")
   print("An output statement which informs the user", mark=1)
   print("This statement requests the user to act", mark=2)
   print("A debugging output useless to the user", mark='bug')
   print ()

Screenshot: |image0|

.. |image0| image:: ./output.jpg
