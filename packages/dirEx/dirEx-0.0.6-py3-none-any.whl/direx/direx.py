def _get_dir_list(obj=None):
    """
    dir([object]) -> list of strings

    If called without an argument, return the names in the current scope.
    Else, return an alphabetized list of names comprising (some of) the attributes
    of the given object, and of attributes reachable from it.
    If the object supplies a method named __dir__, it will be used; otherwise
    the default dir() logic is used and returns:
      for a module object: the module's attributes.
      for a class object:  its attributes, and recursively the attributes
        of its bases.
      for any other object: its attributes, its class's attributes, and
        recursively the attributes of its class's base classes.
    """
    list_attributes = dir(obj)
    return list_attributes


class CellType:
    MOD = "module"
    FUN = "function"


def _show_cell_info(name, content):
    print("[%s]" % name)
    print(content.__doc__)
    print()
    print()


def show_dir_info(obj=None, ctype=None):
    if obj is None:
        return
    for cell in _get_dir_list(obj):
        # cobj = re.__dict__[cell]
        cobj = getattr(obj, cell)

        if ctype is None:
            _show_cell_info(cell, cobj)
        elif ctype in str(type(cobj)):
            _show_cell_info(cell, cobj)


def show_dir_method(obj):
    show_dir_info(obj, CellType.FUN)


def show_dir_module(obj):
    show_dir_info(obj, CellType.MOD)
