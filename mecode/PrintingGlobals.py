from mecode import G

Aerotech = True

g=G()
def init_G(strFile):
    print "Initializing G..."
    global g
    g = G(
        print_lines=False,
        outfile=strFile,
        aerotech_include=False,
    )
    return g


