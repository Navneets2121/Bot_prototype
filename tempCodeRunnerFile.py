
  while(True):
    msg=takeInput()
    result= bot(msg)
    reply=' '.join([str(item) for item in result])
    print(reply)
    if(msg== 'quit'):
      break