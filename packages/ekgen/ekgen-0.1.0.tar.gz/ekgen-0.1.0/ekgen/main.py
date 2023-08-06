from fortlab import Fortlab

from ekgen.mpasocn import MPASOcnKernel

class E3SMKGen(Fortlab):

    _name_ = "ekgen"
    _version_ = "0.1.0"
    _description_ = "Microapp E3SM Fortran Kernel Generator"
    _long_description_ = "Microapp E3SM Fortran Kernel Generator"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/ekgen"
    _builtin_apps_ = [MPASOcnKernel]

    def __init__(self):
        pass
