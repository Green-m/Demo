#encoding=utf-8
import ctypes

import re 
import os 

def parse_dns(filename):
	file = open(filename,'r')
	try:
		lines = file.read()
		stringlist = re.findall(r'Name\s+: \S+',lines)
		stringlist = [re.sub(r'Name\s+: ','',string) for string in stringlist]
		
		stringlist.remove('isatap')
		for string in stringlist:
			print string

	except:
		pass

	finally:
		file.close()


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


disable_file_system_redirection().__enter__()
parse_dns('c:/windows/system32/dnsrslvr.log')
