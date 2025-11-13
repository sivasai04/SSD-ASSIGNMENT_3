# """
# Kaooa Board Game (Vulture and Crows)
# A traditional Indian board game implemented using Python Turtle graphics.

# Rules:
# - 1 Vulture vs 7 Crows on a 10-node pentagram board
# - Phase 1: Crow places 1 piece, Vulture places 1 piece
# - Phase 2: Crows place remaining 6 pieces, Vulture moves
# - Phase 3: All pieces can move
# - Vulture MUST jump when possible (compulsory capture)
# - Vulture wins by capturing 4 crows
# - Crows win by trapping the vulture
# """

# import turtle
# import math
# from typing import Dict, List, Tuple, Optional

# # --- Constants ---
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 800
# PIECE_RADIUS = 22
# NODE_DOT_RADIUS = 12

# # Player types
# EMPTY = "EMPTY"
# VULTURE = "VULTURE"
# KAOOA = "KAOOA"

# # Color scheme - Beautiful gradients and modern colors
# BOARD_BG = "#FFF5E6"
# LINE_COLOR = "#8B7355"
# LINE_HIGHLIGHT = "#D4A574"
# NODE_COLOR = "#F5DEB3"
# NODE_BORDER = "#8B7355"

# VULTURE_COLOR = "#DC143C"
# VULTURE_BORDER = "#8B0000"
# VULTURE_INNER = "#FF6B6B"

# KAOOA_COLOR = "#00CED1"
# KAOOA_BORDER = "#008B8B"
# KAOOA_INNER = "#7FFFD4"

# HIGHLIGHT_COLOR = "#FFD700"
# JUMP_HIGHLIGHT_COLOR = "#FF8C00"
# SELECTED_GLOW = "#FFFF00"

# # Game Phases
# PHASE_CROW_PLACE_1 = "PHASE_CROW_PLACE_1"
# PHASE_VULTURE_PLACE = "PHASE_VULTURE_PLACE"
# PHASE_ALTERNATE_DROP = "PHASE_ALTERNATE_DROP"
# PHASE_MOVE = "PHASE_MOVE"
# PHASE_GAME_OVER = "PHASE_GAME_OVER"

# # --- Board Geometry ---
# OUTER_RADIUS = 240
# INNER_RADIUS = 145

# def calculate_node_coords():
#     """Calculate coordinates for the 10-node pentagram."""
#     coords = {}
    
#     # Outer 5 points (0-4)
#     coords[0] = (0, OUTER_RADIUS)  # Top
#     coords[1] = (OUTER_RADIUS * math.cos(math.radians(18)), 
#                  OUTER_RADIUS * math.sin(math.radians(18)))
#     coords[2] = (OUTER_RADIUS * math.cos(math.radians(-54)), 
#                  OUTER_RADIUS * math.sin(math.radians(-54)))
#     coords[3] = (OUTER_RADIUS * math.cos(math.radians(-126)), 
#                  OUTER_RADIUS * math.sin(math.radians(-126)))
#     coords[4] = (OUTER_RADIUS * math.cos(math.radians(-198)), 
#                  OUTER_RADIUS * math.sin(math.radians(-198)))
    
#     # Inner 5 points (5-9)
#     coords[5] = (INNER_RADIUS * math.cos(math.radians(54)), 
#                  INNER_RADIUS * math.sin(math.radians(54)))
#     coords[6] = (INNER_RADIUS * math.cos(math.radians(-18)), 
#                  INNER_RADIUS * math.sin(math.radians(-18)))
#     coords[7] = (0, -INNER_RADIUS)
#     coords[8] = (INNER_RADIUS * math.cos(math.radians(-162)), 
#                  INNER_RADIUS * math.sin(math.radians(-162)))
#     coords[9] = (INNER_RADIUS * math.cos(math.radians(126)), 
#                  INNER_RADIUS * math.sin(math.radians(126)))
    
#     return coords

# NODE_COORDS = calculate_node_coords()

# # Adjacency list for valid moves
# NODE_CONNECTIONS = {
#     0: [1, 4, 5, 9],
#     1: [0, 2, 5, 6],
#     2: [1, 3, 6, 7],
#     3: [2, 4, 7, 8],
#     4: [3, 0, 8, 9],
#     5: [0, 1, 6, 9],
#     6: [1, 2, 5, 7],
#     7: [2, 3, 6, 8],
#     8: [3, 4, 7, 9],
#     9: [4, 0, 8, 5],
# }

