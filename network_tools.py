#----------------------------------------------- Functions that calculate ip adresses , subnet masks,... -----------------------------------

def table(li: tuple[tuple[str]], color1="\033[34m", color2="\033[33m") -> None:
    for e in range(len(li[0])):
        for i in range(len(li)):
            print(color1+"+", end='')
            for _ in range(len(max(li[i], key=len))+2):
                print('-', end='')
        print("+")
        for i in range(len(li)):
            print("| "+color2+li[i][e]+" "*(len(max(li[i], key=len))+1-len(li[i][e]))+color1, end='')
        print('|')
    for i in range(len(li)):
        print("+", end='')
        for _ in range(len(max(li[i],key=len))+2):
            print('-', end='')
    print("+"+'\033[0m')

def binary_to_int(a: str) -> int:
    a = a[::-1]
    b = 0
    for i in range(len(a)):
        b += int(a[i])*(2**i)
    return b

def ipv4_to_binary(ip: str) -> str:
    ip = [f"{bin(int(i))[2:]:0>8}" for i in ip.split('.')]
    return '.'.join(ip)

def binary_to_ipv4decimal(ip: str) -> str:
    return '.'.join([str(binary_to_int(i)) for i in ip.split('.')])

def decimal_to_cidr(subnet: str) -> str:
    return '/'+str(sum([str(bin(int(i))).count('1') for i in subnet.split('.')]))

def cidr_to_decimal(cidr: str) -> str:
    a = [i for i in f"{'1'*int(cidr.strip('/')):0<32}"]
    for i in [8, 17, 26]:
        a.insert(i, '.')
    return '.'.join([str(binary_to_int(i)) for i in "".join(a).split('.')])

def remove_zero(s: str) -> str:
    if not s.startswith('0') or s == '':
        return s
    x = -1
    for i in range(len(s)-1):
        if s[i] == '0' and s[i+1] != '0':
            x = i 
            break
    return '0' if x == -1 else s[x+1:]

def longest_subsequence_0(li: list) -> tuple:
    i = 0
    longest = (0, 0)
    while i < len(li):
        if li[i] == '0':
            for j in range(i+1, len(li)):
                if li[j] != '0':
                    if longest[1]-longest[0] < j-i:
                        longest = (i, j)
                        i = j
                        break
                elif  j == len(li)-1 and li[j] == '0':
                    if longest[1]-longest[0] < j+1-i:
                        longest = (i, j+1)
                        j = i+1
        i += 1
    return longest

def compress_ipv6(ip: str) -> str :
    ip = ip.split(':')
    ip = [remove_zero(i) for i in ip]

    # ip = map(remove_zero,ip)
    if all(i == '0' for i in ip):
        return '::'
    longest = longest_subsequence_0(ip)
    if longest[1] - longest[0] > 1:
        ip[longest[0]:longest[1]] = [":"] if longest[0] == 0 or longest[1] == 8 else [""]
    for i in range(len(ip)-1):
        ip[i] = ip[i]+':'
    return ''.join(ip)

def decompress_ipv6(ip: str) -> str:
    ip = [f'{i:0>4}' if i != '' else i for i in ip.split(':') ]
    if all(i == '' for i in ip):
        return ':'.join(['0000']*8)
    if '' in ip:
        ind = ip.index('')
        if ind == 0 or (ind == len(ip)-2 and ip[ind+1] == ''):
            del ip[ind:ind+2]
        else:
            del ip[ind]
        ip[ind:ind] = ['0000']*(8 - len(ip))
    return ':'.join(ip)

def networkAddress(ip: str, subnetMask: str='') -> str:
    if '/' in ip: 
        ip , subnetMask = ipv4_to_binary(ip.split('/')[0]).split('.') , ipv4_to_binary(cidr_to_decimal('/'+ip.split('/')[1])).split('.')
    else:
        ip = ipv4_to_binary(ip).split('.')
    if '/' in subnetMask:
        subnetMask = ipv4_to_binary(cidr_to_decimal(subnetMask)).split('.')
    else:
        subnetMask = ipv4_to_binary(subnetMask).split('.')
    adress = [str(int(i) & int(j)) for i,j in zip(''.join(ip),''.join(subnetMask))]
    for i in [8,17,26]:
        adress.insert(i,'.')
    return binary_to_ipv4decimal(''.join(adress))

