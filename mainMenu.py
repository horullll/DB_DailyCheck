import sys, dbConnection, dayCheckMon, parsingJson

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

      instance_list = parsingJson.getInstanceList()
      for i in instance_list :
        print(i)
        #dayCheckMon.main(i)

    elif choice == "Q" or choice == "q":
        sys.exit
    else:
        print("You must only select either A,B,C, or D.")
        print("Please try again")
        menu()



#the program is initiated, so to speak, here
main()