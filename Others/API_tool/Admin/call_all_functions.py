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
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjA3ODE0NDIsInVzZXIiOiJ7XCJhY2NvdW50XCI6XCJoZXNob3V5aVwiLFwiaWRcIjo1LFwibmFtZVwiOlwiaGVzaG91eWlcIixcInBob25lXCI6XCJcIixcInJvbGVJZFwiOjQsXCJyb3V0ZXJQZXJtaXNzaW9uc1wiOltcImxvdC1jb25maWdcIixcImxvdC1pbmZvXCJdLFwidXNlclR5cGVcIjoyfSIsImlhdCI6MTcyMDY5NTA0Mn0.GPHtvsZVcJBKRhYsZffoINZAe0e5TcRqM8DD-m0HxiU"
    call_all_functions(access_token)
