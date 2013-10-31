# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon-name" : "trackbar_routing",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon-summary" : _("trackbar routing"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon-description" : _("""This addon allows comfortable handling of slider control by using the routing keys of a braille display.
You can set the position of a slider control by pressing the corresponding routing key on a braille display.

usage
1. set the focus onto a slider
2. press the cursor routing key at the new position
- to set the slider to its minimum value, press the routing key above the first braille module
- to set the slider to 50%, press the routing key above the middle of the braille display
- to set the slider to its maximum value press the routing key above the last braille module"""),
	# version
	"addon-version" : "1.0",
	# Author(s)
	"addon-author" : u"David Parduhn <xkill85@gmx.net>",
	# URL for the add-on documentation support
	"addon-url" : None
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = []

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py", "docHandler.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
