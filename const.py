# -*- coding: utf-8 -*-

import os
from aqt.utils import showWarning
from aqt import mw

BASE_URL_DICTIONARIES = "https://api.github.com/repos/wooorm/dictionaries/contents"
VERSION_DICTIONARIES = "2a5353f1617f00e606dc036cab1c37df94272ca0"
URL_DICTIONARIES = lambda path: f"{BASE_URL_DICTIONARIES}/{path}?ref={VERSION_DICTIONARIES}"

LANGUAGE_LIST = {'bg': ('Bulgarian', 'dictionaries/bg'), 'br': ('Breton', 'dictionaries/br'),
                 'ca-valencia': ('Catalan', 'dictionaries/ca-valencia'), 'ca': ('Catalan', 'dictionaries/ca'),
                 'cs': ('Czech', 'dictionaries/cs'), 'cy': ('Welsh', 'dictionaries/cy'),
                 'de-AT': ('German (Austria)', 'dictionaries/de-AT'),
                 'de-CH': ('German (Switzerland)', 'dictionaries/de-CH'), 'de': ('German', 'dictionaries/de'),
                 'el-polyton': ('Greek', 'dictionaries/el-polyton'), 'el': ('Greek', 'dictionaries/el'),
                 'en-AU': ('English (Australia)', 'dictionaries/en-AU'),
                 'en-CA': ('English (Canada)', 'dictionaries/en-CA'),
                 'en-GB': ('English (United Kingdom)', 'dictionaries/en-GB'),
                 'en-ZA': ('English (South Africa)', 'dictionaries/en-ZA'), 'en': ('English', 'dictionaries/en'),
                 'eo': ('Esperanto', 'dictionaries/eo'), 'es-AR': ('Spanish (Argentina)', 'dictionaries/es-AR'),
                 'es-BO': ('Spanish (Bolivia)', 'dictionaries/es-BO'),
                 'es-CL': ('Spanish (Chile)', 'dictionaries/es-CL'),
                 'es-CO': ('Spanish (Colombia)', 'dictionaries/es-CO'),
                 'es-CR': ('Spanish (Costa Rica)', 'dictionaries/es-CR'),
                 'es-CU': ('Spanish (Cuba)', 'dictionaries/es-CU'),
                 'es-DO': ('Spanish (Dominican Republic)', 'dictionaries/es-DO'),
                 'es-EC': ('Spanish (Ecuador)', 'dictionaries/es-EC'),
                 'es-GT': ('Spanish (Guatemala)', 'dictionaries/es-GT'),
                 'es-HN': ('Spanish (Honduras)', 'dictionaries/es-HN'),
                 'es-MX': ('Spanish (Mexico)', 'dictionaries/es-MX'),
                 'es-NI': ('Spanish (Nicaragua)', 'dictionaries/es-NI'),
                 'es-PA': ('Spanish (Panama)', 'dictionaries/es-PA'), 'es-PE': ('Spanish (Peru)', 'dictionaries/es-PE'),
                 'es-PH': ('Spanish (Philippines)', 'dictionaries/es-PH'),
                 'es-PR': ('Spanish (Puerto Rico)', 'dictionaries/es-PR'),
                 'es-PY': ('Spanish (Paraguay)', 'dictionaries/es-PY'),
                 'es-SV': ('Spanish (El Salvador)', 'dictionaries/es-SV'),
                 'es-US': ('Spanish (United States)', 'dictionaries/es-US'),
                 'es-UY': ('Spanish (Uruguay)', 'dictionaries/es-UY'),
                 'es-VE': ('Spanish (Venezuela)', 'dictionaries/es-VE'), 'es': ('Spanish', 'dictionaries/es'),
                 'et': ('Estonian', 'dictionaries/et'), 'eu': ('Basque', 'dictionaries/eu'),
                 'fa': ('Persian', 'dictionaries/fa'), 'fo': ('Faroese', 'dictionaries/fo'),
                 'fr': ('French', 'dictionaries/fr'), 'fur': ('Friulian', 'dictionaries/fur'),
                 'fy': ('Western Frisian', 'dictionaries/fy'), 'ga': ('Irish', 'dictionaries/ga'),
                 'gd': ('Scottish Gaelic', 'dictionaries/gd'), 'gl': ('Galician', 'dictionaries/gl'),
                 'he': ('Hebrew', 'dictionaries/he'), 'hr': ('Croatian', 'dictionaries/hr'),
                 'hu': ('Hungarian', 'dictionaries/hu'), 'hy': ('Armenian', 'dictionaries/hy'),
                 'hyw': ('Western Armenian', 'dictionaries/hyw'), 'ia': ('Interlingua', 'dictionaries/ia'),
                 'ie': ('Interlingue', 'dictionaries/ie'), 'is': ('Icelandic', 'dictionaries/is'),
                 'it': ('Italian', 'dictionaries/it'), 'ka': ('Georgian', 'dictionaries/ka'),
                 'ko': ('Korean', 'dictionaries/ko'), 'la': ('Latin', 'dictionaries/la'),
                 'lb': ('Luxembourgish', 'dictionaries/lb'), 'lt': ('Lithuanian', 'dictionaries/lt'),
                 'ltg': ('Latgalian', 'dictionaries/ltg'), 'lv': ('Latvian', 'dictionaries/lv'),
                 'mk': ('Macedonian', 'dictionaries/mk'), 'mn': ('Mongolian', 'dictionaries/mn'),
                 'nb': ('Norwegian Bokmål', 'dictionaries/nb'), 'nds': ('Low German', 'dictionaries/nds'),
                 'ne': ('Nepali', 'dictionaries/ne'), 'nl': ('Dutch', 'dictionaries/nl'),
                 'nn': ('Norwegian Nynorsk', 'dictionaries/nn'), 'oc': ('Occitan', 'dictionaries/oc'),
                 'pl': ('Polish', 'dictionaries/pl'), 'pt-PT': ('Portuguese (Portugal)', 'dictionaries/pt-PT'),
                 'pt': ('Portuguese', 'dictionaries/pt'), 'ro': ('Romanian', 'dictionaries/ro'),
                 'ru': ('Russian', 'dictionaries/ru'), 'rw': ('Kinyarwanda', 'dictionaries/rw'),
                 'sk': ('Slovak', 'dictionaries/sk'), 'sl': ('Slovenian', 'dictionaries/sl'),
                 'sr-Latn': ('Serbian (Latin)', 'dictionaries/sr-Latn'), 'sr': ('Serbian', 'dictionaries/sr'),
                 'sv-FI': ('Swedish (Finland)', 'dictionaries/sv-FI'), 'sv': ('Swedish', 'dictionaries/sv'),
                 'tk': ('Turkmen', 'dictionaries/tk'), 'tlh-Latn': ('Klingon (Latin)', 'dictionaries/tlh-Latn'),
                 'tlh': ('Klingon', 'dictionaries/tlh'), 'tr': ('Turkish', 'dictionaries/tr'),
                 'uk': ('Ukrainian', 'dictionaries/uk'), 'vi': ('Vietnamese', 'dictionaries/vi')}

DICT_DIR = os.path.join(mw.pm.base, "dictionaries")
ADDON_PATH = os.path.dirname(__file__)
USER_PATH = os.path.join(ADDON_PATH, "user_files")
ENABLED_PATH = os.path.join(USER_PATH, "enabled.pck")
PERSONAL_PATH = os.path.join(USER_PATH, "personal.dic")

try:
    os.makedirs(DICT_DIR, exist_ok=True)
    os.makedirs(USER_PATH, exist_ok=True)
except OSError as error:
    showWarning(f"Can't create dictionary folder, check permissions. Error: {error}")



