import os
def run():
    def command_run():
        clear = input("give your screen clearing command [cls or clear]: ")
        os.system(clear)
        print("Designed by Kanish Ravikumar")
        print("____________________________________")
        print(f"            {name}                 ")
        print("____________________________________")
        print("To exit type 'exit()'")
        while True:
            print(prefix+"[@]:")
            main=input("$ ")
            os.system(main)
            if main == "exit()":
                break
    name = input("Enter TERMINAL name: ")
    prefix = input("Enter your prefix: ")
    command_run()
