import regex as re
import unicodedata

from typing import List, Dict
import regex_pattern as Reg


def removeSpace(ptext: str) -> (str):
    """
    Dùng xóa các khoảng trắng thừa trong ptext

    Args:
        ptext (str): comment

    Returns:
        [str]: comment đã xóa các khoảng trắng thừa
    """
    ptext = ptext.replace("\n", " ")
    return re.sub(r'\s+', ' ', ptext)


def containsURL(ptext: str) -> (int):
    """
    Dùng kiểm tra ptext có chứa url hay ko

    Args:
        ptext (str): comment

    Returns:
        [int]: 1 có 0 ko
    """
    flag = re.search(Reg.URL, ptext)
    return int(flag is not None)


def normalizeComment(ptext: str) -> (str):
    """
    Chuẩn hóa text bằng cách lower nó sau đó sử dụng phương pháp NFD để biểu diễn text

    Args:
        ptext (str): comment
        plower (bool): có lower ko

    Returns:
        [str]: comment đã lower và chuẩn hóa
    """
    ptext = ptext.lower()
    return unicodedata.normalize('NFD', ptext)


def removeSpecialLetters(ptext: str) -> (str):
    """
    Dùng xóa các kí tự đặc biệt

    Args:
        ptext (str): comment

    Returns:
        [str]: comment without special characters
    """
    return re.sub("\s+", " ", re.sub(Reg.UTF8_LOWER, " ", ptext)).strip()


def removeDuplicateLetters(ptext: str) -> (str):
    """
    Hàm dùng xóa các kí tự bị duplicate, giả sử :
      * ptext = 'okkkkkkkkkkkkkkkkkkkkkk chờiiiiiiiiii ơiiiiiiii xinhhhhhhhhhhhh quá đẹppppppppp xỉuuuuuuu'
      * Sau khi dùng hàm này thì thành:
        ptext = 'ok chời ơi xinh quá đẹp xỉu'

    Args:
        ptext (str): comment

    Returns:
        [str]: comment that removing duplicated letters
    """
    return re.sub(r'(.)\1+', r'\1', ptext)


def replaceTeencode(ptext: str, pdictionary: Dict[str, str]) -> (str):
    """
    Hàm này dùng để thay thế các từ đơn trong ptext mà là key của pdictionary, sau đó
    thay thế từ này bằng value tương ứng với key đó.

    Args:
        ptext (str): comment
        pdictionary (Dict[str, str]): dictionary

    Returns:
        (str): comment đã dc thay thế bởi các value match với pdictionary
    """
    ptext = re.sub(r'(\s)\1+', r'\1', ptext)
    words = ptext.strip().split(' ')
    new_words = []

    for word in words:
        word = word.strip()

        if word == '': continue

        word = removeDuplicateLetters(word)
        word = pdictionary.get(word, word)
        new_words.append(word)

    return ' '.join(new_words).strip()


def removeNoiseWord(ptext: str, pdictionary: Dict[str, bool], penchantEN) -> (str):
    """
    Xóa các từ rác

    Args:
        ptext (str): comment
        pdictionary (Dict[str, bool]): từ điển tiếng việt
        penchantEN (pyenchant object): kiểm tra một từ ko phải tiếng việt thì có phải tiếng anh ko

    Returns:
        (str): new comment without garbage words
    """
    ptext = re.sub(r'(\s)\1+', r'\1', ptext).strip()
    words = ptext.split(' ')
    new_words = []
    english_cnt = 0
    vietnam_cnt = 0

    for word in words:
        word = word.strip()
        no_duplicate_word = removeDuplicateLetters(word)

        if word == '' or no_duplicate_word == '': continue

        if pdictionary.get(no_duplicate_word, False) == True:  # kiếm tra word có trong tiếng việt ko
            vietnam_cnt += 1
            new_words.append(no_duplicate_word)
        elif penchantEN.check(word) == True:  # kiểm tra từ có trong tiếng anh ko
            english_cnt += 1
            new_words.append(word)

    if english_cnt > vietnam_cnt or vietnam_cnt == 0:  # nếu một câu mà từ tiếng anh nhiều hơn tiếng việt
        return ''
    else:
        return ' '.join(new_words).strip()


def removeStopwords(ptext: str, plist: List[str]) -> (str):
    """
    Loại bỏ stopword

    Args:
        ptext (str): comment
        plist (List[str]): chứa các stopword

    Returns:
        (str): comment mới không chứa stopword
    """
    ptext = f" {ptext} "

    for sw in plist:
        sw = f" {sw} "
        ptext = re.sub(sw, ' ', ptext)

    return re.sub(r'(\s)\1+', r'\1', ptext).strip()
