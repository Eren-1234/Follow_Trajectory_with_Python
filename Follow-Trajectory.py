import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Sabitler
d_star = 0.5       # İstenen takip mesafesi (m)
K_v = 1.5          # Doğrusal hız için kazanç
K_theta = 1.5      # Açısal hız için kazanç
dt = 0.1           # Zaman adımı
total_time = 20    # Toplam simülasyon süresi

# Başlangıç pozisyonu ve yönelimi
x, y, theta = 0, 0, 0

# Simülasyon verilerini saklamak için listeler
x_data, y_data = [x], [y]
time_data = np.arange(0, total_time, dt)

# Yörünge fonksiyonları
def trajectory(t):
    return t, np.sin(t)

# Animasyon ayarları
fig, ax = plt.subplots()
ax.set_xlim(-1, 20)
ax.set_ylim(-2, 2)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid()
trajectory_x = []
trajectory_y = []

for t in time_data:
    traj_x, traj_y = trajectory(t)
    trajectory_x.append(traj_x)
    trajectory_y.append(traj_y)

ax.plot(trajectory_x, trajectory_y, 'r--', label="Takip Edilen Yörünge")
robot_path, = ax.plot([], [], "b-", label="Robotun Yolu")
ax.legend()


robot_arrow = ax.arrow(x, y, 0.5 * np.cos(theta), 0.5 * np.sin(theta),
                       head_width=0.1, head_length=0.2, fc='blue', ec='blue')

# Hareket güncelleme fonksiyonu
def update(frame):
    global x, y, theta, robot_arrow

    # Hedef pozisyonu belirle
    t = frame * dt
    x_ref, y_ref = trajectory(t)

    # Robot ile referans noktası arasındaki açı ve mesafe
    dx = x_ref - x
    dy = y_ref - y
    distance_to_target = np.sqrt(dx**2 + dy**2)
    angle_to_target = np.arctan2(dy, dx)
    
    # Yönelim hatası ve hızları hesapla
    error_theta = angle_to_target - theta
    v = K_v * (distance_to_target - d_star)
    omega = K_theta * error_theta

    # Yeni pozisyonları güncelle
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += omega * dt

    # Verileri güncelle
    x_data.append(x)
    y_data.append(y)
    robot_path.set_data(x_data, y_data)

    # Robotun yön oku güncelle
    robot_arrow.remove()  
    robot_arrow = ax.arrow(x, y, 0.5 * np.cos(theta), 0.5 * np.sin(theta),
                           head_width=0.1, head_length=0.2, fc='blue', ec='blue')

    return robot_path, robot_arrow

# Animasyon fonksiyonu
ani = FuncAnimation(fig, update, frames=int(total_time / dt), interval=100, blit=True)

plt.title("Follow-Trajectory Robot Hareketi (Animasyon)")
plt.show()
