########################################################################
# Copyright (c) 2009 Paul Carduner and Contributors
# All Rights Reserved
# This file is part of divvy.fps.
#
# divvy.fps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# divvy.fps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with divvy.fps.  If not, see
# <http://www.gnu.org/licenses/>.
#########################################################################

try:
    from django.conf import settings
except ImportError, e:
    # django not installed
    settings = object()

RUN_IN_SANDBOX = getattr(settings, "FPS_RUN_IN_SANDBOX", False)

DEFAULT_ACCESS_KEY_ID = getattr(settings, "FPS_DEFAULT_ACCESS_KEY_ID", None)
DEFAULT_SECRET_KEY = getattr(settings, "FPS_DEFAULT_SECRET_KEY", None)
DEFAULT_COBRANDING_URL = getattr(settings, "FPS_DEFAULT_COBRANDING_URL", None)
