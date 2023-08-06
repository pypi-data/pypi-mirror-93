__version__ = "0.1.0"

try:
    import main
except ModuleNotFoundError:
    from search_that_hasg import main

if __name__ == "__main__":
    main.main()