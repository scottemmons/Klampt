from ..model.contact import ContactPoint
from ..model.contact import Hold
from ..robotsim import WorldModel,RobotModelLink,RigidObjectModel,IKObjective

def objectToTypes(object,world=None):
    """Returns names of all possible types that could be associated with the given
    Python Klamp't object."""
    if hasattr(object,'type'):
        return object.type
    if isinstance(object,ContactPoint):
        return 'ContactPoint'
    elif isinstance(object,Hold):
        return 'Hold'
    elif isinstance(object,IKObjective):
        return 'IKGoal'
    elif hasattr(object,'__iter__'):
        if hasattr(object[0],'__iter__'):
            #list of lists or tuples
            if len(object)==2:
                if len(object[0])==9 and len(object[1])==3:
                    #se3
                    return 'RigidTransform'
            return 'Configs'
        else:
            dtypes = []
            if any(isinstance(v,int) for v in object):
                dtypes.append('int')
            if any(isinstance(v,float) for v in object):
                dtypes.append('float')
            if any(isinstance(v,str) for v in object):
                dtypes.append('str')
            vtypes = []
            if not str in dtypes:
                vtypes.append('Config')
                if not float in dtypes:
                    vtypes.append('IntArray')
                if len(object)==2:
                    #2d point
                    vtypes.append('Vector2')
                elif len(object)==3:
                    #3d point
                    vtypes.append('Vector3')
                elif len(object)==9:
                    #so3 or 9d point?
                    vtypes.append('Matrix3')
            else:
                vtypes.append("StringArray")
            if len(vtypes)==1:
                return vtypes[0]
            return vtypes
    else:
        raise ValueError("Unknown object passed to objectToTypes")
