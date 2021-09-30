import getopt
import sys
import reportlive
import reportmock


# Get full command-line arguments
if __name__ == '__main__':
    full_cmd_arguments = sys.argv
    arg=""
    # Keep all but the first
    argument_list = full_cmd_arguments[1:]
    short_options = "hml"
    long_options = ["help", "mock", "live"]
    if len(argument_list) == 0:
        print("Options:\t-m,--mock\t Mock Test\n"
              "\t\t-l,--live\t Live Test")

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ("-h", "--help"):
                print("Options:\t-m,--mock\t Mock Test\n"
                      "\t\t-l,--live\t Live Test")
            elif current_argument in ("-m", "--mock"):
                reportmock.run()
            elif current_argument in ("-l", "--live"):
                reportlive.run()


    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)