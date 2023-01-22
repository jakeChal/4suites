from FourSuites import FourSuites, Doors

# If token expired you need to re-authenticate!
# building = FourSuites()
# building.authenticate(email=email, password=pwd, save_token=True)

with open("token.txt") as f:
    building = FourSuites(f.read())
    building.get_doors()
    building.open_door(Doors.MALL)
