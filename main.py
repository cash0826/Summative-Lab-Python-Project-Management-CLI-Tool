from lib.utils.args import parse_args
import argparse

def main():
  
  # CLI Entry Point
  args = parse_args()
  if hasattr(args, "func"):
    args.func(args)  # Call the function associated with the command
  else:
    print("No command provided. Use --help for more information.")

if __name__ == "__main__":
  main()
    
