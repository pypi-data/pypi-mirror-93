# from . import lib
# from .. import general as g
# ^^ this works if importing but not if you're running the script... because of guido... orz
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import filez.lib as lib
import general as g

import argparse

def chash_main(hash_path, output_path = None, mute = False):
  if hash_path:
    # if output not specified, hash to $data_folder/hash
    # therefore, don't hash this location if it exists ^

    # check location exists
    if not lib.dir_exists(hash_path):
      print(g.error_message(f"Path {hash_path} does not exist"))
      exit()

    if not output_path:
      output_path = os.path.join(hash_path, "hash")
      if dir_exists(output_path):
        print(g.highlight_message(f"Destination folder {output_path} exists, (potentially) overwriting"))

    lib.chash_all_files(hash_path, output_path, write_output = True, mute = mute)
  else:
    print(g.error_message(f"Hash path not specified"))

  return None

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="""
    low level hash tool: creates hashes of folders for comparison purposes

    Examples:

      chash -d $path_to_data_folder -o $path_to_hash_folder
    """,
    formatter_class=argparse.RawTextHelpFormatter
  )

  parser.add_argument('-d', '--hash-path', action='store', help="data root location (absolute path)")
  parser.add_argument('-o', '--output-path', nargs='?', action='store', help="hash root location (absolute path)")
  parser.add_argument('-m', '--mute', action='store_true', help="do not ask for user inputs, just run")

  args = parser.parse_args()

  chash_main(
    hash_path = args.hash_path,
    output_path = args.output_path,
    mute = args.mute
  )