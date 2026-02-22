from lib.utils.args import parse_args
import argparse

def main():
  print("[START]")
  
  # CLI Entry Point
  args = parse_args()
  if hasattr(args, "func"):
    args.func(args)
  else:
    argparse.ArgumentParser(description="Project Management CLI Tool").print_help()

  print("[END]")

if __name__ == "__main__":
  main()
    
