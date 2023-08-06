# /usr/bin/python3
####### PACKAGES
from . import anutils as an
import sio_tools as sio
import numpy as np

# Check if we can plot stuff
__IPV__ = False
try:
    import ipyvolume as ipv
    __IPV__ = True
except:
    print("Unable to import Ipyvolume")

# a generic class for an object set
class Object_set(list):
    """ Object_set
        A class that contains a list of objects plus extra methods and properties
        
    """
    def __init__(self, *args, id=1,
                 config=None, name=None,  build=None, type=None, **kwargs):
        list.__init__(self)

        # Filling info
        self.name = name
        self.id = id
        self.type = type

        # Reading properties
        self.properties = an.get_prop_dicts(config, type=type, name=name)

        # We allow a custom constructor
        if build is not None:
            build(self, *args, **kwargs)
        else:
            self.build_objects(*args, **kwargs)

    # Stupid builder
    def build_objects(self, *args, **kwargs):
        self.append(Object(None))

    # Generic analyzer
    def analyze(self, obj, analyzer=None, *args, **kwargs):
        #analysis = {'id' : obj.id}
        analysis = {}
        if analyzer is not None:
            for name, func in analyzer.items():
                analysis[name] = func(obj)

        return analysis

    #def show(self):
    #    return None


    def show(self,*args, sorter=None, plotter=None, **kwargs):
        if __IPV__:
            if sorter is not None:
                objs = filter(sorter, self)
            else:
                objs = self

            #print("Showing %s objects %s" %(len(objs),self.name))

            if plotter is not None:
                return plotter(objs, *args, **kwargs)
            else:
                return self.plot_objs(objs, *args, **kwargs)
        else:
            return False

    def plot_objs(self, objs, *args, **kwargs):
        try:
            positions=np.array([obj.position for obj in objs])
            ipv.scatter(positions[:,0], positions[:,1], positions[:,2], **kwargs)
            return True
        except:
            sio.custom_warn("Did not manage to plot objects %s. Maybe object.position is not defined" %self.name)
        return False



# A class to contain a single object :
class Object():
    """ Object
        Generic object, not completely useless
        Most objects need id and position
        """

    def __init__(self, *args,  id=1, position=None, **kwargs):
        self.id = id
        self.position = position
