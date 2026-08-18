# BaBxP
# Advanced Forensic Recovery Tool - Professional TUI

A fully-featured Terminal User Interface (TUI) for mobile device forensic analysis with professional color schemes, advanced formatting, and intuitive navigation.

## Features

### ✨ Complete Screens (10 Implemented)

1. **Splash Screen** - Application startup with initialization progress
2. **Main Dashboard** - Overview of connected devices and quick actions
3. **Device Selection** - Choose device with highlighted selection
4. **Scan Mode Selection** - Quick, Deep, or Custom forensic analysis modes
5. **Live Scan Progress** - Real-time scan status with step tracking
6. **Results Dashboard** - Comprehensive scan results and statistics
7. **File Explorer** - Interactive file tree with color-coded entries
8. **Photo Gallery** - Image viewer with EXIF metadata
9. **Message Extraction** - WhatsApp and conversation recovery
10. **Settings Panel** - Configurable tool options and preferences

### 🎨 Professional Design

- **Advanced Color Palette**: 14 semantic colors with proper contrast
- **Rich Text Formatting**: Bold, italic, dim, and color combinations
- **Status Indicators**: Visual ✓, ✗, ⚠, ℹ, ⟳, 🗑, ✦ badges
- **Panel Styling**: Context-aware borders, backgrounds, and highlights
- **Responsive Layout**: Adapts to terminal width (min 80 chars)
- **Accessibility**: High contrast, clear hierarchy, screen-reader friendly

### 🔧 Technical Stack

- **Rich Library**: Advanced terminal formatting and rendering
- **Python 3.7+**: Cross-platform compatibility
- **No Dependencies**: Uses only Rich (installable via pip)
- **Type Hints**: Full typing support for maintainability
- **Object-Oriented**: Clean, extensible architecture

## Installation

### Requirements

```bash
# Python 3.7 or higher
python3 --version

# Install Rich library
pip install rich
```

### Setup

```bash
# Clone or download the tool
git clone <repository> forensic-tool
cd forensic-tool

# Make executable (Linux/Mac)
chmod +x forensic_tool.py

# Run directly with Python
python3 forensic_tool.py

# Or with shebang (Linux/Mac)
./forensic_tool.py
```

## Usage

### Navigation

- **Arrow Keys / W/S**: Navigate between options
- **Enter / Space**: Select highlighted option
- **ESC**: Go back to previous screen
- **Q**: Quit application
- **?**: Show help (on applicable screens)

### Workflow

1. **Launch** → Splash screen initializes components
2. **Main Dashboard** → View connected devices and options
3. **Select Device** → Choose target device for analysis
4. **Choose Scan Mode** → Quick, Deep, or Custom analysis
5. **Monitor Progress** → Watch real-time scan status
6. **Review Results** → Analyze extracted data
7. **Explore Data** → Browse files, photos, messages
8. **Configure** → Adjust tool settings as needed

## Color Palette Reference

### Semantic Colors

```
✓ Success/Complete:   #2ECC40 (Bright Green)
✗ Error/Danger:       #FF4136 (Bright Red)
⚠ Warning/Caution:    #FF851B (Orange)
ℹ Info/Neutral:       #0074D9 (Bright Blue)
⟳ Processing:         #B10DC9 (Magenta)
🗑 Deleted/Archive:    #FFDC00 (Bright Yellow)
✦ Highlighted:        #7FDBCA (Cyan)
- Disabled/Inactive:  #AAAAAA (Gray)
```

### Text Hierarchy

```
Primary (Titles):     Bold White on Dark Blue
Secondary (Headers):  Bold Cyan
Emphasis:             Bold Green or Bold Yellow
Normal:               White
Secondary Info:       Light Gray
Tertiary (Hints):     Medium Gray
```

### Panel Styling

```
Success Panels:   Green border + Dark Green background
Error Panels:     Red border + Dark Red background
Info Panels:      Blue border + Dark Blue background
Warning Panels:   Orange border + Dark Orange background
```

## Component Details

### Device Information Display

