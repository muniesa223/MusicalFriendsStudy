from pack.Artist import Artist 
from pack.addUsers import addUsers    
from pack.addUsers2 import addUsers2
from pack.jaccardSim import jaccardSim

user=""
users= addUsers2()
data=users.main()
jacSim=jaccardSim(data)
jacSim.main()