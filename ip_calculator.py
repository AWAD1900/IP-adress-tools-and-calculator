from network_tools import *
from vlsm import *
from type_checkers import *
from string import ascii_lowercase
from os import system, name


def control(text: str, options: str) -> str:
    a = input(f"\n{text}: ").lower()
    if len(a) != 1 or a not in options:
        print(f"\n\033[31mMake sure you enter a good value (between {' - '.join(i for i in options)})\033[0m")
        return control(text, options)
    return a


def display_menu(options: list) -> None:
    for i in range(len(options)):
        print(f"\t\033[1m{ascii_lowercase[i]}. \033[32m{options[i]}"+"\033[0m")



menu_a = ("IPv4", "IPv6", 'Quit')
menu_b = ("Convert to binary", "From binary to decimal", "Decimal notation to CIDR", "CIDR to decimal notation", "Find the network adress", "Find the broadcast adress", "Find all the possible subnets after switching the subnet mask", "VLSM", "IPv4 cheatsheet", "Return to main menu")
menu_c = ("Compress an IPv6 address", "Decompress an IPv6 address","Return to main menu")

system('cls' if name == 'nt' else 'clear')
display_menu(menu_a)
a = control("Enter an option", 'abc')
system('cls' if name == 'nt' else 'clear')
while a in 'abc':
    match (a):
        case 'a':
            print("""
                    ╔══════════════════════════════╗
                    ║ ___   ____            _  _   ║
                    ║|_ _| |  _ \  __   __ | || |  ║
                    ║ | |  | |_) | \ \ / / | || |_ ║
                    ║ | |  |  __/   \ V /  |__   _|║
                    ║|___| |_|       \_/      |_|  ║
                    ╚══════════════════════════════╝
            """)
            display_menu(menu_b)
            b = control("ipv4> Enter an option",ascii_lowercase[:len(menu_b)])
            # system('cls' if name == 'nt' else 'clear')
            while b in ascii_lowercase[:len(menu_b)]:
                match(b):
                    case 'a':
                        ipv4 = input_ipv4("ipv4> "+menu_b[0]+"> Enter the decimal ipv4 adress", binary=False)
                        table([["DECIMAL", ipv4], ["BINARY", ipv4_to_binary(ipv4)]])
                    
                    
                    case 'b':
                        ipv4 = input_ipv4("ipv4> "+menu_b[1]+"> Enter the binary ipv4 adress", decimal=False)
                        table([["BINARY", ipv4], ["DECIMAL", binary_to_ipv4decimal(ipv4)]])
                    
                    
                    case 'c':
                        subnetMask = input_subnetMask("ipv4> "+menu_b[2]+"> Enter a decimal subnet mask value", cidr=False)
                        table([["DECIMAL", subnetMask], ["CIDR", decimal_to_cidr(subnetMask)]])
                    
                    
                    case 'd':
                        subnetMask = input_subnetMask("ipv4> "+menu_b[3]+"> Enter a cidr subnet mask value", decimal=False)
                        table([["CIDR", subnetMask], ["DECIMAL", cidr_to_decimal(subnetMask)]])
                    
                    
                    case 'e':
                        netAdress = input_ipv4_with_mask("ipv4> "+menu_b[4]+">"+"\n\nNb: You can enter the ip adress with the mask eg: 192.168.16.0/24, 10.0.0.0 /8, 192.168.16.0 255.255.255.0, 11000000.1101100.10101010.00000000/24, ...\n\nEnter the ipv4 (host or net) adress (binary or decimal)")
                        if len(netAdress) == 2:
                            netAdress, subnetMask = netAdress
                        else:
                            subnetMask = input_subnetMask("Enter the network's subnet mask (cidr or decimal)")

                        table([["The network adress is", networkAddress(netAdress,subnetMask)+f' {subnetMask}']])
                    
                    
                    case 'f':
                        netAdress = input_ipv4_with_mask("ipv4> "+menu_b[5]+">"+"\n\nNb: You can enter the ip adress with the mask eg: 192.168.16.0/24, 10.0.0.0 /8, 192.168.16.0 255.255.255.0, 11000000.1101100.10101010.00000000/24, ...\n\nEnter the ipv4 (host or net) adress (binary or decimal)")
                        if len(netAdress) == 2:
                            netAdress, subnetMask = netAdress
                        else:
                            subnetMask = input_subnetMask("Enter the network's subnet mask (cidr or decimal)")
                        table([["The broadcast adress is", broadcastAdress(netAdress, subnetMask)]])
                    
                    
                    case 'g':
                        ipv4 = input_ipv4_with_mask("ipv4> "+menu_b[6]+">"+"\n\nNb: You can enter the ip adress with the mask eg: 192.168.16.0/24, 10.0.0.0 /8, 192.168.16.0 255.255.255.0, 11000000.1101100.10101010.00000000/24, ...\n\nEnter the ipv4 (host or net) adress (binary or decimal)")
                        if len(ipv4) == 2:
                            ipv4, initialSubnetMask = ipv4
                        else:
                            initialSubnetMask = input_subnetMask("Enter the initial new network's subnet mask (cidr or decimal)")
                        while True:
                            newSubnetMask = input_subnetMask("Enter the new network's subnet mask (cidr or decimal)")
                            try:
                                newSubnetMask = decimal_to_cidr(newSubnetMask)
                                initialSubnetMask   = decimal_to_cidr(initialSubnetMask)
                            except ValueError:
                                newSubnetMask = newSubnetMask
                                initialSubnetMask = initialSubnetMask
                            print(initialSubnetMask,newSubnetMask)
                            if int(newSubnetMask[1:]) > int(initialSubnetMask[1:]):
                                break
                            print("\n\033[31mThe new subnet mask must be greater than the initial one\033[0m")
                        table(switchSubnet(ipv4, initialSubnetMask, newSubnetMask))

                    
                    case 'h':
                        networkNeeds = []
                        for i in range(input_int("ipv4> "+menu_b[7]+">"+"How many subnetwork do you want in your network", "Assert that you enter a valid interger superior to 1", 1)):
                            print(f"\n\033[33m{'-'*15} Sunbnetwork {i+1 if len(str(i+1)) > 1 else f'0{i+1}'} {'-'*15}\033[0m")
                            while True:
                                netName = input(f"\nEnter the name of the subnetwork : ")
                                
                                if(len(netName) == 0):
                                    print("\n\033[31mYou're entered nothing\033[0m")
                                elif(any(netName in needs for needs in networkNeeds)):
                                    print("\n\033[31mThat name is already used for a subnetwork\033[0m")
                                else:
                                    break
                                
                                # if len(netName) != 0 and all(netName not in needs for needs in networkNeeds):
                                #     break

                            number_of_hosts = input_int(f"\nEnter the number of hosts in {netName}","Assert you enter an interger superior to 0", 0) 

                            networkNeeds.append((netName, number_of_hosts))

                        print(f"\n\033[33m{'-'*15} Enter the network adress you want to segment {'-'*15}\033[0m")

                        while True:
                            address = input_ipv4_with_mask("\nNb: You can enter the network address with or without the mask eg: 192.168.16.0/24, 10.0.0.0, 192.168.1.0 255.255.255.0, 11000000.1101100.10101010.00000000/24, ...\n\nEnter the ipv4 a network adress (binary or decimal)")
                            if len(address) == 2:
                                address, subnetMask = address
                            else:
                                subnetMask = input_subnetMask("Enter the subnet mask (cidr or decimal)")
                                subnetMask = decimal_to_cidr(subnetMask) if "/" not in subnetMask else subnetMask

                            while((2**(32-int(subnetMask[1:])))+2 <= sum(i[1] for i in networkNeeds)) :
                                print(f"\nThe subnet mask {subnetMask} can only support {(2**(32-int(subnetMask[1:])))-2 if subnetMask != '/32' else 0} host addresses but you network needs {sum(i[1] for i in networkNeeds)} host addresses")
                                subnetMask = input_subnetMask("Enter a subnet mask (cidr or decimal)")
                                if((2**(32-int(subnetMask[1:])))+2 >= sum(i[1] for i in networkNeeds)):
                                    break
                                                        
                            if(networkAddress(address, subnetMask) != address):
                                print(f"\n\033[31mThe address {address} is not a network address with the {subnetMask} mask\033[0m")
                            else:
                                break

                        optimal_subnetMask = '/'+str(32 - (int(log2(sum(i[1] for i in networkNeeds)+2)) if log2(sum(i[1] for i in networkNeeds)+2) - int(log2(sum(i[1] for i in networkNeeds)+2)) == 0 else int(log2(sum(i[1] for i in networkNeeds)+2))+1))

                        if(int(subnetMask[1:]) != int(optimal_subnetMask[1:])):
                            print(f"\n\n{'\033[33m'}Warning the subnet mask you gave is good but it maybe support ways more hosts than the network needs.\nI have a proposition for you : you can instead use \033[32m{optimal_subnetMask}\033[33m subnet mask that be more optimal for your network. Do you wanna use that one or keep yours? Don't worry the result will the same.{'\033[0m'}")
                            if(control("Enter (Y/N)","yn") == "y"):
                                subnetMask = optimal_subnetMask

                        print("\n\n\033[1m----------------------------------------- VLSM Result -----------------------------------------\033[0m\n\n")

                        print(f"Network address: {'\033[1m'+'\033[32m'}{address}\t{'\033[0m'}Subnet mask: {'\033[1m'+'\033[32m'}{subnetMask}{'\033[0m'}\n\n")

                        table(vlsm(address,subnetMask,networkNeeds))


                    case 'i':
                        print("\n\n\033[1m-------------------- Subnet mask possible values --------------------\033[0m\n\n")
                        table([["Decimal subnet mask"]+[cidr_to_decimal(f'/{i}') for i in range(33)], ["CIDR"]+[f'/{i}' for i in range(33)]])
                        print("\n\n\033[1m-------------------- ipv4 adresses classes --------------------\033[0m\n\n")
                        table([["Class A", "Class B", "class C", "Class D (Multicast)", "Class E (Experimental)"], ["0.0.0.0/8 to 127.255.255.255/8", "128.0.0.0/16 to 191.255.255.255/16", "192.0.0.0/24 to 223.255.255.255/24", "224.0.0.0 to 239.255.255.255", "240.0.0.0 to 255.255.255.255"]])
                        print("\n\n\033[1m-------------------- Special IPv4 Addresses --------------------\033[0m\n\n")
                        table([["The unspecified address", "Loopback", "APIPA", "Private Network - Class A", "Private Network - Class B", "Private Network - Class C", "Broadcast Address"] ,['0.0.0.0', "127.0.0.0 to 127.255.255.255", "169.254.0.0 to 169.254.255.255", "10.0.0.0 to 10.255.255.255", "172.16.0.0 to 172.31.255.255","192.168.0.0 to 192.168.255.255", "255.255.255.255"]])
                    
                    case 'j':
                        break

                print("\n\n")
                display_menu(menu_b)
                b = control("ipv4> Enter an option",ascii_lowercase[:len(menu_b)])
                # system('cls' if name == 'nt' else 'clear')

        case 'b':
            print("""
                    ╔═════════════════════════════╗
                    ║ ___   ____             __   ║
                    ║|_ _| |  _ \  __   __  / /_  ║
                    ║ | |  | |_) | \ \ / / | '_ \ ║
                    ║ | |  |  __/   \ V /  | (_) |║
                    ║|___| |_|       \_/    \___/ ║
                    ╚═════════════════════════════╝
                    """)
            display_menu(menu_c)
            b = control("ipv6> Enter an option",ascii_lowercase[:len(menu_c)])
            system('cls' if name == 'nt' else 'clear')
            while b in ascii_lowercase[:len(menu_b)]:
                match(b):
                    case 'a':
                        ipv6 = input_ipv6("ipv6> Enter an ipv6 adress")
                        table([["The adress you've entered", ipv6], ["Compressed form", compress_ipv6(ipv6)]])
                    case 'b':
                        ipv6 = input_ipv6("ipv6> Enter an ipv6 adress")
                        table([["The adress you've entered", ipv6], ["Decompressed form", decompress_ipv6(ipv6)]])
                    case 'c':
                        break
                print("\n\n")
                display_menu(menu_c)
                b = control("ipv6> Enter an option", ascii_lowercase[:len(menu_c)])
                # system('cls' if name == 'nt' else 'clear')

        case 'c':
            break

    print("\n\n")
    display_menu(menu_a)
    a = control("Enter an option", 'abc')
    # system('cls' if name == 'nt' else 'clear')



















