#Author: Olhayeh ali
#date:24/02/2022


#A palindrome is a number, word or sentence that can be read the same way forwards and backwards.
#So today, 22 February, looks like this as a number: 22 02 2022(2 day later)

#this  function check if a sentence of string is palindrome
def isPalindrome(s):
    return s == s[::-1]

#main function
def main():
    sentence = input('please write a sentence to check if it\'s a palindrome: ')
    result = isPalindrome(sentence)
    print('the word is palindrome') if result else print('the word is not palindrome')

if __name__ == '__main__':
    main()