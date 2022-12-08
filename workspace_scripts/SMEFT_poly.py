## NOTE: this si a simple copy of the same function in HEFT_poly, consider moving to a single place

# the coupling part of the polynomial
ci_func_vector = [
    '1',
    '{cdp}*{cdp}',
    '{cdp}',
    '{cdp}*{cp}',
    '{cp}',
    '{cp}*{cp}',
    '{ctp}*{ctp}',
    '{ctp}',
    '{ctp}*{ctG}',
    '{ctG} ',
    '{ctG}*{ctG}',
    '{cdp}*{ctG}',
    '{ctG}*{cp}',
    '{cdp}*{ctp}',
    '{ctp}*{cp}',
    '{cpg}',
    '{cpg}*{cpg}',
    '{cpg}*{cdp}',
    '{cpg}*{cp}',
    '{cpg}*{ctp}',
    '{cpg}*{ctG}',
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
]

# the poly expression, with placeholders for POIs and Ai names
poly_parts  = ['{}*{}'.format(c, e) for c,e in zip(coeffs_vector, ci_func_vector)]
poly_form   = ' +'.join(poly_parts)


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