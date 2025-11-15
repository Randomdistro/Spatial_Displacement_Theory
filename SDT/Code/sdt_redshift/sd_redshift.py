import sdt_redshift as sdt

# Initialize with local Hubble flow
calculator = sdt.RedshiftCalculator(H0=70.0)  # km/s/Mpc

# Get luminosity distance
z = 1.5
D_L = calculator.luminosity_distance(z)  # Returns Mpc

# Get angular diameter distance  
D_A = calculator.angular_diameter_distance(z)

# Get lookback time
t_lookback = calculator.lookback_time(z)  # Returns Gyr

# Batch processing
z_array = np.array([0.5, 1.0, 1.5, 2.0])
D_L_array = calculator.luminosity_distance(z_array)