def broadcastAdress(netAdress: str, subnetMask: str=''):
    if '/' in netAdress: 
        netAdress , subnetMask = ipv4_to_binary(netAdress.split('/')[0]).split('.') , ipv4_to_binary(cidr_to_decimal('/'+netAdress.split('/')[1])).split('.')
    else:
        netAdress = ipv4_to_binary(netAdress).split('.')
    if '/' in subnetMask:
        subnetMask = ipv4_to_binary(cidr_to_decimal(subnetMask)).split('.')
    else:
        subnetMask = ipv4_to_binary(subnetMask).split('.')
    broadAdress = [str(int(i) | int('0' if j == '1' else '1')) for i,j in zip(''.join(netAdress),''.join(subnetMask))]
    for i in [8,17,26]:
        broadAdress.insert(i,'.')
    return binary_to_ipv4decimal(''.join(broadAdress))

def switchSubnet(ip: str, initialMask: str='', newMask: str='') -> list:
    if '.' in initialMask:
        initialMask = decimal_to_cidr(initialMask)
    if '.' in newMask:
        newMask = decimal_to_cidr(newMask)

    subnetAdresses = ['Subnet adress']
    firstUsableAdress = ['First usable adress']
    broadAdress = ['Broadcast adress']
    lastUsableAdress = ['Last usable adress']

    netAdress = [int(i) for i in networkAddress(ip,initialMask).split('.')]
    bAdress = broadcastAdress('.'.join([str(i) for i in netAdress]),newMask).split('.')

    subnetAdresses.append('.'.join([str(i) for i in netAdress]))
    firstUsableAdress.append('.'.join([str(netAdress[i]) if i != len(netAdress)-1 else str(netAdress[i]+1) for i in range(len(netAdress))]))
    broadAdress.append('.'.join(bAdress))
    lastUsableAdress.append('.'.join([bAdress[i] if i != len(bAdress)-1 else str(int(bAdress[i])-1) for i in range(len(bAdress))]))

    for i in range((2**(int(newMask[1:]) - int(initialMask[1:])))-1):
        netAdress[-1] += (2**(32-int(newMask[1:])))
        for j in range(len(netAdress)-1,-1,-1):
            if netAdress[j] >= 256:
                netAdress[j-1] += netAdress[j]//256
                netAdress[j] = netAdress[j]%256

        subnetAdresses.append('.'.join([str(i) for i in netAdress]))
        firstUsableAdress.append('.'.join([str(netAdress[i]) if i != len(netAdress)-1 else str(netAdress[i]+1) for i in range(len(netAdress))]))
        bAdress = broadcastAdress('.'.join([str(i) for i in netAdress]),newMask).split('.')
        broadAdress.append('.'.join(bAdress))
        lastUsableAdress.append('.'.join([bAdress[i] if i != len(bAdress)-1 else str(int(bAdress[i])-1) for i in range(len(bAdress))]))

    return subnetAdresses , firstUsableAdress , lastUsableAdress , broadAdress  , ['Subnet Mask']+[cidr_to_decimal(newMask)]*(2**(int(newMask[1:]) - int(initialMask[1:])))

#------------------------------------------- Input checks ------------------------------------------

def verify_ipv4(ipv4: str, binary: bool=True, decimal: bool=True) -> int:
    if ipv4.count('.') != 3 or ipv4.endswith('.'):
        return -2
    if 7 <= len(ipv4) <= 15:
        if not (all(j.isdigit() for i in ipv4.split('.') for j in i) and all(0 <= int(i) <= 255  for i in ipv4.split('.'))):
            return -1
        return 1 if decimal == True else -1
    elif len(ipv4) > 15:
        if not all(all(j in ['0','1'] for j in i) and len(i) == 8 for i in ipv4.split('.')):
            return 0
        return 10 if binary == True else -2