# # Vulture jump paths (from, over, to)
# VULTURE_JUMPS = [
#     (1, 5, 9), (9, 5, 1),
#     (2, 6, 5), (5, 6, 2),
#     (3, 7, 6), (6, 7, 3),
#     (4, 8, 7), (7, 8, 4),
#     (0, 9, 8), (8, 9, 0),
# ]


# class KaooaGame:
#     """Main game class managing state and graphics."""
    
#     def __init__(self):
#         self.screen = turtle.Screen()
#         self.screen.title("🦅 Kaooa - Vulture and Crows 🐦")
#         self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
#         self.screen.bgcolor(BOARD_BG)
#         self.screen.tracer(0)
        
#         # Create turtle objects
#         self.board_drawer = turtle.Turtle()
#         self.board_drawer.hideturtle()
#         self.board_drawer.speed(0)
        
#         self.piece_drawer = turtle.Turtle()
#         self.piece_drawer.hideturtle()
#         self.piece_drawer.speed(0)
        
#         self.message_writer = turtle.Turtle()
#         self.message_writer.hideturtle()
#         self.message_writer.penup()
#         self.message_writer.goto(0, SCREEN_HEIGHT / 2 - 80)
        
#         self.info_writer = turtle.Turtle()
#         self.info_writer.hideturtle()
#         self.info_writer.penup()
        
#         self.title_writer = turtle.Turtle()
#         self.title_writer.hideturtle()
#         self.title_writer.penup()
#         self.title_writer.goto(0, SCREEN_HEIGHT / 2 - 40)
        
#         self.setup_game()
#         self.draw_title()
#         self.draw_board()
#         self.draw_pieces()
#         self.screen.onclick(self.handle_click)
#         self.screen.update()
    
#     def setup_game(self):
#         """Initialize game state."""
#         self.board_state = {i: EMPTY for i in range(10)}
#         self.game_phase = PHASE_CROW_PLACE_1
#         self.turn = KAOOA
#         self.crows_placed = 0
#         self.kaooas_captured = 0
#         self.selected_node = None
#         self.available_jumps = []
#         self.update_message("🐦 KAOOA: Place your first piece on any node")
#         self.update_info()
    
#     def draw_title(self):
#         """Draw the game title."""
#         self.title_writer.clear()
#         self.title_writer.color("#8B4513")
#         self.title_writer.write("KAOOA", align="center", font=("Arial", 28, "bold"))
    
#     def draw_board(self):
#         """Draw the beautiful pentagram board."""
#         self.board_drawer.clear()
        
#         # Draw decorative background circle
#         self.board_drawer.penup()
#         self.board_drawer.goto(0, -OUTER_RADIUS - 40)
#         self.board_drawer.color("#FFE4B5", "#FFF8DC")
#         self.board_drawer.begin_fill()
#         self.board_drawer.circle(OUTER_RADIUS + 40)
#         self.board_drawer.end_fill()
        
#         # Draw shadow effect for lines
#         drawn = set()
#         for node, connections in NODE_CONNECTIONS.items():
#             for conn in connections:
#                 edge = tuple(sorted([node, conn]))
#                 if edge not in drawn:
#                     drawn.add(edge)
#                     x1, y1 = NODE_COORDS[node]
#                     x2, y2 = NODE_COORDS[conn]
                    
#                     # Shadow
#                     self.board_drawer.penup()
#                     self.board_drawer.goto(x1 + 2, y1 - 2)
#                     self.board_drawer.pendown()
#                     self.board_drawer.color("#D2B48C")
#                     self.board_drawer.width(5)
#                     self.board_drawer.goto(x2 + 2, y2 - 2)
        
#         # Draw main lines with gradient effect
#         drawn = set()
#         for node, connections in NODE_CONNECTIONS.items():
#             for conn in connections:
#                 edge = tuple(sorted([node, conn]))
#                 if edge not in drawn:
#                     drawn.add(edge)
#                     x1, y1 = NODE_COORDS[node]
#                     x2, y2 = NODE_COORDS[conn]
                    
#                     # Main line
#                     self.board_drawer.penup()
#                     self.board_drawer.goto(x1, y1)
#                     self.board_drawer.pendown()
#                     self.board_drawer.color(LINE_COLOR)
#                     self.board_drawer.width(4)
#                     self.board_drawer.goto(x2, y2)
                    
