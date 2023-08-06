# tests for chash

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import filez.lib as lib
import general as g
import random, hashlib

filez_dir = os.path.dirname(os.path.abspath(__file__))
filez_test_dir = os.path.join(filez_dir, 'test')
filez_test_hash_dir = os.path.join(filez_dir, 'test', 'hash')

hash_test_data = {
  '0.txt': 'DCO7I5jdCfIj6PaH8gmiftjUcYyzPgKmkrVlgDXtnexPzfmD4doJyt9yI1HSCMD3VecxsCL6dxOlhNa4RHcnWy7QJB6YrM7YoVy4',
  '1.txt': '[VfrCT>numgS=LTl4M1bQ(Wh|<#t?<ZDD84kR};vmJuX1E}z(o@S^UIUjnM|Z7hjvGD?g(OcV-:|CP2G=+%7Zi8(L9K2XPPTgt[$',
  '2.bin': [176, 174, 96, 108, 53, 196, 169, 39, 160, 69, 97, 225, 102, 138, 40, 125, 108, 200, 102, 242, 245, 109, 133, 139, 144, 183, 62, 198, 104, 93, 117, 169, 160, 229, 41, 142, 196, 242, 192, 44, 253, 92, 91, 243, 84, 234, 46, 185, 243, 194, 217, 33, 249, 160, 0, 8, 255, 46, 28, 213, 160, 148, 212, 127, 43, 142, 51, 129, 129, 247, 90, 111, 39, 30, 215, 10, 141, 248, 56, 231, 204, 88, 111, 194, 71, 135, 239, 90, 183, 205, 97, 63, 104, 147, 68, 58, 175, 173, 154, 115],
  '3.bin': [random.randint(0, 255) for i in range(100)],
}

hash_expected_values = {
  '0.txt': '88fe9ea46eabe47af51ec6307aa4e350',
  '1.txt': '8a4af0b9a7fa9c1f17ccee4d1d8f5997',
  '2.bin': '85a6afe2cc55acb1d466dc8053a30f60',
  '3.bin': hashlib.md5(bytes(bytearray(hash_test_data['3.bin']))).hexdigest(),
}

def clean_up_test():
  os.system(f"rm -rf {filez_test_dir}")

def set_up_tests():
  clean_up_test()
  os.system(f"mkdir {filez_test_dir}")
  os.system(f"mkdir {filez_test_hash_dir}")

  for k, v in hash_test_data.items():
    if k.split('.')[-1] == 'txt':
      g.write_file(os.path.join(filez_test_dir, k), v)
    else:
      # binary file
      f = open(os.path.join(filez_test_dir, k), 'wb')
      f.write(bytearray(v))
      f.close()

def run_test():
  set_up_tests()
  os.system(f"python3.7 {os.path.join(filez_dir, 'chash.py')} -d {filez_test_dir} -o {filez_test_hash_dir}")
  # read in hashes and compare to original
  for k, v in hash_expected_values.items():
    hashed_value = g.read_file(os.path.join(filez_test_hash_dir, f"{k}.hash"))
    if hashed_value != v:
      return False
  return True

if __name__ == "__main__":
  if not run_test():
    print(g.error_message("Test filez.test failed!"))
  else:
    print(g.ok_message("Test filez.test passed"))

  clean_up_test()