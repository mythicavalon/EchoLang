"""
Emoji to language code mapping for Discord flag reactions
Maps flag emojis to their corresponding language codes for Google Translate
"""

EMOJI_TO_LANGUAGE = {
    # Major languages with flag emojis
    '🇺🇸': 'en',      # United States -> English
    '🇬🇧': 'en',      # United Kingdom -> English
    '🇫🇷': 'fr',      # France -> French
    '🇩🇪': 'de',      # Germany -> German
    '🇪🇸': 'es',      # Spain -> Spanish
    '🇮🇹': 'it',      # Italy -> Italian
    '🇵🇹': 'pt',      # Portugal -> Portuguese
    '🇧🇷': 'pt',      # Brazil -> Portuguese
    '🇷🇺': 'ru',      # Russia -> Russian
    '🇯🇵': 'ja',      # Japan -> Japanese
    '🇰🇷': 'ko',      # South Korea -> Korean
    '🇨🇳': 'zh',      # China -> Chinese
    '🇹🇼': 'zh',      # Taiwan -> Chinese
    '🇭🇰': 'zh',      # Hong Kong -> Chinese
    '🇮🇳': 'hi',      # India -> Hindi
    '🇸🇦': 'ar',      # Saudi Arabia -> Arabic
    '🇦🇪': 'ar',      # UAE -> Arabic
    '🇪🇬': 'ar',      # Egypt -> Arabic
    '🇳🇱': 'nl',      # Netherlands -> Dutch
    '🇧🇪': 'nl',      # Belgium -> Dutch (or French)
    '🇸🇪': 'sv',      # Sweden -> Swedish
    '🇳🇴': 'no',      # Norway -> Norwegian
    '🇩🇰': 'da',      # Denmark -> Danish
    '🇫🇮': 'fi',      # Finland -> Finnish
    '🇵🇱': 'pl',      # Poland -> Polish
    '🇨🇿': 'cs',      # Czech Republic -> Czech
    '🇸🇰': 'sk',      # Slovakia -> Slovak
    '🇭🇺': 'hu',      # Hungary -> Hungarian
    '🇷🇴': 'ro',      # Romania -> Romanian
    '🇧🇬': 'bg',      # Bulgaria -> Bulgarian
    '🇭🇷': 'hr',      # Croatia -> Croatian
    '🇷🇸': 'sr',      # Serbia -> Serbian
    '🇸🇮': 'sl',      # Slovenia -> Slovenian
    '🇧🇦': 'bs',      # Bosnia -> Bosnian
    '🇲🇰': 'mk',      # North Macedonia -> Macedonian
    '🇦🇱': 'sq',      # Albania -> Albanian
    '🇬🇷': 'el',      # Greece -> Greek
    '🇹🇷': 'tr',      # Turkey -> Turkish
    '🇮🇱': 'he',      # Israel -> Hebrew
    '🇮🇷': 'fa',      # Iran -> Persian
    '🇦🇫': 'fa',      # Afghanistan -> Persian
    '🇵🇰': 'ur',      # Pakistan -> Urdu
    '🇧🇩': 'bn',      # Bangladesh -> Bengali
    '🇱🇰': 'si',      # Sri Lanka -> Sinhala
    '🇹🇭': 'th',      # Thailand -> Thai
    '🇻🇳': 'vi',      # Vietnam -> Vietnamese
    '🇲🇾': 'ms',      # Malaysia -> Malay
    '🇮🇩': 'id',      # Indonesia -> Indonesian
    '🇵🇭': 'tl',      # Philippines -> Filipino
    '🇸🇬': 'en',      # Singapore -> English
    '🇦🇺': 'en',      # Australia -> English
    '🇳🇿': 'en',      # New Zealand -> English
    '🇨🇦': 'en',      # Canada -> English
    '🇲🇽': 'es',      # Mexico -> Spanish
    '🇦🇷': 'es',      # Argentina -> Spanish
    '🇨🇱': 'es',      # Chile -> Spanish
    '🇨🇴': 'es',      # Colombia -> Spanish
    '🇵🇪': 'es',      # Peru -> Spanish
    '🇻🇪': 'es',      # Venezuela -> Spanish
    '🇺🇾': 'es',      # Uruguay -> Spanish
    '🇪🇨': 'es',      # Ecuador -> Spanish
    '🇧🇴': 'es',      # Bolivia -> Spanish
    '🇵🇾': 'es',      # Paraguay -> Spanish
    '🇨🇺': 'es',      # Cuba -> Spanish
    '🇩🇴': 'es',      # Dominican Republic -> Spanish
    '🇬🇹': 'es',      # Guatemala -> Spanish
    '🇭🇳': 'es',      # Honduras -> Spanish
    '🇸🇻': 'es',      # El Salvador -> Spanish
    '🇳🇮': 'es',      # Nicaragua -> Spanish
    '🇨🇷': 'es',      # Costa Rica -> Spanish
    '🇵🇦': 'es',      # Panama -> Spanish
    '🇺🇦': 'uk',      # Ukraine -> Ukrainian
    '🇧🇾': 'be',      # Belarus -> Belarusian
    '🇱🇹': 'lt',      # Lithuania -> Lithuanian
    '🇱🇻': 'lv',      # Latvia -> Latvian
    '🇪🇪': 'et',      # Estonia -> Estonian
    '🇦🇹': 'de',      # Austria -> German
    '🇨🇭': 'de',      # Switzerland -> German
    '🇱🇺': 'fr',      # Luxembourg -> French
    '🇲🇨': 'fr',      # Monaco -> French
    '🇦🇩': 'ca',      # Andorra -> Catalan
    '🇻🇦': 'it',      # Vatican -> Italian
    '🇸🇲': 'it',      # San Marino -> Italian
    '🇮🇪': 'ga',      # Ireland -> Irish
    '🇮🇸': 'is',      # Iceland -> Icelandic
    '🇲🇹': 'mt',      # Malta -> Maltese
    '🇨🇾': 'el',      # Cyprus -> Greek
    '🇬🇪': 'ka',      # Georgia -> Georgian
    '🇦🇲': 'hy',      # Armenia -> Armenian
    '🇦🇿': 'az',      # Azerbaijan -> Azerbaijani
    '🇰🇿': 'kk',      # Kazakhstan -> Kazakh
    '🇰🇬': 'ky',      # Kyrgyzstan -> Kyrgyz
    '🇹🇯': 'tg',      # Tajikistan -> Tajik
    '🇹🇲': 'tk',      # Turkmenistan -> Turkmen
    '🇺🇿': 'uz',      # Uzbekistan -> Uzbek
    '🇲🇳': 'mn',      # Mongolia -> Mongolian
    '🇰🇭': 'km',      # Cambodia -> Khmer
    '🇱🇦': 'lo',      # Laos -> Lao
    '🇲🇲': 'my',      # Myanmar -> Myanmar
    '🇳🇵': 'ne',      # Nepal -> Nepali
    '🇧🇹': 'dz',      # Bhutan -> Dzongkha
    '🇲🇻': 'dv',      # Maldives -> Dhivehi
    '🇲🇺': 'en',      # Mauritius -> English
    '🇿🇦': 'en',      # South Africa -> English
    '🇰🇪': 'sw',      # Kenya -> Swahili
    '🇹🇿': 'sw',      # Tanzania -> Swahili
    '🇺🇬': 'en',      # Uganda -> English
    '🇷🇼': 'rw',      # Rwanda -> Kinyarwanda
    '🇪🇹': 'am',      # Ethiopia -> Amharic
    '🇸🇳': 'wo',      # Senegal -> Wolof
    '🇬🇭': 'en',      # Ghana -> English
    '🇳🇬': 'en',      # Nigeria -> English
    '🇨🇮': 'fr',      # Côte d'Ivoire -> French
    '🇲🇦': 'ar',      # Morocco -> Arabic
    '🇹🇳': 'ar',      # Tunisia -> Arabic
    '🇩🇿': 'ar',      # Algeria -> Arabic
    '🇱🇾': 'ar',      # Libya -> Arabic
    '🇸🇩': 'ar',      # Sudan -> Arabic
    '🇸🇴': 'so',      # Somalia -> Somali
    '🇩🇯': 'fr',      # Djibouti -> French
    '🇪🇷': 'ti',      # Eritrea -> Tigrinya
    '🇸🇸': 'en',      # South Sudan -> English
    '🇨🇫': 'fr',      # Central African Republic -> French
    '🇹🇩': 'fr',      # Chad -> French
    '🇳🇪': 'fr',      # Niger -> French
    '🇧🇫': 'fr',      # Burkina Faso -> French
    '🇲🇱': 'fr',      # Mali -> French
    '🇬🇳': 'fr',      # Guinea -> French
    '🇸🇱': 'en',      # Sierra Leone -> English
    '🇱🇷': 'en',      # Liberia -> English
    '🇬🇲': 'en',      # Gambia -> English
    '🇬🇼': 'pt',      # Guinea-Bissau -> Portuguese
    '🇨🇻': 'pt',      # Cape Verde -> Portuguese
    '🇸🇹': 'pt',      # São Tomé and Príncipe -> Portuguese
    '🇦🇴': 'pt',      # Angola -> Portuguese
    '🇲🇿': 'pt',      # Mozambique -> Portuguese
    '🇿🇼': 'en',      # Zimbabwe -> English
    '🇧🇼': 'en',      # Botswana -> English
    '🇳🇦': 'en',      # Namibia -> English
    '🇿🇲': 'en',      # Zambia -> English
    '🇲🇼': 'en',      # Malawi -> English
    '🇱🇸': 'en',      # Lesotho -> English
    '🇸🇿': 'en',      # Eswatini -> English
    '🇰🇲': 'ar',      # Comoros -> Arabic
    '🇲🇬': 'mg',      # Madagascar -> Malagasy
    '🇲🇺': 'en',      # Mauritius -> English
    '🇸🇨': 'en',      # Seychelles -> English
    '🇷🇪': 'fr',      # Réunion -> French
    '🇾🇹': 'fr',      # Mayotte -> French
    '🇯🇴': 'ar',      # Jordan -> Arabic
    '🇱🇧': 'ar',      # Lebanon -> Arabic
    '🇸🇾': 'ar',      # Syria -> Arabic
    '🇮🇶': 'ar',      # Iraq -> Arabic
    '🇰🇼': 'ar',      # Kuwait -> Arabic
    '🇧🇭': 'ar',      # Bahrain -> Arabic
    '🇶🇦': 'ar',      # Qatar -> Arabic
    '🇴🇲': 'ar',      # Oman -> Arabic
    '🇾🇪': 'ar',      # Yemen -> Arabic
    '🇦🇿': 'az',      # Azerbaijan -> Azerbaijani
    '🇪🇨': 'es',      # Ecuador -> Spanish
    '🇬🇾': 'en',      # Guyana -> English
    '🇸🇷': 'nl',      # Suriname -> Dutch
    '🇫🇰': 'en',      # Falkland Islands -> English
    '🇬🇫': 'fr',      # French Guiana -> French
    '🇺🇸': 'en',      # United States -> English
    '🏴󠁧󠁢󠁥󠁮󠁧󠁿': 'en',  # England -> English
    '🏴󠁧󠁢󠁳󠁣󠁴󠁿': 'gd',  # Scotland -> Scottish Gaelic
    '🏴󠁧󠁢󠁷󠁬󠁳󠁿': 'cy',  # Wales -> Welsh
}

