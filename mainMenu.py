import sys, dbConnection, dayCheckMon

def main():
    menu()

def menu():
    print("************MAIN MENU**************")
    # time.sleep(1)
    print()

    choice = input("""
                      A: View all DB instance monitoring info
                      R: Register DB instance 
                      Q: Quit/Log Out

                      Please enter your choice: """)

    if choice == "A" or choice == "a":

      dayCheckMon.main('DEV502')
      # dayCheckMon.main('HIS012')
      # dayCheckMon.main('HIS013')
      # dayCheckMon.main('HIS014')
      # dayCheckMon.main('HIS015')
      # dayCheckMon.main('HIS016')
      # dayCheckMon.main('HIS017')
      # dayCheckMon.main('MIS001')
      # dayCheckMon.main('CMC001')

    elif choice == "Q" or choice == "q":
        sys.exit
    else:
        print("You must only select either A,B,C, or D.")
        print("Please try again")
        menu()



#the program is initiated, so to speak, here
main()