def verify_ipv6(ipv6: str) -> int:
    if len(ipv6) < 2 or ':' not in ipv6:
        return -1
    if ipv6.count('::') > 1 or (ipv6.startswith(':') and ipv6[1] != ':') or (ipv6.endswith(':') and ipv6[-2] != ':') or ':::' in ipv6 :
        return -1
    if len(ipv6) >= 2:
        if not all(all(j.lower() in [str(a) for a in range(10)]+['a','b','c','d','e','f',''] for j in i ) and 0 <= len(i) <= 4 for i in ipv6.split(':')):
            return 0
        return 1
    
def verifiy_subnet_mask(subnetMask: str, decimal: bool=True, cidr=True) -> int:
    if '.' in subnetMask:
        if subnetMask.count('.') != 3 or subnetMask.endswith('.'):
            return -2
        if not all(i.isdigit() for i in subnetMask.split('.')):
            return -1
        binarySubnet = ''.join(ipv4_to_binary(subnetMask).split('.'))
        if '1' in binarySubnet:
            for i in range(len(binarySubnet)-1):
                if binarySubnet[i] == '0' and binarySubnet[i+1] == '1':
                    return 0              
        if not int(decimal_to_cidr(subnetMask)[1:]) in range(32+1):
            return 0
        return 1 if decimal == True else -2
    elif '/' in subnetMask:
        if not int(subnetMask[1:]) in range(32+1):
            return 0
        return 1 if cidr == True else -2
    return -2


def is_private_address(ip:str, subnetMask:str) -> str:
    PRIVATE_ADRESSES = {
        'A': (10,8),
        'B': (172,16,31,16),
        'C': (192,168,168,24)
    }

    ip = list(map(int,ip.split('.')))

    for address_class, plage in PRIVATE_ADRESSES.items():
        if((address_class == 'A') and (plage[0] == ip[0]) and (int(subnetMask[1:]) >= plage[-1])):
            return True
        else:
            if(address_class == 'A'):
                return False

            if((plage[0] == ip[0]) and (ip[2] in range(plage[1],plage[2]+1)) and (int(subnetMask[1:]) >= plage[-1]) ):
                return True
    return False
            

        
def input_ipv4(text: str, binary: bool=True, decimal: bool=True) -> str:
    errors = {
        -2:"Make sure you enter a four decimal field between 0 and 255 separated by a dot(.) e.g: 172.30.16.0",
        -1:"It looks like you've entered an aphabetic character in the adress or a decimal that exceed the limit of 255",
        0:"You trying to entering the adress in it binary but it may seems that you it wrong. Make sure every field contain 8 bits",
    }
    ipv4 = input(f"\n{text}: ").strip()
    if verify_ipv4(ipv4, binary, decimal) not in (1, 10):
        print(f"\n{'\033[31m'}Invalid input. {errors[verify_ipv4(ipv4, binary, decimal)]}{'\033[0m'}")
        return input_ipv4(text, binary, decimal)
    return '.'.join([remove_zero(i) for i in ipv4.split('.')]) if verify_ipv4(ipv4, binary, decimal) == 1 else binary_to_ipv4decimal(ipv4)

def input_ipv4_with_mask(text: str):
    ipv4 = input(f"\n{text}: ").strip()
    if len(ipv4.split()) == 1:
        if len(ipv4.split('/')) == 2:
            ipv4, subnetMask = ipv4.split('/')[0].strip(), '/'+ipv4.split('/')[1].strip()
            if verify_ipv4(ipv4) not in (1, 10) or verifiy_subnet_mask(subnetMask) != 1:
                print("\n\033[31mBad input\033[0m")
                return input_ipv4_with_mask(text)
            return '.'.join([remove_zero(i) for i in ipv4.split('.')]) if verify_ipv4(ipv4) == 1 else binary_to_ipv4decimal(ipv4), subnetMask
        if verify_ipv4(ipv4) not in (1, 10):
            print("\n\033[31mBad input\033[0m")
            return input_ipv4(text)
        return '.'.join([remove_zero(i) for i in ipv4.split('.')]) if verify_ipv4(ipv4) == 1 else binary_to_ipv4decimal(ipv4)
    elif len(ipv4.split()) == 2:
        ipv4, subnetMask = tuple(i.strip() for i in ipv4.split())
        if verify_ipv4(ipv4) not in (1, 10) or verifiy_subnet_mask(subnetMask) != 1:
            print("\n\033[31mBad input\033[0m")
            return input_ipv4_with_mask(text)
        return '.'.join([remove_zero(i) for i in ipv4.split('.')]) if verify_ipv4(ipv4) == 1 else binary_to_ipv4decimal(ipv4), decimal_to_cidr(subnetMask)
    return input_ipv4_with_mask(text)



