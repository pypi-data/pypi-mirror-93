import re
from collections import OrderedDict

import regex
import random
from npf import npf
from npf.nic import NIC
from asteval import Interpreter
import itertools

import random

def is_numeric(s):
    try:
        val = float(s)
        return True
    except TypeError:
        return False
    except ValueError:
        return False

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        if val == 0: return False
        if val == 1: return True
        raise ValueError("Number %d is not a bool" % val)

    if val == "0" or val.lower() == "f" or val.lower() == "false":
        return False
    if val == "1" or val.lower() == "t" or val.lower() == "true":
        return True
    raise ValueError("%s is not a bool" % val)

def is_bool(s):
    try:
        get_bool(s)
        return True
    except ValueError:
        return False

def get_numeric(data):
    if is_numeric(data):
        v = float(data)
        if v.is_integer():
            v = int(v)
        return v
    else:
        return data

def numericable(l):
    for x in l:
        if not is_numeric(x):
            return False
    return True

def dtype(v):
    if is_numeric(v):
        if is_integer(v):
            return int
        else:
            return float
    else:
        return str

def is_log(l):
    if len(l) < 3:
        return False

    for i in range(len(l)):
        if not is_numeric(l[i]):
            return False
        l[i] = get_numeric(l[i])

    i = 0
    if l[0] == 0:
        if l[1] != 1:
            return False
        else:
            i = 1
    n = l[i+1] / l[i]
    i = i+1 #1
    c = l[i]
    i = i + 1 #2

    for i in range(i,len(l)):
        c = c * n
        if l[i] != c:
            return False
    return n


def ae_product_range(a,b):
    return itertools.product(range(a),range(b))

def ae_rand(a,b):
    return random.randint(a,b)

aeval = Interpreter(usersyms ={'parseBool':get_bool,"randint":ae_rand,"productrange":ae_product_range,"chain":itertools.chain})


def replace_variables(v: dict, content: str, self_role=None, self_node=None, default_role_map={}, role_index = 0):
    """
    Replace all variable and nics references in content
    This is done in two step : variables first, then NICs reference so variable can be used in NIC references
    :param v: Dictionary of variables
    :param content: Text to change
    :param self_role: Role of the caller, that self reference in nic will map to
    :return: The text with reference to variables and nics replaced
    """

    def do_replace(match):
        varname = match.group('varname_sp') if match.group('varname_sp') is not None else match.group('varname_in')
        if varname in v:
            val = v[varname]
            return str(val[0] if type(val) is tuple else val)
        return match.group(0)

    content = re.sub(
        Variable.VARIABLE_REGEX,
        do_replace, content)

    def do_replace_nics(nic_match):
        varRole = nic_match.group('role')

        nodes = npf.nodes_for_role(varRole, self_role, self_node, default_role_map)
        nodeidx = role_index % len(nodes)
        if nic_match.groupdict()['node']:
            t = str(nic_match.group('node'))
            if t == "node":
                return str(len(nodes))
            v = getattr(nodes[nodeidx], t)
            if v is None:
                if t == "multi":
                    return "1"
                else:
                    raise Exception("Unknown node variable %s" % t)
            else:
                return str(v)
        else:
            return str(nodes[nodeidx].get_nic(
            int(nic_match.group('nic_idx') if nic_match.group('nic_idx') else v[nic_match.group('nic_var')]))[
                       nic_match.group('type')])

    content = re.sub(
        Variable.VARIABLE_NICREF_REGEX,
        do_replace_nics, content)



    def do_replace_math(match):

        prefix = match.group('prefix')
        expr = match.group('expr').strip()
        expr = re.sub(
            Variable.VARIABLE_REGEX,
            do_replace, expr)
        if prefix:
            return "$((" + str(expr) + "))"
        else:
            return str(aeval(expr))

    content = re.sub(
        Variable.MATH_REGEX,
        do_replace_math, content)
    return content


