from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# ---------------- BASIC RATES ----------------
RATE = 6  # ₹ per unit
WATER_RATE = 2 / 100  # ₹ per liter

# ---------------- GLOBAL USAGE VALUES ----------------
solar = 8.0        # kWh
water = 400        # Liters

# ---------------- APPLIANCE POWER (kW) ----------------
APPLIANCE_POWER = {
    "Light": 0.06,
    "Fan": 0.07,
    "AC": 1.5,
    "TV": 0.12
}

# ---------------- ROOMS & DEVICES ----------------
rooms = {
    "Living Room": {"Light": True, "AC": False, "Fan": True, "TV": False},
    "Kitchen": {"Light": True, "Fan": False},
    "Bedroom": {"Light": False, "Fan": False}
}

# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    electricity = calculate_total_electricity()
    bill = electricity * RATE

    return render_template(
        "dashboard.html",
        electricity=electricity,
        solar=solar,
        water=water,
        bill=bill
    )

# ---------------- ELECTRICITY (APPLIANCE-WISE) ----------------
@app.route("/electricity")
def electricity_page():
    appliance_usage = {}
    total = 0

    for room, devices in rooms.items():
        for device, state in devices.items():
            if state and device in APPLIANCE_POWER:
                usage = round(APPLIANCE_POWER[device] * 4, 2)  # 4 hrs simulated
                appliance_usage[device] = appliance_usage.get(device, 0) + usage
                total += usage

    highest_device = (
        max(appliance_usage, key=appliance_usage.get)
        if appliance_usage else "None"
    )

    return render_template(
        "electricity.html",
        electricity=round(total, 2),
        appliance_usage=appliance_usage,
        highest_device=highest_device
    )

# ---------------- COST ----------------
@app.route("/cost")
def cost_page():
    electricity = calculate_total_electricity()

    elec_week_bill = round((electricity * 7 / 30) * RATE, 2)
    elec_month_bill = round(electricity * RATE, 2)

    water_week_bill = round((water * 7 / 30) * WATER_RATE, 2)
    water_month_bill = round(water * WATER_RATE, 2)

    return render_template(
        "cost.html",
        electricity=round(electricity, 2),
        water=water,
        elec_week_bill=elec_week_bill,
        elec_month_bill=elec_month_bill,
        water_week_bill=water_week_bill,
        water_month_bill=water_month_bill
    )


# ---------------- WATER ----------------
@app.route("/water")
def water_page():
    return render_template("water.html", water=water)

@app.route("/water/add")
def water_add():
    global water
    water += 50
    return redirect(url_for("water_page"))

@app.route("/water/reduce")
def water_reduce():
    global water
    water = max(0, water - 50)
    return redirect(url_for("water_page"))

# ---------------- SOLAR ----------------
@app.route("/solar")
def solar_page():
    return render_template("solar.html", solar=solar)

@app.route("/solar/add")
def solar_add():
    global solar
    solar += 1
    return redirect(url_for("solar_page"))

@app.route("/solar/reduce")
def solar_reduce():
    global solar
    solar = max(0, solar - 1)
    return redirect(url_for("solar_page"))

# ---------------- ROOMS ----------------
@app.route("/rooms")
def rooms_page():
    room_energy = {}

    for room, devices in rooms.items():
        total = 0
        for device, state in devices.items():
            if state and device in APPLIANCE_POWER:
                total += APPLIANCE_POWER[device]
        room_energy[room] = round(total, 2)

    return render_template(
        "rooms.html",
        rooms=rooms,
        room_energy=room_energy
    )

# ---------------- TOGGLE DEVICE ----------------
@app.route("/toggle/<room>/<device>")
def toggle_appliance(room, device):
    rooms[room][device] = not rooms[room][device]
    return redirect(url_for("rooms_page"))

# ---------------- APPLIANCES ----------------
@app.route("/appliances")
def appliances_page():
    return render_template("appliances.html", rooms=rooms)

# ---------------- HELPER FUNCTION ----------------
def calculate_total_electricity():
    total = 0
    for room, devices in rooms.items():
        for device, state in devices.items():
            if state and device in APPLIANCE_POWER:
                total += APPLIANCE_POWER[device] * 4
    return round(total, 2)

# ---------------- ELECTRICITY LOAD CONTROL ----------------
@app.route("/electricity/add")
def electricity_add():
    # Turn ON AC in Living Room (simulate adding load)
    rooms["Living Room"]["AC"] = True
    return redirect(url_for("electricity_page"))

@app.route("/electricity/reduce")
def electricity_reduce():
    # Turn OFF AC in Living Room (simulate reducing load)
    rooms["Living Room"]["AC"] = False
    return redirect(url_for("electricity_page"))



# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
