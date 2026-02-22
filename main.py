from lib.utils.args import parse_args
import argparse

def main():
  print("[START]")
  
  # CLI Entry Point
  args = parse_args()
  if hasattr(args, "func"):
    args.func(args)  # Call the function associated with the command
  else:
    print("No command provided. Use --help for more information.")
  
  print("[END]")

if __name__ == "__main__":
  main()
    