class VariableFactory:
    @staticmethod
    def build(name, valuedata, vsection=None):
        result = re.match("\[(-?[0-9.]+)([+-]|[*]|[,])(-?[0-9.]+)([#][0-9.]+)?\]", valuedata)
        if result:
            return RangeVariable(name, result.group(1), result.group(3), result.group(2) == "*", (get_numeric(result.group(4)[1:]) if result.group(4) else None))

        result = regex.match("\{([^:]*:[^,:]+)(?:(?:,)([^,:]*:[^,:]+))*\}", valuedata)
        if result:
            return DictVariable(name, result.captures(1) + result.captures(2))

        result = regex.match("\{([^,]+)(?:(?:,)([^,]*))*}", valuedata)
        if result:
            return ListVariable(name, result.captures(1) + result.captures(2))

        result = regex.match("EXPAND\((.*)\)", valuedata)
        if result:
            return ExpandVariable(name, result.group(1), vsection)

        result = regex.match("RANDOM[ ]*\([ ]*([^,]+)[ ]*,[ ]*([^,]+)[ ]*\)", valuedata)
        if result:
            if vsection is None:
                raise Exception("RANDOM variable without vsection",vsection)
            return RandomVariable(name, vsection.replace_all(result.group(1))[0], vsection.replace_all(result.group(2))[0])

        result = regex.match("HEAD[ ]*\([ ]*([^,]+)[ ]*,[ ]*\$([^,]+)[ ]*(,[ ]*(?P<sep>.+)[ ]*)?\)", valuedata)
        if result:
            if vsection is None:
                raise Exception("HEAD variable without vsection",vsection)
            nums = vsection.replace_all(result.group(1))[0].strip()
            return HeadVariable(name, nums,
                                vsection.vlist[result.group(2)].makeValues(), result.group('sep'))
        result = regex.match("IF[ ]*\([ ]*([^,]+)[ ]*,[ ]*([^,]+)[ ]*,[ ]*([^,]+)[ ]*\)", valuedata)
        if result:
            if vsection is None:
                raise Exception("IF variable without vsection",vsection)
            return IfVariable(name, vsection.replace_all(result.group(1))[0], result.group(2), result.group(3))

        return SimpleVariable(name, valuedata)


# raise Exception("Unkown variable type : " + valuedata)

class Variable:
    def __init__(self):
        self.assign = '='
        self.is_default = False

    NAME_REGEX = r'[a-zA-Z0-9._-]+'
    TAGS_REGEX = r'[a-zA-Z0-9._,|!-]+'
    VALUE_REGEX = r'[a-zA-Z0-9._/,{}^$-]+'
    VARIABLE_REGEX = r'(?<!\\)[$](' \
                     r'[{](?P<varname_in>' + NAME_REGEX + ')[}]|' \
                     r'(?P<varname_sp>' + NAME_REGEX + ')(?=}|[^a-zA-Z0-9_]|$))'
    MATH_REGEX = r'(?P<prefix>\\)?[$][(][(](?P<expr>.*?)[)][)]'
    ALLOWED_NODE_VARS = 'path|user|addr|tags|nfs|arch|port'
    NICREF_REGEX = r'(?P<role>[a-z0-9]+)[:](:?(?P<nic_idx>[0-9]+)[:](?P<type>' + NIC.TYPES + '+)|(?P<node>'+ALLOWED_NODE_VARS+'|ip|multi|mode|node))'
    VARIABLE_NICREF_REGEX = r'(?<!\\)[$][{]' + NICREF_REGEX + '[}]'

# For each value N of nums, generate a variable with the first N element of values
class HeadVariable(Variable):
    def __init__(self, name, nums, values, join = None):
        self.values = values
        if not is_numeric(nums):
            raise Exception("%s is not a number!" % nums)
        self.nums = nums
        self.join = join if join else "\n"


    def makeValues(self):
        if self.nums == 0:
            return ['']
        vs = []
        i = int(self.nums)
        if type(i) is str:
            i = int(i.strip())
        vs.append((self.join.join(self.values[:i]), i))
        return vs

    def count(self):
        return sum(self.nums) if len(self.nums) > 0 else 1

    def format(self):
        return str

    def is_numeric(self):
        return False

class ExpandVariable(Variable):
    """ Create a list wihich expands a string with all possible value for the variable
        it contains like it would be in a script or file section"""
    def __init__(self, name, value, vsection):
        self.values = vsection.replace_all(value)

    def makeValues(self):
        return self.values

    def count(self):
        return len(self.values)

    def format(self):
        return str

    def is_numeric(self):
        return False

    def __add__(self, other):
        v = []
        for ov in other.makeValues():
            for mv in self.values:
                v.append(mv + ov)
        self.values = v
        return self

