def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]
