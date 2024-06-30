def calc_pnl(ppl: float, ps: float,  pt: float, pg: float, correct: bool) -> float:
    """
    Arguments:
        ps: p(slip) = p(obst=0 | l_t = 1)

    Returns:
        npl: new P(L)
    """
    if correct:
        cpl = (ppl * (1 - ps)) / (ppl * (1 - ps) +
                                  (1 - ppl) * pg)  # conditional P(L|obs)
        pass
    else:

        cpl = (ppl * ps) / (ppl * ps + (1 - ppl) * (1 - pg))

    npl = cpl + (1 - cpl) * pt

    return npl
