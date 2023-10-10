# -*- coding: utf-8 -*-
from aqt.utils import showWarning
from aqt import mw
import os

BASE_URL_DICTIONARIES = "https://api.github.com/repos/wooorm/dictionaries/contents"
URL_BINARIES = "https://github.com/jankelemen/convert-dict-tool-from-chromium/archive/refs/heads/master.zip"\
    if os.name != 'nt' else 'https://github.com/jmbeach/convert_dict_windows/archive/refs/heads/main.zip'
VERSION_DICTIONARIES = "2a5353f1617f00e606dc036cab1c37df94272ca0"
URL_DICTIONARIES = lambda path: f"{BASE_URL_DICTIONARIES}/{path}?ref={VERSION_DICTIONARIES}"

DICT_DIR = os.path.join(mw.pm.base, "dictionaries")
ADDON_PATH = os.path.dirname(__file__)
USER_PATH = os.path.join(ADDON_PATH, "user_files")
ENABLED_PATH = os.path.join(USER_PATH, "enabled.pck")
USER_DICT_PATH = os.path.join(USER_PATH, "user_dics")
BINS_PATH = os.path.join(ADDON_PATH, "convert_dict")
BIN_PATH = os.path.join(ADDON_PATH, "convert_dict",  "convert_dict" if os.name != 'nt' else "convert_dict.exe")
PERSONAL_PATH = os.path.join(USER_PATH, "user_dics", "personal.txt")

try:
    os.makedirs(DICT_DIR, exist_ok=True)
    os.makedirs(USER_PATH, exist_ok=True)
    os.makedirs(USER_DICT_PATH, exist_ok=True)
except OSError as error:
    showWarning(f"Can't create dictionary folder, check permissions. Error: {error}")

