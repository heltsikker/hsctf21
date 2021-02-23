# AGENT69

This is a dotnet program. It plays horrible synthesized audio upon execution and expects a pin code. The idea here is to make people try to use dnspy/ilspy and you basically get complete decompiled code. 

See the image for the decompiled code. 

You dont have to guess the pincode, patch the if statement to succeed every time (the first if-statement, that is).

After this you get some beeps and boops, and guess what, its the flag represented as bytes, played as audio. Extract this sequence and convert to ascii. 