#                     # Highlight overlay
#                     self.board_drawer.penup()
#                     self.board_drawer.goto(x1, y1)
#                     self.board_drawer.pendown()
#                     self.board_drawer.color(LINE_HIGHLIGHT)
#                     self.board_drawer.width(2)
#                     self.board_drawer.goto(x2, y2)
        
#         # Draw beautiful nodes with gradient effect
#         for i in range(10):
#             x, y = NODE_COORDS[i]
            
#             # Node shadow
#             self.board_drawer.penup()
#             self.board_drawer.goto(x + 2, y - NODE_DOT_RADIUS - 2)
#             self.board_drawer.color("#C0C0C0", "#D3D3D3")
#             self.board_drawer.begin_fill()
#             self.board_drawer.circle(NODE_DOT_RADIUS)
#             self.board_drawer.end_fill()
            
#             # Node outer circle
#             self.board_drawer.penup()
#             self.board_drawer.goto(x, y - NODE_DOT_RADIUS)
#             self.board_drawer.color(NODE_BORDER, NODE_COLOR)
#             self.board_drawer.width(2)
#             self.board_drawer.begin_fill()
#             self.board_drawer.circle(NODE_DOT_RADIUS)
#             self.board_drawer.end_fill()
            
#             # Node inner highlight
#             self.board_drawer.penup()
#             self.board_drawer.goto(x, y - NODE_DOT_RADIUS // 2)
#             self.board_drawer.color("#FFFACD")
#             self.board_drawer.begin_fill()
#             self.board_drawer.circle(NODE_DOT_RADIUS // 2)
#             self.board_drawer.end_fill()
    
#     def draw_pieces(self):
#         """Draw all pieces with beautiful effects."""
#         self.piece_drawer.clear()
        
#         # Draw pieces
#         for node, piece in self.board_state.items():
#             x, y = NODE_COORDS[node]
#             if piece == VULTURE:
#                 self.draw_vulture_piece(x, y)
#             elif piece == KAOOA:
#                 self.draw_kaooa_piece(x, y)
        
#         # Highlight selected piece with pulsing glow
#         if self.selected_node is not None:
#             x, y = NODE_COORDS[self.selected_node]
#             # Outer glow
#             for i in range(3):
#                 radius = PIECE_RADIUS + 8 + i * 3
#                 self.draw_circle_outline(x, y, radius, SELECTED_GLOW, 2)
#             # Inner highlight
#             self.draw_circle_outline(x, y, PIECE_RADIUS + 5, HIGHLIGHT_COLOR, 4)
        
#         # Highlight compulsory jumps with animated effect
#         if self.turn == VULTURE and self.available_jumps:
#             for (from_n, over_n, to_n) in self.available_jumps:
#                 fx, fy = NODE_COORDS[from_n]
#                 tx, ty = NODE_COORDS[to_n]
                
#                 # Pulsing circles for jump targets
#                 for i in range(2):
#                     self.draw_circle_outline(fx, fy, PIECE_RADIUS + 8 + i * 4, 
#                                             JUMP_HIGHLIGHT_COLOR, 3)
#                     self.draw_circle_outline(tx, ty, PIECE_RADIUS + i * 4, 
#                                             JUMP_HIGHLIGHT_COLOR, 3)
                
#                 # Arrow from source to destination
#                 self.piece_drawer.penup()
#                 self.piece_drawer.goto(fx, fy)
#                 self.piece_drawer.pendown()
#                 self.piece_drawer.color(JUMP_HIGHLIGHT_COLOR)
#                 self.piece_drawer.width(2)
#                 self.piece_drawer.goto(tx, ty)
        
#         self.screen.update()
    
#     def draw_vulture_piece(self, x, y):
#         """Draw a beautiful vulture piece."""
#         # Shadow
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x + 2, y - PIECE_RADIUS - 2)
#         self.piece_drawer.color("#696969", "#808080")
#         self.piece_drawer.begin_fill()
#         self.piece_drawer.circle(PIECE_RADIUS)
#         self.piece_drawer.end_fill()
        
#         # Outer circle
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x, y - PIECE_RADIUS)
#         self.piece_drawer.color(VULTURE_BORDER, VULTURE_COLOR)
#         self.piece_drawer.width(3)
#         self.piece_drawer.begin_fill()
#         self.piece_drawer.circle(PIECE_RADIUS)
#         self.piece_drawer.end_fill()
        
#         # Inner gradient circle
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x, y - PIECE_RADIUS // 2)
#         self.piece_drawer.color(VULTURE_INNER)
#         self.piece_drawer.begin_fill()
#         self.piece_drawer.circle(PIECE_RADIUS // 2)
#         self.piece_drawer.end_fill()
        