- Device name and path
- OS version and model
- Unique identifiers (IMEI/UDID)
- Connection status with indicator
- Battery level
- Storage usage with visual progress
- Last scan timestamp

### Scan Modes

#### Quick Scan
- Time: 5-15 minutes
- Impact: Minimal
- Coverage: Filesystem enumeration only
- Best for: Recent files, quick overview

#### Deep Scan
- Time: 1-4 hours
- Impact: Significant resource usage
- Coverage: Filesystem + deleted file carving + app extraction
- Best for: Complete recovery, evidence collection

#### Custom Scan
- Time: Variable
- Impact: Configurable
- Coverage: User-selected modules
- Best for: Targeted analysis, specific data types

### Results Dashboard

Displays comprehensive statistics:
- Media files (photos, videos)
- Documents
- Messages and conversations
- Contact information
- Browser history
- Call logs
- Recovered deleted files

### File Explorer

Interactive tree view with:
- Folder hierarchy
- File counts and sizes
- Color-coded file types
- Visual indicators for status
- Nested directory expansion
- Search and filter capabilities

### Photo Gallery

Image viewer with:
- Photo preview display
- Complete EXIF metadata
- GPS location extraction
- Camera information
- Date/time stamps
- Color profile details
- Status indicators

### Message Extraction

Conversation recovery featuring:
- Multi-app support (WhatsApp, Telegram, etc.)
- Conversation threading
- Timestamp preservation
- Media attachment tracking
- Contact identification
- Export capabilities

## Configuration

### Settings Panel Options

**General Settings**
- Output directory for reports
- Temporary file location
- Log file paths

**Scan Settings**
- Default scan mode
- Auto-cleanup behavior
- File carving options
- Thread count

**Security & Privacy**
- Temporary file encryption
- Audit logging
- Secure deletion method
- Data retention policies

**Report & Display**
- HTML/PDF generation
- JSON export options
- Thumbnail inclusion
- Report language
- Color theme selection

## Advanced Features

### Live Statistics

Real-time display of:
- Files found
- Folders scanned
- Data processed
- Processing speed
- Progress percentage
- Time remaining

### Activity Log

Complete audit trail with:
- Timestamp logging
- Operation details
- Status indicators
- Error reporting
- Success confirmations

### Multi-Device Support

Handle multiple connected devices:
- Simultaneous device detection
- Individual device queues
- Comparative analysis
- Batch operations

## Extensibility

The tool is designed for easy extension:

```python
# Add new screen
class Screen(Enum):
    MY_CUSTOM_SCREEN = "custom"

# Implement renderer
def render_custom_screen(self):
    """Custom screen implementation"""
    pass

# Add to main loop
elif self.current_screen == Screen.MY_CUSTOM_SCREEN:
    self.render_custom_screen()
```

### Custom Themes

Modify the Rich theme dictionary:

```python
custom_theme = Theme({
    "success": "bold #2ECC40",  # Modify colors
    "my_custom_style": "bold cyan on black",
    # ... additional styles
})
```

## Performance Considerations

- **Memory Usage**: Optimized for large device scans (128GB+)
- **Rendering**: Efficient terminal drawing with caching
- **Responsiveness**: Non-blocking UI updates
- **Scalability**: Handles 50,000+ files in tree view

## Troubleshooting

### Terminal Issues

**Colors not displaying:**
```bash
# Force terminal capabilities
export TERM=xterm-256color
python3 forensic_tool.py

# Or use Rich's native detection
# Tool handles this automatically
```

**Narrow terminal:**
- Tool adapts to terminals < 80 chars width
- Compact mode activates automatically
- Minimum 40-char width recommended

**Unicode characters not showing:**
```bash
# Ensure UTF-8 locale
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
python3 forensic_tool.py
```

### Navigation Issues

- Use W/S or Arrow keys to navigate
- Some terminals don't support all key codes
- ESC key may need configuration in some shells

### Performance Issues

- Reduce file tree depth for large scans
- Enable lazy loading for big directories
- Disable real-time statistics if sluggish

## File Structure

