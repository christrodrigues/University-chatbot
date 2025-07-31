# write a function to reverse a string and print
def reverse_string(s):
    """Reverses the input string and prints it."""
    reversed_s = s[::-1]
    print(reversed_s)
def main():
    # Example usage
    input_string = "Hello, World!"
    reverse_string(input_string)

if __name__ == "__main__":
    main()
