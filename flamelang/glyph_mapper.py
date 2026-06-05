"""
Glyph Mapper: Phonetic to Unicode Glyph Transformation
Supports Meroitic Hieroglyphs and Cuneiform scripts for dense semantic encoding
"""

from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class GlyphMapper(ABC):
    """Abstract base class for glyph mapping systems"""
    
    @abstractmethod
    def get_map(self) -> Dict[str, str]:
        """Return the phonetic to glyph mapping dictionary"""
        pass
    
    @abstractmethod
    def map_text(self, text: str) -> str:
        """Map input text to glyphs"""
        pass
    
    def get_unicode_hex(self, glyphs: str) -> List[str]:
        """Convert glyphs to Unicode hex representation"""
        return [f'U+{ord(c):04X}' for c in glyphs]


class MeroiticMapper(GlyphMapper):
    """
    Meroitic Hieroglyphic mapper (Unicode U+10980–U+1099F)
    Ancient Nubian script for phonetic syllables
    """
    
    def __init__(self):
        self._map = {
            # Vowels
            'a': '\U00010980',  # 𐦀 (a)
            'e': '\U00010981',  # 𐦁 (e)
            'i': '\U00010982',  # 𐦂 (i)
            'o': '\U00010983',  # 𐦃 (o)
            'u': '\U00010984',  # 𐦄 (u)
            
            # Consonants
            'b': '\U00010985',  # 𐦅 (b)
            'd': '\U00010986',  # 𐦆 (d)
            'h': '\U00010987',  # 𐦇 (h)
            'k': '\U00010988',  # 𐦈 (k)
            'l': '\U00010989',  # 𐦉 (l)
            'm': '\U0001098A',  # 𐦊 (m)
            'n': '\U0001098B',  # 𐦋 (n)
            'p': '\U0001098C',  # 𐦌 (p)
            'q': '\U0001098D',  # 𐦍 (q)
            'r': '\U0001098E',  # 𐦎 (r)
            's': '\U0001098F',  # 𐦏 (s)
            't': '\U00010990',  # 𐦐 (t)
            'w': '\U00010991',  # 𐦑 (w)
            'y': '\U00010992',  # 𐦒 (y)
            'z': '\U00010993',  # 𐦓 (z)
            
            # Syllables (common combinations)
            'ka': '\U00010994',  # 𐦔 (ka)
            'ku': '\U00010995',  # 𐦕 (ku)
            'la': '\U00010996',  # 𐦖 (la)
            'ma': '\U00010997',  # 𐦗 (ma)
            'na': '\U00010998',  # 𐦘 (na)
            'ne': '\U00010999',  # 𐦙 (ne)
            'ra': '\U0001099A',  # 𐦚 (ra)
            'se': '\U0001099B',  # 𐦛 (se)
            'te': '\U0001099C',  # 𐦜 (te)
            'to': '\U0001099D',  # 𐦝 (to)
        }
    
    def get_map(self) -> Dict[str, str]:
        return self._map
    
    def map_text(self, text: str) -> str:
        """
        Map English phonetic text to Meroitic glyphs
        Uses greedy longest-match strategy
        """
        text = text.lower().replace(' ', '')
        result = []
        i = 0
        
        while i < len(text):
            matched = False
            # Try longest matches first (2 chars, then 1)
            for length in [2, 1]:
                if i + length <= len(text):
                    substr = text[i:i+length]
                    if substr in self._map:
                        result.append(self._map[substr])
                        i += length
                        matched = True
                        break
            
            if not matched:
                # Keep unmatched character as-is
                result.append(text[i])
                i += 1
        
        return ''.join(result)


