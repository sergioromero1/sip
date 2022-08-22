from scipy import interpolate

def q_s_suelos_cohesivos(proc_iny, q_u):
    if proc_iny == "IGU":
        igu_q_us = [54,100,443,600]
        igu_q_ss = [47,72,200,200]
        f = interpolate.interp1d(igu_q_us, igu_q_ss, kind="linear",fill_value="extrapolate")
        return float(f(q_u))
    elif proc_iny == "IRS":
        irs_q_us = [44.5,100,365,600]
        irs_q_ss = [116,200,400,400]
        f = interpolate.interp1d(irs_q_us, irs_q_ss, kind="linear",fill_value="extrapolate")
        return float(f(q_u))
    else:
        raise  ValueError(f"Proceso de inyección desconocido: {proc_iny}")

def q_s_suelos_granulares(proc_iny, N):
    if proc_iny == "IGU":
        igu_Ns = [9,67.6,150]
        igu_q_ss = [40,400,400]
        f = interpolate.interp1d(igu_Ns, igu_q_ss, kind="linear",fill_value="extrapolate")
        return float(f(N))
    elif proc_iny == "IRS":
        irs_Ns = [9,55,150]
        irs_q_ss = [135.5,631,631]
        f = interpolate.interp1d(irs_Ns, irs_q_ss, kind="linear",fill_value="extrapolate")
        return float(f(N))
    else:
        raise  ValueError(f"Proceso de inyección desconocido: {proc_iny}")    