LANGUAGE_LIST = {'hy': ('Armenian', 'dictionaries/hy'), 'eu': ('Basque', 'dictionaries/eu'),
                 'br': ('Breton', 'dictionaries/br'), 'bg': ('Bulgarian', 'dictionaries/bg'),
                 'ca': ('Catalan', 'dictionaries/ca'), 'ca-valencia': ('Catalan', 'dictionaries/ca-valencia'),
                 'hr': ('Croatian', 'dictionaries/hr'), 'cs': ('Czech', 'dictionaries/cs'),
                 'nl': ('Dutch', 'dictionaries/nl'), 'en': ('English', 'dictionaries/en'),
                 'en-AU': ('English (Australia)', 'dictionaries/en-AU'),
                 'en-CA': ('English (Canada)', 'dictionaries/en-CA'),
                 'en-ZA': ('English (South Africa)', 'dictionaries/en-ZA'),
                 'en-GB': ('English (United Kingdom)', 'dictionaries/en-GB'), 'eo': ('Esperanto', 'dictionaries/eo'),
                 'et': ('Estonian', 'dictionaries/et'), 'fo': ('Faroese', 'dictionaries/fo'),
                 'fr': ('French', 'dictionaries/fr'), 'fur': ('Friulian', 'dictionaries/fur'),
                 'gl': ('Galician', 'dictionaries/gl'), 'ka': ('Georgian', 'dictionaries/ka'),
                 'de': ('German', 'dictionaries/de'), 'de-AT': ('German (Austria)', 'dictionaries/de-AT'),
                 'de-CH': ('German (Switzerland)', 'dictionaries/de-CH'), 'el': ('Greek', 'dictionaries/el'),
                 'el-polyton': ('Greek', 'dictionaries/el-polyton'), 'he': ('Hebrew', 'dictionaries/he'),
                 'hu': ('Hungarian', 'dictionaries/hu'), 'is': ('Icelandic', 'dictionaries/is'),
                 'ia': ('Interlingua', 'dictionaries/ia'), 'ie': ('Interlingue', 'dictionaries/ie'),
                 'ga': ('Irish', 'dictionaries/ga'), 'it': ('Italian', 'dictionaries/it'),
                 'rw': ('Kinyarwanda', 'dictionaries/rw'), 'tlh': ('Klingon', 'dictionaries/tlh'),
                 'tlh-Latn': ('Klingon (Latin)', 'dictionaries/tlh-Latn'), 'ko': ('Korean', 'dictionaries/ko'),
                 'ltg': ('Latgalian', 'dictionaries/ltg'), 'la': ('Latin', 'dictionaries/la'),
                 'lv': ('Latvian', 'dictionaries/lv'), 'lt': ('Lithuanian', 'dictionaries/lt'),
                 'nds': ('Low German', 'dictionaries/nds'), 'lb': ('Luxembourgish', 'dictionaries/lb'),
                 'mk': ('Macedonian', 'dictionaries/mk'), 'mn': ('Mongolian', 'dictionaries/mn'),
                 'ne': ('Nepali', 'dictionaries/ne'), 'nb': ('Norwegian Bokmål', 'dictionaries/nb'),
                 'nn': ('Norwegian Nynorsk', 'dictionaries/nn'), 'oc': ('Occitan', 'dictionaries/oc'),
                 'fa': ('Persian', 'dictionaries/fa'), 'pl': ('Polish', 'dictionaries/pl'),
                 'pt': ('Portuguese', 'dictionaries/pt'), 'pt-PT': ('Portuguese (Portugal)', 'dictionaries/pt-PT'),
                 'ro': ('Romanian', 'dictionaries/ro'), 'ru': ('Russian', 'dictionaries/ru'),
                 'gd': ('Scottish Gaelic', 'dictionaries/gd'), 'sr': ('Serbian', 'dictionaries/sr'),
                 'sr-Latn': ('Serbian (Latin)', 'dictionaries/sr-Latn'), 'sk': ('Slovak', 'dictionaries/sk'),
                 'sl': ('Slovenian', 'dictionaries/sl'), 'es': ('Spanish', 'dictionaries/es'),
                 'es-AR': ('Spanish (Argentina)', 'dictionaries/es-AR'),
                 'es-BO': ('Spanish (Bolivia)', 'dictionaries/es-BO'),
                 'es-CL': ('Spanish (Chile)', 'dictionaries/es-CL'),
                 'es-CO': ('Spanish (Colombia)', 'dictionaries/es-CO'),
                 'es-CR': ('Spanish (Costa Rica)', 'dictionaries/es-CR'),
                 'es-CU': ('Spanish (Cuba)', 'dictionaries/es-CU'),
                 'es-DO': ('Spanish (Dominican Republic)', 'dictionaries/es-DO'),
                 'es-EC': ('Spanish (Ecuador)', 'dictionaries/es-EC'),
                 'es-SV': ('Spanish (El Salvador)', 'dictionaries/es-SV'),
                 'es-GT': ('Spanish (Guatemala)', 'dictionaries/es-GT'),
                 'es-HN': ('Spanish (Honduras)', 'dictionaries/es-HN'),
                 'es-MX': ('Spanish (Mexico)', 'dictionaries/es-MX'),
                 'es-NI': ('Spanish (Nicaragua)', 'dictionaries/es-NI'),
                 'es-PA': ('Spanish (Panama)', 'dictionaries/es-PA'),
                 'es-PY': ('Spanish (Paraguay)', 'dictionaries/es-PY'),
                 'es-PE': ('Spanish (Peru)', 'dictionaries/es-PE'),
                 'es-PH': ('Spanish (Philippines)', 'dictionaries/es-PH'),
                 'es-PR': ('Spanish (Puerto Rico)', 'dictionaries/es-PR'),
                 'es-US': ('Spanish (United States)', 'dictionaries/es-US'),
                 'es-UY': ('Spanish (Uruguay)', 'dictionaries/es-UY'),
                 'es-VE': ('Spanish (Venezuela)', 'dictionaries/es-VE'), 'sv': ('Swedish', 'dictionaries/sv'),
                 'sv-FI': ('Swedish (Finland)', 'dictionaries/sv-FI'), 'tr': ('Turkish', 'dictionaries/tr'),
                 'tk': ('Turkmen', 'dictionaries/tk'), 'uk': ('Ukrainian', 'dictionaries/uk'),
                 'vi': ('Vietnamese', 'dictionaries/vi'), 'cy': ('Welsh', 'dictionaries/cy'),
                 'hyw': ('Western Armenian', 'dictionaries/hyw'), 'fy': ('Western Frisian', 'dictionaries/fy')}
