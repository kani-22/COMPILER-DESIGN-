class StackAllocator:
    def __init__(self, size):
        self.size = size
        self.stack = []
        self.top = 0

    def allocate(self, var_name, var_size):
        if self.top + var_size > self.size:
            print(f"Memory Overflow! Cannot allocate {var_name}")
            return

        address = self.top
        self.stack.append((var_name, var_size, address))
        self.top += var_size
        print(f"Allocated {var_name} of size {var_size} at address {address}")

    def deallocate(self):
        if not self.stack:
            print("Stack Underflow! No memory to deallocate")
            return

        var_name, var_size, address = self.stack.pop()
        self.top -= var_size
        print(f"Deallocated {var_name} of size {var_size} from address {address}")

    def display(self):
        print("\nCurrent Stack Allocation:")
        if not self.stack:
            print("Stack is empty")
        else:
            for var_name, var_size, address in reversed(self.stack):
                print(f"{var_name} | Size: {var_size} | Address: {address}")
        print(f"Top Pointer = {self.top}")


def main():
    allocator = StackAllocator(100)

    while True:
        print("\n1. Allocate")
        print("2. Deallocate")
        print("3. Display")
        print("4. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            var_name = input("Enter variable name: ")
            var_size = int(input("Enter variable size: "))
            allocator.allocate(var_name, var_size)

        elif choice == 2:
            allocator.deallocate()

        elif choice == 3:
            allocator.display()

        elif choice == 4:
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