# Alternative mapping for common language requests
LANGUAGE_ALIASES = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'russian': 'ru',
    'japanese': 'ja',
    'korean': 'ko',
    'chinese': 'zh',
    'arabic': 'ar',
    'hindi': 'hi',
    'dutch': 'nl',
    'swedish': 'sv',
    'norwegian': 'no',
    'danish': 'da',
    'finnish': 'fi',
    'polish': 'pl',
    'czech': 'cs',
    'hungarian': 'hu',
    'romanian': 'ro',
    'bulgarian': 'bg',
    'croatian': 'hr',
    'serbian': 'sr',
    'greek': 'el',
    'turkish': 'tr',
    'hebrew': 'he',
    'persian': 'fa',
    'urdu': 'ur',
    'bengali': 'bn',
    'thai': 'th',
    'vietnamese': 'vi',
    'indonesian': 'id',
    'malay': 'ms',
    'filipino': 'tl',
    'ukrainian': 'uk',
    'belarusian': 'be',
    'lithuanian': 'lt',
    'latvian': 'lv',
    'estonian': 'et',
    'slovak': 'sk',
    'slovenian': 'sl',
    'bosnian': 'bs',
    'macedonian': 'mk',
    'albanian': 'sq',
    'georgian': 'ka',
    'armenian': 'hy',
    'azerbaijani': 'az',
    'kazakh': 'kk',
    'kyrgyz': 'ky',
    'tajik': 'tg',
    'uzbek': 'uz',
    'mongolian': 'mn',
    'khmer': 'km',
    'lao': 'lo',
    'myanmar': 'my',
    'nepali': 'ne',
    'swahili': 'sw',
    'amharic': 'am',
    'somali': 'so',
    'malagasy': 'mg',
    'irish': 'ga',
    'icelandic': 'is',
    'maltese': 'mt',
    'catalan': 'ca',
    'basque': 'eu',
    'galician': 'gl',
    'welsh': 'cy',
    'scottish': 'gd',
    'yiddish': 'yi',
    'esperanto': 'eo',
    'latin': 'la'
}

def get_language_code(emoji_or_name):
    """
    Get language code from emoji or language name
    
    Args:
        emoji_or_name (str): Flag emoji or language name
        
    Returns:
        str: Language code or None if not found
    """
    # Try emoji mapping first
    if emoji_or_name in EMOJI_TO_LANGUAGE:
        return EMOJI_TO_LANGUAGE[emoji_or_name]
    
    # Try language name mapping
    name_lower = emoji_or_name.lower()
    if name_lower in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[name_lower]
    
    return None

def get_supported_emojis():
    """
    Get list of all supported flag emojis
    
    Returns:
        list: List of flag emojis
    """
    return list(EMOJI_TO_LANGUAGE.keys())

def get_supported_languages():
    """
    Get list of all supported languages
    
    Returns:
        dict: Dictionary mapping language codes to language names
    """
    return {code: name.title() for name, code in LANGUAGE_ALIASES.items()}