class CuneiformMapper(GlyphMapper):
    """
    Cuneiform mapper (Unicode U+12000–U+123FF)
    Ancient Mesopotamian syllabic/logographic script
    ~900 signs for dense semantic encoding
    """
    
    def __init__(self):
        self._map = {
            # Basic syllables (60+ signs)
            'a': '\U00012000',    # 𒀀 (a)
            'ab': '\U0001200A',   # 𒀊 (ab)
            'ad': '\U00012037',   # 𒀷 (ad)
            'ag': '\U000120A0',   # 𒂠 (ag)
            'ak': '\U00012157',   # 𒅗 (ak)
            'al': '\U000121AA',   # 𒆪 (al)
            'am': '\U00012028',   # 𒀨 (am)
            'an': '\U00012000',   # 𒀀 (an - alt)
            'ar': '\U00012048',   # 𒁈 (ar)
            'ba': '\U00012040',   # 𒁀 (ba)
            'bad': '\U00012041',  # 𒁁 (bad)
            'bal': '\U00012044',  # 𒁄 (bal)
            'be': '\U00012046',   # 𒁆 (be)
            'bi': '\U00012049',   # 𒁉 (bi)
            'bu': '\U0001204D',   # 𒁍 (bu)
            'da': '\U00012055',   # 𒁕 (da)
            'di': '\U00012072',   # 𒁲 (di)
            'du': '\U0001207A',   # 𒁺 (du)
            'e': '\U0001208A',    # 𒂊 (e)
            'en': '\U00012097',   # 𒂗 (en)
            'ga': '\U000120B5',   # 𒂵 (ga)
            'ga2': '\U000120B7',  # 𒂷 (ga2)
            'gal': '\U000120F0',  # 𒃰 (gal)
            'gi': '\U000120F0',   # 𒃰 (gi)
            'gu': '\U00012116',   # 𒄖 (gu)
            'gu2': '\U00012118', # 𒄘 (gu2)
            'ha': '\U00012129',   # 𒄩 (ha)
            'hi': '\U0001212D',   # 𒄭 (hi)
            'hu': '\U00012137',   # 𒄷 (hu)
            'i': '\U0001213F',    # 𒄿 (i)
            'im': '\U0001214E',   # 𒅎 (im)
            'ka': '\U00012157',   # 𒅗 (ka)
            'ka2': '\U0001218D',  # 𒆍 (ka2)
            'ki': '\U000121A0',   # 𒆠 (ki)
            'ku': '\U000121AA',   # 𒆪 (ku)
            'ku3': '\U000121AC', # 𒆬 (ku3)
            'la': '\U000121B7',   # 𒆷 (la)
            'li': '\U000121F7',   # 𒇷 (li)
            'lu': '\U00012221',   # 𒈡 (lu)
            'ma': '\U00012220',   # 𒈠 (ma)
            'mi': '\U00012228',   # 𒈨 (mi)
            'mu': '\U00012233',   # 𒈳 (mu)
            'na': '\U00012261',   # 𒉡 (na)
            'ne': '\U00012248',   # 𒉈 (ne)
            'ni': '\U00012252',   # 𒉒 (ni)
            'nu': '\U00012261',   # 𒉡 (nu)
            'pa': '\U0001227A',   # 𒉺 (pa)
            'pi': '\U00012280',   # 𒊀 (pi)
            'pu': '\U0001228A',   # 𒊊 (pu)
            'ra': '\U000122A3',   # 𒊣 (ra)
            'ri': '\U000122A8',   # 𒊨 (ri)
            'ru': '\U000122B6',   # 𒊶 (ru)
            'sa': '\U000122AB',   # 𒊫 (sa)
            'si': '\U000122C1',   # 𒋁 (si)
            'su': '\U000122D7',   # 𒋗 (su)
            'ta': '\U000122EB',   # 𒋫 (ta)
            'ti': '\U000122FC',   # 𒋼 (ti)
            'tu': '\U00012309',   # 𒌉 (tu)
            'u': '\U00012313',    # 𒌓 (u)
            'um': '\U00012323',   # 𒌣 (um)
            'ur': '\U00012328',   # 𒌨 (ur)
            'us': '\U00012351',   # 𒍑 (us)
            'uz': '\U0001235C',   # 𒍜 (uz)
            'za': '\U0001235D',   # 𒍝 (za)
            'zi': '\U00012364',   # 𒍤 (zi)
            'zu': '\U0001236A',   # 𒍪 (zu)
        }
        
        # Add logograms for concepts (separate namespace to avoid conflicts)
        self._logograms = {
            'lord': '\U00012097',   # 𒂗 (EN - governance)
            'wind': '\U0001214E',   # 𒅎 (IM - wave)
            'fire': '\U00012049',   # 𒁉 (BIL - fire, using BI as proxy)
            'head': '\U00012295',   # 𒊕 (SAG - leadership)
        }
    
    def get_map(self) -> Dict[str, str]:
        return self._map
    
    def map_text(self, text: str) -> str:
        """
        Map English phonetic text to Cuneiform glyphs
        Uses greedy longest-match strategy (prioritizes 3-char, then 2-char, then 1-char)
        """
        text = text.lower().replace(' ', '')
        result = []
        i = 0
        
        while i < len(text):
            matched = False
            # Try longest matches first (3 chars, 2 chars, then 1)
            for length in [3, 2, 1]:
                if i + length <= len(text):
                    substr = text[i:i+length]
                    if substr in self._map:
                        result.append(self._map[substr])
                        i += length
                        matched = True
                        break
            
            if not matched:
                # Keep unmatched character as-is
                result.append(text[i])
                i += 1
        
        return ''.join(result)


def get_mapper(script: str = 'meroitic') -> GlyphMapper:
    """
    Factory function to get appropriate glyph mapper
    
    Args:
        script: Either 'meroitic' or 'cuneiform'
    
    Returns:
        GlyphMapper instance
    """
    if script.lower() == 'meroitic':
        return MeroiticMapper()
    elif script.lower() == 'cuneiform':
        return CuneiformMapper()
    else:
        raise ValueError(f"Unknown script type: {script}. Use 'meroitic' or 'cuneiform'")