#         # Highlight dot
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x - 5, y + 5)
#         self.piece_drawer.color("white")
#         self.piece_drawer.dot(6)
    
#     def draw_kaooa_piece(self, x, y):
#         """Draw a beautiful kaooa/crow piece."""
#         # Shadow
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x + 2, y - PIECE_RADIUS - 2)
#         self.piece_drawer.color("#696969", "#808080")
#         self.piece_drawer.begin_fill()
#         self.piece_drawer.circle(PIECE_RADIUS)
#         self.piece_drawer.end_fill()
        
#         # Outer circle
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x, y - PIECE_RADIUS)
#         self.piece_drawer.color(KAOOA_BORDER, KAOOA_COLOR)
#         self.piece_drawer.width(3)
#         self.piece_drawer.begin_fill()
#         self.piece_drawer.circle(PIECE_RADIUS)
#         self.piece_drawer.end_fill()
        
#         # Inner gradient circle
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x, y - PIECE_RADIUS // 2)
#         self.piece_drawer.color(KAOOA_INNER)
#         self.piece_drawer.begin_fill()
#         self.piece_drawer.circle(PIECE_RADIUS // 2)
#         self.piece_drawer.end_fill()
        
#         # Highlight dot
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x - 5, y + 5)
#         self.piece_drawer.color("white")
#         self.piece_drawer.dot(6)
    
#     def draw_circle_outline(self, x, y, radius, color, width):
#         """Draw a circle outline."""
#         self.piece_drawer.penup()
#         self.piece_drawer.goto(x, y - radius)
#         self.piece_drawer.pendown()
#         self.piece_drawer.color(color)
#         self.piece_drawer.width(width)
#         self.piece_drawer.circle(radius)
#         self.piece_drawer.width(1)
    
#     def update_message(self, text):
#         """Update the main message display."""
#         self.message_writer.clear()
#         self.message_writer.color("#4B0082")
#         self.message_writer.write(text, align="center", font=("Arial", 14, "bold"))
    
#     def update_info(self):
#         """Update game info display with beautiful formatting."""
#         self.info_writer.clear()
        
#         # Vulture info (left side)
#         self.info_writer.goto(-200, -SCREEN_HEIGHT / 2 + 80)
#         self.info_writer.color(VULTURE_COLOR)
#         self.info_writer.write("🦅 VULTURE", align="center", font=("Arial", 12, "bold"))
        
#         self.info_writer.goto(-200, -SCREEN_HEIGHT / 2 + 60)
#         self.info_writer.color("#4B0082")
#         self.info_writer.write(f"Captured: {self.kaooas_captured}/4", 
#                               align="center", font=("Arial", 11, "normal"))
        
#         # Draw vulture icon
#         self.info_writer.goto(-200, -SCREEN_HEIGHT / 2 + 35)
#         self.draw_mini_vulture(-200, -SCREEN_HEIGHT / 2 + 40)
        
#         # Kaooa info (right side)
#         self.info_writer.goto(200, -SCREEN_HEIGHT / 2 + 80)
#         self.info_writer.color(KAOOA_COLOR)
#         self.info_writer.write("🐦 CROWS", align="center", font=("Arial", 12, "bold"))
        
#         self.info_writer.goto(200, -SCREEN_HEIGHT / 2 + 60)
#         self.info_writer.color("#4B0082")
#         self.info_writer.write(f"On Board: {self.crows_placed}/7", 
#                               align="center", font=("Arial", 11, "normal"))
        
#         # Draw kaooa icon
#         self.info_writer.goto(200, -SCREEN_HEIGHT / 2 + 35)
#         self.draw_mini_kaooa(200, -SCREEN_HEIGHT / 2 + 40)
        
#         # Phase indicator
#         phase_text = ""
#         if self.game_phase == PHASE_CROW_PLACE_1:
#             phase_text = "Phase 1: Initial Placement"
#         elif self.game_phase == PHASE_VULTURE_PLACE:
#             phase_text = "Phase 1: Vulture Placement"
#         elif self.game_phase == PHASE_ALTERNATE_DROP:
#             phase_text = "Phase 2: Crow Placement"
#         elif self.game_phase == PHASE_MOVE:
#             phase_text = "Phase 3: Full Movement"
#         elif self.game_phase == PHASE_GAME_OVER:
#             phase_text = "Game Over"
        
