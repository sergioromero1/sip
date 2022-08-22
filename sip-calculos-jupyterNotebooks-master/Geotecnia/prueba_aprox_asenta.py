import math

def ajustar_a_0005(s):
	s_cm = math.floor(s * 100) / 100
	s_resto = s - s_cm
	if round(s_resto,3) < 0.005:
		return s_cm
	elif s_resto < 0.007:
		return s_cm + 0.005
	else:
		return s_cm + 0.01



test = [0.047, 0.328, 0.991, 4.0749999]
print([ajustar_a_0005(t) for t in test])