#  ______                           __  ____                __                       __      __                              
# /\  _  \                         /\ \/\  _`\             /\ \  __                 /\ \  __/\ \                             
# \ \ \L\ \  __  __  __     __     \_\ \ \ \/\_\    ___    \_\ \/\_\    ___      __ \ \ \/\ \ \ \     __     __  __    ____  
#  \ \  __ \/\ \/\ \/\ \  /'__`\   /'_` \ \ \/_/_  / __`\  /'_` \/\ \ /' _ `\  /'_ `\\ \ \ \ \ \ \  /'__`\  /\ \/\ \  /',__\ 
#   \ \ \/\ \ \ \_/ \_/ \/\ \L\.\_/\ \L\ \ \ \L\ \/\ \L\ \/\ \L\ \ \ \/\ \/\ \/\ \L\ \\ \ \_/ \_\ \/\ \L\.\_\ \ \_\ \/\__, `\
#    \ \_\ \_\ \___x___/'\ \__/.\_\ \___,_\ \____/\ \____/\ \___,_\ \_\ \_\ \_\ \____ \\ `\___x___/\ \__/.\_\\/`____ \/\____/
#     \/_/\/_/\/__//__/   \/__/\/_/\/__,_ /\/___/  \/___/  \/__,_ /\/_/\/_/\/_/\/___L\ \'\/__//__/  \/__/\/_/ `/___/> \/___/ 
#                                                                                /\____/                         /\___/      
#                                                                                \_/__/                          \/__/       