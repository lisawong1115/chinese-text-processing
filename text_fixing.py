# -*- coding: utf-8 -*-

import re
import sys


def remove_extra_punctuation(line): 
    """
    Delete consecutive punctuations, only keeping the first;
    Filter out punctuations like '~' and '…'.
    """
    punc = "！？。＂＃$＄％&＆'＇()（）*＊+＋，-－/／:：;；<＜=＝>＞@[［＼\］] \
    ＾^＿_｀`{｛|｜}｝~～《》｟｠｢｣､、〃「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟 \
    〰〾〿–—‘’‛“”„‟…‧﹏."
    
    charList = []
    if len(line)> 0:
        for char in line:
            if char not in punc:
                charList.append(char)
            elif (char != "~" and char != "～" and char != "…"):
                if len(charList) == 0 or (len(charList) > 0 and char != charList[-1]):
                    charList.append(char)
            else:
                charList.append(' ')
                            
    return "".join(charList)
    
    
def filter_other(line):
    """
    filter out characters that are not Chinese, letters, normal punctuations or numbers.
    """
    punc = "！？。＂＃$＄％&＆'＇()（）*＊+＋，-－/／:：;；<＜=＝>＞@[［＼\］] \
        ＾^＿｀`{｛|｜}｝~～《》｟｠｢｣､、〃「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟 \
        〰〾〿–—‘’‛“”„‟…‧﹏."
        
    if len(line)>0:
        for uchar in line:
            if uchar not in punc:
                if not ((uchar >= u'\u4e00' and uchar<=u'\u9fa5') \
                or (uchar >= u'\u0030' and uchar<=u'\u0039') \
                or (uchar >= u'\u0041' and uchar<=u'\u005a') \
                or (uchar >= u'\u0061' and uchar<=u'\u007a') \
                or (uchar == ' ' or uchar == '\n')):
                    line = line.replace(uchar, u'')
                elif uchar == '_':
                    line = line.replace(uchar, u' ')

    return line
    

def filter_nonsense(line):
    """
    Filter out nonsense words and phrases.
    """
    nonsense = ["图片评论", "评论配图", "O网页链接", "查看动图", \
                'Comment with pics']
    for word in nonsense:
        if word in line:
            line = line.replace(word, u'')

    return line

def filter_brackets(line):
    """
    Filter out words, especailly emoticon phrases, that are surrounded by square 
    brackets.
    """
    a1 = re.compile(r'[［[].*?[]］]' )
    new = a1.sub('', line) 
    return new
    
def username_and_duplicate_char(line):
    """
    Filter out usernames followed by '@' and repeating characters:
        1) If the repeating characters are Chinese, shorten the number to be 2;
        2) If the repeating characters are non-Chinese, delete them.
    """
    s1 = re.sub(r'(.)\1+', r'\1\1', line)
    s2 = re.sub(r'([h6]){2,}', r'', s1)
    s3 = re.sub(r'\@{1}[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}\s*', r' ', s2)
    s4 = re.sub(r'\#(.)+\#', r' ', s3)

    return s4
            


def remove_extra_space(line):
    """
    Remove spaces that are at the beginning of a line.
    """
    i=0
    if len(line) > 0:
        while line[i].isspace() and i < len(line)-1:
            i=i+1
        else:
            empty=line[0:i].replace(' ','')
            line=empty+line[i:]
            return line

        
#--------------------------- Main Function ----------------------------                
                       
                                        
def main():
    filename = input("Filename: ")
    with open(filename, 'r', encoding='utf-8') as fl1:
        lines = fl1.readlines()

    fl2 = open(filename.split('.')[0] + '_fixed.txt', 'w', encoding='utf-8')
    lines_seen = set()
    lines_added = []
    
    for i in range(len(lines)):  
        if lines[i] not in lines_seen:
            noUsernRepeat = username_and_duplicate_char(lines[i])
            noOther = filter_other(noUsernRepeat)
            noNonsense = filter_nonsense(noOther)
            noBrackets = filter_brackets(noNonsense)
            noPunc = remove_extra_punctuation(noBrackets)
            result = remove_extra_space(noPunc)            

            lines_seen.add(lines[i])
            
            if lines[i] == '\n' or (noUsernRepeat != '\n' and noOther != '\n' \
                and noNonsense != '\n' and noBrackets != '\n' and noPunc != '\n' \
                and result != '\n'): 
                lines_added.append(lines[i])
                fl2.write(result)
                
        elif lines[i] == '\n' and i != 0 and lines[i-1] != '\n':
            lines_added.append(lines[i])

            if lines_added[-2] != '\n':
                fl2.write('\n')


    fl2.close()

#------------------------------ Testing ----------------------------------

if __name__ == "__main__":
    main()
