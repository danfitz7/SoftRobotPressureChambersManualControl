from mecode import G

g=G()
def init_G(strFile):
    print "Initializing G..."
    global g
    g = G(
        print_lines=False,
        outfile=strFile,
        aerotech_include=False,
    )


