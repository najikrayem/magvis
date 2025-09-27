
from decimal import Decimal, getcontext, ROUND_HALF_UP
import matplotlib.pyplot as plt

# Set the precision
getcontext().prec = 64

PI = Decimal('3.14159265358979323846264338327950')

# Free space permeability
MU = Decimal('4') * Decimal(PI) * Decimal('10')**Decimal('-7')

# copper resistivity
RHO = Decimal('1.68') * Decimal('10')**Decimal('-8')


def circle_area(r):
    """
    Returns the area of a circle with radius r
    """
    r = Decimal(r)
    return PI * r**2

    
def awg_to_d_mm(awg):
    """
    Takes an American Wire Gauge (AWG) value and returns the diameter of the wire in millimeters.
    """
    # Constants
    factor = Decimal('0.005')  # inch
    exponential_base = Decimal('92')
    numerator = Decimal('36') - Decimal(awg)
    denominator = Decimal('39')
    inch_to_mm = Decimal('25.4')

    # Calculate diameter in inches
    diameter_inches = factor * (exponential_base ** (numerator / denominator))
    
    # Convert diameter to millimeters
    return diameter_inches * inch_to_mm
    

def awg_to_area(awg):
    """
    Takes an American Wire Gauge (AWG) value and returns the cross-sectional
    area of the wire in square meters.
    """
    diameter_mm = awg_to_d_mm(awg)
    
    diameter_m = diameter_mm * Decimal('10')**Decimal('-3')
    radius_m = diameter_m / Decimal('2')

    return circle_area(radius_m)


def coplanar_teslas(n, I, R, r):
    """
    Returns the magnetic field strength in Teslas at a distance r (meters) from the center of a
    coil with n turns, carrying a current I(amps), and with a radius R(meters).

    B_z = (MU * n * I * R^2) / (2 * (R^2 + r^2)^(3/2))
    """
    n = Decimal(n)
    I = Decimal(I)
    R = Decimal(R)
    r = Decimal(r)
    
    return (MU * n * I * R**2) / (2 * (R**2 + r**2)**Decimal('1.5'))
    


def coil_inductance(n, R, l):
    """
    Inductance of a solenoid with n turns, radius R meters, and length l meters.
    
    L = MU * n^2 * A / l
    """

    n = Decimal(n)
    R = Decimal(R)
    l = Decimal(l)
    
    return MU * n**2 * (circle_area(R) / l)
    


def wire_resistance(p, g, l):
    """
    Calculate wire resistance given copper resistivity p, wire length l in meters
    and wire gauge g in american wire gauge unit.

    R = p * l / A
    """

    p = Decimal(p)
    g = Decimal(g)
    l = Decimal(l)
    
    # Calculate the cross-sectional area of the wire
    A = awg_to_area(g)

    # Calculate the resistance
    return p * l / A




def coil_reactance(f, L):
    """
    Calculate coil reactance given frequency f, and inductance L
    """

    f = Decimal(f)
    L = Decimal(L)
    
    return (Decimal('2') * PI * f * L)
    



def time_constant(R, L):
    """
    calculate the time constant given resistance R and inductance L
    
    tau = L / R
    """

    R = Decimal(R)
    L = Decimal(L)
    
    return L / R



def joule_loss(I, R):
    """
    Calculate the joule heating loss in watts given current I and resistance R

    P = I^2 * R
    """
    
    I = Decimal(I)
    R = Decimal(R)
    
    return (I**2) * R



def heat_dissipation(P, h, A):
    """
    Calculate heat dissipation in celcius given P power dissipation in watts, 
    heat transfer coefficient h, and A, the external surface area of the solenoid
    available for heat dissipation (if this is an air core solenoid, A can be approximated
    as the external surface area of the coil times 2).
    """
        
    P = Decimal(P)
    h = Decimal(h)
    A = Decimal(A)
    
    return P / (h * A)



# num coils
num_coils = Decimal('6')

# Target Bz in Teslas
Bz_target = Decimal('0.000005') / num_coils

# Target I in amps
I_target = Decimal('2.5') / num_coils

# Target coil radius in meters
R_target = Decimal('0.23')

# Target distance from the center of the coil in meters
r_target = Decimal('0.01')

# Target solenoid length in meters
l_target = Decimal('0.03') / num_coils

# Target gauge in AWG
awg_target = '32'

# For the magnet i am building I using the following values:
# Bz = 0.00003
# I = 4
# R = 0.23
# r = 0.60
# l = 0.03
# awg = 22 


print(f"wire cross sectional area is {awg_to_area(awg_target)}")





#--------------------------------------------------------------


# find the number of turns required to achieve the target
n = Decimal('1')
n = Decimal('32')

# while True:
#     Bz = coplanar_teslas(n, I_target, R_target, r_target)
    
#     if Bz > Bz_target:
#         break
    
#     n += Decimal('1')

Bz = coplanar_teslas(n, I_target, R_target, r_target)
print(f'Bz: {Bz * Decimal("1000000")} uT, and {Bz * Decimal("1000000") * num_coils} uT for all coils')

print(f'Number of turns required: {n}')



# estimate wire length
wire_length = Decimal('2') * PI * R_target * n  # estimate wire length in meters
print(f'Wire length: {wire_length.quantize(Decimal("1.00"))} meters, {(wire_length * Decimal("3.280839895")).quantize(Decimal("1.00"))} feet')

#--------------------------------------------------------------

# find critical frequency
L = coil_inductance(n, R_target, l_target)  # estimate inductance, with 

resistance = wire_resistance(RHO, awg_target, wire_length) # estimate resistance

time_const = time_constant(resistance, L)   # estimate time constant

print(f'Resistance: {resistance.quantize(Decimal("1.00"))}')
print(f'Inductance: {L.quantize(Decimal("1.000"))}')

print(f'Time constant: {time_const.quantize(Decimal("1.000"))}')

# change the 5 to 1.54 when done with plane stuff
print(f'Critical frequency: {(Decimal(1) / (Decimal(1.54) * time_const)).quantize(Decimal("1"))}')

#-----------------------------------------------------------------------------------------
# Check if wire temperature will exceed 100 degrees celcius.
# Assume conservative heat transfer coefficient of 200 W/m^2K.
assumed_h = Decimal('200')

# Estimate the surface area of the solenoid using the formula for a cylinder's lateral
# surface area: pi * d * l where d is the diameter of the coil and l is the length of the coil.
# Since the coil is air core, we can approximate the surface area as the external surface 
# area of the coil times 2.
est_surface_area = Decimal('2') * PI * (R_target * Decimal('2')) * l_target

# Assume an ambient starting temperature of 25 degrees celcius
T0 = Decimal('25')

# Estimate the power dissipation in the coil
P = joule_loss(I_target, resistance)

# Estimate the temperature rise
T = heat_dissipation(P, assumed_h, est_surface_area)

# estimate the final temperature
T_final = T0 + T

print(f'Estimated temperature rise: {T.quantize(Decimal("1.00"))} degrees celcius')
print(f'Estimated final temperature: {T_final.quantize(Decimal("1.00"))} degrees celcius')

#-----------------------------------------------------------------------------------------


# calculate the needed voltage to achieve the target current
V = I_target * resistance
print(f'Voltage required to achieve target current: {V.quantize(Decimal("1.00"))} volts')

# given voltage, calculate how much current will flow
I = Decimal(12) / resistance
print(f'Current that will flow with 12 volts: {I.quantize(Decimal("1.00"))} amps with resistance {resistance.quantize(Decimal("1.00"))} ohms')