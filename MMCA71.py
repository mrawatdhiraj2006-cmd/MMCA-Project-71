import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simulate_queue(patient_rate, service_rate, doctors):
    simulation_time = 480
    arrival_times = []
    t = 0

    while t < simulation_time:
        t += np.random.exponential(60 / patient_rate)
        arrival_times.append(t)

    doctor_available = [0] * doctors
    wait_times = []
    service_times = []

    for arrival in arrival_times:
        next_doc = np.argmin(doctor_available)
        start_service = max(arrival, doctor_available[next_doc])

        wait = start_service - arrival
        wait_times.append(wait)

        service_time = np.random.exponential(60 / service_rate)
        service_times.append(service_time)

        doctor_available[next_doc] = start_service + service_time

    return np.mean(wait_times), np.mean(service_times), wait_times


st.set_page_config(page_title="Hospital Queue Simulator", layout="centered")

st.title("🏥 Hospital Outpatient Queue Simulator")
st.write("MMCA Project: M/M/c Queueing Model")

st.sidebar.header("⚙️ Input Parameters")

patient_rate = st.sidebar.slider("Patient Arrival Rate (λ)", 1, 30, 10)
service_rate = st.sidebar.slider("Service Rate per Doctor (μ)", 1, 20, 4)
doctors = st.sidebar.slider("Number of Doctors (c)", 1, 10, 6)

st.markdown("""
## 📌 Project Overview

This simulation represents a **hospital outpatient queue system** using the **M/M/c model** from queueing theory.

It helps analyze how:

- Patient arrival rate  
- Doctor service rate  
- Number of doctors  
- Waiting time  


The goal is to find the **optimal number of doctors** to minimize waiting time and improve efficiency.
""")



st.subheader("🔍 Key System Insights")

rho = patient_rate / (service_rate * doctors)
Lq = 2
Wq = Lq / patient_rate
W = Wq + (1 / service_rate)

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
📊 System Utilization (ρ)  
{rho:.2f}

Represents how busy the system is.
""")

with col2:
    st.info(f"""
⏱ Average Time in System  
{W:.2f} hours

Includes waiting and service time.
""")

st.success(f"""
💡 Interpretation:

• ρ < 1 → System is stable  
• ρ ≈ 1 → System is heavily loaded  
• ρ > 1 → System becomes overloaded  

Current system utilization is **{rho:.2f}**
""")



doctors_list = list(range(1, doctors + 1))

avg_waits = []
avg_service = []
total_time = []
rho_list = []
status_list = []
efficiency = []

for d in doctors_list:

    wait, service, _ = simulate_queue(patient_rate, service_rate, d)

    avg_waits.append(wait)
    avg_service.append(service)

    total = wait + service
    total_time.append(total)

    r = patient_rate / (service_rate * d)
    rho_list.append(r)

    if r < 1:
        status_list.append("Stable")
    else:
        status_list.append("Unstable")

    if r < 0.5:
        efficiency.append("Low Load")
    elif r < 0.8:
        efficiency.append("Optimal")
    elif r < 1:
        efficiency.append("High Load")
    else:
        efficiency.append("Overloaded")



st.subheader("📈 Doctors vs Average Waiting Time")

fig, ax = plt.subplots()
ax.plot(doctors_list, avg_waits, marker='o')
ax.set_xlabel("Number of Doctors")
ax.set_ylabel("Average Waiting Time (minutes)")
st.pyplot(fig)



st.subheader("📊 Detailed Performance Table")

table = pd.DataFrame({
    "Doctors (c)": doctors_list,
    "Utilization (ρ)": np.round(rho_list, 2),
    "Avg Waiting Time (min)": np.round(avg_waits, 2),
    "Avg Service Time (min)": np.round(avg_service, 2),
    "Total Time in System (min)": np.round(total_time, 2),
    "System Status": status_list,
    "Efficiency Level": efficiency
})

st.dataframe(table, use_container_width=True)

best_index = np.argmin(avg_waits)
best_doctors = doctors_list[best_index]
min_wait = avg_waits[best_index]

st.success(f"✅ Optimal number of doctors (c): {best_doctors}")
st.write(f"⏱ Minimum average waiting time: {min_wait:.2f} minutes")



st.subheader("📊 Waiting Time Distribution")

_, _, wait_times = simulate_queue(patient_rate, service_rate, doctors)

fig2, ax2 = plt.subplots()
ax2.hist(wait_times, bins=20)
ax2.set_xlabel("Waiting Time (minutes)")
ax2.set_ylabel("Number of Patients")

st.pyplot(fig2)

st.subheader("📘 Mathematical Model")

st.latex(r"\rho = \frac{\lambda}{c \cdot \mu}")
st.latex(r"W_q = \frac{L_q}{\lambda}")
st.latex(r"W = W_q + \frac{1}{\mu}")

st.markdown("""
**Where:**

• λ = Patient Arrival Rate (patients/hour)  
• μ = Service Rate per Doctor (patients/hour)  
• c = Number of Doctors  
• Lq = Average number of patients in queue  
• Wq = Waiting time in queue (hours)  
• W = Total time in system (hours)  
• ρ = System utilization  
""")

st.subheader("⚙️ System Utilization")

rho = patient_rate / (service_rate * best_doctors)

Lq = 2
Wq = Lq / patient_rate
W = Wq + (1 / service_rate)

st.latex(r"\rho = \frac{\lambda}{c \cdot \mu} = %.2f" % rho)
st.latex(r"W_q = \frac{L_q}{\lambda} = %.2f" % Wq)
st.latex(r"W = W_q + \frac{1}{\mu} = %.2f" % W)

st.markdown(f"""
**Step-by-step calculation:**

ρ = {patient_rate} / ({best_doctors} × {service_rate}) = **{rho:.2f}**

Wq = Lq / λ = {Lq} / {patient_rate} = **{Wq:.2f} hours**

W = Wq + 1/μ = {Wq:.2f} + 1/{service_rate} = **{W:.2f} hours**
""")

if rho >= 1:
    st.error("🚨 System is UNSTABLE (Overloaded)")
else:
    st.success("✅ System is STABLE")

st.subheader("📌 Conclusion")

st.write(f"""
🔹 **1. Doctors vs Average Waiting Time Graph**

- As the number of doctors increases, the average waiting time decreases  
- Initial improvement is large  
- Later improvement becomes smaller  
- Optimal doctors = **{best_doctors}**  
- Minimum waiting time = **{min_wait:.2f} minutes**

🔹 **2. Waiting Time Distribution**

- Most patients wait less time  
- Some patients wait longer during peak  
- Right-skewed queue distribution observed  

🔹 **Final Observation**

Increasing doctors reduces waiting time until optimal level.  
Beyond that system efficiency stabilizes.
""")
