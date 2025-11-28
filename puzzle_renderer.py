"""
Puzzle Image Renderer
Creates beautiful, social media-ready Sudoku puzzle images with multi-language support
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import List, Tuple
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PuzzleRenderer:
    """Render Sudoku puzzles as beautiful images for social media."""
    
    # Image dimensions optimized for Instagram (1:1 ratio)
    IMAGE_SIZE = (1080, 1080)
    GRID_SIZE = 9
    
    # Modern color scheme
    COLORS = {
        'background': '#0F172A',  # Dark blue-gray
        'gradient_start': '#1E293B',
        'gradient_end': '#0F172A',
        'card_bg': '#1E293B',
        'grid_line': '#475569',
        'grid_thick': '#64748B',
        'number_given': '#F1F5F9',
        'number_empty': '#64748B',
        'accent': '#3B82F6',  # Bright blue
        'accent_gradient': '#8B5CF6',  # Purple
        'difficulty_easy': '#10B981',  # Green
        'difficulty_medium': '#F59E0B',  # Orange
        'difficulty_hard': '#EF4444',  # Red
        'difficulty_complex': '#A855F7'  # Purple
    }
    
    def __init__(self, fonts_dir: str = 'fonts'):
        """
        Initialize the renderer.
        
        Args:
            fonts_dir: Directory containing font files
        """
        self.fonts_dir = fonts_dir
        self._ensure_fonts()
    
    def _ensure_fonts(self) -> None:
        """Ensure font files exist or use system defaults."""
        if not os.path.exists(self.fonts_dir):
            os.makedirs(self.fonts_dir)
            logger.info(f"Created fonts directory: {self.fonts_dir}")
    
    def _get_font(self, size: int, bold: bool = False, script: str = 'Latin') -> ImageFont.FreeTypeFont:
        """
        Get appropriate font for the script.
        
        Args:
            size: Font size
            bold: Whether to use bold font
            script: Script type (Latin, Devanagari, Tamil, etc.)
            
        Returns:
            PIL Font object
        """
        # Try to find system fonts for each script
        system_fonts = {
            'Latin': ['arial.ttf', 'Arial.ttf', 'calibri.ttf', 'segoeui.ttf'],
            'Devanagari': ['NotoSansDevanagari-Regular.ttf', 'mangal.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf'],
            'Tamil': ['NotoSansTamil-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf'],
            'Telugu': ['NotoSansTelugu-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf'],
            'Bengali': ['NotoSansBengali-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf', 'vrinda.ttf'],
            'Gujarati': ['NotoSansGujarati-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf', 'shruti.ttf'],
            'Kannada': ['NotoSansKannada-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf', 'tunga.ttf'],
            'Malayalam': ['NotoSansMalayalam-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf', 'kartika.ttf'],
            'Gurmukhi': ['NotoSansGurmukhi-Regular.ttf', 'Nirmala.ttf', 'NirmalaUI.ttf', 'raavi.ttf'],
        }
        
        # Get font list for this script, fallback to Latin
        font_candidates = system_fonts.get(script, system_fonts['Latin'])
        
        # Try custom fonts directory first
        for font_name in font_candidates:
            font_path = os.path.join(self.fonts_dir, font_name)
            try:
                return ImageFont.truetype(font_path, size)
            except:
                pass
        
        # Try Windows system fonts
        windows_font_dirs = [
            'C:\\Windows\\Fonts',
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        ]
        
        for font_dir in windows_font_dirs:
            for font_name in font_candidates:
                font_path = os.path.join(font_dir, font_name)
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    pass
        
        # Last resort: try common system fonts
        for fallback in ['arial.ttf', 'segoeui.ttf', 'calibri.ttf']:
            try:
                return ImageFont.truetype(fallback, size)
            except:
                pass
        
        # Ultimate fallback
        logger.warning(f"No suitable font found for {script}, using PIL default")
        return ImageFont.load_default()
    
    def _create_gradient_background(self, size: Tuple[int, int]) -> Image.Image:
        """Create a gradient background."""
        img = Image.new('RGB', size, self.COLORS['background'])
        draw = ImageDraw.Draw(img)
        
        # Create vertical gradient
        for i in range(size[1]):
            ratio = i / size[1]
            # Interpolate between gradient colors
            color = self._interpolate_color(
                self.COLORS['gradient_start'],
                self.COLORS['gradient_end'],
                ratio
            )
            draw.line([(0, i), (size[0], i)], fill=color)
        
        return img
    
    def _interpolate_color(self, color1: str, color2: str, ratio: float) -> str:
        """Interpolate between two hex colors."""
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def render_puzzle(
        self,
        puzzle: List[List[int]],
        difficulty: str,
        puzzle_number: int,
        title: str = "Daily Sudoku",
        difficulty_label: str = None,
        script: str = 'Latin',
        output_path: str = 'puzzle.png'
    ) -> str:
        """
        Render a Sudoku puzzle as an image.
        
        Args:
            puzzle: 9x9 grid with puzzle (0 for empty cells)
            difficulty: Difficulty level
            puzzle_number: Puzzle number for display
            title: Title text
            difficulty_label: Difficulty label in local language
            script: Script type for text rendering
            output_path: Where to save the image
            
        Returns:
            Path to saved image
        """
        # Create base image with gradient
        img = self._create_gradient_background(self.IMAGE_SIZE)
        draw = ImageDraw.Draw(img)
        
        # Fonts
        title_font = self._get_font(48, bold=True, script=script)
        number_font = self._get_font(56, bold=True)
        label_font = self._get_font(32, bold=True, script=script)
        small_font = self._get_font(24, script=script)
        
        # Header
        header_y = 40
        draw.text(
            (self.IMAGE_SIZE[0] // 2, header_y),
            title,
            font=title_font,
            fill=self.COLORS['number_given'],
            anchor='mt'
        )
        
        # Difficulty badge
        difficulty_color = self.COLORS.get(f'difficulty_{difficulty}', self.COLORS['accent'])
        badge_y = header_y + 70
        badge_text = difficulty_label or difficulty.title()
        
        # Draw rounded rectangle for badge
        bbox = draw.textbbox((0, 0), badge_text, font=label_font)
        badge_width = bbox[2] - bbox[0] + 40
        badge_height = bbox[3] - bbox[1] + 20
        badge_x = (self.IMAGE_SIZE[0] - badge_width) // 2
        
        self._draw_rounded_rectangle(
            draw,
            (badge_x, badge_y, badge_x + badge_width, badge_y + badge_height),
            radius=20,
            fill=difficulty_color
        )
        
        draw.text(
            (self.IMAGE_SIZE[0] // 2, badge_y + badge_height // 2),
            badge_text,
            font=label_font,
            fill='#FFFFFF',
            anchor='mm'
        )
        
        # Sudoku grid
        grid_size = 650
        grid_x = (self.IMAGE_SIZE[0] - grid_size) // 2
        grid_y = badge_y + badge_height + 60
        
        # Draw grid card (elevated look)
        card_padding = 20
        self._draw_rounded_rectangle(
            draw,
            (
                grid_x - card_padding,
                grid_y - card_padding,
                grid_x + grid_size + card_padding,
                grid_y + grid_size + card_padding
            ),
            radius=15,
            fill=self.COLORS['card_bg']
        )
        
        # Draw grid
        cell_size = grid_size / self.GRID_SIZE
        
        # Draw grid lines
        for i in range(self.GRID_SIZE + 1):
            line_width = 4 if i % 3 == 0 else 1
            color = self.COLORS['grid_thick'] if i % 3 == 0 else self.COLORS['grid_line']
            
            # Horizontal lines
            y = grid_y + i * cell_size
            draw.line(
                [(grid_x, y), (grid_x + grid_size, y)],
                fill=color,
                width=line_width
            )
            
            # Vertical lines
            x = grid_x + i * cell_size
            draw.line(
                [(x, grid_y), (x, grid_y + grid_size)],
                fill=color,
                width=line_width
            )
        
        # Draw numbers
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if puzzle[i][j] != 0:
                    x = grid_x + (j + 0.5) * cell_size
                    y = grid_y + (i + 0.5) * cell_size
                    
                    draw.text(
                        (x, y),
                        str(puzzle[i][j]),
                        font=number_font,
                        fill=self.COLORS['number_given'],
                        anchor='mm'
                    )
        
        # Footer
        footer_y = grid_y + grid_size + card_padding + 40
        draw.text(
            (self.IMAGE_SIZE[0] // 2, footer_y),
            f"Puzzle #{puzzle_number}",
            font=small_font,
            fill=self.COLORS['number_empty'],
            anchor='mt'
        )
        
        # Save image
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        img.save(output_path, quality=95, optimize=True)
        logger.info(f"Saved puzzle image to {output_path}")
        
        return output_path
    
    def render_solution(
        self,
        solution: List[List[int]],
        puzzle: List[List[int]],
        difficulty: str,
        puzzle_number: int,
        title: str = "Solution",
        script: str = 'Latin',
        output_path: str = 'solution.png'
    ) -> str:
        """
        Render the solution with given numbers highlighted.
        
        Args:
            solution: Complete 9x9 grid
            puzzle: Original puzzle to identify given numbers
            difficulty: Difficulty level
            puzzle_number: Puzzle number
            title: Title text
            script: Script type
            output_path: Where to save
            
        Returns:
            Path to saved image
        """
        # Create base image
        img = self._create_gradient_background(self.IMAGE_SIZE)
        draw = ImageDraw.Draw(img)
        
        # Fonts
        title_font = self._get_font(48, bold=True, script=script)
        number_font = self._get_font(56, bold=True)
        
        # Header
        header_y = 60
        draw.text(
            (self.IMAGE_SIZE[0] // 2, header_y),
            title,
            font=title_font,
            fill=self.COLORS['number_given'],
            anchor='mt'
        )
        
        # Grid
        grid_size = 700
        grid_x = (self.IMAGE_SIZE[0] - grid_size) // 2
        grid_y = 200
        
        # Card background
        card_padding = 20
        self._draw_rounded_rectangle(
            draw,
            (
                grid_x - card_padding,
                grid_y - card_padding,
                grid_x + grid_size + card_padding,
                grid_y + grid_size + card_padding
            ),
            radius=15,
            fill=self.COLORS['card_bg']
        )
        
        # Draw grid and numbers
        cell_size = grid_size / self.GRID_SIZE
        
        for i in range(self.GRID_SIZE + 1):
            line_width = 4 if i % 3 == 0 else 1
            color = self.COLORS['grid_thick'] if i % 3 == 0 else self.COLORS['grid_line']
            
            y = grid_y + i * cell_size
            draw.line([(grid_x, y), (grid_x + grid_size, y)], fill=color, width=line_width)
            
            x = grid_x + i * cell_size
            draw.line([(x, grid_y), (x, grid_y + grid_size)], fill=color, width=line_width)
        
        # Draw numbers (highlight solved cells)
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                x = grid_x + (j + 0.5) * cell_size
                y = grid_y + (i + 0.5) * cell_size
                
                # Use accent color for solved numbers
                color = self.COLORS['number_given'] if puzzle[i][j] != 0 else self.COLORS['accent']
                
                draw.text(
                    (x, y),
                    str(solution[i][j]),
                    font=number_font,
                    fill=color,
                    anchor='mm'
                )
        
        # Save
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        img.save(output_path, quality=95, optimize=True)
        logger.info(f"Saved solution image to {output_path}")
        
        return output_path
    
    def _draw_rounded_rectangle(
        self,
        draw: ImageDraw.ImageDraw,
        coords: Tuple[int, int, int, int],
        radius: int,
        fill: str
    ) -> None:
        """Draw a rounded rectangle."""
        x1, y1, x2, y2 = coords
        
        # Draw rounded rectangle using ellipses and rectangles
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        
        # Corners
        draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
        draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
        draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
        draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)


if __name__ == "__main__":
    # Test the renderer
    from sudoku_generator import SudokuGenerator
    
    generator = SudokuGenerator()
    puzzle, solution = generator.create_puzzle('medium')
    
    renderer = PuzzleRenderer()
    
    # Render puzzle
    renderer.render_puzzle(
        puzzle=puzzle,
        difficulty='medium',
        puzzle_number=1,
        title="Daily Sudoku",
        difficulty_label="Medium",
        output_path='output/test_puzzle.png'
    )
    
    # Render solution
    renderer.render_solution(
        solution=solution,
        puzzle=puzzle,
        difficulty='medium',
        puzzle_number=1,
        title="Solution",
        output_path='output/test_solution.png'
    )
    
    print("Test images created successfully!")