#         self.info_writer.goto(0, -SCREEN_HEIGHT / 2 + 50)
#         self.info_writer.color("#8B4513")
#         self.info_writer.write(phase_text, align="center", font=("Arial", 10, "italic"))
    
#     def draw_mini_vulture(self, x, y):
#         """Draw mini vulture icon."""
#         self.info_writer.goto(x, y - 10)
#         self.info_writer.pendown()
#         self.info_writer.color(VULTURE_BORDER, VULTURE_COLOR)
#         self.info_writer.begin_fill()
#         self.info_writer.circle(10)
#         self.info_writer.end_fill()
#         self.info_writer.penup()
    
#     def draw_mini_kaooa(self, x, y):
#         """Draw mini kaooa icon."""
#         self.info_writer.goto(x, y - 10)
#         self.info_writer.pendown()
#         self.info_writer.color(KAOOA_BORDER, KAOOA_COLOR)
#         self.info_writer.begin_fill()
#         self.info_writer.circle(10)
#         self.info_writer.end_fill()
#         self.info_writer.penup()
    
#     def get_node_at(self, x, y):
#         """Find which node was clicked."""
#         for node, (nx, ny) in NODE_COORDS.items():
#             dist = math.sqrt((x - nx)**2 + (y - ny)**2)
#             if dist < PIECE_RADIUS + 15:
#                 return node
#         return None
    
#     def handle_click(self, x, y):
#         """Handle mouse click events."""
#         if self.game_phase == PHASE_GAME_OVER:
#             self.setup_game()
#             self.draw_board()
#             self.draw_pieces()
#             return
        
#         clicked_node = self.get_node_at(x, y)
#         if clicked_node is None:
#             self.selected_node = None
#             self.draw_pieces()
#             return
        
#         # Route to appropriate handler based on phase
#         if self.game_phase == PHASE_CROW_PLACE_1:
#             self.handle_crow_place_1(clicked_node)
#         elif self.game_phase == PHASE_VULTURE_PLACE:
#             self.handle_vulture_place(clicked_node)
#         elif self.game_phase == PHASE_ALTERNATE_DROP:
#             if self.turn == KAOOA:
#                 self.handle_crow_drop(clicked_node)
#             else:
#                 self.handle_vulture_move(clicked_node)
#         elif self.game_phase == PHASE_MOVE:
#             if self.turn == KAOOA:
#                 self.handle_kaooa_move(clicked_node)
#             else:
#                 self.handle_vulture_move(clicked_node)
        
#         self.draw_pieces()
#         self.update_info()
    
#     def handle_crow_place_1(self, node):
#         """Handle first crow placement."""
#         if self.board_state[node] == EMPTY:
#             self.board_state[node] = KAOOA
#             self.crows_placed = 1
#             self.game_phase = PHASE_VULTURE_PLACE
#             self.turn = VULTURE
#             self.update_message("🦅 VULTURE: Place your piece on any empty node")
#         else:
#             self.update_message("🐦 KAOOA: Invalid. Choose an empty node")
    
#     def handle_vulture_place(self, node):
#         """Handle vulture placement."""
#         if self.board_state[node] == EMPTY:
#             self.board_state[node] = VULTURE
#             self.game_phase = PHASE_ALTERNATE_DROP
#             self.turn = KAOOA
#             self.update_message(f"🐦 KAOOA: Place a piece ({7 - self.crows_placed} remaining)")
#         else:
#             self.update_message("🦅 VULTURE: Invalid. Choose an empty node")
    
#     def handle_crow_drop(self, node):
#         """Handle crow placement during drop phase."""
#         if self.board_state[node] == EMPTY:
#             self.board_state[node] = KAOOA
#             self.crows_placed += 1
            
#             if self.crows_placed == 7:
#                 self.game_phase = PHASE_MOVE
            
#             self.turn = VULTURE
#             self.update_vulture_status()
#         else:
#             self.update_message("🐦 KAOOA: Invalid. Choose an empty node")
    
#     def handle_kaooa_move(self, node):
#         """Handle crow movement in move phase."""
#         if self.selected_node is None:
#             if self.board_state[node] == KAOOA:
#                 self.selected_node = node
#             else:
#                 self.update_message("🐦 KAOOA: Select a crow (cyan piece)")
#         else:
#             if self.is_valid_adjacent_move(self.selected_node, node):
#                 self.board_state[self.selected_node] = EMPTY
#                 self.board_state[node] = KAOOA
#                 self.selected_node = None
#                 self.turn = VULTURE
#                 self.update_vulture_status()
#             else:
#                 self.update_message("🐦 KAOOA: Invalid move. Must move to adjacent empty node")
#                 self.selected_node = None
    
