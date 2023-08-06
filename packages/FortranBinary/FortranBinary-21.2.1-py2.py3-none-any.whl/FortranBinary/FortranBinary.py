"""A file-derived class to read/write Fortran unformatted files."""

import struct
from io import FileIO

class FortranFile(FileIO):

     """File object with methods for dealing with FORTRAN unformatted data files"""

     def __init__(self,fname, mode='r'):
         """Open the file for writing, defaults to native endian."""
         FileIO.__init__(self, fname, mode)
         self.ENDIAN = '@'

     def setEndian(self,c):
         """Set endian to big (c='>') or little (c='<') or native (c='@')

         Args:
           c(string) : The endian-ness to use when reading from this file.
         """
         if c == '<' or c == '>' or c =='@' or c == '=':
             self.ENDIAN = c
         else:
             raise ValueError('Cannot set endian-ness')

     def readString(self):
         """Read in a string with error checking"""
         l = struct.unpack(self.ENDIAN+'i',self.read(4))[0]
         str = self.read(l)
         if  struct.unpack(self.ENDIAN+'i',self.read(4))[0] != l:
             raise IOError('Error reading string from data file')
         return str

     def writeString(self,s):
         """Write a string.

         Args:
           s(string): The string to write.
         """
         self.write(struct.pack(self.ENDIAN+'i',len(s)))
         self.write(s)
         self.write(struct.pack(self.ENDIAN+'i',len(s)))

     def readReals(self, prec='d'):
         """Read in an array of FORTRAN reals (given precision) with error checking.

         Args:
            prec(string): float precision (d: double, f: sinlge) of data. Defautls to "d".

         Returns:
            list of floats read.
         """

         if prec not in ['d','f']:
             raise ValueError('Unknown precision flag, use "d" for double or "f" for single precision.')

         b=self.read(4)
         if len(b)==0:
           return False
         else:
           l = struct.unpack(self.ENDIAN+'i',b)[0]
           data_str = self.read(l)
           len_real = struct.calcsize(prec)
           if l % len_real != 0:
             raise IOError('Error reading array of reals from data file')
           num = l//len_real
           reals = struct.unpack(self.ENDIAN+str(num)+prec,data_str)
           if struct.unpack(self.ENDIAN+'i',self.read(4))[0] != l:
             raise IOError('Error reading array of reals from data file')
           return list(reals)

     def writeReals(self, reals, prec='d'):
         """Write an array of FORTRAN reals in given precision.

         Args:
           reals(float array) : Data to write.
           prec(string): float precision do use (d: double, f: sinlge). Defautls to "d".
         """
         if prec not in ['d','f']: raise ValueError('Unknown precision flag, use "d" for double or "f" for single precision')
         num=len(reals)
         self.write(struct.pack(self.ENDIAN+'i',num*struct.calcsize(prec)))
         #for r in reals:
         #    self.write(struct.pack(self.ENDIAN+prec,r))
         self.write(struct.pack(self.ENDIAN+str(num)+prec,*reals))
         self.write(struct.pack(self.ENDIAN+'i',num*struct.calcsize(prec)))

     def readInts(self):
         """Read in an array of integers with error checking.

         Returns:
            list of integers read."""
         l = struct.unpack('i',self.read(4))[0]
         data_str = self.read(l)
         len_int = struct.calcsize('i')
         if l % len_int != 0:
             raise IOError('Error reading array of integers from data file')
         num = l//len_int
         ints = struct.unpack(str(num)+'i',data_str)
         if struct.unpack(self.ENDIAN+'i',self.read(4))[0] != l:
             raise IOError('Error reading array of integers from data file')
         return list(ints)

     def readRecord(self):
         """Read a single fortran record.

         Returns:
            Data record read."""
         l = struct.unpack(self.ENDIAN+'i',self.read(4))[0]
         data_str = self.read(l)
         # check length
         if len(data_str) != l:
             raise IOError("Didn't read enough data")
         check = self.read(4)
         if len(check) != 4:
             raise IOError("Didn't read enough data")
         if struct.unpack(self.ENDIAN+'i',check)[0] != l:
             raise IOError('Error reading record from data file')
         return data_str

     def readDirectAccessReals(self,prec='d'):
         """Read FORTRAN Reals from a direct access file.

         Args:
            prec(string): String identifying the precision used in input files

         Returns:
            Reals read from direct access file.
         """
         len_real=struct.calcsize("d")
         filesize=self.seek(0,2) #position at EoF
         self.seek(0,0) #rewind
         if filesize % len_real != 0:
             raise IOError('Error reading array of reals from data file')
         noR=filesize//len_real
         reals = struct.unpack(self.ENDIAN+str(noR)+prec,self.read(filesize))
         return reals
