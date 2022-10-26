import random
import string
import hashlib
import os
import rsa
import base64
from cryptography.fernet import Fernet
import cryptocode
import pyAesCrypt
#encryption as an importable module(using classes)
publicKey, privateKey = rsa.newkeys(512)


class nCrypt:
  
  def __init__(self):
    #fileEncrypt = self.fileEncrypt()
    pass
  class base64:
    def encrypt(input):
      message = input #get our given input
      message_bytes = message.encode('ascii')#encode the message to ascii
      base64_bytes = base64.b64encode(message_bytes) #convert the ascii encoded message to base64
      base64_message = base64_bytes.decode('ascii')#decode the base64 message of ascii
      finalOutput = base64_message[::-1] #flip the base64
      return finalOutput #output to variable

      
    def decrypt(input):
        finalInput = input[::-1]#flip base64 and return to regular
        base64message = finalInput #put it into another name
        base64bytes = base64message.encode('ascii')#encode the base64 with ascii
        message_bytes_output = base64.b64decode(base64bytes)#decode the base64
        output = message_bytes_output.decode('ascii')#decode the ascii
        return output #output to variable

  class cryptoCode:
    def encrypt(input, key):
      finalOutput = cryptocode.encrypt(input, key)
      return finalOutput  # output to variable

    def decrypt(input, key):
        output = cryptocode.decrypt(
            input, key)

        return output  # output to variable
  def getRandomString(self):
    letters = string.printable
    #return "hi"
    return ((''.join(random.choice(letters) for i in range(60)))+(''.join(random.choice(letters) for i in range(60)))).rstrip()
  class fileEncrypt:
    #def __init__(self):
    #  pass
    def encrypt(input, key):
      key = nCrypt.hash.hash(key)
      bufferSize = 128 * 1024
      pyAesCrypt.encryptFile(input, input+".aes", key, bufferSize)
    def decrypt(input, key):
      key = nCrypt.hash.hash(key)
      bufferSize = 128 * 1024
      input = input.rstrip(" ")
      outName = input[:-4]
      
      #print(outName)
      
      pyAesCrypt.decryptFile(
          input, outName, key, bufferSize)
      return outName
  class hash:
    def hash(input):
      from hashlib import blake2b


      h = blake2b()

      h.update(str.encode(input))

      hex_dig = h.hexdigest()
      #print(hex_dig)
      return hex_dig



