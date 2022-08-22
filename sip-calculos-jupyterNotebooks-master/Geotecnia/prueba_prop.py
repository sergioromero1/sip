class Foo():
    def __init__(self):
        self.x = 10
    
    y = property(lambda self: 20 + self.x)

def main():
    f = Foo()
    print(f.x)
    print(f.y)
    print(getattr(f, "x"))
    print(getattr(f, "y"))

if __name__ == "__main__":
    main()