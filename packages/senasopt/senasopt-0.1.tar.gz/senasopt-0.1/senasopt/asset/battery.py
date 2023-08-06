# -*- coding: utf-8 -*-
"""
Functions related to modelling of batteries.

This file can also be imported as a module and contains the following
functions:


References:
    [1] J. Twidell & T. Weir, Renewable Energy Resources, 2nd edition, 
    Taylor and Francis, 2006

"""

# Import all useful libraries
import casadi as ca
import casadi.tools
import numpy as np

from .optimise import runge_kuta, solve_optimisation, extract_optimisation_results

__battery_model = dict(
    capacity=1e4,
    rated_power=1e3,
    charge_efficiency=0.98,
    discharge_efficiency=0.98,
    connection_sizing=np.inf,
)


def battery_model(
    model=__battery_model,
    initial_state_of_charge=0,
):

    # Loading the battery model
    initial_soc = initial_state_of_charge
    capacity = model["capacity"]
    rated_power = model["rated_power"]
    charge_efficiency = model["charge_efficiency"]
    discharge_efficiency = model["discharge_efficiency"]
    connection_sizing = model["connection_sizing"]

    # State vector
    fields_x = ["state_of_charge"]
    x = ca.tools.struct_symMX(fields_x)
    x0 = initial_soc

    # Input vector
    fields_u = ["battery_power_intake", "battery_power_output"]
    u = ca.tools.struct_symMX(fields_u)

    # Disturbance vector (none for now)
    fields_v = ["None"]
    v = ca.tools.struct_symMX(fields_v)

    # State equations
    dxdt = ca.tools.struct_MX(x)
    dxdt["state_of_charge"] = (
        charge_efficiency * u["battery_power_intake"]
        - u["battery_power_output"] / discharge_efficiency
    )

    # ODE Right-hand side
    f = ca.Function("f", [x, u, v], [dxdt], ["x", "u", "v"], ["dx/dt"])

    # Single step time propagation
    dt = ca.MX.sym("dt")
    F_SSM = runge_kuta(f, x, u, v, dt, order=4)

    model = {
        "SSM": F_SSM,
        "x0": x0,
        "u": u,
        "v": v,
        "x": x,
        "data_fields": {
            "u": fields_u,
            "v": fields_v,
            "x": fields_x,
        },
        "performance_fields": {
            "energy": "Php",
            "indoor_temperature": "Tr",
        },
        "constraints": {
            "u_min": 0,
            "u_max": rated_power,
            "x_min": 0,
            "x_max": capacity,
            "connection_sizing": connection_sizing,
        },
    }

    return model


def battery_optimal_controller(
    data,
    model=__battery_model,
    initial_state_of_charge=0,
):
    # Input data=[power_price,local_demand,local_production]

    # Converting for usage of hour time units
    dt_index = data.index[1:-1] - data.index[0:-2]
    dt_data = (dt_index.to_numpy() / np.timedelta64(1, "h")).mean()
    N = len(data)

    price = data["power_price"].to_numpy()  # Price is usually given in unit/kWh

    if "local_demand" in data.keys():
        local_demand = data["local_demand"].to_numpy().reshape(1, N)
    else:
        local_demand = np.zeros(N).reshape(1, N)

    if "local_production" in data.keys():
        local_production = data["local_production"].to_numpy().reshape(1, N)
    else:
        local_production = np.zeros(N).reshape(1, N)

    ## ----------- System description -------------------
    model2use = battery_model(
        model=model, initial_state_of_charge=initial_state_of_charge
    )

    F_SSM = model2use["SSM"]
    u = model2use["u"]
    v = model2use["v"]
    x = model2use["x"]
    x0 = model2use["x0"]
    fields_u = model2use["data_fields"]["u"]
    fields_v = model2use["data_fields"]["v"]
    fields_x = model2use["data_fields"]["x"]

    field_perf_energy = model2use["performance_fields"]["energy"]
    field_perf_Ti = model2use["performance_fields"]["indoor_temperature"]

    V = np.zeros(N).reshape(1, N)

    ## ----------- Optimal control -------------------
    # Optimization horizon
    N = len(data)
    opti = ca.Opti()

    # Decision variables for states and inputs
    X = opti.variable(x.size, N + 1)
    U = opti.variable(u.size, N)

    # Computing imports and exports
    fields_u = ["battery_power_intake", "battery_power_output"]
    Pin_battery = U[0, :]
    Pout_battery = U[1, :]
    y_net_export = (Pout_battery + local_production) - (Pin_battery + local_demand)
    y_Pimport = ca.fmax(0, -y_net_export)
    y_Pexport = ca.fmax(0, y_net_export)

    # Initial state is a parameter
    x_min = model2use["constraints"]["x_min"]
    x_max = model2use["constraints"]["x_max"]
    u_min = model2use["constraints"]["u_min"]
    u_max = model2use["constraints"]["u_max"]

    x0 = model2use["x0"]
    opti.subject_to(X[:, 0] == x0)
    opti.subject_to(X[0, :] <= x_max)
    opti.subject_to(X[0, :] >= x_min)

    opti.subject_to(U[0, :] <= u_max)
    opti.subject_to(U[0, :] >= u_min)
    opti.subject_to(U[1, :] <= u_max)
    opti.subject_to(U[1, :] >= u_min)

    # State constraints
    for k in range(N):
        opti.subject_to(X[:, k + 1] == F_SSM(X[:, k], U[:, k], V[:, k], dt_data))

    transformer_sizing = model2use["constraints"]["connection_sizing"]
    if np.isinf(transformer_sizing) is False:
        opti.subject_to(y_Pimport <= transformer_sizing)
        opti.subject_to(y_Pexport <= transformer_sizing)

    # Objectives
    cost = ca.mtimes(y_Pimport, price) - ca.mtimes(y_Pexport, price)
    opti.minimize(cost)

    # Solve the optimisation
    sol = solve_optimisation(problem=opti, solver="ipopt", verbose=False)

    # Structuring outputs
    val_Pout = sol.value(Pout_battery)
    val_Pin = sol.value(Pin_battery)
    val_revenue = -sol.value(cost)
    val_export = sol.value(y_Pexport)
    val_import = sol.value(y_Pimport)

    performance = dict(
        revenue=np.sum(val_revenue),
        energy_output=np.sum(val_Pout),
        energy_intake=np.sum(val_Pin),
        energy_losses=np.sum(val_Pin) - np.sum(val_Pout),
        energy_export=np.sum(val_export),
        energy_import=np.sum(val_import),
    )

    timeseries = extract_optimisation_results(
        solution=sol, model=model2use, data=data, X=X, U=U, V=V, keep=["power_price"]
    )
    # timeseries["battery_power_intake"] = sol.value(val_Pin)
    # timeseries["battery_power_output"] = sol.value(val_Pout)
    timeseries["power_import"] = sol.value(val_import)
    timeseries["power_export"] = sol.value(val_export)
    timeseries["power_import"] = sol.value(val_import)
    timeseries["revenue"] = (
        timeseries["power_export"] - timeseries["power_import"]
    ) * timeseries["power_price"]

    return performance, timeseries
