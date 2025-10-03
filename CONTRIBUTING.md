# Contributing to AI Chess Bot

Thank you for your interest in contributing to AI Chess Bot! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- Basic understanding of chess rules
- Familiarity with Python and Pygame (helpful but not required)

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/ai-chess-bot.git
   cd ai-chess-bot
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run tests** to ensure everything works:
   ```bash
   python test_game.py
   ```

## 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

### How to Submit a Bug Report
1. **Use a clear, descriptive title**
2. **Describe the exact steps** to reproduce the problem
3. **Explain what you expected** to happen
4. **Describe what actually happened**
5. **Include screenshots** if applicable
6. **Specify your environment**:
   - OS (Windows/macOS/Linux)
   - Python version
   - Pygame version

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 10]
- Python Version: [e.g. 3.9.0]
- Pygame Version: [e.g. 2.6.1]
```

## 💡 Suggesting Features

Feature suggestions are welcome! Please:

1. **Check existing feature requests** to avoid duplicates
2. **Provide a clear description** of the feature
3. **Explain why it would be useful**
4. **Consider implementation complexity**

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context about the feature request.
```

## 🔧 Code Contributions

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the coding standards
3. **Test your changes** thoroughly
4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: brief description of changes"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request** on GitHub

### Coding Standards

#### Python Style
- Follow **PEP 8** style guidelines
- Use **meaningful variable names**
- Add **docstrings** to all functions and classes
- Keep functions **focused and small**
- Use **type hints** where appropriate

#### Code Organization
- Keep related functionality together
- Separate concerns appropriately
- Maintain the existing module structure
- Add new features as separate modules when possible

#### Example Code Style
```python
def calculate_piece_value(piece: Piece, position: Tuple[int, int]) -> int:
    """
    Calculate the total value of a piece including positional bonus.
    
    Args:
        piece: The chess piece to evaluate
        position: The (row, col) position on the board
        
    Returns:
        The total value of the piece
    """
    base_value = PIECE_VALUES[piece.type]
    positional_bonus = get_positional_bonus(piece, position)
    return base_value + positional_bonus
```

### Testing
- **Write tests** for new functionality
- **Run existing tests** to ensure no regression
- **Test edge cases** and error conditions
- **Manual testing** of the game interface

### Commit Message Guidelines
Use clear, descriptive commit messages:

- **Add**: New features or files
- **Fix**: Bug fixes
- **Update**: Changes to existing functionality
- **Refactor**: Code restructuring without behavior change
- **Docs**: Documentation changes
- **Test**: Adding or updating tests

Examples:
```
Add: minimax algorithm with alpha-beta pruning
Fix: pawn promotion dialog not appearing
Update: improve AI evaluation function
Refactor: extract piece movement validation
Docs: update installation instructions
Test: add unit tests for board validation
```

## 🧪 Testing Guidelines

### Running Tests
```bash
python test_game.py
```

### Writing Tests
- Test new functionality you add
- Include both positive and negative test cases
- Test edge cases and error conditions
- Keep tests focused and independent

### Test Categories
1. **Unit Tests**: Individual functions and methods
2. **Integration Tests**: Component interactions
3. **Game Logic Tests**: Chess rule validation
4. **AI Tests**: Algorithm behavior
5. **GUI Tests**: User interface functionality

## 📋 Pull Request Process

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New functionality includes tests
- [ ] Documentation is updated if needed
- [ ] No merge conflicts with main branch

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] New tests added (if applicable)

## Screenshots
If applicable, add screenshots of changes

## Additional Notes
Any additional information about the changes
```

## 🎯 Areas for Contribution

### High Priority
- **Bug fixes** in game logic or AI
- **Performance optimizations**
- **Test coverage improvements**
- **Documentation enhancements**

### Medium Priority
- **New AI evaluation factors**
- **GUI improvements**
- **Additional game features**
- **Code refactoring**

### Low Priority
- **Visual enhancements**
- **Sound effects**
- **Additional game modes**
- **Advanced features**

## ❓ Questions?

If you have questions about contributing:

1. **Check existing issues** and documentation
2. **Create a new issue** with the "question" label
3. **Be specific** about what you need help with

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for helping make AI Chess Bot better! 🏁♟️