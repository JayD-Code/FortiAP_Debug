start_patterns = ('config wireless-controller')
end_patterns = ('end')

def section_with_bounds(gen):
  section_in_play = False
  for line in gen:
    if line.startswith(start_patterns):
      section_in_play = True
    if section_in_play:
        print(line,end='')
    if line.startswith(end_patterns):
      section_in_play = False

with open("FortiWiFi-60E.conf") as f: #Put your config file name here
  gen = section_with_bounds(f)
  for line in gen:
    print(line, end = '')


