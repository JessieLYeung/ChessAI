# 🏁 AI Chess Bot

A fully functional chess game built from scratch using Python and Pygame, featuring both player vs player and AI modes with sophisticated minimax algorithm implementation.

![Chess Game](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🎮 Two Game Modes**: 
  - Player vs Player: Classic chess for two human players
  - Player vs AI: Challenge a smart AI opponent
- **🧠 Intelligent AI**: Powered by minimax algorithm with alpha-beta pruning
- **♟️ Complete Chess Rules**: All standard rules including castling, en passant, and pawn promotion
- **🎨 Beautiful GUI**: Clean Pygame interface with piece graphics and move highlighting
- **📊 Game Statistics**: Track your wins, losses, and game history
- **💾 Save/Load**: Save your games and continue later
- **🎯 Object-Oriented Design**: Clean, modular, and extensible code

## 🖼️ Screenshots

*Game interface showing the chess board with move highlighting and game information panel*

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-chess-bot.git
   cd ai-chess-bot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## 🎮 How to Play

### Game Controls
- **Mouse Click**: Select and move pieces
- **ESC**: Exit to main menu or quit game
- **R**: Restart game (when game is over)
- **S**: Save current game state

### AI Settings
When selecting "Player vs AI":
- Choose your color (White/Black)
- Select AI difficulty (1-5)
  - 1: Very Easy - Quick moves
  - 2: Easy - Basic strategy  
  - 3: Medium - Good planning
  - 4: Hard - Strong tactics
  - 5: Very Hard - Deep analysis

## 🏗️ Architecture

### Project Structure
```
AI Chess Bot/
├── main.py              # Game entry point
├── requirements.txt     # Dependencies
├── test_game.py         # Test suite
├── src/
│   ├── pieces/          # Chess piece classes
│   ├── board.py         # Game board logic
│   ├── game.py          # Main game coordination
│   ├── gui.py           # Pygame interface
│   ├── ai.py            # AI with minimax algorithm
│   ├── menu.py          # Main menu system
│   └── utils.py         # Utilities and statistics
└── assets/
    └── images/          # Generated piece images
```

### Key Components

- **Chess Engine**: Complete rule implementation with move validation
- **AI Brain**: Minimax algorithm with alpha-beta pruning and position evaluation
- **Visual Interface**: Pygame-based GUI with intuitive controls
- **Game Management**: Save/load, statistics, and game state tracking

## 🤖 AI Implementation

The AI uses a sophisticated **minimax algorithm** with several optimizations:

- **Alpha-Beta Pruning**: Reduces search space by ~50%
- **Position Evaluation**: Multi-factor assessment including:
  - Material value (pieces worth)
  - Piece positioning (piece-square tables)
  - King safety evaluation
  - Center control assessment
  - Mobility analysis
- **Configurable Depth**: 1-5 levels of lookahead
- **Move Ordering**: Improves pruning efficiency

## 🧪 Testing

Run the test suite to verify all functionality:

```bash
python test_game.py
```

Tests cover:
- ✅ Board setup and piece placement
- ✅ Move validation and execution
- ✅ AI move generation
- ✅ Check detection
- ✅ Game state management

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Report bugs** - Found an issue? Open a GitHub issue
2. **Suggest features** - Have ideas for improvements?
3. **Submit pull requests** - Fix bugs or add features
4. **Improve documentation** - Help make the project more accessible

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📈 Roadmap

Future enhancements planned:
- [ ] **Network Multiplayer**: Play with friends online
- [ ] **Advanced AI**: Opening book and endgame tablebase
- [ ] **Game Analysis**: Move suggestions and position evaluation
- [ ] **Tournament Mode**: Multiple games with ELO rating
- [ ] **Custom Themes**: Different board and piece styles
- [ ] **Sound Effects**: Audio feedback for moves and captures
- [ ] **PGN Support**: Import/export standard chess notation

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Chess piece movement algorithms inspired by standard chess programming techniques
- Minimax implementation based on classic game theory principles
- Pygame community for excellent graphics library documentation

## 📞 Contact

Created by **Karen** - Feel free to reach out!

- GitHub: [@yourusername](https://github.com/yourusername)
- Project Link: [https://github.com/yourusername/ai-chess-bot](https://github.com/yourusername/ai-chess-bot)

---

⭐ **Star this repo** if you found it helpful!