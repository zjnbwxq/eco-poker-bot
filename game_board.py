from PIL import Image, ImageDraw, ImageFont
import random
import io

class GameBoard:
    def __init__(self, size=6):
        self.size = size
        self.board = self.initialize_board()
        self.load_images()

    def initialize_board(self):
        environments = ['F', 'G', 'M', 'W']  # Forest, Grassland, Mountain, Water
        return [[random.choice(environments) for _ in range(self.size)] for _ in range(self.size)]

    def load_images(self):
        self.images = {
            'F': Image.open("assets/forest.png").convert("RGBA"),
            'G': Image.open("assets/grassland.png").convert("RGBA"),
            'M': Image.open("assets/mountain.png").convert("RGBA"),
            'W': Image.open("assets/water.png").convert("RGBA")
        }

    def create_board_image(self):
        cell_size = 100
        margin = 50  # Margin for labels
        image_size = self.size * cell_size + 2 * margin
        board_image = Image.new('RGB', (image_size, image_size), color='white')
        draw = ImageDraw.Draw(board_image)

        # Load a font
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except IOError:
            font = ImageFont.load_default()

        # Draw the grid and paste environment images
        for i in range(self.size):
            for j in range(self.size):
                x = j * cell_size + margin
                y = i * cell_size + margin
                env_type = self.board[i][j]
                
                # Paste the environment image
                env_image = self.images[env_type].resize((cell_size, cell_size))
                board_image.paste(env_image, (x, y), env_image)
                
                # Draw cell borders
                draw.rectangle([x, y, x + cell_size, y + cell_size], outline="black", width=2)

        # Draw row labels (1, 2, 3, ...)
        for i in range(self.size):
            draw.text((margin // 2, i * cell_size + margin + cell_size // 2), str(i+1), font=font, fill="black")

        # Draw column labels (A, B, C, ...)
        for j in range(self.size):
            draw.text((j * cell_size + margin + cell_size // 2, margin // 2), chr(65 + j), font=font, fill="black")

        img_byte_arr = io.BytesIO()
        board_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

# Test code
if __name__ == "__main__":
    game = GameBoard()
    img = game.create_board_image()
    with open("game_board.png", "wb") as f:
        f.write(img.getvalue())