#!/usr/bin/python
import sys, os, time
#sys.path.add(os.realpath(".."))

#import pymclevel
try:
    from pymclevel import mclevel
    err=False
except ImportError:
    err=True
if err:
    try:
        import mclevel
        err=False
    except ImportError:
        err=True
if err:
    print "this script requires pymclevel to be on the pythonpath."
    print "get it from https://github.com/codewarrior0/pymclevel"
    print "or use one of these:"
    print "$ wget --no-check-certificate https://github.com/codewarrior0/pymclevel/tarball/master && tar -xf codewarrior0-pymclevel-*.tar.gz"
    print "$ git clone https://github.com/codewarrior0/pymclevel.git"
    sys.exit(1)
    
#get the world and a chunk set
print "# loading world (%d)" % time.time()
world = mclevel.fromFile("world_modif")
print "# loading chunks (%d)" % time.time()
chunkPositions = set(world.allChunks)
print "## logging found chunks to file cbr_chunks"
writer = open("cbr_chunks","wb")
writer.write(repr(chunkPositions))
writer.close()

def vadd(vec1, vec2):
    if len(vec1) != len(vec2):
        raise Exception("mismatched lengths")
    return tuple([vec1[i]+vec2[i] for i in range(len(vec1))])
    
#offset definitions
square=((1,0),(-1,0),(0,1),(0,-1))
square3=[(15,16,0,16,0,128), (0,1,0,16,0,128), (0,16,15,16,0,128), (0,16,0,1,0,128)]
print "# finding chunk edges (%d)" % time.time()
#find the edges
allwalls = [(c,tuple([(vadd(c, ofs) not in chunkPositions) for ofs in square])) for c in chunkPositions]
walls=[x for x in allwalls if sum(x[1]) > 0]

print "## logging found edges to file cbr_edges"
writer = open("cbr_edges","wb")
writer.write(repr(walls))
writer.close()

print "# adding bedrock to edges (%d)" % time.time()

count = 0
#add bedrock to the edges
for wall in walls:
    c = world.getChunk(wall[0][0], wall[0][1])
    for num in range(4):
        if wall[1][num]:
            i=square3[num]
            c.Blocks[i[0]:i[1],i[2]:i[3],i[4]:i[5]] = 7
    c.chunkChanged()
    time.sleep(0.005)
    if count%30 == 29:
        world.saveInPlace()
world.saveInPlace()
print "# done (%d)" % time.time()
