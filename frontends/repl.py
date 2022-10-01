from botplug import run


def mainloop():
    while True:
        try:
            text = input(">> ")
        except KeyboardInterrupt:
            break
        command, args = text.split(" ", 1)
        try:
            for cmd in commands:
                if command in cmd.commands:
                    print(cmd.hook(text=args, reply=print))
                    break
            else:
                print("Command not found\n")
        except Exception as e:
            print(e)

mainloop()
