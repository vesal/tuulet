from PIL import Image
import requests
from io import BytesIO
# import matplotlib.pyplot as plt


def get_rasp_wind(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "-"
    img = Image.open(BytesIO(response.content))

    # Muunna palettikuva RGB-muotoon
    if img.mode == 'P':
        img = img.convert('RGB')

    # Määritä alueen koordinaatit ja koko
    x, y = 534, 619
    width, height = 20, 20

    # Rajaa alue kuvasta
    cropped_img = img.crop((x, y, x + width, y + height))
    px, py, pwidth = 109, 956, 770
    palkki_img = img.crop((px, py, px + pwidth, py + 1))

    """
    plt.imshow(cropped_img)
    # plt.imshow(palkki_img)
    plt.axis('off') # Piilota akselit
    plt.show()
    """

    # Analysoi pikselit
    pixels = cropped_img.load()
    unique_colors = []
    for i in range(width):
        for j in range(height):
            color = pixels[i, j]
            # jos valkoinen tai painekäyrä, unohda
            if color == (255, 255, 255) or color == (133, 0, 98):
                continue
            if color not in unique_colors:
                unique_colors.append(color)

    # for color in unique_colors:
    #     print(color)

    pixels = palkki_img.load()
    wind = -2
    current_color = (0, 0, 0)
    winds = []
    for i in range(pwidth):
        color = pixels[i, 0]
        if color == (0, 0, 0):
            continue
        if color != current_color:
            wind += 2
            # print(i+px,wind)
            current_color = color
            if color in unique_colors:
                # print(color, wind)
                winds.append(wind)
    if len(winds) == 0:
        return "0"
    return f"{str(winds[0])}-{str(winds[-1] + 2)}"


def hae_rasp(tulos):
    times = ["09", "12", "15", "18"]
    for i, t in enumerate(times):
        tulos[i][1] = get_rasp_wind(f"http://ennuste.ilmailuliitto.fi/0/sfcwind.curr.{t}00lst.d2.png")


"""
def main():
    tulos = [["" for _ in range(17)] for _ in range(4)]
    hae_rasp(tulos)
    for rivi in tulos:
        print("\t".join(rivi))


if __name__ == "__main__":
    main()
"""