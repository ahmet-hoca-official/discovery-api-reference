# Contributing to Discovery API Reference

Thank you for your interest in contributing! 🎉

This documentation helps the Discovery community automate and improve their workflows. Your contributions make it better for everyone.

---

## 🤝 Ways to Contribute

### 1. Report Issues
- Found an error in the documentation?
- API method not working as documented?
- Missing information?

**Create an issue:** Describe what's wrong and include:
- Discovery version
- Code example (if applicable)
- Expected vs actual behavior

### 2. Improve Documentation
- Fix typos or unclear explanations
- Add missing API methods
- Improve code examples
- Add diagrams or images

### 3. Add Code Examples
- Share your working scripts
- Demonstrate advanced techniques
- Show real-world use cases

### 4. Test & Validate
- Test examples on different Discovery versions
- Validate API calls
- Report version compatibility issues

---

## 📝 Contribution Guidelines

### Code Examples
- Must be tested and working
- Include comments explaining key steps
- Use SI units (meters, Pa, N)
- Follow existing code style
- Add error handling where appropriate

### Documentation
- Use clear, simple language
- Include code examples
- Explain WHY, not just HOW
- Mark version-specific features
- Update table of contents if needed

### Formatting
- Use Markdown formatting
- Code blocks must specify language (```python)
- Keep line length reasonable (~80-100 chars)
- Use consistent heading levels

---

## 🔄 Contribution Process

1. **Fork** the repository
2. **Create a branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Edit documentation
   - Add examples
   - Test thoroughly
4. **Commit** with clear message
   ```bash
   git commit -m "Add: BlockBody cylinder hole example"
   ```
5. **Push** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

---

## ✅ Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code examples are tested in Discovery
- [ ] Documentation is clear and accurate
- [ ] No typos or grammar errors
- [ ] Follows existing style/format
- [ ] Updated CHANGELOG.md (if significant)
- [ ] No proprietary or confidential information

---

## 🎯 Priority Areas

We especially welcome contributions in:

- **V252 API Updates** - Document Discovery 2025 R2 changes
- **Advanced Examples** - Topology optimization, complex assemblies
- **Simulation** - Thermal, modal, CFD examples
- **Error Handling** - Robust script patterns
- **Performance** - Optimization tips
- **Extension Builder** - Custom tool examples

---

## 📜 Code of Conduct

- Be respectful and professional
- Help others learn
- No spam or self-promotion
- Focus on technical content
- Constructive feedback only

---

## 🐛 Bug Reports

A good bug report includes:

```markdown
**Discovery Version:** 2024 R2 (v242)
**API Version:** V24
**Operating System:** Windows 10

**Description:**
BlockBody.Create() throws error when...

**Code to Reproduce:**
```python
# Minimal example that reproduces the issue
from SpaceClaim.Api.V24 import *
...
```

**Expected Behavior:**
Should create a box...

**Actual Behavior:**
Error: ...

**Error Message:**
```
Full error traceback...
```
```

---

## 💡 Feature Requests

For new documentation features:

- Describe the use case
- Explain why it's useful
- Provide example if possible
- Tag with `enhancement` label

---

## 📚 Style Guide

### Code Style

```python
# ✅ GOOD
def create_bracket(width, height, thickness):
    """Create L-bracket with given dimensions.

    Args:
        width: Bracket width [m]
        height: Bracket height [m]
        thickness: Plate thickness [m]

    Returns:
        DesignBody: Created bracket
    """
    origin = Point.Create(0, 0, 0)
    frame = Frame.Create(origin, Direction.DirX, Direction.DirY)
    return BlockBody.Create(frame, width, height, thickness)

# ❌ BAD (no docstring, unclear names)
def cb(w, h, t):
    o = Point.Create(0, 0, 0)
    f = Frame.Create(o, Direction.DirX, Direction.DirY)
    return BlockBody.Create(f, w, h, t)
```

### Documentation Style

```markdown
### API Method Name

**Description:** Brief one-line description

**Signature:**
```python
MethodName(param1, param2) -> ReturnType
```

**Parameters:**
- `param1` (Type): Description
- `param2` (Type): Description

**Returns:**
- `ReturnType`: Description

**Example:**
```python
# Working example with comments
result = MethodName(value1, value2)
```

**Notes:**
- Important detail 1
- Important detail 2
```

---

## 🌍 Translation

Interested in translating the documentation?

- Open an issue proposing the language
- We'll create a separate branch
- Translate following the same structure
- Keep code examples in English (with translated comments)

---

## 🙏 Recognition

Contributors will be:
- Listed in README.md
- Credited in CHANGELOG.md
- Recognized in release notes

---

## 📞 Questions?

- **GitHub Issues:** For public questions
- **GitHub Discussions:** For general discussion
- **Email:** For private inquiries

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping improve the Discovery API Reference!** 🚀
