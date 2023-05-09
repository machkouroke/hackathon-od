def get_final_fleet(vehicles: list, incident):
    total_cap = 0
    fleet = []

    for vehicle in vehicles:
        if vehicle.cap >= incident.level:
            fleet = [vehicle]
            break
        else:
            total_cap += vehicle.cap
            fleet.append(vehicle)
            if total_cap >= incident.level:
                break
    return fleet
