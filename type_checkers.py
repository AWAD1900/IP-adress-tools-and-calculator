def input_int(text:str, error:str, min_limit:int) -> int:
    try:
        a = int(input(f"\n{text}: "))
        assert a > min_limit
        return a
    except:
        print(f"\n\033[31m{error}\033[0m")
        return input_int(text, error,min_limit)