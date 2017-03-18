
def convert_to_roman(number):
    dict = [
        {1: 'I', 5: 'V', 10: 'X'},
        {1: 'X', 5: 'L', 10: 'C'},
        {1: 'C', 5: 'D', 10: 'M'},
        {1: 'M'},
    ]
    
    if number < 4000 and number > 0:
        count = 0
        ans = ''
        
        while (number > 0):
            n = number % 10
            if n in [1, 5, 10]:
                ans = dict[count][n] + ans
            elif n < 4:
                ans = (dict[count][1] * n) + ans
            elif n == 4:
                ans = dict[count][1] + dict[count][5] + ans
            elif n < 9:
                ans = dict[count][5] + (dict[count][1] * (n - 5)) + ans
            elif n == 9:
                ans = dict[count][1] + dict[count][10] + ans
            
            number = int(number / 10)
            count += 1
            
        print(ans)
        
    else: 
        print('This input cannot be converted to Roman')


def main():
    print("You can type 'convert 100' or 'convert 2986 to roman' or simply '57' ")
    while(True):
        input = raw_input().strip().lower()
        if input.startswith('convert '):
            convert_to_roman(int(input.split()[1]))
        elif int(input) > 0:
            convert_to_roman(int(input))
        else:
            print('This input cannot be converted to Roman')
        
    
if __name__ == '__main__':
    main()