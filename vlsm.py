from network_tools import broadcastAdress, cidr_to_decimal,table
from math import log2


def vlsm(address:str, subnetMask:str, networkNeeds:list[tuple]) -> list:
    networkNames = ['Name (subnet need)']
    subnetAdresses = ['Subnet adress']
    firstUsableAdresses = ['First usable adress']
    broadAdresses = ['Broadcast adress']
    lastUsableAdresses = ['Last usable adress']
    subnetMasks = ['Subnet Mask']
    number_of_usable_host = ['Number of usable hosts']
    
    netAdress = [int(i) for i in address.split('.')]

    for name,number_of_host in sorted(networkNeeds, key=lambda x:x[1], reverse=True):
        
        subnetMask = '/' + str(32 - (int(log2(number_of_host+2)) if log2(number_of_host+2) - int(log2(number_of_host+2)) == 0 else int(log2(number_of_host+2))+1))
        broadAdress = broadcastAdress('.'.join([str(i) for i in netAdress]), subnetMask).split('.')
        
        networkNames.append(name+f' ({number_of_host})')
        number_of_usable_host.append(f"{(2**(32-int(subnetMask[1:])))-2} ({(2**(32-int(subnetMask[1:])))}-2)")
        subnetAdresses.append('.'.join([str(i) for i in netAdress]))
        firstUsableAdresses.append('.'.join([str(netAdress[i]) if i != len(netAdress)-1 else str(netAdress[i]+1) for i in range(len(netAdress))]))
        lastUsableAdresses.append('.'.join([broadAdress[i] if i != len(broadAdress)-1 else str(int(broadAdress[i])-1) for i in range(len(broadAdress))]))
        broadAdresses.append('.'.join(broadAdress))
        subnetMasks.append(cidr_to_decimal(subnetMask))

        netAdress[-1] += (2**(32-int(subnetMask[1:])))
        for j in range(len(netAdress)-1,-1,-1):
            if netAdress[j] >= 256:
                netAdress[j-1] += netAdress[j]//256
                netAdress[j] = netAdress[j]%256

    return networkNames, number_of_usable_host, subnetAdresses, firstUsableAdresses, lastUsableAdresses, broadAdresses, subnetMasks



if __name__ == '__main__':
    table(vlsm('192.168.0.0','/24', [('a',58),('b',63),('c',8),('d',12),('e',2)]))













#  ______                           __  ____                __                       __      __                              
# /\  _  \                         /\ \/\  _`\             /\ \  __                 /\ \  __/\ \                             
# \ \ \L\ \  __  __  __     __     \_\ \ \ \/\_\    ___    \_\ \/\_\    ___      __ \ \ \/\ \ \ \     __     __  __    ____  
#  \ \  __ \/\ \/\ \/\ \  /'__`\   /'_` \ \ \/_/_  / __`\  /'_` \/\ \ /' _ `\  /'_ `\\ \ \ \ \ \ \  /'__`\  /\ \/\ \  /',__\ 
#   \ \ \/\ \ \ \_/ \_/ \/\ \L\.\_/\ \L\ \ \ \L\ \/\ \L\ \/\ \L\ \ \ \/\ \/\ \/\ \L\ \\ \ \_/ \_\ \/\ \L\.\_\ \ \_\ \/\__, `\
#    \ \_\ \_\ \___x___/'\ \__/.\_\ \___,_\ \____/\ \____/\ \___,_\ \_\ \_\ \_\ \____ \\ `\___x___/\ \__/.\_\\/`____ \/\____/
#     \/_/\/_/\/__//__/   \/__/\/_/\/__,_ /\/___/  \/___/  \/__,_ /\/_/\/_/\/_/\/___L\ \'\/__//__/  \/__/\/_/ `/___/> \/___/ 
#                                                                                /\____/                         /\___/      
#                                                                                \_/__/                          \/__/      