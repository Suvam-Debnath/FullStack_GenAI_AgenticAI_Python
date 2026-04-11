import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")
text = "Hello, I am Suvam Debnath."
tokens = encoding.encode(text)

#Tokens: [13225, 11, 357, 939, 3893, 105737, 18659, 77, 725, 13]
print("Tokens:", tokens)

decoded_text = encoding.decode([13225, 11, 357, 939, 3893, 105737, 18659, 77, 725, 13])
print("Decoded Text:", decoded_text)