#     def handle_vulture_move(self, node):
#         """Handle vulture movement."""
#         if self.selected_node is None:
#             if self.board_state[node] == VULTURE:
#                 self.selected_node = node
#             else:
#                 self.update_message("🦅 VULTURE: Select the vulture (red piece)")
#         else:
#             # Check for compulsory jump
#             if self.available_jumps:
#                 jump = self.is_valid_jump(self.selected_node, node)
#                 if jump:
#                     from_n, over_n, to_n = jump
#                     self.board_state[from_n] = EMPTY
#                     self.board_state[over_n] = EMPTY
#                     self.board_state[to_n] = VULTURE
#                     self.kaooas_captured += 1
#                     self.selected_node = None
                    
#                     if self.kaooas_captured >= 4:
#                         self.game_over(VULTURE)
#                     else:
#                         self.turn = KAOOA
#                         self.update_kaooa_status()
#                 else:
#                     self.update_message("🦅 VULTURE: Must take the compulsory jump!")
#                     self.selected_node = None
#             else:
#                 # Regular move
#                 if self.is_valid_adjacent_move(self.selected_node, node):
#                     self.board_state[self.selected_node] = EMPTY
#                     self.board_state[node] = VULTURE
#                     self.selected_node = None
#                     self.turn = KAOOA
#                     self.update_kaooa_status()
#                 else:
#                     self.update_message("🦅 VULTURE: Invalid move. Must move to adjacent empty node")
#                     self.selected_node = None
    
#     def is_valid_adjacent_move(self, from_node, to_node):
#         """Check if a move is valid (adjacent and empty)."""
#         return (to_node in NODE_CONNECTIONS[from_node] and 
#                 self.board_state[to_node] == EMPTY)
    
#     def get_vulture_pos(self):
#         """Find the vulture's position."""
#         for node, piece in self.board_state.items():
#             if piece == VULTURE:
#                 return node
#         return None
    
#     def get_all_vulture_jumps(self):
#         """Find all valid jumps for the vulture."""
#         jumps = []
#         for (n1, n_mid, n2) in VULTURE_JUMPS:
#             if (self.board_state[n1] == VULTURE and
#                 self.board_state[n_mid] == KAOOA and
#                 self.board_state[n2] == EMPTY):
#                 jumps.append((n1, n_mid, n2))
#             if (self.board_state[n1] == EMPTY and
#                 self.board_state[n_mid] == KAOOA and
#                 self.board_state[n2] == VULTURE):
#                 jumps.append((n2, n_mid, n1))
#         return jumps
    
#     def get_all_vulture_moves(self):
#         """Find all valid regular moves for the vulture."""
#         pos = self.get_vulture_pos()
#         if pos is None:
#             return []
#         moves = []
#         for conn in NODE_CONNECTIONS[pos]:
#             if self.board_state[conn] == EMPTY:
#                 moves.append((pos, conn))
#         return moves
    
#     def is_valid_jump(self, from_node, to_node):
#         """Check if a specific jump is valid."""
#         for (f, o, t) in self.available_jumps:
#             if f == from_node and t == to_node:
#                 return (f, o, t)
#         return None
    
#     def update_vulture_status(self):
#         """Update status for vulture's turn."""
#         self.available_jumps = self.get_all_vulture_jumps()
#         vulture_moves = self.get_all_vulture_moves()
        
#         # Check if vulture is trapped
#         if not self.available_jumps and not vulture_moves:
#             self.game_over(KAOOA)
#             return
        
#         if self.available_jumps:
#             self.update_message("🦅 VULTURE: ⚡ COMPULSORY JUMP! You must capture a crow")
#         else:
#             self.update_message("🦅 VULTURE: Your move")
    
#     def update_kaooa_status(self):
#         """Update status for crow's turn."""
#         if self.game_phase == PHASE_ALTERNATE_DROP:
#             remaining = 7 - self.crows_placed
#             self.update_message(f"🐦 KAOOA: Place a piece ({remaining} remaining)")
#         else:
#             self.update_message("🐦 KAOOA: Your move")
    
#     def game_over(self, winner):
#         """End the game."""
#         self.game_phase = PHASE_GAME_OVER
#         self.selected_node = None
#         self.available_jumps = []
        
#         if winner == VULTURE:
#             self.update_message("🎉 VULTURE WINS! 🦅 (4 crows captured) - Click to restart")
#         else:
#             self.update_message("🎉 CROWS WIN! 🐦 (Vulture trapped) - Click to restart")
    
