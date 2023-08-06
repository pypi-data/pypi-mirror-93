"""   Functionalities related to the navigation of hdf5 type files
"""
import h5py
import numpy as np
import yaml
import hdfdict

__all__ = ["get_h5_structure", "print_h5_structure","get_h5_field"]


def get_h5_structure(h5_filename):
    """ Show hdf5 file components

        Input:
            :h5_filename: path to hdf5 file to inspect
    """
    with h5py.File(h5_filename, "r") as node:
        out = log_hdf_node(node)
    return out


def print_h5_structure(h5_filename):
    """ Show hdf5 file components

        Input:
            :h5_filename: path to hdf5 file to inspect
        Output:
            Print to terminal
    """
    if isinstance(h5_filename,str):
        dict_ = get_h5_structure(h5_filename)
    else:
        dict_ = h5_filename
        # does weird stuff if dict_ contains data.
        # Must be a structure dictionary
    print(yaml.dump(dict_, default_flow_style=False))


def get_h5_field(h5_filename):
    """ Return a dictionary of an hdf5 file, e.g. a
        flow field or mesh file.

        Input:
            :h5_filename: path to the file to be read in
        Output:
            :out_: field dictionary
    """
    with h5py.File(h5_filename, "r") as h5pf:
        out_ = hdfdict.load(h5pf, lazy=False)
    return out_


def log_hdf_node(node):
    """
    Build a dictionnary with the structure of a HDF5 node

    Parameters:
    -----------
    node : hdf5 node

    Returns:
    --------
    a dictionnary
    """
    out = dict()


    def extend_dict(dict_, address, attr):
        tmp = dict_
        #print(attr)
        #!! Needs to be adapted for a multi-level nested object!!
        # Single level works fine, because we currently add attr to each level
        #  of the address, should be on the last level only -> 2 loops?
        for key in address[:]:
            if key not in tmp:
                #tmp[key] = dict()
                #print("Items current key and last key:", key, address[-1])
                if key == address[-1]:
                    #print("Last key", tmp)
                    tmp[key] = attr.copy()
                else:
                    tmp[key] = {}
            #print(tmp)
            tmp = tmp[key] # so we redefine the dict to continue through

    def visitor_func(name, node):
        key_list = [item.strip() for item in name.split('/')]
        #print(key_list)
        if isinstance(node, h5py.Dataset):
            #print("Create dict with dtype and value")
            attr = dict()
            attr["dtype"] = str(node.dtype)
            attr["value"] = _get_node_description(node)
            #print(out)
            extend_dict(out, key_list, attr)
            #print(out)
        else:
            pass

    node.visititems(visitor_func)

    return out

def _ascii2string(ascii_list):
    """ Ascii to string conversion

        Parameters:
        -----------
        ascii_list : a list of string to be converted

        Returns:
        --------
        a string joining the list elements

    """
    return ''.join(chr(i) for i in ascii_list[:-1])


def _get_node_description(node):
    """Get number of elements in an array or
      value of a single-valued node.

    Parameters:
    -----------
    node : hdf5 node

    Returns:
    --------
    a value with a Python format
    None if data is not a singlevalued quantity
    """
    out = None
    value = node[()]
    shape = node.shape
    #print(node)
    #print(shape)
    if np.prod(shape) == 1:
        # this is a strong assumption because if you find int8
        # your are probably looking at an hdf5 file applying the cgns standard
        #print(node)
        if node.dtype in ["int8"]:
            #print(_ascii2string(value))
            out = np.char.array(_ascii2string(value))[0]
        elif shape in [(1), (1,)]:
            if node.dtype in ["int32", "int64"]:
                out = int(value[0])
            elif node.dtype in ["float32", "float64"]:
                out = float(value[0])
            #else:
            #    raise RuntimeError()
        # else:
        #     raise RuntimeError()
    else:
        out = "array of %s elements" %(" x ".join([str(k) for k in shape]))
    return out
