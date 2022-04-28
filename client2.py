import socket, select, string, sys
from functools import wraps
import random,sympy

global PR
global G
PR = 0
G = 0
def generatePrimeRandom():
    minPrime = 1000
    maxPrime = 4000
    cached_primes = [i for i in range(minPrime,maxPrime) if sympy.isprime(i)]
    n = random.choice([i for i in cached_primes if 1000<i<4000])
    return n

def cache_gcd(f):
    cache = {}

    @wraps(f)
    def wrapped(a, b):
        key = (a, b)
        try:
            result = cache[key]
        except KeyError:
            result = cache[key] = f(a, b)
        return result
    return wrapped

@cache_gcd
def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a


def generateRandomPR(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
    pr = [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)for powers in range(1, modulo)}]
    x = random.randint(0,len(pr))
    return pr[x]

def sendInit():
    global PR
    global G
    primeNumber = generatePrimeRandom()
    pr = generateRandomPR(primeNumber)
    PR = primeNumber
    G = pr
    msg = "I,{},{}".format(primeNumber,pr)
    return msg
    # s.send(msg.encode())

def display() :
	you="\33[33m\33[1m"+" You: "+"\33[0m"
	sys.stdout.write(you)
	sys.stdout.flush()



def main():
    global PR
    global G
    if len(sys.argv)<2:
        host = input("Enter host ip address: ")
    else:
        host = sys.argv[1]
    # print(len(sys.argv))
    # assert len(sys.argv)<3,"masukan nama a/b"
    name = str(sys.argv[2])
    # assert name=="a" or name=="b", "Nama yang anda masukan salah"
    # assert len(sys.argv<4),"masukan private number"
    pn = int(sys.argv[3])




    port = 5006
    # name = "Bob"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connecting host
    try :
        s.connect((host, port))
    except :
        print("\33[31m\33[1m Can't connect to the server \33[0m")
        sys.exit()

    #if connected
    s.send(name.encode())
    if(name == "a"):
        print("masuk alice")
        s.send(sendInit().encode())
    print("Connected")
    # display()
    # sys.stdout.write("Connected")
    while 1:
        try:
            socket_list = [sys.stdin, s]
            
            # Get the list of sockets which are readable
            rList, wList, error_list = select.select(socket_list , [], [])
            
            for sock in rList:
                #incoming message from server
                if sock == s:
                    data = sock.recv(4096)
                    if not data :
                        pass
                        # print('\33[31m\33[1m \rDISCONNECTED!!\n \33[0m')
                        # sys.exit()
                    else :
                        pesanTerima = data.decode()
                        if name == "b":
                            pesan = pesanTerima.split(",")
                            print(pesan)
                            if len(pesan) == 3 and pesan[0] =="I":
                                val = pow(int(pesan[2],pn,pesan[1]))
                                PR = int(pesan[1])
                                G = int(pesan[0])
                                msg = "B,{}".format(val)
                                s.send(msg.encode())
                            if len(pesan) == 2 and pesan[0] == "A":
                                val = pow(int(pesan[1]),pn,PR)
                                print("akhir: {}".format(val))
                                # sys.stdout.write("{}".format(val))
                        if name == "a":
                            pesan = pesanTerima.split(",")
                            if len(pesan) == 2 and pesan[0] == "B":
                                val = pow(G,pn,PR)  
                                msg = "A,{}".format(val)
                                s.send(msg.encode())
                                val = pow(int(pesan[1]),pn,PR)
                                print("akhir: {}".format(val))
                                # sys.stdout.write("{}".format(val))
                        
                        # display()
            
                #user entered a message
                else :
                    msg=sys.stdin.readline()
                    if name == "a" and msg.strip("\n") == "p":
                        s.send(sendInit().encode())
                    # else:
                    #     val = pow(G,pn,PR)
                    #     msg = "A,{}".format(val)
                    #     s.send(msg.encode())
                    #     sys.stdout.write(""
        except KeyboardInterrupt:
            msg = "bye"
            s.send(msg.encode())
            sys.exit()

if __name__ == "__main__":
    main()
