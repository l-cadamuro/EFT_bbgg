# parameters and functions to access HEFT parametrizations

# the coupling part of the polynomial
ci_func_vector = [
    '{ctth}*{ctth}*{ctth}*{ctth}',
    '{ctthh}*{ctthh}',
    '{ctth}*{ctth}*{chhh}*{chhh}',
    '{cggh}*{cggh}*{chhh}*{chhh}',
    '{cgghh}*{cgghh}',
    '{ctthh}*{ctth}*{ctth}',
    '{ctth}*{chhh}*{ctth}*{ctth}',
    '{ctth}*{chhh}*{ctthh}',
    '{cggh}*{chhh}*{ctthh}',
    '{ctthh}*{cgghh} ',
    '{cggh}*{chhh}*{ctth}*{ctth}',
    '{cgghh}*{ctth}*{ctth}',
    '{chhh}*{cggh}*{ctth}*{chhh}',
    '{cgghh} *{ctth}*{chhh}',
    '{cggh}*{cgghh}*{chhh}',
    '{cggh}*{ctth}*{ctth}*{ctth}',
    '{ctthh}*{ctth}*{cggh}',
    '{ctth}*{chhh}*{cggh}*{cggh}',
    '{ctth}*{cggh}*{cgghh}',
    '{ctth}*{ctth}*{cggh}*{cggh}',
    '{ctthh}*{cggh}*{cggh}',
    '{chhh}*{cggh}*{cggh}*{cggh}',
    '{cgghh}*{cggh}*{cggh}',
]

# the coefficients of the polynomial
coeffs_vector = [
    '{A1}',
    '{A2}',
    '{A3}',
    '{A4}',
    '{A5}',
    '{A6}',
    '{A7}',
    '{A8}',
    '{A9}',
    '{A10}',
    '{A11}',
    '{A12}',
    '{A13}',
    '{A14}',
    '{A15}',
    '{A16}',
    '{A17}',
    '{A18}',
    '{A19}',
    '{A20}',
    '{A21}',
    '{A22}',
    '{A23}',
]

# the poly expression, with placeholders for POIs and Ai names
poly_parts  = ['{}*{}'.format(c, e) for c,e in zip(coeffs_vector, ci_func_vector)]
poly_form   = ' +'.join(poly_parts)

# same as above, but with multiplications grouped - just for numerical cross checks
poly_form_grouped = (
"{A1}*{ctth}*{ctth}*{ctth}*{ctth} +"
"{A2}*{ctthh}*{ctthh} +"
"({A3}*{ctth}*{ctth} + {A4}*{cggh}*{cggh})*{chhh}*{chhh} +"
"{A5}*{cgghh}*{cgghh} +"
"({A6}*{ctthh} + {A7}*{ctth}*{chhh})*{ctth}*{ctth} +"
"({A8}*{ctth}*{chhh} + {A9}*{cggh}*{chhh})*{ctthh} +"
"{A10}*{ctthh}*{cgghh} +"
"({A11}*{cggh}*{chhh} + {A12}*{cgghh})*{ctth}*{ctth} +"
"({A13}*{chhh}*{cggh} + {A14}*{cgghh})*{ctth}*{chhh} +"
"{A15}*{cggh}*{cgghh}*{chhh} +"
"{A16}*{cggh}*{ctth}*{ctth}*{ctth} +"
"{A17}*{ctthh}*{ctth}*{cggh} +"
"{A18}*{ctth}*{chhh}*{cggh}*{cggh} +"
"{A19}*{ctth}*{cggh}*{cgghh} +"
"{A20}*{ctth}*{ctth}*{cggh}*{cggh} +"
"{A21}*{ctthh}*{cggh}*{cggh} +"
"{A22}*{chhh}*{cggh}*{cggh}*{cggh} +"
"{A23}*{cgghh}*{cggh}*{cggh}"
)

def read_coeffs_ATLAS(fname, nAi):
    """ read the coefficients in the ATLAS format 
        Returns them as a vector coeffs[i_mHHbin][icoeff]
    """
    fIn = open(fname, 'r')
    bins = []
    data = []
    for l in fIn:
        l = l.strip()
        if not l:
            continue
        tokens = l.split()
        tokens = [float(i) for i in tokens]
        if len(tokens) == nAi + 1: ## coeffs + mHH bin center
            # data.append(tokens)
            bins.append(tokens[0])
            data.append(tokens[1:])
        elif len(tokens) == nAi: ## the last line has a different format
            # data.append([999999,] + tokens)
            bins.append(999999,)
            data.append(tokens)

        else:
            raise RuntimeError("Cannot parse coefficients")
    last_line = data[-1]
    bins = bins[:-1]
    data = data[:-1]
    return bins, data, last_line