import cairosvg

def convert_svg_to_png(input_file, output_file):
    cairosvg.svg2png(url=input_file, write_to=output_file)

# 示例用法
input_file = "face.svg"
output_file = "face.png"
convert_svg_to_png(input_file, output_file)
