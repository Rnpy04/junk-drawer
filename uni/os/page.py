def translate_address(logical_address, page_size, base=10):
    if base == 16:
        logical_address = int(logical_address, 16)

    page_number = logical_address // page_size
    offset = logical_address % page_size

    return page_number, offset


# ورودی هگز
logical_address_hex = "0x45F3A0"
page_size = 8192

page, offset = translate_address(logical_address_hex, page_size, base=16)

print("Page Number:", page)
print("Offset (decimal):", offset)
print("Offset (hex):", hex(offset))
