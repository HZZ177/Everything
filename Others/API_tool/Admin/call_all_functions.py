import generated_request_functions as api


def call_all_functions(access_token):
    functions = [func for func in dir(api) if callable(getattr(api, func)) and not func.startswith("__")]

    results = {}
    for func_name in functions:
        func = getattr(api, func_name)
        try:
            result = func(access_token)
            results[func_name] = result
            print(f"{func_name} called successfully, result: {result}")
        except Exception as e:
            results[func_name] = str(e)
            print(f"Error calling {func_name}: {e}")

    return results


if __name__ == "__main__":
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjA3MDIyNTksInVzZXIiOiJ7XCJhY2NvdW50XCI6XCJhZG1pbkBrZXl0b3AuY29tXCIsXCJpZFwiOjEsXCJuYW1lXCI6XCJBZG1pbmlzdHJhdG9yXCIsXCJ1c2VyVHlwZVwiOjF9IiwiaWF0IjoxNzIwNjE1ODU5fQ.GQ1l_BUq2uTC3nHSVB_GIEfpzWPVJ7K2DKHomY5WSiE"
    call_all_functions(access_token)
