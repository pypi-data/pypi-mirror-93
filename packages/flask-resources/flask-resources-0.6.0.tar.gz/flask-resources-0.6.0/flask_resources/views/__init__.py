# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Views."""

from .collections import ItemView, ListView
from .singleton import SingletonView

__all__ = ("ItemView", "ListView", "SingletonView")
