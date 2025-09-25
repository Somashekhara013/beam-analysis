# ----------------- USER INPUT -----------------
L = float(input("Enter the length of the beam (m): "))

# Point loads
P = []
a = []
n_point_loads = int(input("Enter the number of point loads: "))
for i in range(n_point_loads):
    P.append(float(input(f"Enter point load {i+1} (kN): ")))
    a.append(float(input(f"Enter distance of point load {i+1} from support A (m): ")))

# UDLs
w = []
w_length = []
w_start = []
n_udls = int(input("Enter the number of UDLs: "))
for i in range(n_udls):
    w.append(float(input(f"Enter UDL {i+1} intensity (kN/m): ")))
    w_length.append(float(input(f"Enter length of UDL {i+1} (m): ")))
    w_start.append(float(input(f"Enter start position of UDL {i+1} from support A (m): ")))

# UVLs
w_max = []
w_max_length = []
w_max_start = []
n_uvls = int(input("Enter the number of UVLs: "))
for i in range(n_uvls):
    w_max.append(float(input(f"Enter UVL {i+1} maximum intensity (kN/m): ")))
    w_max_length.append(float(input(f"Enter length of UVL {i+1} (m): ")))
    w_max_start.append(float(input(f"Enter start position of UVL {i+1} from support A (m): ")))

# Point moments
M = []
m_pos = []
n_moments = int(input("Enter the number of point moments: "))
for i in range(n_moments):
    M.append(float(input(f"Enter point moment {i+1} (kNm): ")))
    m_pos.append(float(input(f"Enter position of point moment {i+1} from support A (m): ")))

# ----------------- CALCULATE REACTIONS -----------------
total_load = 0
moment_about_A = 0

# Point loads
for i in range(len(P)):
    total_load += P[i]
    moment_about_A += P[i] * a[i]

# UDLs
for i in range(len(w)):
    total_load += w[i] * w_length[i]
    moment_about_A += w[i] * w_length[i] * (w_start[i] + w_length[i] / 2)

# UVLs
for i in range(len(w_max)):
    total_load += 0.5 * w_max[i] * w_max_length[i]
    moment_about_A += 0.5 * w_max[i] * w_max_length[i] * (w_max_start[i] + (2/3.0) * w_max_length[i])

# Point moments
for i in range(len(M)):
    moment_about_A += M[i]

RB = moment_about_A / L
RA = total_load - RB

print("\nSupport Reactions:")
print(f"Reaction at A (RA): {RA:.2f} kN")
print(f"Reaction at B (RB): {RB:.2f} kN")

# ----------------- SHEAR FORCE & BENDING MOMENT -----------------
x = []
shear_force = []
bending_moment = []

for i in range(int(L * 10 + 1)):  # step = 0.1 m
    current_x = i / 10.0
    x.append(current_x)

    current_shear_force = RA
    current_bending_moment = RA * current_x

    # Point loads
    for j in range(len(P)):
        if current_x > a[j]:
            current_shear_force -= P[j]
            current_bending_moment -= P[j] * (current_x - a[j])

    # UDLs
    for j in range(len(w)):
        if current_x > w_start[j] and current_x < w_start[j] + w_length[j]:
            current_shear_force -= w[j] * (current_x - w_start[j])
            current_bending_moment -= 0.5 * w[j] * (current_x - w_start[j]) ** 2
        elif current_x >= w_start[j] + w_length[j]:
            current_shear_force -= w[j] * w_length[j]
            current_bending_moment -= w[j] * w_length[j] * (current_x - w_start[j] - w_length[j] / 2)

    # UVLs
    for j in range(len(w_max)):
        if current_x > w_max_start[j] and current_x < w_max_start[j] + w_max_length[j]:
            current_shear_force -= 0.5 * w_max[j] * ((current_x - w_max_start[j]) / w_max_length[j]) * (current_x - w_max_start[j])
            current_bending_moment -= (1/6.0) * w_max[j] * ((current_x - w_max_start[j]) / w_max_length[j]) * (current_x - w_max_start[j]) ** 2
        elif current_x >= w_max_start[j] + w_max_length[j]:
            current_shear_force -= 0.5 * w_max[j] * w_max_length[j]
            current_bending_moment -= 0.5 * w_max[j] * w_max_length[j] * (current_x - w_max_start[j] - (2/3.0) * w_max_length[j])

    # Point moments
    for j in range(len(M)):
        if current_x > m_pos[j]:
            current_bending_moment -= M[j]

    shear_force.append(current_shear_force)
    bending_moment.append(current_bending_moment)

# ----------------- OUTPUT -----------------
print("\nPosition (m) | Shear Force (kN) | Bending Moment (kNm)")
for i in range(len(x)):
    print(f"{x[i]:.2f}\t\t{shear_force[i]:.2f}\t\t{bending_moment[i]:.2f}")