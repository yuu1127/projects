def SeeSMac(text):
    dic = {"A":23,"B":47,"I":397,"L":507,"O":581,"P":635,"R":687,"U":763,"Y":901,"0":405,"1":73}
    output = 481
    for i in text:
        output += dic[i]
        output = 521 * output
        output = output % 10000
        output = output + 450
        output = output % 967
    return output
if __name__ == "__main__":
    text = "AU"
    text1 = "PAYBOB100"
    text2 = "PAYROB1000"
    textf = "AALPAYBOB1000"
    # print(SeeSMac(text1))
    # print(SeeSMac(text2))
    # print(SeeSMac(textf))
    print(SeeSMac("0"))