```
forensic_tool.py          # Main application file
README.md                 # This documentation
CHANGELOG.md             # Version history (if included)
requirements.txt         # Python dependencies (Rich)
LICENSE                  # License information
```

## Requirements File

Save as `requirements.txt`:

```
rich>=13.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Platform Support

- **Linux**: ✓ Full support
- **macOS**: ✓ Full support
- **Windows**: ✓ Full support (Windows Terminal recommended)
- **WSL**: ✓ Full support
- **SSH/Remote**: ✓ Full support

## Best Practices

### Before Running Scans

1. ✓ Verify device connection
2. ✓ Check available disk space
3. ✓ Enable appropriate permissions
4. ✓ Close other device applications
5. ✓ Back up original device image

### During Analysis

1. ✓ Maintain stable connection
2. ✓ Monitor progress regularly
3. ✓ Don't interrupt scan process
4. ✓ Note any warnings/errors
5. ✓ Track scan time for reporting

### After Recovery

1. ✓ Verify extracted data integrity
2. ✓ Check metadata completeness
3. ✓ Export results in appropriate format
4. ✓ Document findings
5. ✓ Secure temporary files

## Keyboard Shortcuts Reference

| Key | Action |
|-----|--------|
| `↑/↓` or `W/S` | Navigate up/down |
| `←/→` | Navigate left/right (in trees) |
| `Enter` | Select/Confirm |
| `Space` | Toggle option |
| `ESC` | Go back |
| `Q` | Quit application |
| `?` | Show help |
| `D` | View details |
| `I` | Device info |
| `E` | Export |
| `S` | Save/Settings |
| `G` | Gallery view |
| `F` | Filter/Find |

## Examples

### Quick Device Scan

```
1. Launch tool
2. Main Dashboard → Start New Scan
3. Device Selection → Select device
4. Scan Mode → Quick Scan
5. Monitor progress
6. Review results
```

### Deep Forensic Analysis

```
1. Launch tool
2. Main Dashboard → Start New Scan
3. Device Selection → Select device
4. Scan Mode → Deep Scan
5. Wait for completion (1-4 hours)
6. Results → Detailed analysis
7. File Explorer → Browse recovered files
```

### Photo Recovery

```
1. Results Dashboard
2. File Explorer → Navigate to Pictures
3. Gallery view → Browse all images
4. Select photos → Save/Export
```

## Reporting

The tool generates multiple report formats:

- **HTML Report**: Interactive, browsable results
- **PDF Report**: Court-admissible documentation
- **JSON Export**: Machine-readable data
- **CSV Export**: Spreadsheet compatible

All reports include:
- Complete file listings
- Metadata summaries
- Timeline analysis
- Statistical summaries
- Recovered deleted items

## Security & Privacy

- Temporary files encrypted during processing
- Optional secure deletion (DoD 5220.22-M standard)
- Audit logging of all operations
- No data uploaded or transmitted
- Local processing only
- Compliant with forensic standards

## Legal Notice

This tool is for authorized forensic analysis only. Users are responsible for:
- Legal authorization to access devices
- Compliance with local regulations
- Proper evidence handling procedures
- Chain of custody documentation
- Professional standards adherence

## Support & Contributing

For issues, improvements, or contributions:

1. Check existing documentation
2. Review troubleshooting section
3. Test with minimal reproduction
4. Report issues with full context
5. Submit improvements via pull request

## License

[Your License Here]

## Version History

### v2.1 (Current)
- Complete TUI implementation
- All 10 screens fully functional
- Professional color palette
- Rich library integration
- Full keyboard navigation
- Comprehensive documentation

### v2.0
- Major redesign with Rich
- Modern terminal aesthetics
- Extended color support

### v1.0
- Initial release
- Basic functionality

## Acknowledgments

Built with:
- [Rich](https://github.com/Textualize/rich) - Professional terminal rendering
- [Python 3](https://www.python.org/) - Core language
- Community feedback and contributions

---

**Last Updated**: 2024-01-15  
**Current Version**: 2.1  
**Status**: Production Ready ✓
