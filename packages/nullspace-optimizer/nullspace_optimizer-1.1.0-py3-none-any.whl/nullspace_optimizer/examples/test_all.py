def main():
    import os
    import importlib
    from nullspace_optimizer.nullspace import display, colored
    examples_folder = os.path.split(__file__)[0]
    display("Testing all examples in "+examples_folder,color="magenta",attr="bold")
    print("")
    files = os.listdir(examples_folder)
    files.sort()
    for f in files:
        if f.startswith('ex') and f.endswith('.py'):
            module = os.path.splitext(f)[0]
            display("="*80,color="magenta",attr="bold")
            display("Testing "+f,color="magenta",attr="bold")
            display("="*80,color="magenta",attr="bold")
            print("")
            try:
                mod = importlib.import_module(f".{module}", package="nullspace_optimizer.examples")
                mod.main()
            except Exception as e:
                print(e)
                display("Warning, testing of "+f+" failed.",color="red",attr="bold")
            input(colored(f"\nEnd of test {f}. Press any key to continue.",color="magenta",attr="bold"))
            display("\n\n")

if __name__ == "__main__":
    main()