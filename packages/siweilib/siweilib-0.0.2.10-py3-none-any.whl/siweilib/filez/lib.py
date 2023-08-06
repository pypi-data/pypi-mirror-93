import hashlib
import os, time, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import general as g

def dir_exists(path):
  return os.path.isdir(path)

def file_exists(path):
  return os.path.isfile(path)

def path_exists(path):
  return os.path.exists(path)

def is_hidden_path(p):
  fnames = p.split('/')
  ret = False
  for f in fnames:
    if len(f) > 0 and f[0] == '.' and f != '.':
      ret = True
  return ret

# basic ignore function: no hidden files, links, locks, log files, item has to be a file, no root/hash
def default_ignore(full_path, data_root_path = None):
  if not path_exists(full_path):
    return True
  if is_hidden_path(full_path):
    return True
  if os.path.islink(full_path):
    return True

  # ignore lock files and log files
  x = full_path.split('/')[-1]
  if x in [
    'log.txt',
    'log.txt.hash',
  ]:
    return True
  f_type = x.split('.')[-1]
  f_type2 = None
  if len(x.split('.')) >= 2:
    f_type2 = x.split('.')[-2]
  if f_type in [
    'lock',
    'sock',
  ] or (
    f_type == 'hash' and f_type2 in ['lock', 'sock']
  ):
    return True

  # ignore root/hash
  rpath = os.path.relpath(full_path, data_root_path)
  if len(rpath.split('/')) > 0 and rpath.split('/')[0] == 'hash':
    return True
  return False

def data_to_hash_filename_mapper(fnom):
  return fnom + '.hash'

def hash_to_data_filename_mapper(fnom):
  tmp = fnom.split('.hash')
  if tmp[-1] == '':
    # remove any trailing '.hash' in the filename
    return '.hash'.join(tmp[:-1])
  else:
    return fnom

def compute_digest(plaintext):
  return hashlib.md5(plaintext.encode('utf-8')).hexdigest()

def compute_digest_from_file(fnom):
  return hashlib.md5(open(fnom, 'rb').read()).hexdigest()

# hash the file data_file_path and put into hash_root_path, maintaining the same folder structure
# so that data_root_path maps to hash_root_path
def chash_file(
  data_file_path,
  data_root_path,
  hash_root_path,
  ignore_funcs = [default_ignore],
  write_output = True
):
  rpath = os.path.relpath(data_file_path, data_root_path)
  hpath = data_to_hash_filename_mapper(os.path.join(hash_root_path, rpath))
  for func in ignore_funcs:
    if func(data_file_path, data_root_path):
      return
  hash_digest = compute_digest_from_file(data_file_path)
  if write_output:
    g.write_file(hpath, hash_digest)

# hash all the files in a given folder
def chash_all_files(
  data_root_path,
  hash_root_path,
  ignore_funcs = [default_ignore],
  write_output = True,
  mute = False
):
  progress_pcts = [ 0.01 ] + [ 0.1 * (i+1) for i in range(10) ]
  total_file_ct = sum([len(files) for dirpath, dirs, files in os.walk(data_root_path)])
  progress_cts = [ int(total_file_ct*pct) for pct in progress_pcts ]
  current_pointer = 0
  current_ct = 0
  sub_start_time = time.time()
  for dirpath, dirs, files in os.walk(data_root_path):
    rpath = os.path.relpath(dirpath, data_root_path)
    hpath = os.path.join(hash_root_path, rpath)
    if is_hidden_path(rpath):
      if not mute:
        print("skipping path %s" % rpath)
    else:
      if not os.path.isdir(hpath):
        os.makedirs(hpath)
      for f in files:
        current_ct += 1
        if(current_ct > progress_cts[current_pointer]):
          current_pct = progress_pcts[current_pointer]
          sys.stdout.write("\r%d files (%0.2f percent) hashed in %0.2fs. " % (
            current_ct, current_pct*100, (time.time() - sub_start_time)
          ) + "Estimated total time for completion: %s" % (
            "{:,}".format(int((time.time() - sub_start_time)/current_pct))
          ))
          sys.stdout.flush()
          current_pointer += 1

        fpath = os.path.join(dirpath, f)
        chash_file(fpath, data_root_path, hash_root_path, ignore_funcs)
  print("")

# paginate the hashes so there aren't a billion files
# def do_chash_paginated():