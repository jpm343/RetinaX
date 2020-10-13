import SACnetwork
import iodef as io


ginit = SACnetwork.gabaInit(SACnetwork.excGmin)
print "Saving initial GABA parameters to json file"
io.save_gabaInit_file(ginit, SACnetwork.all_params, './gabaInit.json')