#     def run(self):
#         """Start the game loop."""
#         try:
#             turtle.done()
#         except turtle.Terminator:
#             pass


# def main():
#     """Main entry point."""
#     game = KaooaGame()
#     game.run()


# if __name__ == "__main__":
#     main()







"""
Kaooa - Vulture & Crows 🦅🐦
10-point star version using built-in turtle shapes.
"""

import turtle
import math

# ---------- CONFIG ----------
SCREEN_W, SCREEN_H = 900, 900
NODE_R = 12
STAR_R_OUT = 250
STAR_R_IN = 100

EMPTY = "EMPTY"
VULTURE = "VULTURE"
CROW = "CROW"

BOARD_BG = "#FFF5E6"
LINE_COLOR = "#8B4513"

# ---------- GEOMETRY ----------
def make_star_coords():
    """Return dict of 10 (x,y) coordinates forming a 5-point star."""
    coords = {}
    # outer vertices (0-4)
    for i in range(5):
        ang = math.radians(90 + i * 72)
        coords[i] = (STAR_R_OUT * math.cos(ang), STAR_R_OUT * math.sin(ang))
    # inner pentagon vertices (5-9)
    for i in range(5):
        ang = math.radians(90 + 36 + i * 72)
        coords[5 + i] = (STAR_R_IN * math.cos(ang), STAR_R_IN * math.sin(ang))
    return coords

NODE_POS = make_star_coords()

# connections following the real Kaooa 10-point star
CONN = {
    0: [5, 6, 9],
    1: [6, 7, 5],
    2: [7, 8, 6],
    3: [8, 9, 7],
    4: [9, 5, 8],
    5: [0, 1, 4, 6, 9],
    6: [0, 1, 2, 5, 7],
    7: [1, 2, 3, 6, 8],
    8: [2, 3, 4, 7, 9],
    9: [0, 3, 4, 5, 8],
}

