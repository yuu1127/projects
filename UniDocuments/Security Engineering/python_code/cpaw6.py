def SeeSDecript(text,key):
    ctext = ""
    for c in list(text):
        asc2 = ord(c)
        if asc2 >= ord("A") and asc2 <= ord("Z"):
            ctext += chr((asc2 - ord("A") - key) % 26 + ord("A"))
        elif asc2 >= ord("a") and asc2 <= ord("z"):
            ctext += chr((asc2 - ord("a") - key) % 26 + ord("a"))
        else:
            ctext += c
    return ctext

if __name__ == "__main__":
    text = "fsdz{Fdhvdu_flskhu_lv_fodvvlfdo_flskhu}"
    print(SeeSDecript(text,3))
