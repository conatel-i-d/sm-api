import base64

def encode(text):
  enc = base64.b64encode(text.encode('UTF-8'))
  enc_result = str(enc, 'UTF-8')
  return enc_result

def decode(text):
  dec = base64.b64decode(text.encode('UTF-8'))
  dec_result = str(dec, 'UTF-8')
  return dec_result