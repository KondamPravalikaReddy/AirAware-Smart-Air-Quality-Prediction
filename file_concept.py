# Writing to a file
f = open("example.txt", "w")
f.write("Hello, this is a file write example.\n")
f.close()

# Reading from a file
f = open("example.txt", "r")
print("File Content:\n", f.read())
f.close()

# Appending to a file
f = open("example.txt", "a")
f.write("This line is appended.\n")
f.close()

# Reading line by line
f = open("example.txt", "r")
for line in f:
    print("Line:", line.strip())
f.close()

# Using with-statement (auto-closes file)
with open("example.txt", "r") as f:
    data = f.read()
    print("\nUsing with-statement:\n", data)
