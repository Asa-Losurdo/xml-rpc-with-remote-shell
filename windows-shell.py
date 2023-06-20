import xmlrpc.client
import sys
import msvcrt

def wipe_line(self,len_line):
        sys.stdout.write("\r$ " + ' '*len_line + '\b'*len_line)
        sys.stdout.flush()

class windows_shell():
    def stop(self):
        print("\nexiting...")
        self.proxy.shell_set_lines(self.lines)
        exit()

    def run(self,addr="http://localhost:7080/"):
        with xmlrpc.client.ServerProxy(addr) as self.proxy:

            print("type: 'help()' for list of proxies methods\npress ESC or ctrl+c to exit")
            self.lines = self.proxy.shell_fetch_lines()
            # keyboard.on_press_key(key, callback, suppress=False)
            while True:
                try:
                    lines_rindex = 0
                    line_index = 0
                    line = ""
                    sys.stdout.write("$ ")
                    sys.stdout.flush()
                    while True:
                        if msvcrt.kbhit():
                            match msvcrt.getwch():
                                case '\b':
                                    if line != "":
                                        wipe_line(len(line))
                                        line_index = line_index - 1
                                        if line_index < 0:
                                            line_index = 0
                                        line = line[:line_index] + line[line_index+1:]
                                        sys.stdout.write(line + '\b'*len(line[line_index:]))
                                        sys.stdout.flush()
                                case '\r':
                                    sys.stdout.write("\n")
                                    line = line.strip()
                                    break
                                case '\xe0'|'\000':
                                    match msvcrt.getwch():
                                        case 'H': # up arrow
                                            wipe_line(len(line))
                                            lines_rindex = lines_rindex - 1
                                            if -lines_rindex > len(self.lines):
                                                lines_rindex = -len(self.lines) - 1
                                                line = ''
                                            else:
                                                line = self.lines[lines_rindex]
                                            line_index = len(line)
                                            sys.stdout.write(line)
                                            sys.stdout.flush()
                                        case 'P': # down arrow
                                            wipe_line(len(line))
                                            lines_rindex = lines_rindex + 1
                                            if lines_rindex > -1:
                                                lines_rindex = 0
                                                line = ''
                                            else:
                                                line = self.lines[lines_rindex]
                                            line_index = len(line)
                                            sys.stdout.write(line)
                                            sys.stdout.flush()
                                        case 'K': # left arrow
                                            line_index = line_index - 1
                                            if line_index < 0:
                                                line_index = 0
                                            else:
                                                sys.stdout.write('\b')
                                                sys.stdout.flush()
                                        case 'M': # right arrow
                                            line_index = line_index + 1
                                            if line_index > len(line):
                                                line_index = len(line)
                                            else:
                                                sys.stdout.write(line[line_index-1])
                                                sys.stdout.flush()
                                        case 'S': #del
                                            if line != "":
                                                wipe_line(len(line))
                                                line = line[:line_index] + line[line_index+1:]
                                                # if line_index > len(line) - 1:
                                                #     line_index = len(line) - 1
                                                sys.stdout.write(line + '\b'*len(line[line_index:]))
                                                sys.stdout.flush()
                                        case x:
                                            print(x)
                                case '\033':
                                    self.stop()
                                case char:
                                    wipe_line(len(line))
                                    line = line[:line_index] + char + line[line_index:]
                                    line_index = line_index + 1
                                    sys.stdout.write(line + '\b'*len(line[line_index:]))
                                    sys.stdout.flush()

                    if line != '':
                        self.lines.append(line)
                        self.proxy.shell_push_line(line)
                    print('  '+line,eval("proxy."+line))
                
                except Exception as e: print(e)
                except KeyboardInterrupt:
                    self.stop()
        
        
if __name__ == "__main__":
    windows_shell().run()