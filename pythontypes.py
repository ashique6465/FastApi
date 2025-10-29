def add(firstName: str,lastName:str = None):
    return firstName + " " + lastName

fname = "Bill"
lname = "Gates"

name = add(fname.capitalize(),lname)
print(name)