class SimpleVariable(Variable):
    def __init__(self, name, value):
        super().__init__()
        self.value = get_numeric(value)

    def makeValues(self):
        return [self.value]

    def count(self):
        return 1

    def format(self):
        return dtype(self.value)

    def is_numeric(self):
        return self.format() != str

    def __add__(self, other):
        self.value += other.makeValues()[0]
        return self

    def pop(self, item):
        if self.value == item:
            return ListVariable(None, [])
        else:
            return self


class ListVariable(Variable):
    def __init__(self, name, l):
        super().__init__()
        all_num = True
        for x in l:
            if not is_numeric(x):
                all_num = False
                break
        if all_num:
            self.lvalues = [int(x) if is_integer(x) else float(x) if is_numeric(x) else x for x in l]
        else:
            self.lvalues = [str(x) for x in l]
        self.all_num = all_num

    def __add__(self,other):
        self.lvalues.extend(other.lvalues)
        return self

    def makeValues(self):
        vs = []
        for v in self.lvalues:
            if (v is None):
                continue
            vs.append(v)
        return vs

    def count(self):
        return len(self.lvalues)

    def format(self):
        t = dtype(self.lvalues[0])
        if t is int and is_bool(self.lvalues[0]):
            unique = list(set(self.lvalues))
            if len(unique) == 2 and all([int(u) in (0, 1) for u in unique]):
                return bool
            elif len(unique) == 1 and (unique[0] == 'true' or unique[0] == 'false'):
                return bool
        return t

    def is_numeric(self):
        return self.all_num

    def pop(self, item):
        if item in self.lvalues:
            self.lvalues.remove(item)
        return self


class DictVariable(Variable):
    def __init__(self, name, data):
        super().__init__()
        if type(data) is dict:
            self.vdict = data
        else:
            self.vdict = OrderedDict()
            for g in data:
                d = g.split(':')
                self.vdict[d[0]] = d[1]

    def makeValues(self):
        return [(k, v) for k, v in self.vdict.items()]

    def count(self):
        return len(self.vdict)

    def format(self):
        k, v = next(self.vdict.items().__iter__())
        return dtype(v)

    def is_numeric(self):
        k, v = next(self.vdict.items().__iter__())
        return dtype(v) != str

    def __add__(self, other):
        self.vdict.update(other.vdict)
        return self

    def pop(self, item):
        if item in self.vdict:
            del self.vdict[item]
        return self

class RangeVariable(Variable):
    def __init__(self, name, valuestart, valueend, log, step = None):
        super().__init__()
        if is_integer(valuestart) and is_integer(valueend):
            valuestart=int(valuestart)
            valueend=int(valueend)
        else:
            valuestart=float(valuestart)
            valueend=float(valueend)
        if valuestart > valueend:
            self.a = valueend
            self.b = valuestart
        else:
            self.a = valuestart
            self.b = valueend
        self.log = log
        if step is None:
            if log:
                self.step = 2
            else:
                self.step = 1
        else:
            self.step = step

    def count(self):
        """todo: think"""
        if self.log:
            return len(self.makeValues())
        else:
            return int(((self.b-self.a) / self.step) + 1)


    def makeValues(self):
            vs = []
            i = self.a
            while i <= self.b:
                vs.append(i)
                if i == self.b:
                    break
                if i == 0 and self.log:
                    if self.b > 0:
                        i = 1
                    else:
                        i = -1
                else:
                    if self.log:
                        i *= self.step
                    else:
                        i += self.step
            if i > self.b:
                vs.append(self.b)
            return vs

    def format(self):
        return int

    def is_numeric(self):
        return True

class IfVariable(Variable):
    def __init__(self, name, cond, a, b):
        self.cond = cond
        self.a = a
        self.b = b

    def makeValues(self):
        vs = []
        if aeval(self.cond):
            return [self.a]
        else:
            return [self.b]

    def count(self):
        return 1

    def format(self):
        return str

    def is_numeric(self):
        return False

class RandomVariable(Variable):
    def __init__(self, name, a, b):
        self.a = int(a.strip())
        self.b = int(b.strip())

    def makeValues(self):
        return [random.randint(self.a, self.b)]


    def count(self):
        return 1

    def format(self):
        return int

    def is_numeric(self):
        return True