# ---------- GAME ----------
class Kaooa:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Kaooa - Vulture & Crows (10-Point Star)")
        self.screen.setup(SCREEN_W, SCREEN_H)
        self.screen.bgcolor(BOARD_BG)
        self.screen.tracer(0)

        # No image registration needed anymore
        
        self.drawer = turtle.Turtle(visible=False)
        self.drawer.speed(0)

        self.tokens = {}  # node → turtle
        self.board = {i: EMPTY for i in NODE_POS}
        self.turn = CROW
        self.phase = "PLACE_CROW1"
        self.crows = 0
        self.captured = 0
        self.selected = None

        self.msg = turtle.Turtle(visible=False)
        self.msg.penup()
        self.msg.goto(0, 350)

        self.draw_board()
        self.update_msg("🐦 Crows: place your first crow")
        self.screen.onclick(self.click)
        self.screen.update()

    # ---------- DRAW ----------
    def draw_board(self):
        self.drawer.color(LINE_COLOR)
        self.drawer.width(3)
        drawn = set()
        for a, links in CONN.items():
            x1, y1 = NODE_POS[a]
            for b in links:
                if (b, a) in drawn:
                    continue
                drawn.add((a, b))
                x2, y2 = NODE_POS[b]
                self.drawer.penup()
                self.drawer.goto(x1, y1)
                self.drawer.pendown()
                self.drawer.goto(x2, y2)
        # nodes
        for i, (x, y) in NODE_POS.items():
            self.drawer.penup()
            self.drawer.goto(x, y - NODE_R)
            self.drawer.pendown()
            self.drawer.begin_fill()
            self.drawer.circle(NODE_R)
            self.drawer.end_fill()

    # ---------- HELPERS ----------
    def node_at(self, x, y):
        for n, (nx, ny) in NODE_POS.items():
            if math.dist((x, y), (nx, ny)) < 20:
                return n
        return None

    def place_image(self, node, piece_type):
        """Places a shape on the board based on piece type."""
        if node in self.tokens:
            self.tokens[node].hideturtle()
            del self.tokens[node]
        
        t = turtle.Turtle()
        t.penup()
        t.speed(0)
        x, y = NODE_POS[node]
        t.goto(x, y) # Center the shape on the node

        if piece_type == VULTURE:
            t.shape("triangle")
            t.color("black")
            t.shapesize(1.3) # Make vulture slightly larger
        else: # CROW
            t.shape("circle")
            t.color("#404040") # Dark gray
            t.shapesize(1.0)
        
        self.tokens[node] = t

    def remove_image(self, node):
        if node in self.tokens:
            self.tokens[node].hideturtle()
            del self.tokens[node]

    def update_msg(self, text):
        self.msg.clear()
        self.msg.color("#4B0082")
        self.msg.write(text, align="center", font=("Arial", 16, "bold"))
        self.screen.update()

    # ---------- INPUT ----------
    def click(self, x, y):
        n = self.node_at(x, y)
        if n is None:
            return
        if self.phase == "PLACE_CROW1":
            self.place_first_crow(n)
        elif self.phase == "PLACE_VULTURE":
            self.place_vulture(n)
        elif self.phase == "PLACE_CROWS":
            if self.turn == CROW:
                self.place_next_crow(n)
            else:
                self.move_vulture(n)
        elif self.phase == "PLAY":
            if self.turn == CROW:
                self.move_crow(n)
            else:
                self.move_vulture(n)

    # ---------- GAMEPLAY ----------
    def place_first_crow(self, n):
        if self.board[n] == EMPTY:
            self.board[n] = CROW
            self.place_image(n, CROW) # <-- CHANGED
            self.crows = 1
            self.turn = VULTURE
            self.phase = "PLACE_VULTURE"
            self.update_msg("🦅 Vulture: place your piece")
        else:
            self.update_msg("🐦 Invalid: occupied")

    def place_vulture(self, n):
        if self.board[n] == EMPTY:
            self.board[n] = VULTURE
            self.place_image(n, VULTURE) # <-- CHANGED
            self.turn = CROW
            self.phase = "PLACE_CROWS"
            self.update_msg("🐦 Crows: place remaining pieces")
        else:
            self.update_msg("🦅 Invalid: occupied")

    def place_next_crow(self, n):
        if self.board[n] == EMPTY:
            self.board[n] = CROW
            self.place_image(n, CROW) # <-- CHANGED
            self.crows += 1
            if self.crows == 7:
                self.phase = "PLAY"
            self.turn = VULTURE
            self.update_msg("🦅 Vulture: move or jump")
        else:
            self.update_msg("🐦 Invalid: occupied")

    def move_crow(self, n):
        if self.selected is None:
            if self.board[n] == CROW:
                self.selected = n
                self.update_msg("🐦 Select empty adjacent node")
            else:
                self.update_msg("🐦 Select your crow")
        else:
            if n in CONN[self.selected] and self.board[n] == EMPTY:
                self.remove_image(self.selected)
                self.board[self.selected] = EMPTY
                self.board[n] = CROW
                self.place_image(n, CROW) # <-- CHANGED
                self.selected = None
                self.turn = VULTURE
                self.update_msg("🦅 Vulture: your move")
            else:
                self.update_msg("🐦 Invalid move")
                self.selected = None

    def move_vulture(self, n):
        if self.selected is None:
            if self.board[n] == VULTURE:
                self.selected = n
                self.update_msg("🦅 Select destination")
            else:
                self.update_msg("🦅 Select vulture")
        else:
            jumps = self.valid_jumps()
            for f, mid, t in jumps:
                if f == self.selected and t == n:
                    self.remove_image(f)
                    self.remove_image(mid)
                    self.board[f] = EMPTY
                    self.board[mid] = EMPTY
                    self.board[t] = VULTURE
                    self.place_image(t, VULTURE) # <-- CHANGED
                    self.captured += 1
                    self.selected = None
                    if self.captured >= 4:
                        self.update_msg("🎉 VULTURE WINS 🎉")
                        return
                    self.turn = CROW
                    self.update_msg("🐦 Crows: move")
                    return
            if n in CONN[self.selected] and self.board[n] == EMPTY:
                self.remove_image(self.selected)
                self.board[self.selected] = EMPTY
                self.board[n] = VULTURE
                self.place_image(n, VULTURE) # <-- CHANGED
                self.selected = None
                self.turn = CROW
                self.update_msg("🐦 Crows: move")
            else:
                self.update_msg("🦅 Invalid move")
                self.selected = None

    def valid_jumps(self):
        lst = []
        for a, links in CONN.items():
            for b in links:
                if self.board[a] == VULTURE and self.board[b] == CROW:
                    # find opposite node roughly in line (simplified check)
                    for c in CONN[b]:
                        if c != a and self.board[c] == EMPTY:
                            lst.append((a, b, c))
        return lst


if __name__ == "__main__":
    Kaooa()
    turtle.mainloop()