# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __license__, __copyright__, __author_email__


from .app import conversion
from .app import Find
from .app import Generic
from .app import extensionAndName


# To save you time
# If you swapped case

Conversion = conversion
find = Find
generic = Generic
extAndName = extensionAndName


__all__ = (
  __version__
  + __title__
  + __description__
  + __url__
  + __author__
  + __license__
  + __copyright__
  + __author_email__

)