def input_ipv6(text: str) -> str:
    errors = {
        -1:"It look like the syntax of your ipv6 adress is wrong e.g of valid ipv6 adress: ::1 , 2001:db8:4444:555:4:ff:1:0, ....",
        0:"Your adress may containt a not hexadecimal digit (hexadecimal digits are 0 to 9 and a to f)",
    }
    ipv6 = input(f"\n{text}: ").strip()
    if verify_ipv6(ipv6) != 1:
        print(f"\n{'\033[31m'}Invalid input. {errors[verify_ipv6(ipv6)]}{'\033[0m'}")
        return input_ipv6(text)
    return ipv6.lower()
    
def input_subnetMask(text: str, decimal: bool=True, cidr: bool=True) -> str:
    errors = {
        -2:"Make sure you enter a four decimal field between 0 and 255 separated by a dot(.) e.g: 255.255.255.0",
        -1:"It looks like you've entered an aphabetic character in the mask",
        0:"That value of subnet mask is impossible",
    }
    subnetMask = input(f"\n{text}: ").strip()
    if verifiy_subnet_mask(subnetMask, decimal, cidr) != 1:
        print(f"\n{'\033[31m'}Invalid input. {errors[verifiy_subnet_mask(subnetMask, decimal, cidr)]}{'\033[0m'}")
        return input_subnetMask(text, decimal ,cidr)
    return subnetMask


# table(([f'/{i}' for i in range(33)], [cidr_to_decimal(f'/{i}') for i in range(33)]))
if __name__ == "__main__":
    # table(switchSubnet('192.168.16.0', '/24','/25'))
    # a = input_ipv4_with_mask("Enter une adresse ip")

    # print(a)
    print(networkAddress('192.168.1.0', '/24'))
    print(input_ipv4_with_mask("Yo"))
    # print(input_ipv6("Yo"))
    # print(input_subnetMask("Yo"))
















#  ______                           __  ____                __                       __      __                              
# /\  _  \                         /\ \/\  _`\             /\ \  __                 /\ \  __/\ \                             
# \ \ \L\ \  __  __  __     __     \_\ \ \ \/\_\    ___    \_\ \/\_\    ___      __ \ \ \/\ \ \ \     __     __  __    ____  
#  \ \  __ \/\ \/\ \/\ \  /'__`\   /'_` \ \ \/_/_  / __`\  /'_` \/\ \ /' _ `\  /'_ `\\ \ \ \ \ \ \  /'__`\  /\ \/\ \  /',__\ 
#   \ \ \/\ \ \ \_/ \_/ \/\ \L\.\_/\ \L\ \ \ \L\ \/\ \L\ \/\ \L\ \ \ \/\ \/\ \/\ \L\ \\ \ \_/ \_\ \/\ \L\.\_\ \ \_\ \/\__, `\
#    \ \_\ \_\ \___x___/'\ \__/.\_\ \___,_\ \____/\ \____/\ \___,_\ \_\ \_\ \_\ \____ \\ `\___x___/\ \__/.\_\\/`____ \/\____/
#     \/_/\/_/\/__//__/   \/__/\/_/\/__,_ /\/___/  \/___/  \/__,_ /\/_/\/_/\/_/\/___L\ \'\/__//__/  \/__/\/_/ `/___/> \/___/ 
#                                                                                /\____/                         /\___/      
#                                                                                \_/__/                          \/__/       